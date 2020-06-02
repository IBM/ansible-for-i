#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Wang Yun <cdlwangy@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_fix_imgclg
short_description: Install fixes such as PTF, PTF Group, Technology refresh to the target IBM i system by image catalog.
version_added: 1.0
description:
     - The C(ibmi_fix) module install fixes to target IBM i system by image catalog.
     - Single PTF, PTF group and TR PTF are supported.
options:
  src:
    description:
      - The path on the target IBM i system where the fix installation file is located.
      - The path is an IFS directory format.
    type: str
    required: true
  virtual_image_name_list:
    description:
      - The name list of the installation file.
    type: list
    elements: str
    default: ['*ALL']
    required: false
  product_id:
    description:
      - The product ID of the fixes to be installed.
    type: list
    elements: str
    default: ["*ALL"]
  fix_omit_list:
    description:
      - The list of PTFs that will be omitted.
      - The key of the dict should be the product ID of the fix that is omitted.
    type: list
    elements: dict
    required: false
  use_temp_path:
    description:
      - Whether or not to copy the installation file to a temp path.
      - If true is chosen, it will copy the installation file to a temp path.
      - The temp directory and the installation file copied to the temp directory will be both deleted after the task.
      - It is recommended to use temp path to avoid conflicts.
      - If false is chosen, the install will directly use the file specified in src option.
      - The installation file will not be deleted after install if false is chosen.
    type: bool
    default: true
  apply_type:
    description:
      - The fix apply type of the install to perform.
    type: str
    choices: ["*DLYALL", "*IMMDLY", "*IMMONLY"]
    default: "*DLYALL"
  hiper_only:
    description:
      - Whether or not only install the hiper fixes.
      - Specify true if only need to install hiper fixes.
    default: false
    type: bool
  rollback:
    description:
      - Whether or not rollback if there's failure during the installation of the fixes
    default: true
    type: bool

notes:
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
seealso:
- module: ibmi_fix, ibmi_fix_savf

author:
    - Wang Yun (@airwangyun)
'''

EXAMPLES = r'''
- name: Install a list of PTFs of LPP 5733SC1 from image catalog
  ibmi_fix_imgclg:
    product_id:
      - '5733SC1'
    src: '{{ fix_install_path }}'
    apply_type: '*DLYALL'
    hiper_only: False
    use_temp_path: True
    rollback: True
    virtual_image_name_list:
      - 'S2018V01.BIN'
    fix_omit_list:
      - 5733SC1: "SI70819"
'''

RETURN = r'''
start:
    description: The task execution start time
    type: str
    sample: '2019-12-02 11:07:53.757435'
    returned: When rc is zero
end:
    description: The task execution end time
    type: str
    sample: '2019-12-02 11:07:54.064969'
    returned: When rc is zero
delta:
    description: The task execution delta time
    type: str
    returned: When rc is zero
    sample: '0:00:00.307534'
stdout:
    description: The task standard output
    returned: When error occurs.
    type: str
    sample: 'CPC2102: Library TESTLIB created'
stderr:
    description: The task standard error
    returned: When error occurs.
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    returned: always
    sample: 255
stdout_lines:
    description: The task standard output split in lines
    type: list
    returned: When error occurs.
    sample: [
        "CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i')",
        "+++ success CRTDEVOPT DEVD(ANSIBOPT2) RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i')",
        "CRTIMGCLG IMGCLG(ANSIBCLG1) DIR('/home/ansiblePTFInstallTemp/') CRTDIR(*YES)"
    ]
stderr_lines:
    description: The task standard error split in lines
    type: list
    returned: When error occurs.
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
need_action_ptf_list:
    description: The list contains the information of the just installed PTFs that need further IPL actions.
    type: list
    returned: When rc is zero.
    sample: [
        {
            "PTF_ACTION_PENDING": "NO",
            "PTF_ACTION_REQUIRED": "NONE",
            "PTF_CREATION_TIMESTAMP": "2019-12-06T01:00:43",
            "PTF_IDENTIFIER": "SI71746",
            "PTF_IPL_ACTION": "TEMPORARILY APPLIED",
            "PTF_IPL_REQUIRED": "IMMEDIATE",
            "PTF_LOADED_STATUS": "LOADED",
            "PTF_PRODUCT_ID": "5733SC1",
            "PTF_SAVE_FILE": "NO",
            "PTF_STATUS_TIMESTAMP": "2020-03-24T09:03:55",
            "PTF_TEMPORARY_APPLY_TIMESTAMP": null
        }
    ]
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
import re
import os
import time
import shutil
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi.temp_directory import TemporaryDirectory
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools

