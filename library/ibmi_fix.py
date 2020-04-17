#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_patch
short_description: Install patch such as PTF, PTF Group, Technology refresh to the target IBM i system.
version_added: 1.0
description:
     - The C(ibmi_patch) module install patch to target IBM i system.
     - The patch can be PTF, PTF group, technology refresh.
     - The format of the patch can be save file or image catalog.
options:
  type:
    description:
      - The type of the patch. 
    type: str
    required: false
    choices: ["*PTF", "*GRPPTF"]
  path:
    description:
      - The path on the target IBM i system where the fix installation file is located.
      - The path is an IFS directory format.
    type: str
    required: true
  format:
    description:
      - The format of the fix.
      - The format can be *SAVF or *IMAGE
    type: str
    default: *SAVF
    choices: ['*SAVF', '*IMAGE']
  name:
    description:
      - The name of the fix. For single PTF, this is the name of the PTF save file.
        This option will be ignored if *NONE is specified for option 'status'.
    type: str
    default: '1m'
    required: false
  product_id:
    description:
      - The parameters that SBMJOB will take. Other than CMD, all other parameters need to be specified here.
        The default values of parameters for SBMJOB will be taken if not specified.
    type: str
    required: false
    default: ''

notes:
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
seealso:
- module: ibmi_job

author:
    - Wang Yun (@airwangyun)
'''

EXAMPLES = r'''
- name: Submit a batch job and run CALL QGPL/PGM1
  ibmi_submit_job:
    cmd: 'CALL QGPL/PGM1'
    parameters: 'JOB(TEST)'
    check_interval: '30s'
    time_out: '80s'
    status: ['*OUTQ', '*COMPLETE']
'''

RETURN = r'''
start:
    description: The task execution start time
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The task execution end time
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The task execution delta time
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The task standard output
    type: str
    sample: 'CPC2102: Library TESTLIB created'
stderr:
    description: The task standard error
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
sbmjob_cmd:
    description: The SBMJOB CL command that has been used.
    type: str
    sample: 'SBMJOB CMD(CRTLIB LIB(TESTLIB))'
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    sample: 255
stdout_lines:
    description: The task standard output split in lines
    type: list
    sample: [
        "CPC2102: Library TESTLIB created."
    ]
stderr_lines:
    description: The task standard error split in lines
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
import re
import time
from ansible.module_utils.basic import AnsibleModule

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
IBMi_JOB_STATUS_NOT_EXPECTED = 258
IBMi_JOB_STATUS_LIST = ["*NONE", "*ACTIVE", "*COMPLETE", "*JOBQ", "*OUTQ"]


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
    elif rc == IBMi_JOB_STATUS_NOT_EXPECTED:
        return "The returned status of the submitted job is not expected. "
    else:
        return "Unknown error"


def run_cl_command(job_number, job_user, job_name):
    itool = iToolKit()
    itool.add(iCmd('test', 'CRTLIB wytest'))
    # itransport = DatabaseTransport(conn)
    itransport = DirectTransport()
    itool.call(itransport)

    # output
    rtvjoba = itool.dict_out('rtvjoba')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(rtvjoba)
    if 'error' in rtvjoba:
        print(rtvjoba['error'])
        exit()
    elif 'row' in rtvjoba:
        rtvjoba_vals = rtvjoba['row']

        for item_dict in rtvjoba_vals:
            for key in item_dict:
                print(item_dict[key])

        print('hahahahahahhahahahahhaah')

        # print('value:' + rtvjoba)
        # print('USRLIBL = ' + rtvjoba_vals['USRLIBL'])
        # print('SYSLIBL = ' + rtvjoba_vals['SYSLIBL'])
        # print('CCSID   = ' + rtvjoba_vals['CCSID'])
        # print('OUTQ    = ' + rtvjoba_vals['OUTQ'])
    else:
        print('ERRORRRRRRRRRRRRRRRRRRR')
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


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
    # itransport = DirectTransport()
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


def return_fix_information(db_connection, ptf_list):
    sql_ptf = ""
    pass


def run_a_list_of_commands(module, cmd_key_list, cmd_map):

    for item in cmd_key_list:
        cur_cmd = cmd_map[item]
        args = ['system', cur_cmd]
        module.run_command(args, use_unsafe_shell=False)


