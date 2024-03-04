#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Wang Yuyu <wangyuyu@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_fix_network_install_client
short_description: Install PTFs on the client via IBM i Network install
version_added: '1.4.0'
description:
     - The C(ibmi_fix) module installs PTFs on the client via IBM i Network install.
     - Single PTF, PTF group and TR PTF are supported.
options:
  operation:
    description:
      - The operation on the client, the options are as follows
      - setup_only will only setup the environment to install PTFs.
      - setup_and_installPTF will setup the environment and install PTFs.
      - installPTF_only will only install PTFs.
      - reload will vary off and vary on the optical device when the image catalog files are updated on the server.
      - uninstall will remove the environment on the client.
      - setup_and_installPTF_and_uninstall will setup the environment, install PTFs and then remove the environment.
    choices: ['setup_only',
              'setup_and_installPTF',
              'installPTF_only',
              'reload',
              'uninstall',
              'setup_and_installPTF_and_uninstall']
    type: str
    default: 'setup_and_installPTF_and_uninstall'
  device_name:
    description:
      - The virtual optical device name on the client
    type: str
    default: 'CLNTPTFOPT'
  server_address:
    description:
      - The address of IBM i network install server
      - It could be IP address or host name
    type: str
  image_catalog_directory_name:
    description:
      - The image catalog directory on the server
      - The path is an IFS directory format.
    type: str
    default: '/etc/ibmi_ansible/fix_management/network_install'
  product_id:
    description:
      - The product ID of the fixes to be installed.
    type: list
    elements: str
    default: '*ALL'
  fix_omit_list:
    description:
      - The list of PTFs which will be omitted.
      - The key of the dict should be the product ID of the fix that is omitted.
    type: list
    elements: dict
    required: false
  apply_type:
    description:
      - The fix apply type of the install to perform.
    choices: ['*DLYALL', '*IMMDLY', '*IMMONLY']
    type: str
    default: '*DLYALL'
  hiper_only:
    description:
      - Whether or not only install the hiper fixes.
      - Specify true if only need to install hiper fixes.
    default: false
    type: bool
  rollback:
    description:
      - Whether or not rollback if there's failure during the operation
    default: true
    type: bool
  joblog:
    description:
      - The job log of the job executing the task will be returned even rc is zero if it is set to True.
    type: bool
    default: false
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str

notes:
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3
seealso:
- module: ibmi_fix

author:
    - Wang Yuyu (@wangyuyu)
'''

EXAMPLES = r'''
- name: Setup the client
  ibm.power_ibmi.ibmi_fix_network_install_client:
    operation: 'setup_only'
    server_address: '9.123.123.45'
    image_catalog_directory_name: '/tmp/PTFs'
    rollback: True
    become_user: "QSECOFR"
    become_user_password: "yourpassword"
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
job_log:
    description: The job log of the job executes the task.
    returned: always
    type: list
    sample: [
        {
            "FROM_INSTRUCTION": "318F",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "",
            "FROM_PROCEDURE": "",
            "FROM_PROGRAM": "QWTCHGJB",
            "FROM_USER": "CHANGLE",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPD0912",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Printer device PRT01 not found.",
            "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897",
            "MESSAGE_TYPE": "DIAGNOSTIC",
            "ORDINAL_POSITION": "5",
            "SEVERITY": "20",
            "TO_INSTRUCTION": "9369",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
        }
    ]
device_name:
    description: The virtual optical device name
    returned: always
    type: str
    sample: 'REPOSVROPT'
need_action_ptf_list:
    description: The list contains the information of the just installed PTFs that need further IPL actions.
    type: list
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
    returned: When use operation 'setup_and_installPTF', 'installPTF_only' and 'setup_and_installPTF_and_uninstall'
requisite_ptf_list:
    description: The PTF list contains the requiste PTF of the PTF being applied.
    type: list
    sample: [
        {
            "ptf_id": "SI76012",
            "requisite": "SI76014"
        },
        {
            "ptf_id": "SI76012",
            "requisite": "SI76013"
        }
    ]
    returned: When use operation 'setup_and_installPTF', 'installPTF_only' and 'setup_and_installPTF_and_uninstall'