try:
    from itoolkit import iToolKit
    from itoolkit import iCmd
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit.transport import DatabaseTransport, DirectTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False


IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257


def interpret_return_code(rc):
    if rc == IBMi_COMMAND_RC_SUCCESS:
        return 'Success'
    elif rc == IBMi_COMMAND_RC_ERROR:
        return 'Generic failure'
    elif rc == IBMi_COMMAND_RC_UNEXPECTED:
        return 'Unexpected error'
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG:
        return "iToolKit result dict does not have key 'joblog'"
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR:
        return "iToolKit result dict does not have key 'error'"
    else:
        return "Unknown error"


def itoolkit_run_sql(sql):
    conn = dbi.connect()
    db_itransport = DatabaseTransport(conn)
    itool = iToolKit()

    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFetch('fetch'))
    itool.add(iSqlFree('free'))

    itool.call(db_itransport)

    command_output = itool.dict_out('fetch')

    rc = IBMi_COMMAND_RC_UNEXPECTED
    out = ''
    err = ''
    if 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    else:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['row']

    return rc, out, err


def itoolkit_run_command(command):
    conn = dbi.connect()
    # itransport = iDB2Call(conn)
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(iCmd('command', command, {'error': 'on'}))
    itool.call(itransport)

    rc = IBMi_COMMAND_RC_UNEXPECTED
    out = ''
    err = ''

    command_output = itool.dict_out('command')

    if 'success' in command_output:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['success']
    elif 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    else:
        # should not be here, must xmlservice has internal error
        rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
        err = "iToolKit result dict does not have key 'error', the output is %s" % command_output

    return rc, out, err


def convert_wait_time_to_seconds(input_wait_time):
    m = re.match(r"^(-?\d+)([smhdw])?$", input_wait_time.lower())
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if m:
        wait_time = int(m.group(1)) * seconds_per_unit.get(m.group(2), 1)
    else:
        wait_time = 0
    return wait_time


def wait_for_certain_time(input_wait_time):
    wait_time = convert_wait_time_to_seconds(input_wait_time)
    time.sleep(wait_time)


def remove_ptf(module, product_id, ptf_selected_list, ptf_omit_list, temp_or_perm="*TEMP", delayed_option="*NO"):
    cl_rmv_ptf_map = {"LICPGM": product_id,
                      "RMV": temp_or_perm,
                      "SELECT": "", "OMIT": "",
                      "DELAYED": delayed_option}

    if len(ptf_selected_list) > 0:
        ptf_str_to_select = ' '.join(ptf_selected_list)
        cl_rmv_ptf_map["SELECT"] = ptf_str_to_select

    if len(ptf_omit_list) > 0:
        ptf_str_to_omit = ' '.join(ptf_omit_list)
        cl_rmv_ptf_map["OMIT"] = ptf_str_to_omit

    cl_rmv_ptf = "RMVPTF"
    for key, value in cl_rmv_ptf_map.items():
        cl_rmv_ptf = cl_rmv_ptf + " " + key + "(" + value + ") "

    args = ['system', cl_rmv_ptf]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)

    return rc, out, err


def install_ptf(module, product_id, ptf_list_to_select, ptf_list_to_omit,
                device, save_file, delayed_option="*NO", temp_or_perm="*TEMP"):

    cl_load_ptf_map = {"LICPGM": product_id,
                       "DEV": "*SAVF",
                       "SELECT": "", "OMIT": "",
                       "SAVF": ""}

    cl_apply_ptf_map = {"LICPGM": product_id, "SELECT": "", "OMIT": "",
                        "APY": temp_or_perm, "DELAYED": delayed_option}

    if len(ptf_list_to_select) > 0:
        ptf_str_to_select = ' '.join(ptf_list_to_select)
        cl_load_ptf_map["SELECT"] = ptf_str_to_select
        cl_apply_ptf_map["SELECT"] = ptf_str_to_select

    if len(ptf_list_to_omit) > 0:
        ptf_str_to_omit = ' '.join(ptf_list_to_omit)
        cl_load_ptf_map["OMIT"] = ptf_str_to_omit
        cl_apply_ptf_map["OMIT"] = ptf_str_to_omit

    if device == "*SAVF":
        cl_load_ptf_map["SAVF"] = save_file

    cl_load_ptf = "LODPTF"
    for key, value in cl_load_ptf_map.items():
        cl_load_ptf = cl_load_ptf + " " + key + "(" + value + ") "

    cl_apply_ptf = "APYPTF"
    for key, value in cl_apply_ptf_map.items():
        cl_apply_ptf = cl_apply_ptf + " " + key + "(" + value + ") "

    load_ptf_args = ['system', cl_load_ptf]
    rc_load_ptf, out_load_ptf, err_load_ptf = module.run_command(load_ptf_args, use_unsafe_shell=False)

    apy_ptf_args = ['system', cl_apply_ptf]
    rc_apy_ptf, out_apy_ptf, err_apy_ptf = module.run_command(apy_ptf_args, use_unsafe_shell=False)

    rc = rc_apy_ptf
    out = None
    err = None
    if out_apy_ptf is not None:
        out = out_load_ptf + "\n" + out_apy_ptf

    if err_apy_ptf is not None:
        err = err_load_ptf + "\n" + err_apy_ptf

    return rc, out, err