def install_by_image_catalog(module, product_id="*ALL", temp_dir_target="/home/ansiblePTFInstallTemp",
                             opt_device=None, catalog_name=None, is_rollback=False):

    opt_device_name = None
    catalog_name_to_create = None
    if opt_device is None:
        opt_device_name = "ANSIOPTDEV"
    else:
        opt_device_name = opt_device
    if catalog_name is None:
        catalog_name_to_create = "ANSICATLG1"
    else:
        catalog_name_to_create = catalog_name

    command_map = {}

    command_map["cl_crt_device"] = "CRTDEVOPT DEVD(" + opt_device_name +\
                    ") RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i')"

    command_map["cl_crt_catalog"] = "CRTIMGCLG IMGCLG(" + catalog_name_to_create + \
                     ") DIR('" + temp_dir_target + "') CRTDIR(*YES) ADDVRTVOL(*DIR) " \
                                                   "TEXT('Created by Ansible for IBM i')"
    command_map["cl_vary_on_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*ON)"
    command_map["lod_image_catalog"] = "LODIMGCLG IMGCLG(" + catalog_name_to_create + ") DEV("\
                                       + opt_device_name + ") OPTION(*LOAD)"
    command_map["cl_catalog_in_order"] = "VFYIMGCLG IMGCLG(" + catalog_name_to_create + ") TYPE(*PTF) SORT(*YES)"
    command_map["cl_inst_ptf"] = "INSPTF LICPGM((" + product_id + ")) DEV(" + opt_device_name + ") INSTYP(*DLYALL)"
    command_map["unload_image_catalog"] = "LODIMGCLG IMGCLG(" + catalog_name_to_create + ")  OPTION(*UNLOAD)"
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*OFF)"
    command_map["cl_delete_image_catalog"] = "DLTIMGCLG IMGCLG(" + catalog_name_to_create + ") KEEP(*NO)"
    command_map["cl_dlt_device"] = "DLTDEVD DEVD(" + opt_device_name + ")"

    print("Run CL Command: " + command_map["cl_crt_device"])
    # need to check the existense of the created opt device
    args = ['system', command_map["cl_crt_device"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_crt_catalog"])
    args = ['system', command_map["cl_crt_catalog"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_vary_on_device"])
    args = ['system', command_map["cl_vary_on_device"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["lod_image_catalog"])
    args = ['system', command_map["lod_image_catalog"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["unload_image_catalog", "cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_catalog_in_order"])
    args = ['system', command_map["cl_catalog_in_order"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["unload_image_catalog", "cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_inst_ptf"])
    args = ['system', command_map["cl_inst_ptf"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["unload_image_catalog", "cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["unload_image_catalog"])
    args = ['system', command_map["unload_image_catalog"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_vary_off_device",
                                            "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_vary_off_device"])
    args = ['system', command_map["cl_vary_off_device"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_delete_image_catalog"])
    args = ['system', command_map["cl_delete_image_catalog"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(module, ["cl_dlt_device"], command_map)
        return rc, out, err

    print("Run CL Command: " + command_map["cl_dlt_device"])
    args = ['system', command_map["cl_dlt_device"]]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc > 0:
        return rc, out, err

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, None, None


def main():
    module = AnsibleModule(
        argument_spec=dict(
            product_id=dict(type='str', default='*ALL'),
            ptf_list=dict(type='list'),
            ptf_omit_list=dict(type='list'),
            format=dict(type='str', default='save_file', choices=['save_file', 'virtual_image']),
            # save_file_lib=dict(type='str', default='QGPL'),
            # save_file_object=dict(type='str', default=''),
            path=dict(type='str', default='/home'),
            delayed_option=dict(type='str', choices=['*YES', '*NO']),
            temp_or_perm=dict(type='str', choices=['*TEMP', '*PERM']),
            operation=dict(type='str', default='install_fix', choices=['install_fix', 'remove_fix', 'query_fix']),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    product_id = module.params['product_id']
    ptf_list_to_select = module.params['ptf_list']
    ptf_list_to_omit = module.params['ptf_omit_list']
    # save_file_object = module.params['save_file_object']
    # save_file_lib = module.params['save_file_lib']
    format_name = module.params['format']
    delayed_option = module.params['delayed_option']
    temp_or_perm = module.params['temp_or_perm']
    path = module.params['path']
    operation = module.params['operation']

    startd = datetime.datetime.now()

    if operation == 'install_fix':
        if format_name == 'save_file':
            pass
            # install single or a list of PTFs
            # savf_obj = save_file_lib + "/" + save_file_object
            # rc, out, err = install_ptf(module, product_id, ptf_list_to_select,
            #                           ptf_list_to_omit, "*SAVF", savf_obj, delayed_option, temp_or_perm)
        else:
            rc, out, err = install_by_image_catalog(module, product_id, path,
                                                    opt_device=None, catalog_name=None, is_rollback=True)
    elif operation == 'remove_fix':
        if format_name == 'save_file':
            rc, out, err = remove_ptf(module, product_id, ptf_list_to_select, ptf_list_to_omit,
                                      temp_or_perm=temp_or_perm, delayed_option=delayed_option)
    elif operation == 'query_fix':
        pass

    else:
        pass

    # Need to query the status of the PTF

    endd = datetime.datetime.now()
    delta = endd - startd

    if rc > 0:
        result_failed = dict(
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            out=out,
            err=err,
            # changed=True,
        )
        module.fail_json(msg='non-zero return code', **result_failed)
    else:
        result_success = dict(
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            # changed=True,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