ptf_install_fail_reason:
    description: The failure reason if it fails to install PTFs. It is from the message content
    type: str
    sample: 'Program temporary fixes (PTFs) can only be loaded, applied and removed for products which are installed.'
    returned: When use operation 'setup_and_installPTF', 'installPTF_only' and 'setup_and_installPTF_and_uninstall'
'''

import datetime
import re
import sys
import socket
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

HAS_ITOOLKIT = True
try:
    from itoolkit import iToolKit
    from itoolkit import iPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit import iCmd
    from itoolkit.transport import DatabaseTransport as BaseDatabaseTransport

    class DatabaseTransport(BaseDatabaseTransport):
        def _close(self):
            """Don't close connection, we'll manage it ourselves"""
            pass

except ImportError:
    HAS_ITOOLKIT = False
HAS_IBM_DB = True

__ibmi_module_version__ = "2.0.1"
IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257


def itoolkit_run_command(ibmi_module, command):
    rc, out, err = ibmi_module.itoolkit_run_command(command)
    return rc, out, err


def run_a_list_of_commands(ibmi_module, cmd_key_list, cmd_map):
    for item in cmd_key_list:
        cur_cmd = cmd_map[item]
        itoolkit_run_command(ibmi_module, cur_cmd)


def _is_ipv4_addr(ip):
    p = re.compile(
        r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def check_object_existence(db_connection, lib_name, type_name, obj_name):
    obj_existence_expression = "SELECT COUNT(*) " \
                               " FROM TABLE (QSYS2.OBJECT_STATISTICS('" + lib_name + "','" + type_name + "','"\
                               + obj_name + "')) X "
    out_result_set, err = db2i_tools.ibm_dbi_sql_query(db_connection, obj_existence_expression)
    if err is None:
        if out_result_set[0][0] != 0:
            # This object alreay exists
            return 1
        else:
            return 0
    else:
        return 0


def get_opt_device_info_basic(imodule, opt_device_name):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    # Reserved field need hex on because if any garbage characters in it
    # API calling will hang without hex on
    itool.add(
        iPgm('qdcrdevd', 'QDCRDEVD')
        .addParm(
            iDS('Qdc_DEVD1600_t', {'len': 'dmilen'})
            .addData(iDS('Qdc_DEVD0100_t')
                     .addData(iData('Bytes_Returned', '10i0', ''))
                     .addData(iData('Bytes_Available', '10i0', ''))
                     .addData(iData('Date_Info_Retrieved', '7A', ''))
                     .addData(iData('Time_Info_Retrieved', '6A', ''))
                     .addData(iData('Device_Name', '10A', '',))
                     .addData(iData('Device_Category', '10A', ''))
                     .addData(iData('Online_At_IPL', '10A', ''))
                     .addData(iData('Text_Desc', '50A', ''))
                     .addData(iData('Reserved', '3A', '', {'hex': 'on'}))
                     )
            .addData(iData('Device_Type', '10A', ''))
            .addData(iData('Device_Model', '10A', ''))
            .addData(iData('Resource_Name', '10A', ''))
            .addData(iData('Message_Queue_Name', '10A', ''))
            .addData(iData('Message_Queue_Library', '10A', ''))
            .addData(iData('Current_Message_Queue_Name', '10A', ''))
            .addData(iData('Current_Message_Queue_Library', '10A', ''))
            .addData(iData('Last_Activity_Date', '7A', ''))
            .addData(iData('Reserved', '3A', '', {'hex': 'on'}))
            .addData(iData('Offset_Sup_Med_Typ_Entries', '10i0', ''))
            .addData(iData('Num_Sup_Med_Typ_Entries', '10i0', ''))
            .addData(iData('Length_Sup_Med_Typ_Entries', '10i0', ''))
            .addData(iData('Type_Lcl_IntnetA', '10i0', ''))
            .addData(iData('Length_Lcl_IntnetA', '10i0', ''))
            .addData(iData('Lcl_IntnetA', '45A', ''))
            .addData(iData('Reserved1', '3A', '', {'hex': 'on'}))
            .addData(iData('Type_Rmt_IntnetA', '10i0', ''))
            .addData(iData('Length_Rmt_IntnetA', '10i0', ''))
            .addData(iData('Rmt_IntnetA', '45A', ''))
            .addData(iData('Reserved2', '3A', '', {'hex': 'on'}))
            .addData(iData('User_ID_Number', '10u0', ''))
            .addData(iData('Group_ID_Number', '10u0', ''))
            .addData(iData('Offset_Net_Img_Dir', '10i0', ''))
            .addData(iData('Length_Net_Img_Dir', '10i0', ''))
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'dmilen'}))
        .addParm(iData('fmtnam', '8A', 'DEVD1600'))
        .addParm(iData('optdevname', '10A', ibmi_util.fmtTo10(opt_device_name)))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )
    itool.call(itransport)
    qdcrdevd = itool.dict_out('qdcrdevd')
    ibmi_util.log_debug(str(qdcrdevd), sys._getframe().f_code.co_name)
    if 'success' in qdcrdevd:
        devd1600_t = qdcrdevd['Qdc_DEVD1600_t']
        ibmi_util.log_debug(str(devd1600_t), sys._getframe().f_code.co_name)
        return 0, devd1600_t, qdcrdevd['success']
    else:
        return 1, None, qdcrdevd['error']


def get_opt_device_info(imodule, opt_device_name, number_of_sup_med_entries):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iPgm('qdcrdevd', 'QDCRDEVD')
        .addParm(
            iDS('Qdc_DEVD1600_t', {'len': 'dmilen'})
            .addData(iDS('Qdc_DEVD0100_t')
                     .addData(iData('Bytes_Returned', '10i0', ''))
                     .addData(iData('Bytes_Available', '10i0', ''))
                     .addData(iData('Date_Info_Retrieved', '7A', ''))
                     .addData(iData('Time_Info_Retrieved', '6A', ''))
                     .addData(iData('Device_Name', '10A', ''))
                     .addData(iData('Device_Category', '10A', ''))
                     .addData(iData('Online_At_IPL', '10A', ''))
                     .addData(iData('Text_Desc', '50A', ''))
                     .addData(iData('Reserved', '3A', '', {'hex': 'on'}))
                     )
            .addData(iData('Device_Type', '10A', ''))
            .addData(iData('Device_Model', '10A', ''))
            .addData(iData('Resource_Name', '10A', ''))
            .addData(iData('Message_Queue_Name', '10A', ''))
            .addData(iData('Message_Queue_Library', '10A', ''))
            .addData(iData('Current_Message_Queue_Name', '10A', ''))
            .addData(iData('Current_Message_Queue_Library', '10A', ''))
            .addData(iData('Last_Activity_Date', '7A', ''))
            .addData(iData('Reserved', '3A', '', {'hex': 'on'}))
            .addData(iData('Offset_Sup_Med_Typ_Entries', '10i0', ''))
            .addData(iData('Num_Sup_Med_Typ_Entries', '10i0', '', {'enddo': 'mycnt'}))
            .addData(iData('Length_Sup_Med_Typ_Entries', '10i0', ''))
            .addData(iData('Type_Lcl_IntnetA', '10i0', ''))
            .addData(iData('Length_Lcl_IntnetA', '10i0', ''))
            .addData(iData('Lcl_IntnetA', '45A', ''))
            .addData(iData('Reserved1', '3A', '', {'hex': 'on'}))
            .addData(iData('Type_Rmt_IntnetA', '10i0', ''))
            .addData(iData('Length_Rmt_IntnetA', '10i0', ''))
            .addData(iData('Rmt_IntnetA', '45A', ''))
            .addData(iData('Reserved2', '3A', '', {'hex': 'on'}))
            .addData(iData('User_ID_Number', '10u0', ''))
            .addData(iData('Group_ID_Number', '10u0', ''))
            .addData(iData('Offset_Net_Img_Dir', '10i0', ''))
            .addData(iData('Length_Net_Img_Dir', '10i0', ''))
            .addData(iDS('Qdc_Sup_Med_Typ_Entries', {'dim': number_of_sup_med_entries, 'dou': 'mycnt'})
                     # if 'dim': '999', dir_name is blank
                     .addData(iData('Media_Name', '11A', ''))
                     .addData(iData('Read_Capability', '1A', ''))
                     .addData(iData('Write_Capability', '1A', ''))
                     .addData(iData('Record_Capability', '1A', ''))
                     )
            .addData(iData('dir_name', '127A', ''))
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'dmilen'}))
        .addParm(iData('fmtnam', '8A', 'DEVD1600'))
        .addParm(iData('optdevname', '10A', ibmi_util.fmtTo10(opt_device_name)))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )
    itool.call(itransport)
    qdcrdevd = itool.dict_out('qdcrdevd')
    ibmi_util.log_debug(str(qdcrdevd), sys._getframe().f_code.co_name)
    if 'success' in qdcrdevd:
        devd1600_t = qdcrdevd['Qdc_DEVD1600_t']
        ibmi_util.log_debug(str(devd1600_t), sys._getframe().f_code.co_name)
        return 0, devd1600_t, qdcrdevd['success']
    else:
        return 1, None, qdcrdevd['error']


def check_existing_opt_device(db_conn, ibmi_module, server_ip_address, image_catalog_directory, opt_device_name):
    # do not check the input device name
    all_existing_devd = "SELECT TRIM(OBJNAME)" +\
                        " FROM TABLE (QSYS2.OBJECT_STATISTICS('QSYS','*DEVD')) X " +\
                        " WHERE OBJATTRIBUTE = 'OPT' and OBJNAME <> '" +\
                        opt_device_name + "'"

    out_result_set, err = db2i_tools.ibm_dbi_sql_query(db_conn, all_existing_devd)
    if err is None:
        existing_devd_return = ""
        for result in out_result_set:
            existing_devd = result[0]
            rc, info_return, err = get_opt_device_info_basic(ibmi_module, existing_devd)
            if rc > 0:
                return -1, ""
            number_of_sup_med_entries = str(info_return['Num_Sup_Med_Typ_Entries'])
            rc, info_return_detail, err = get_opt_device_info(ibmi_module, existing_devd,
                                                              number_of_sup_med_entries)
            if rc > 0:
                return -1, ""
            local_internet_address = info_return_detail['Lcl_IntnetA'].strip()
            remote_internet_address = info_return_detail['Rmt_IntnetA'].strip()
            network_image_directory = info_return_detail['dir_name'].strip()
            network_image_directory_u = network_image_directory.strip('/').upper()
            image_catalog_directory_u = image_catalog_directory.strip('/').upper()
            if local_internet_address == '*SRVLAN' and remote_internet_address == server_ip_address and network_image_directory_u == image_catalog_directory_u:
                if existing_devd_return != "":
                    existing_devd_return = existing_devd_return + ", " + existing_devd
                else:
                    existing_devd_return = existing_devd_return + existing_devd
        if existing_devd_return != "":
            return 1, existing_devd_return
        else:
            return 0, ""
    else:
        return -1, ""


def setup_operation(ibmi_module, module, opt_device_name, server_ip_address, image_catalog_directory, is_rollback):

    if server_ip_address is None:
        return 1, None, "missing server ip address", ""

    if image_catalog_directory is None:
        return 1, None, "missing image catalog directory", ""

    db_conn = ibmi_module.get_connection()

    command_map = {}
    command_log = "Command log of setup operation."
    command_map["cl_crt_device"] = "QSYS/CRTDEVOPT DEVD(" + opt_device_name +\
                                   ") RSRCNAME(*VRT) LCLINTNETA(*SRVLAN) RMTINTNETA('" + server_ip_address +\
                                   "') NETIMGDIR('" + image_catalog_directory +\
                                   "') TEXT('Created by Ansible on the client for PTFs install')"
    command_map["cl_vary_on_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*ON)"
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*OFF)"
    command_map["cl_dlt_device"] = "QSYS/DLTDEVD DEVD(" + opt_device_name + ")"

    # step 1: check if there is already a existing optical device with same IP address and same imgclg directory
    rc, existing_device = check_existing_opt_device(db_conn, ibmi_module, server_ip_address,
                                                    image_catalog_directory, opt_device_name)
    if rc != 0:
        if rc == -1:
            err_message = "Failure in retrieving existing optical devices."
        else:
            if existing_device.find(",") == -1:
                err_message = "Optical device " + existing_device +\
                              " already exists with the same server IP address and same image catalog directory."
            else:
                err_message = "Optical devices " + existing_device +\
                              " already exist with the same server IP address and same image catalog directory."
        return rc, None, err_message, command_log

    # step 2: create optical device
    # check the optical device exists or not
    device_exist = check_object_existence(db_conn, "QSYS", "*DEVD", opt_device_name)
    if device_exist == 0:
        module.log("Run CL Command: " + command_map["cl_crt_device"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_crt_device"])
        command_log = command_log + "\n" + command_map["cl_crt_device"]
        command_log = command_log + "\n" + out
        if rc > 0:
            if is_rollback:
                run_a_list_of_commands(ibmi_module, ["cl_vary_off_device", "cl_dlt_device"], command_map)
            return rc, out, err, command_log

    else:
        # check if the expected ip address and image catalog directory in the configuration
        rc, info_return, err = get_opt_device_info_basic(ibmi_module, opt_device_name)
        if rc > 0:
            return rc, info_return, err, command_log
        number_of_sup_med_entries = str(info_return['Num_Sup_Med_Typ_Entries'])

        rc, info_return_detail, err = get_opt_device_info(ibmi_module, opt_device_name, number_of_sup_med_entries)
        if rc > 0:
            return rc, info_return_detail, err, command_log
        local_internet_address = info_return_detail['Lcl_IntnetA'].strip()
        remote_internet_address = info_return_detail['Rmt_IntnetA'].strip()
        network_image_directory = info_return_detail['dir_name'].strip()
        network_image_directory_u = network_image_directory.strip('/').upper()
        image_catalog_directory_u = image_catalog_directory.strip('/').upper()
        if local_internet_address != '*SRVLAN':
            return 1, None, "Same optical device with different configuration already exists", command_log
        if remote_internet_address != server_ip_address:
            return 1, None, "Same optical device with different server IP address already exists", command_log
        if network_image_directory_u != image_catalog_directory_u:
            return 1, None, "Same optical device with different image catalog directory already exists", command_log

    # step 3: vary on optical device
    module.log("Run CL Command: " + command_map["cl_vary_on_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_on_device"])
    command_log = command_log + "\n" + command_map["cl_vary_on_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(ibmi_module, ["cl_vary_off_device", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log


def get_optical_device_status(ibmi_module, module, opt_device_name):
    conn = ibmi_module.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    rcommand = "QSYS/RTVCFGSTS CFGD(" + opt_device_name + ") CFGTYPE(*DEV) STSCDE(?N)"
    itool.add(iCmd('rtv_command', rcommand))
    itool.call(itransport)
    rtv_command = itool.dict_out('rtv_command')
    ibmi_util.log_debug("rtv_command to run: " + str(rtv_command), sys._getframe().f_code.co_name)
    if 'error' in rtv_command:
        rc = ibmi_util.IBMi_COMMAND_RC_ERROR
        out_dict = {}
        error = str(rtv_command)
    else:
        # remove the key 'success' and its value, just left the result
        del rtv_command['success']
        rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
        out_dict = rtv_command['row']
        error = ''
    return rc, out_dict, error


def INSPTF_operation(ibmi_module, module, product_id, device_name, fix_omit_list, is_rollback, apply_type, hiper_only, rollback_remove_devd):
    command_map = {}
    command_log = "Command log of INSPTF operation."

    product_id_str = ") (".join(product_id)
    if fix_omit_list is not None:
        cl_ptf_omit = "OMIT("
        for i in fix_omit_list:
            for key in i:
                cl_ptf_omit = cl_ptf_omit + "(" + key + " " + i[key] + ") "
        cl_ptf_omit = cl_ptf_omit + ")"
    else:
        cl_ptf_omit = ""

    if hiper_only:
        hiper_option = "*YES"
    else:
        hiper_option = "*NO"

    # check if optical device is varied on (It may take time to vary on it)
    dev_status = ""
    for i in range(0, 35, 1):
        rc_dlyjob, out_dlyjob, err = itoolkit_run_command(ibmi_module, "QSYS/DLYJOB DLY(5)")
        rc, dev_out, error = get_optical_device_status(ibmi_module, module, device_name)
        if rc == 0:
            dev_status = dev_out['STSCDE']
            # 60: active
            if dev_status == "60":
                break

    if dev_status != "60":
        return rc, None, "Optical device is not varied on", ""

    command_map["cl_inst_ptf"] = "QSYS/INSPTF LICPGM((" + product_id_str + ")) DEV(" + device_name\
                                 + ") INSTYP(" + apply_type + ") HIPER(" + hiper_option + ") " + cl_ptf_omit

    module.log("Run CL Command: " + command_map["cl_inst_ptf"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_inst_ptf"])
    command_log = command_log + "\n" + command_map["cl_inst_ptf"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback and rollback_remove_devd:
            command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + device_name + ")" +\
                                                " CFGTYPE(*DEV) STATUS(*OFF)"
            command_map["cl_dlt_device"] = "QSYS/DLTDEVD DEVD(" + device_name + ")"
            command_map["cl_rmv_volumn"] = "QSYS/RMVOPTCTG VOL(*MOUNTED) DEV(" + device_name + ")"

            command_log = command_log + "Command log of rollback operation."

            module.log("Run CL Command: " + command_map["cl_rmv_volumn"])
            r_rc, out, r_err = itoolkit_run_command(ibmi_module, command_map["cl_rmv_volumn"])
            command_log = command_log + "\n" + command_map["cl_rmv_volumn"]
            command_log = command_log + "\n" + out

            module.log("Run CL Command: " + command_map["cl_vary_off_device"])
            r_rc, r_out, r_err = itoolkit_run_command(ibmi_module, command_map["cl_vary_off_device"])
            command_log = command_log + "\n" + command_map["cl_vary_off_device"]
            command_log = command_log + "\n" + r_out

            module.log("Run CL Command: " + command_map["cl_dlt_device"])
            r_rc, r_out, r_err = itoolkit_run_command(ibmi_module, command_map["cl_dlt_device"])
            command_log = command_log + "\n" + command_map["cl_dlt_device"]
            command_log = command_log + "\n" + r_out

        return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log


def uninstall_operation(ibmi_module, module, device_name, rollback):
    db_conn = ibmi_module.get_connection()

    command_map = {}
    command_log = "Command log of uninstall operation."
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + device_name + ") CFGTYPE(*DEV) STATUS(*OFF)"
    command_map["cl_vary_on_device"] = "QSYS/VRYCFG CFGOBJ(" + device_name + ") CFGTYPE(*DEV) STATUS(*ON)"
    command_map["cl_dlt_device"] = "QSYS/DLTDEVD DEVD(" + device_name + ")"
    command_map["cl_rmv_volumn"] = "QSYS/RMVOPTCTG VOL(*MOUNTED) DEV(" + device_name + ")"

    # check the optical device exists or not
    device_exist = check_object_existence(db_conn, "QSYS", "*DEVD", device_name)
    if device_exist == 0:
        return 0, None, "The optical device does not exist", ""

    # step 1: vary on the optical device (in order to do RMVOPTCTG)
    module.log("Run CL Command: " + command_map["cl_vary_on_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_on_device"])
    command_log = command_log + "\n" + command_map["cl_vary_on_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    # step 2: remove the volumn from the optical device
    module.log("Run CL Command: " + command_map["cl_rmv_volumn"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_rmv_volumn"])
    command_log = command_log + "\n" + command_map["cl_rmv_volumn"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    # step 3: vary off the optical device
    module.log("Run CL Command: " + command_map["cl_vary_off_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_off_device"])
    command_log = command_log + "\n" + command_map["cl_vary_off_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    # step 4: delete the device
    module.log("Run CL Command: " + command_map["cl_dlt_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_dlt_device"])
    command_log = command_log + "\n" + command_map["cl_dlt_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log


def reload_operation(ibmi_module, module, device_name, rollback):
    command_map = {}
    command_log = "Command log of setup operation."
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + device_name + ") CFGTYPE(*DEV) STATUS(*OFF)"
    command_map["cl_vary_on_device"] = "QSYS/VRYCFG CFGOBJ(" + device_name + ") CFGTYPE(*DEV) STATUS(*ON)"

    # step 1: vary off the optical device
    module.log("Run CL Command: " + command_map["cl_vary_off_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_off_device"])
    command_log = command_log + "\n" + command_map["cl_vary_off_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    # step 2: vary on the optical device
    module.log("Run CL Command: " + command_map["cl_vary_on_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_on_device"])
    command_log = command_log + "\n" + command_map["cl_vary_on_device"]
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
    if (out_result_set is not None):
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', default='setup_and_installPTF_and_uninstall', choices=['setup_only',
                                                                                              'setup_and_installPTF',
                                                                                              'installPTF_only',
                                                                                              'uninstall',
                                                                                              'setup_and_installPTF_and_uninstall',
                                                                                              'reload']),
            device_name=dict(type='str', default='CLNTPTFOPT'),
            server_address=dict(type='str'),
            image_catalog_directory_name=dict(type='str', default='/etc/ibmi_ansible/fix_management/network_install'),
            product_id=dict(type='list', elements='str', default=['*ALL']),
            fix_omit_list=dict(type='list', elements='dict'),
            apply_type=dict(type='str', default='*DLYALL', choices=['*DLYALL', '*IMMDLY', '*IMMONLY']),
            hiper_only=dict(type='bool', default=False),
            rollback=dict(type='bool', default=True),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        required_if=[
            ["operation", "setup_only", ["server_address"]],
            ["operation", "setup_and_installPTF", ["server_address"]],
            ["operation", "setup_and_installPTF_and_uninstall", ["server_address"]]
        ],
        supports_check_mode=True,
    )

    operation = module.params['operation']
    device_name = module.params['device_name']
    server_address = module.params['server_address']
    image_catalog_directory = module.params['image_catalog_directory_name']
    product_id = module.params['product_id']
    fix_omit_list = module.params['fix_omit_list']
    apply_type = module.params['apply_type']
    hiper_only = module.params['hiper_only']
    rollback = module.params['rollback']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()

    if image_catalog_directory.find('~') >= 0:
        module.fail_json(msg='Invalid image catalog directory input')

    # check if the input is ip address or host name
    server_ip_address = ""
    if operation in ['setup_only', 'setup_and_installPTF', 'setup_and_installPTF_and_uninstall']:
        if _is_ipv4_addr(server_address):
            server_ip_address = server_address
        else:
            try:
                server_ip_address = socket.gethostbyname(server_address)
            except Exception:
                module.fail_json(msg='Invalid server address input')

    ibmi_module = imodule.IBMiModule(become_user_name=become_user,
                                     become_user_password=become_user_password)

    db_conn = ibmi_module.get_connection()

    # make sure the optical device name is in upper case
    device_name = device_name.upper()

    if operation == 'setup_only':
        rc, out, err, command_log = setup_operation(ibmi_module, module, device_name, server_ip_address, image_catalog_directory, rollback)
    elif operation == 'installPTF_only':
        # vary off and then vary on the device in case:
        # The device is off
        # or
        # The image catalog entries on the server are changed. This requires device to be varied off and on
        # on the client to mount the latest PTF image files.
        rc, out, err, command_log = reload_operation(ibmi_module, module, device_name, rollback)
        # if rollback removes device
        rollback_remove_devd = False
        if rc == IBMi_COMMAND_RC_SUCCESS:
            rc, out, err, command_log = INSPTF_operation(ibmi_module, module, product_id, device_name, fix_omit_list, rollback, apply_type,
                                                         hiper_only, rollback_remove_devd)
    elif operation == 'setup_and_installPTF':
        rollback_remove_devd = True
        rc, out, err, command_log = setup_operation(ibmi_module, module, device_name, server_ip_address, image_catalog_directory, rollback)
        if rc == IBMi_COMMAND_RC_SUCCESS:
            rc, out, err, command_log = INSPTF_operation(ibmi_module, module, product_id, device_name, fix_omit_list, rollback, apply_type,
                                                         hiper_only, rollback_remove_devd)
    elif operation == 'uninstall':
        rc, out, err, command_log = uninstall_operation(ibmi_module, module, device_name, rollback)
    elif operation == 'reload':
        rc, out, err, command_log = reload_operation(ibmi_module, module, device_name, rollback)
    elif operation == 'setup_and_installPTF_and_uninstall':
        rollback_remove_devd = True
        rc, out, err, command_log = setup_operation(ibmi_module, module, device_name, server_ip_address, image_catalog_directory, rollback)
        if rc == IBMi_COMMAND_RC_SUCCESS:
            rc, out, err, command_log = INSPTF_operation(ibmi_module, module, product_id, device_name, fix_omit_list, rollback, apply_type,
                                                         hiper_only, rollback_remove_devd)
        if rc == IBMi_COMMAND_RC_SUCCESS:
            rc, out, err, command_log = uninstall_operation(ibmi_module, module, device_name, rollback)
    else:
        module.fail_json(msg='Invalid operation input')

    endd = datetime.datetime.now()
    delta = endd - startd

    if joblog or (rc != IBMi_COMMAND_RC_SUCCESS):
        job_log = ibmi_module.itoolkit_get_job_log_NLS(startd)
    else:
        job_log = []

    requisite_ptf_list = []
    fail_reason = ""
    if operation in ['setup_and_installPTF', 'installPTF_only', 'setup_and_installPTF_and_uninstall']:
        out_ptf_list, query_err = return_fix_information(db_conn, product_id, str(startd), str(endd))

        if joblog or (rc != IBMi_COMMAND_RC_SUCCESS):
            for joblog_var in job_log:
                if joblog_var.get('MESSAGE_ID') in ['CPF3632', 'CPD35B1']:
                    message_token = joblog_var.get('MESSAGE_TOKENS')
                    requisite_ptf = {"ptf_id": message_token[21:28],
                                     "requiste": message_token[7:14]
                                     }
                    requisite_ptf_list.append(requisite_ptf)
                if joblog_var.get('MESSAGE_ID') in ['CPF3606', 'CPF3616', 'CPF3619', 'CPF3660', 'CPF3640']:
                    # CPF3606 product not installed
                    # CPF3616 PTFs already exist or options not installed
                    # CPF3619 release not match
                    # CPF3660 No program temporary fixes identified
                    # CPF3640 No immediate PTFs applied
                    fail_reason = joblog_var.get('MESSAGE_SECOND_LEVEL_TEXT')
                    start_index = fail_reason.find(':') + 1
                    # &N Recovery
                    end_index = fail_reason.find('&N', 5)
                    if end_index < 0:
                        fail_reason = fail_reason[start_index:]
                    else:
                        fail_reason = fail_reason[start_index: end_index]
                    fail_reason = fail_reason.strip()

    if rc != 0:
        if operation in ['setup_and_installPTF', 'installPTF_only', 'setup_and_installPTF_and_uninstall']:
            result_failed = dict(
                stderr=err,
                stdout=command_log,
                rc=rc,
                job_log=job_log,
                need_action_ptf_list=out_ptf_list,
                requisite_ptf_list=requisite_ptf_list,
                ptf_install_fail_reason=fail_reason
            )
        else:
            result_failed = dict(
                stderr=err,
                stdout=command_log,
                rc=rc,
                job_log=job_log,
            )
        module.fail_json(msg='Operation failed.', **result_failed)
    else:
        if operation in ['setup_and_installPTF', 'installPTF_only', 'setup_and_installPTF_and_uninstall']:
            result_success = dict(
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                stdout=command_log,
                stderr=err,
                rc=rc,
                job_log=job_log,
                device_name=device_name,
                need_action_ptf_list=out_ptf_list,
            )
        else:
            result_success = dict(
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                stdout=command_log,
                stderr=err,
                rc=rc,
                job_log=job_log,
                device_name=device_name,
            )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