def run_a_list_of_commands(module, cmd_key_list, cmd_map):

    for item in cmd_key_list:
        cur_cmd = cmd_map[item]
        args = ['system', cur_cmd]
        module.run_command(args, use_unsafe_shell=False)


def install_by_image_catalog(module, product_id_list, virtual_image_list, dir_target,
                             opt_device, catalog_name, fix_omit_list, is_rollback=False, delayed_option="*DLYALL",
                             hiper_only=False):

    opt_device_name = None
    catalog_name_to_create = None
    if hiper_only:
        hiper_option = "*YES"
    else:
        hiper_option = "*NO"

    if opt_device is None:
        opt_device_name = "ANSIOPTDEV"
    else:
        opt_device_name = opt_device
    if catalog_name is None:
        catalog_name_to_create = "ANSICATLG1"
    else:
        catalog_name_to_create = catalog_name

    command_map = {}
    command_log = "Command log of fix install by image catalog."

    command_map["cl_crt_device"] = "QSYS/CRTDEVOPT DEVD(" + opt_device_name +\
                                   ") RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i')"

    command_map["cl_crt_catalog"] = "QSYS/CRTIMGCLG IMGCLG(" + catalog_name_to_create + \
                                    ") DIR('" + dir_target + "') CRTDIR(*YES) ADDVRTVOL(*DIR) " \
                                    "TEXT('Created by Ansible for IBM i')"
    if (virtual_image_list is not None) and (virtual_image_list != ["*ALL"]):
        command_map["cl_crt_catalog"] = "QSYS/CRTIMGCLG IMGCLG(" + catalog_name_to_create + ") DIR('" + dir_target +\
                                        "') CRTDIR(*YES) TEXT('Created by Ansible for IBM i')"

    command_map["cl_vary_on_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*ON)"
    command_map["lod_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + catalog_name_to_create + ") DEV("\
                                       + opt_device_name + ") OPTION(*LOAD)"
    command_map["cl_catalog_in_order"] = "QSYS/VFYIMGCLG IMGCLG(" + catalog_name_to_create + ") TYPE(*PTF) SORT(*YES)"

    product_id_str = ") (".join(product_id_list)
    if fix_omit_list is not None:
        cl_ptf_omit = "OMIT("
        for i in fix_omit_list:
            for key in i:
                cl_ptf_omit = cl_ptf_omit + "(" + key + " " + i[key] + ") "
        cl_ptf_omit = cl_ptf_omit + ")"
    else:
        cl_ptf_omit = ""

    command_map["cl_inst_ptf"] = "QSYS/INSPTF LICPGM((" + product_id_str + ")) DEV(" + opt_device_name\
                                 + ") INSTYP(" + delayed_option + ") HIPER(" + hiper_option + ") " + cl_ptf_omit
    command_map["unload_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + catalog_name_to_create + ")  OPTION(*UNLOAD)"
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*OFF)"
    command_map["cl_delete_image_catalog"] = "QSYS/DLTIMGCLG IMGCLG(" + catalog_name_to_create + ") KEEP(*YES)"
    command_map["cl_dlt_device"] = "QSYS/DLTDEVD DEVD(" + opt_device_name + ")"

    module.log("Run CL Command: " + command_map["cl_crt_device"])
    # need to check the existense of the created opt device
    rc, out, err = itoolkit_run_command(command_map["cl_crt_device"])
    # command_log.append(command_map["cl_crt_device"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_crt_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_crt_catalog"])
    rc, out, err = itoolkit_run_command(command_map["cl_crt_catalog"])
    # command_log.append(command_map["cl_crt_catalog"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_crt_catalog"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_vary_on_device"])
    rc, out, err = itoolkit_run_command(command_map["cl_vary_on_device"])
    # command_log.append(command_map["cl_vary_on_device"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_vary_on_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    if (virtual_image_list is not None) and (virtual_image_list != ["*ALL"]):
        for image_name in virtual_image_list:
            cl_catalog_entry_adding = "QSYS/ADDIMGCLGE IMGCLG(" + catalog_name_to_create + ") FROMFILE("\
                                      + image_name + ") TOFILE(*fromfile) TEXT('Added by Ansible')"
            module.log("Run CL Command: " + cl_catalog_entry_adding)

            rc, out, err = itoolkit_run_command(cl_catalog_entry_adding)
            # command_log.append(cl_catalog_entry_adding)
            # command_log.append(out)
            command_log = command_log + "\n" + cl_catalog_entry_adding
            command_log = command_log + "\n" + out
            if rc > 0:
                if is_rollback:
                    run_a_list_of_commands(module, ["cl_vary_off_device",
                                                    "cl_delete_image_catalog", "cl_dlt_device"], command_map)
                return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["lod_image_catalog"])
    rc, out, err = itoolkit_run_command(command_map["lod_image_catalog"])
    # command_log.append(command_map["lod_image_catalog"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["lod_image_catalog"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["unload_image_catalog", "cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_catalog_in_order"])
    rc, out, err = itoolkit_run_command(command_map["cl_catalog_in_order"])
    # command_log.append(command_map["cl_catalog_in_order"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_catalog_in_order"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["unload_image_catalog", "cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_inst_ptf"])
    rc, out, err = itoolkit_run_command(command_map["cl_inst_ptf"])
    # command_log.append(command_map["cl_inst_ptf"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_inst_ptf"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["unload_image_catalog", "cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["unload_image_catalog"])
    rc, out, err = itoolkit_run_command(command_map["unload_image_catalog"])
    # command_log.append(command_map["unload_image_catalog"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["unload_image_catalog"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_vary_off_device"])
    rc, out, err = itoolkit_run_command(command_map["cl_vary_off_device"])
    # command_log.append(command_map["cl_vary_off_device"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_vary_off_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_delete_image_catalog"])
    rc, out, err = itoolkit_run_command(command_map["cl_delete_image_catalog"])
    # command_log.append(command_map["cl_delete_image_catalog"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_delete_image_catalog"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_dlt_device"], command_map)
        return rc, out, err, command_log

    module.log("Run CL Command: " + command_map["cl_dlt_device"])
    rc, out, err = itoolkit_run_command(command_map["cl_dlt_device"])
    # command_log.append(command_map["cl_dlt_device"])
    # command_log.append(out)
    command_log = command_log + "\n" + command_map["cl_dlt_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log


def return_fix_information(db_connection, product_id, start_timestamp, end_timestamp):

    # get the version and release info
    release_info, err = db2i_tools.get_ibmi_release(db_connection)

    if release_info["version_release"] < 7.3:
        ptf_temp_apply_time_label = "'NOT SUPPORT'"
    else:
        ptf_temp_apply_time_label = "PTF_TEMPORARY_APPLY_TIMESTAMP"

    str_product_id_list = "','".join(product_id)
    sql = "SELECT PTF_PRODUCT_ID, PTF_IDENTIFIER, PTF_LOADED_STATUS, PTF_SAVE_FILE, PTF_IPL_ACTION," \
          " PTF_ACTION_PENDING, PTF_ACTION_REQUIRED, PTF_IPL_REQUIRED,  " \
          " PTF_STATUS_TIMESTAMP, PTF_CREATION_TIMESTAMP, " \
          " " + ptf_temp_apply_time_label + " FROM QSYS2.PTF_INFO " \
          " WHERE PTF_IPL_ACTION <> 'NONE' AND " \
          " (PTF_STATUS_TIMESTAMP BETWEEN '" + start_timestamp + "' AND '" + end_timestamp + "') "

    if (product_id is None) or ("*ALL" in product_id):
        where_product_id = ""
    else:
        where_product_id = " AND PTF_PRODUCT_ID IN ('" + str_product_id_list + "') "

    sql = sql + where_product_id

    out_result_set, err = db2i_tools.ibm_dbi_sql_query(db_connection, sql)

    out = []
    for result in out_result_set:
        result_map = {"PTF_PRODUCT_ID": result[0], "PTF_IDENTIFIER": result[1],
                      "PTF_LOADED_STATUS": result[2], "PTF_SAVE_FILE": result[3],
                      "PTF_IPL_ACTION": result[4], "PTF_ACTION_PENDING": result[5],
                      "PTF_ACTION_REQUIRED": result[6], "PTF_IPL_REQUIRED": result[7],
                      "PTF_STATUS_TIMESTAMP": result[8],
                      "PTF_CREATION_TIMESTAMP": result[9], "PTF_TEMPORARY_APPLY_TIMESTAMP": result[10]
                      }
        out.append(result_map)
    return out, err


def generate_object_name(db_connection, lib_name, type_name, obj_name_prefix):
    name_is_ok = False
    i = 1
    while name_is_ok is not True:
        cur_name = obj_name_prefix + str(i)
        obj_stats_expression = "SELECT COUNT(*) " \
                               " FROM TABLE (QSYS2.OBJECT_STATISTICS('" + lib_name + "','" + type_name + "','"\
                               + cur_name + "')) X "
        out_result_set, err = db2i_tools.ibm_dbi_sql_query(db_connection, obj_stats_expression)
        if err is None:
            if out_result_set[0][0] != 0:
                i = i + 1
                continue
            return cur_name
        else:
            break


def main():
    module = AnsibleModule(
        argument_spec=dict(
            product_id=dict(type='list', elements='str', default=['*ALL']),
            virtual_image_name_list=dict(type='list', elements='str', default=['*ALL']),
            fix_omit_list=dict(type='list', elements='dict'),
            use_temp_path=dict(type='bool', default=True),
            src=dict(type='str', required=True),
            apply_type=dict(type='str', default='*DLYALL', choices=['*DLYALL', '*IMMDLY', '*IMMONLY']),
            hiper_only=dict(type='bool', default=False),
            rollback=dict(type='bool', default=True),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    product_id = module.params['product_id']
    fix_file_name_list = module.params['virtual_image_name_list']
    fix_omit_list = module.params['fix_omit_list']
    delayed_option = module.params['apply_type']
    path = module.params['src']
    use_temp_path = module.params['use_temp_path']
    hiper_only = module.params['hiper_only']
    rollback = module.params['rollback']

    if not os.path.exists(path):
        return module.fail_json(msg="The path specified in src does not exist. The value is: " + path)

    if not os.path.isdir(path):
        return module.fail_json(msg="The value specified in src is not a valid directory. The value is " + path)

    startd = datetime.datetime.now()

    connection_id = None
    try:
        connection_id = dbi.connect()
    except Exception as e_db_connect:
        module.fail_json(msg="Exception when connecting to IBM i Db2. " + str(e_db_connect))

    catalog_name = generate_object_name(connection_id, "QUSRSYS", "*IMGCLG", "ANSIBCLG")
    dev_name = generate_object_name(connection_id, "QSYS", "*DEVD", "ANSIBOPT")

    if use_temp_path:

        with TemporaryDirectory() as tmp_dir:
            module.log("Creating temp dir: " + tmp_dir)
            if os.path.isdir(tmp_dir):
                if (fix_file_name_list == ["*ALL"]) or (fix_file_name_list is None):
                    # move all the objects to the target folder
                    for f in os.listdir(path):
                        source_file = os.path.join(path, f)
                        target_file = os.path.join(tmp_dir, f)
                        if os.path.isfile(source_file):
                            shutil.copy(source_file, tmp_dir)
                else:
                    # move specific file to the target
                    for fix_file_name in fix_file_name_list:
                        source_file = os.path.join(path, fix_file_name)
                        if os.path.exists(source_file):
                            if os.path.isfile(source_file):
                                shutil.copy(source_file, tmp_dir)
                            else:
                                return module.fail_json(msg=source_file + " is not a file.")
                        else:
                            return module.fail_json(msg="Image file " + source_file + " does not exist.")

                rc, out, err, command_log = install_by_image_catalog(module, product_id, None, tmp_dir,
                                                                     str(dev_name), str(catalog_name),
                                                                     fix_omit_list, is_rollback=rollback,
                                                                     delayed_option=delayed_option,
                                                                     hiper_only=hiper_only)
            else:
                module.fail_json(msg="Failed creating temp dir.")
    else:
        rc, out, err, command_log = install_by_image_catalog(module, product_id, fix_file_name_list, path,
                                                             dev_name, catalog_name, fix_omit_list,
                                                             is_rollback=rollback,
                                                             delayed_option=delayed_option,
                                                             hiper_only=hiper_only)

    endd = datetime.datetime.now()
    delta = endd - startd
    out_ptf_list, query_err = return_fix_information(connection_id, product_id, str(startd), str(endd))

    if connection_id is not None:
        try:
            connection_id.close()
        except Exception as e_disconnect:
            err = "ERROR: Unable to disconnect from the database. " + str(e_disconnect)

    if rc > 0:
        result_failed = dict(
            stderr=err,
            stdout=command_log,
            rc=rc,
            # changed=True,
        )
        module.fail_json(msg='Install from image catalog failed.', **result_failed)
    else:
        result_success = dict(
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            rc=rc,
            changed=True,
            need_action_ptf_list=out_ptf_list,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
