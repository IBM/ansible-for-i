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
module: ibmi_fix_network_install_server
short_description: Setup IBM i Network install server which contains image files of PTFs, PTF Group and Technology refresh.
version_added: '1.4.0'
description:
     - The C(ibmi_fix) module setup IBM i Network install server which contains images files.
     - Single PTF, PTF group and TR PTF are supported.
options:
  operation:
    description:
      - The operation on the Network install server, the options are as follows
      - setup_only will only setup the network install server, including configuring a virtual optical device and image catalog.
      - setup_and_addimgclge will setup the network install server and add image catalog entries for PTF image files.
      - addimgclge_only will only add image catalog entries for PTF image files.
      - rmvimgclge_only will only remove all the image catalog entries for PTF image files.
      - rmvimgclge_and_addimgclge will first remove all the image catalog entries for existing PTF image files, then add entries for new PTF image files.
      - uninstall will remove the network install server configuration.
      - retrieve_image_catalog_entries will retrieve the current image catalog entries.
      - restart_NFS_server will restart NFS Server.
    choices: ['setup_only',
              'setup_and_addimgclge',
              'addimgclge_only',
              'rmvimgclge_only',
              'rmvimgclge_and_addimgclge',
              'uninstall',
              'retrieve_image_catalog_entries',
              'restart_NFS_server']
    type: str
    default: 'setup_only'
  image_catalog_directory_name:
    description:
      - The image catalog directory on the IBM i Network install server.
      - The path is an IFS directory format.
    type: str
    default: '/etc/ibmi_ansible/fix_management/network_install'
  virtual_image_name_list:
    description:
      - The name list of the PTF image file and its directory, for example, C(/tmp/5733WQXPTFs/SF99433_1.bin).
      - You can specify all the PTF image files under one directory, for example, C(/tmp/PTFs/*ALL).
      - bin and iso image files are supported.
      - default is C(*ALL) for all the PTF image files under image catalog directory.
    type: list
    elements: str
    default: '*ALL'
  virtual_image_name_remove_list:
    description:
      - The name list of the PTF image file which will be moved from the image catalog, for example, C(SF99433_1.bin).
      - default is C(*ALL) for all the PTF image files under the image caltalog.
    type: list
    elements: str
    default: '*ALL'
  remove_image_files:
    description:
      - Whether the PTF image files under image catalog directory will be removed when removing entries from image catalog.
      - Whether the PTF image files under image catalog directory will be removed when removing the network install server configuration.
    type: bool
    default: true
  image_catalog_name:
    description:
      - The name of image catalog that is created on the server.
    type: str
    default: 'REPOSVRCLG'
  device_name:
    description:
      - The virtual optical device name.
    type: str
    default: 'REPOSVROPT'
  rollback:
    description:
      - Whether or not rollback if there's failure during the operation.
    type: bool
    default: true
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
   - If operation is setup_only or setup_and_addimgclge, the user who this task will run under, should be enrolled in system distribution directorty
   - Issue ADDDIRE command to add the user to the system distribution directory entry
   - Issue WRKDIRE command to check the current system distribution directory entries
seealso:
- module: ibmi_fix

author:
    - Wang Yuyu (@wangyuyu)
'''

EXAMPLES = r'''
- name: Setup IBM i Netwotk install server and add image files of group PTF for LPP 5733WQX
  ibm.power_ibmi.ibmi_fix_network_install_server:
    operation: 'setup_and_addimgclge'
    rollback: True
    virtual_image_name_list:
      - "/tmp/5733WQXPTFs/SF99433_1.bin"
      - "/tmp/5733WQXPTFs/SF99433_2.bin"
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
    type: str
    sample: 'CPC2102: Library TESTLIB created'
    returned: When error occurs.
stderr:
    description: The task standard error
    type: str
    returned: When error occurs.
    sample: 'Same optical device with different configuration already exists'
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
image_catalog_name:
    description: The name of image catalog on the server
    returned: always
    type: str
    sample: 'REPOSVRCLG'
device_name:
    description: The virtual optical device name
    returned: always
    type: str
    sample: 'REPOSVROPT'
image_catalog_directory_name:
    description: The path on the IBM i Network install server where the PTF image files are located.
    returned: always
    type: str
    sample: '/etc/ibmi_ansible/fix_management/network_install'
image_catalog_entries:
    description: The image catalog entries (image file name and its index) in the image catalog after the operation
    returned: When use operation setup_and_addmgclge, addimgclge_only, rmvimgclge_and_addimgclge, rmvimgclge_only or retrieve_image_catalog_entries
    type: list
    sample: [
        {"SF99433_1.bin": "1"},
        {"SF99433_2.bin": "2"}
    ]
success_list:
    description: The image catalog entries (image file name) which are added or removed successfully
    returned: When use operation setup_and_addmgclge, addimgclge_only, rmvimgclge_and_addimgclge, rmvimgclge_only
    type: list
    sample: [
        {"add": "SF99433_1.bin"},
        {"remove": "SF99433_2.bin"},
    ]
fail_list:
    description: The image catalog entries (image file name) which are failed to be added or removed
    returned: When use operation setup_and_addmgclge, addimgclge_only, rmvimgclge_and_addimgclge, rmvimgclge_only
    type: list
    sample: [
        {"add": "SF99433_1.bin"},
        {"remove": "SF99433_2.bin"},
    ]
'''

import datetime
import os
import sys
import binascii
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


def get_image_catalog_info(imodule, image_catalog_name):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    image_catalog_name_input = ibmi_util.fmtTo10(image_catalog_name) + "QUSRSYS   "
    itool.add(
        iPgm('qvoircld', 'QVOIRCLD')
        .addParm(
            iDS('Qvoi_RCLD0100_t', {'len': 'dmilen'})
            .addData(iData('Bytes_Returned', '10i0', ''))
            .addData(iData('Bytes_Available', '10i0', ''))
            .addData(iData('Image_Catalog_Type', '1A', ''))
            .addData(iData('Image_Catalog_Status', '1A', ''))
            .addData(iData('Reference_Catalog_Indicator', '1A', ''))
            .addData(iData('Dependent_Catalog_Indicator', '1A', ''))
            .addData(iData('Image_Catalog_Text', '50A', ''))
            .addData(iData('Virtual_Device_Name', '10A', ''))
            .addData(iData('Catalog_Directory_Offset', '10i0', ''))
            .addData(iData('Number_Of_Directories', '10i0', ''))
            .addData(iData('Catalog_Directory_Length', '10i0', ''))
            .addData(iData('Image_Catalog_CCSID', '10i0', ''))
            .addData(iData('Offset_To_First_Catalog_Entry', '10i0', ''))
            .addData(iData('Number_Of_Returned_Entries', '10i0', ''))
            .addData(iData('Image_Catalog_Entry_Length', '10i0', ''))
            .addData(iData('Total_Number_Of_Entries', '10i0', ''))
            .addData(iData('Reference_Catalog', '10A', ''))
            .addData(iData('Reference_Catalog_Library', '10A', ''))
            .addData(iData('Next_Vol', '6A', ''))
            .addData(iData('Image_Catalog_mode', '1A', ''))
            # CCSID 1200
            # 300A is pre-defined
            .addData(iData('Directory', '300A', '', {'hex': 'on'}))
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'dmilen'}))
        .addParm(iData('fmtnam', '8A', 'RCLD0200'))
        .addParm(iData('imgclgnam', '20A', image_catalog_name_input))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )
    itool.call(itransport)
    qvoircld = itool.dict_out('qvoircld')
    ibmi_util.log_debug(str(qvoircld), sys._getframe().f_code.co_name)
    if 'success' in qvoircld:
        rcld0100_t = qvoircld['Qvoi_RCLD0100_t']
        ibmi_util.log_debug(str(rcld0100_t), sys._getframe().f_code.co_name)
        return 0, rcld0100_t, qvoircld['success']
    else:
        return 1, None, qvoircld['error']


def get_image_catalog_info_with_entries(imodule, image_catalog_name, directory_length, reserved_field_length):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    # the location of entries in the returned set is decided by directory_length
    directory_length = directory_length + 'A'
    image_catalog_name_input = ibmi_util.fmtTo10(image_catalog_name) + "QUSRSYS   "
    if reserved_field_length == "0":
        itool.add(
            iPgm('qvoircld', 'QVOIRCLD')
            .addParm(
                iDS('Qvoi_RCLD0200_t', {'len': 'dmilen'})
                .addData(iData('Bytes_Returned', '10i0', ''))
                .addData(iData('Bytes_Available', '10i0', ''))
                .addData(iData('Image_Catalog_Type', '1A', ''))
                .addData(iData('Image_Catalog_Status', '1A', ''))
                .addData(iData('Reference_Catalog_Indicator', '1A', ''))
                .addData(iData('Dependent_Catalog_Indicator', '1A', ''))
                .addData(iData('Image_Catalog_Text', '50A', ''))
                .addData(iData('Virtual_Device_Name', '10A', ''))
                .addData(iData('Catalog_Directory_Offset', '10i0', ''))
                .addData(iData('Number_Of_Directories', '10i0', ''))
                .addData(iData('Catalog_Directory_Length', '10i0', ''))
                .addData(iData('Image_Catalog_CCSID', '10i0', ''))
                .addData(iData('Offset_To_First_Catalog_Entry', '10i0', ''))
                .addData(iData('Number_Of_Returned_Entries', '10i0', '', {'enddo': 'mycnt'}))
                .addData(iData('Image_Catalog_Entry_Length', '10i0', ''))
                .addData(iData('Total_Number_Of_Entries', '10i0', ''))
                .addData(iData('Reference_Catalog', '10A', ''))
                .addData(iData('Reference_Catalog_Library', '10A', ''))
                .addData(iData('Next_Vol', '6A', ''))
                .addData(iData('Image_Catalog_mode', '1A', ''))
                # CCSID 1200
                .addData(iData('Directory', directory_length, '', {'hex': 'on'}))
                .addData(iDS('Qvoi_Optical_Entry_Info_t', {'dim': '999', 'dou': 'mycnt'})
                         .addData(iData('Optical_Entry_Index', '10i0', ''))
                         .addData(iData('Optical_Entry_Status', '1A', ''))
                         # CCSID 1200
                         .addData(iData('Optical_Entry_Text', '100A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Entry_Write_Protect', '1A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Entry_Volume', '32A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Entry_Access', '1A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Media_Type', '1A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Image_Size', '10i0', ''))
                         .addData(iData('Optical_Entry_File_Name_Length', '10i0', ''))
                         # CCSID 1200
                         .addData(iData('Optical_Entry_File_Name', '512A', '', {'hex': 'on'}))
                         )
            )
            .addParm(iData('rcvlen', '10i0', '', {'setlen': 'dmilen'}))
            .addParm(iData('fmtnam', '8A', 'RCLD0200'))
            .addParm(iData('imgclgnam', '20A', image_catalog_name_input))
            .addParm(
                iDS('ERRC0100_t', {'len': 'errlen'})
                .addData(iData('errRet', '10i0', ''))
                .addData(iData('errAvl', '10i0', ''))
                .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                .addData(iData('errRsv', '1A', ''))
            )
        )
    else:
        reserved_field_length = reserved_field_length + 'B'
        itool.add(
            iPgm('qvoircld', 'QVOIRCLD')
            .addParm(
                iDS('Qvoi_RCLD0200_t', {'len': 'dmilen'})
                .addData(iData('Bytes_Returned', '10i0', ''))
                .addData(iData('Bytes_Available', '10i0', ''))
                .addData(iData('Image_Catalog_Type', '1A', ''))
                .addData(iData('Image_Catalog_Status', '1A', ''))
                .addData(iData('Reference_Catalog_Indicator', '1A', ''))
                .addData(iData('Dependent_Catalog_Indicator', '1A', ''))
                .addData(iData('Image_Catalog_Text', '50A', ''))
                .addData(iData('Virtual_Device_Name', '10A', ''))
                .addData(iData('Catalog_Directory_Offset', '10i0', ''))
                .addData(iData('Number_Of_Directories', '10i0', ''))
                .addData(iData('Catalog_Directory_Length', '10i0', ''))
                .addData(iData('Image_Catalog_CCSID', '10i0', ''))
                .addData(iData('Offset_To_First_Catalog_Entry', '10i0', ''))
                .addData(iData('Number_Of_Returned_Entries', '10i0', '', {'enddo': 'mycnt'}))
                .addData(iData('Image_Catalog_Entry_Length', '10i0', ''))
                .addData(iData('Total_Number_Of_Entries', '10i0', ''))
                .addData(iData('Reference_Catalog', '10A', ''))
                .addData(iData('Reference_Catalog_Library', '10A', ''))
                .addData(iData('Next_Vol', '6A', ''))
                .addData(iData('Image_Catalog_mode', '1A', ''))
                # CCSID 1200
                .addData(iData('Directory', directory_length, '', {'hex': 'on'}))
                # reserved length is not fixed. It is Space included for alignment.
                .addData(iData('Reserved', reserved_field_length, ''))
                .addData(iDS('Qvoi_Optical_Entry_Info_t', {'dim': '999', 'dou': 'mycnt'})
                         .addData(iData('Optical_Entry_Index', '10i0', ''))
                         .addData(iData('Optical_Entry_Status', '1A', ''))
                         # CCSID 1200
                         .addData(iData('Optical_Entry_Text', '100A', '', {'hex': 'on'}))
                         # if no entries are mounted(All are loaded)
                         # garbage characters in Optical_Entry_Write_Protect and following fields
                         .addData(iData('Optical_Entry_Write_Protect', '1A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Entry_Volume', '32A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Entry_Access', '1A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Media_Type', '1A', '', {'hex': 'on'}))
                         .addData(iData('Optical_Image_Size', '10i0', ''))
                         .addData(iData('Optical_Entry_File_Name_Length', '10i0', ''))
                         # CCSID 1200
                         .addData(iData('Optical_Entry_File_Name', '512A', '', {'hex': 'on'}))
                         )
            )
            .addParm(iData('rcvlen', '10i0', '', {'setlen': 'dmilen'}))
            .addParm(iData('fmtnam', '8A', 'RCLD0200'))
            .addParm(iData('imgclgnam', '20A', image_catalog_name_input))
            .addParm(
                iDS('ERRC0100_t', {'len': 'errlen'})
                .addData(iData('errRet', '10i0', ''))
                .addData(iData('errAvl', '10i0', ''))
                .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                .addData(iData('errRsv', '1A', ''))
            )
        )
    itool.call(itransport)
    qvoircld = itool.dict_out('qvoircld')
    ibmi_util.log_debug(str(qvoircld), sys._getframe().f_code.co_name)
    if 'success' in qvoircld:
        rcld0200_t = qvoircld['Qvoi_RCLD0200_t']
        ibmi_util.log_debug(str(rcld0200_t), sys._getframe().f_code.co_name)
        return 0, rcld0200_t, qvoircld['success']
    else:
        return 1, None, qvoircld['error']


def retrieve_image_catalog_entries(ibmi_module, image_catalog_name, directory_length, reserved_length):
    image_catalog_entries = []
    rc, info_image, err = get_image_catalog_info_with_entries(ibmi_module, image_catalog_name, directory_length, reserved_length)
    if rc != 0:
        return rc, None, err

    entries_count = int(info_image['Number_Of_Returned_Entries'])
    if entries_count > 0:
        entries = info_image['Qvoi_Optical_Entry_Info_t']
        # when there is only 1 record in entries, it is not a list returned
        if entries_count == 1:
            entry_name = binascii.a2b_hex(entries['Optical_Entry_File_Name']).decode("utf-16")
            entry_index = entries['Optical_Entry_Index']
            image_catalog_entries.append({entry_name: entry_index})
        else:
            for each_entry in entries:
                entry_name = binascii.a2b_hex(each_entry['Optical_Entry_File_Name']).decode("utf-16")
                entry_index = each_entry['Optical_Entry_Index']
                image_catalog_entries.append({entry_name: entry_index})
    return rc, image_catalog_entries, err


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


def get_entry_index_in_image_catalog(image_catalog_existing_entries, entry_file_name):

    entry_index = "0"
    if image_catalog_existing_entries is not None and len(image_catalog_existing_entries) != 0:
        for each_entry in image_catalog_existing_entries:
            file_name = tuple(each_entry.keys())[0].strip()
            if file_name.upper() == entry_file_name.upper():
                entry_index = str(tuple(each_entry.values())[0])
                break

    return entry_index


def setup_operation(ibmi_module, module, image_catalog_name, opt_device_name, dir_target, is_rollback):
    db_conn = ibmi_module.get_connection()
    # check the optical device and image catalog exist or not
    device_exist = check_object_existence(db_conn, "QSYS", "*DEVD", opt_device_name)
    imgclg_exist = check_object_existence(db_conn, "QUSRSYS", "*IMGCLG", image_catalog_name)

    command_map = {}
    command_log = "Command log of setup operation."
    command_map["cl_crt_device"] = "QSYS/CRTDEVOPT DEVD(" + opt_device_name +\
                                   ") RSRCNAME(*VRT) ONLINE(*YES) TEXT('Created by Ansible for IBM i Network install')"
    command_map["cl_crt_catalog"] = "QSYS/CRTIMGCLG IMGCLG(" + image_catalog_name + ") DIR('" + dir_target +\
                                    "') CRTDIR(*YES) TEXT('Created by Ansible for IBM i')"
    command_map["cl_vary_on_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*ON)"
    command_map["cl_start_NFS_service"] = "QSYS/STRNFSSVR *ALL"
    command_map["cl_export_catalog"] = "QSYS/CHGNFSEXP OPTIONS('-i -o ro') DIR('" + dir_target + "')"
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*OFF) FRCVRYOFF(*YES)"
    command_map["cl_delete_image_catalog"] = "QSYS/DLTIMGCLG IMGCLG(" + image_catalog_name + ") KEEP(*NO)"
    command_map["unload_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + image_catalog_name + ")  OPTION(*UNLOAD)"
    command_map["cl_dlt_device"] = "QSYS/DLTDEVD DEVD(" + opt_device_name + ")"

    # step 1: create optical device
    if device_exist == 0:
        module.log("Run CL Command: " + command_map["cl_crt_device"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_crt_device"])
        command_log = command_log + "\n" + command_map["cl_crt_device"]
        command_log = command_log + "\n" + out
        if rc > 0:
            if is_rollback:
                run_a_list_of_commands(ibmi_module, ["cl_dlt_device"], command_map)
            return rc, out, err, command_log

    # step 2: image catalog
    # if image catalog already exists, check if it is loaded with the expected optical device and expected directory
    imgclg_create = 1
    if imgclg_exist == 1:
        rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
        if rc == 0:
            catalog_directory_length = info_return['Catalog_Directory_Length']
            first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
            directory_offset = info_return['Catalog_Directory_Offset']
            reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))
            rc, info_detail, err = get_image_catalog_info_with_entries(ibmi_module, image_catalog_name, catalog_directory_length, str(reserved_field_length))
            if rc != 0:
                return rc, None, err, ""
            current_image_directory = binascii.a2b_hex(info_detail['Directory']).decode("utf-16").upper()
            current_image_directory = current_image_directory.strip('/')
            current_device_name = info_return['Virtual_Device_Name'].upper()
            if (current_device_name != "" and current_device_name != opt_device_name.upper()) or current_image_directory != dir_target.upper().strip('/'):
                # Same image catalog name with different image catalog directory. Remove the current image catalog
                # run_a_list_of_commands(ibmi_module, ["unload_image_catalog", "cl_delete_image_catalog"], command_map)
                if info_return['Image_Catalog_Status'] == '1':
                    module.log("Run CL Command: " + command_map["unload_image_catalog"])
                    rc, out, err = itoolkit_run_command(ibmi_module, command_map["unload_image_catalog"])
                    command_log = command_log + "\n" + command_map["unload_image_catalog"]
                    command_log = command_log + "\n" + out
                module.log("Run CL Command: " + command_map["cl_delete_image_catalog"])
                rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_delete_image_catalog"])
                command_log = command_log + "\n" + command_map["cl_delete_image_catalog"]
                command_log = command_log + "\n" + out
            else:
                imgclg_create = 0
        else:
            run_a_list_of_commands(ibmi_module, ["unload_image_catalog", "cl_delete_image_catalog"], command_map)

    if imgclg_create == 1:
        module.log("Run CL Command: " + command_map["cl_crt_catalog"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_crt_catalog"])
        command_log = command_log + "\n" + command_map["cl_crt_catalog"]
        command_log = command_log + "\n" + out
        if rc > 0:
            if is_rollback:
                run_a_list_of_commands(ibmi_module, ["cl_vary_off_device",
                                                     "cl_delete_image_catalog", "cl_dlt_device"], command_map)
            return rc, out, err, command_log

    # cannot load the image catalog here
    # To load image catalog REPOSVRCLG, at least one image catalog entry must be in loaded status

    # step 3: vary on optical device
    module.log("Run CL Command: " + command_map["cl_vary_on_device"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_on_device"])
    command_log = command_log + "\n" + command_map["cl_vary_on_device"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(ibmi_module, ["cl_vary_off_device",
                                                 "cl_delete_image_catalog", "cl_dlt_device"], command_map)
        return rc, out, err, command_log

    # step 4: start NCS server
    module.log("Run CL Command: " + command_map["cl_start_NFS_service"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_start_NFS_service"])
    command_log = command_log + "\n" + command_map["cl_start_NFS_service"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    # step 5: export the image catalog
    module.log("Run CL Command: " + command_map["cl_export_catalog"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_export_catalog"])
    command_log = command_log + "\n" + command_map["cl_export_catalog"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log


def rollback_imgclg_entries(ibmi_module, module, image_catalog_name, rollback_entries, rollback_operation):
    command_log = "Command log of rollback operation."

    if rollback_operation == "remove":
        rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
        if rc != 0:
            return rc
        catalog_directory_length = info_return['Catalog_Directory_Length']
        first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
        directory_offset = info_return['Catalog_Directory_Offset']
        reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))
        entry_rc, image_catalog_existing_entries, err = retrieve_image_catalog_entries(ibmi_module, image_catalog_name,
                                                                                       catalog_directory_length,
                                                                                       str(reserved_field_length))
        for each_entry in rollback_entries:
            each_file = tuple(each_entry.keys())[0]
            index_exist = get_entry_index_in_image_catalog(image_catalog_existing_entries, each_file)
            if index_exist != "0":
                cl_catalog_entry_removing = "QSYS/RMVIMGCLGE IMGCLG(" + image_catalog_name + ") IMGCLGIDX("\
                                            + index_exist + ") KEEP(*NO)"
                module.log("Run CL Command: " + cl_catalog_entry_removing)
                rc, out, err = itoolkit_run_command(ibmi_module, cl_catalog_entry_removing)
                command_log = command_log + "\n" + cl_catalog_entry_removing
                command_log = command_log + "\n" + out

        return rc, command_log

    if rollback_operation == "add":
        for each_entry in rollback_entries:
            each_file = tuple(each_entry.keys())[0]
            cl_catalog_entry_adding = "QSYS/ADDIMGCLGE IMGCLG(" + image_catalog_name + ") FROMFILE('"\
                                      + each_file + "') TOFILE(*fromfile) REPLACE(*YES) "\
                                      + "TEXT('Added by Ansible for IBM i for Network install')"
            module.log("Run CL Command: " + cl_catalog_entry_adding)
            rc, out, err = itoolkit_run_command(ibmi_module, cl_catalog_entry_adding)
            command_log = command_log + "\n" + cl_catalog_entry_adding
            command_log = command_log + "\n" + out

        return rc, command_log


def addimgclge_operation(ibmi_module, module, image_catalog_name, opt_device_name, dir_target, fix_file_name_list, is_rollback):
    image_catalog_entries = []

    command_map = {}
    command_log = "Command log of addimgclge operation."
    command_map["unload_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + image_catalog_name + ")  OPTION(*UNLOAD)"
    command_map["lod_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + image_catalog_name + ") DEV("\
                                       + opt_device_name + ") OPTION(*LOAD)"
    command_map["cl_catalog_in_order"] = "QSYS/VFYIMGCLG IMGCLG(" + image_catalog_name + ") TYPE(*PTF) SORT(*YES)"
    command_map["cl_catalog_NFSSHR"] = "QSYS/VFYIMGCLG IMGCLG(" + image_catalog_name + ") TYPE(*PTF) NFSSHR(*YES)"
    command_map["cl_catalog_authorities"] = "QSYS/CHGAUT OBJ('" + dir_target + "') USER(*PUBLIC) DTAAUT(*RX) SUBTREE(*ALL)"

    success_list = []
    fail_list = []

    # step 1: inital fail_list
    rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
    if rc != 0:
        return rc, None, err, "", image_catalog_entries, success_list, fail_list
    catalog_directory_length = info_return['Catalog_Directory_Length']
    first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
    directory_offset = info_return['Catalog_Directory_Offset']
    reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))
    entry_rc, image_catalog_existing_entries, err = retrieve_image_catalog_entries(ibmi_module, image_catalog_name,
                                                                                   catalog_directory_length, str(reserved_field_length))
    if entry_rc != 0:
        return entry_rc, None, err, "", image_catalog_entries, success_list, fail_list

    for entry_file_name in fix_file_name_list:
        entry_file_name = entry_file_name.strip()
        if len(entry_file_name) >= 4 and (entry_file_name[-4:]).upper() == '*ALL':
            if len(entry_file_name) == 4:
                # *ALL
                file_target = dir_target
            else:
                # /XXX/XXX/*ALL
                file_target = entry_file_name[0:-4]

            if not os.path.exists(file_target):
                err = "No such directory: " + file_target
                return -1, None, err, "ADDIMGCLGE", image_catalog_entries, success_list, fail_list

            file_index = 1
            add_file = 0
            for each_file in os.listdir(file_target):
                try:
                    f_suffix = (each_file[-4:]).upper()
                    if (f_suffix == ".BIN") or (f_suffix == ".ISO"):
                        add_file = 1
                except Exception:
                    add_file = 0
                if add_file == 1:
                    # check if the image file already exists in the image catalog
                    index_exist = get_entry_index_in_image_catalog(image_catalog_existing_entries, each_file)
                    file_index = file_index + 1
                    if index_exist == "0":
                        target_file = os.path.join(file_target, each_file)
                        fail_list.append({"add": target_file})
                    add_file = 0
            # no files
            if file_index == 1 and add_file == 0:
                err = "No image files was found"
                return -1, None, err, "ADDIMGCLGE", image_catalog_entries, success_list, fail_list

        else:
            # check if the image file already exists in the image catalog
            index_exist = get_entry_index_in_image_catalog(image_catalog_existing_entries, os.path.basename(entry_file_name))
            if index_exist == "0":
                fail_list.append({"add": entry_file_name})

    # step 2: unload the image catalog for the ADDIMGCLGE operation
    # if image catalog is unloaded already, skip this step
    current_imgclg_status = info_return['Image_Catalog_Status']
    if current_imgclg_status == '1':
        module.log("Run CL Command: " + command_map["unload_image_catalog"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["unload_image_catalog"])
        command_log = command_log + "\n" + command_map["unload_image_catalog"]
        command_log = command_log + "\n" + out
        if rc > 0:
            return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    # step 3: ADDIMGCLGE
    todo_add_entries = fail_list.copy()
    # already_added_entries for rollback
    already_added_entries = []
    for todo_entry in todo_add_entries:
        todo_entry_file = tuple(todo_entry.values())[0]
        cl_catalog_entry_adding = "QSYS/ADDIMGCLGE IMGCLG(" + image_catalog_name + ") FROMFILE('"\
                                  + todo_entry_file + "') TOFILE(*fromfile) REPLACE(*YES) "\
                                  + "TEXT('Added by Ansible for IBM i for Network install')"
        module.log("Run CL Command: " + cl_catalog_entry_adding)
        rc, out, err = itoolkit_run_command(ibmi_module, cl_catalog_entry_adding)
        command_log = command_log + "\n" + cl_catalog_entry_adding
        command_log = command_log + "\n" + out
        if rc > 0:
            if is_rollback:
                # remove all the newly added entries
                rc_rollback, command_log_rollback = rollback_imgclg_entries(ibmi_module, module, image_catalog_name,
                                                                            already_added_entries, "remove")
                success_list.clear()
                # fail_list = todo_add_entries.copy()
                return rc, out, err, command_log + command_log_rollback, image_catalog_entries, success_list, todo_add_entries
            else:
                return rc, out, err, command_log, image_catalog_entries, success_list, fail_list
        else:
            # index unknown.
            already_added_entries.append({os.path.basename(todo_entry_file): "0"})
            success_list.append({"add": todo_entry_file})
            fail_list.remove({"add": todo_entry_file})

    # step 4: load the image catalog
    module.log("Run CL Command: " + command_map["lod_image_catalog"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["lod_image_catalog"])
    command_log = command_log + "\n" + command_map["lod_image_catalog"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            # remove all the newly added entries
            rc_rollback, command_log_rollback = rollback_imgclg_entries(ibmi_module, module, image_catalog_name, already_added_entries, "remove")
            if current_imgclg_status == '1':
                run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
            success_list.clear()
            # fail_list = todo_add_entries.copy()
            return rc, out, err, command_log + command_log_rollback, image_catalog_entries, success_list, todo_add_entries
        else:
            return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    # step 5: Verify that the images are in the correct order
    module.log("Run CL Command: " + command_map["cl_catalog_in_order"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_catalog_in_order"])
    command_log = command_log + "\n" + command_map["cl_catalog_in_order"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
        return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    # step 6: verify the image catalog to create a volume list file (VOLUME_LIST).
    module.log("Run CL Command: " + command_map["cl_catalog_NFSSHR"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_catalog_NFSSHR"])
    command_log = command_log + "\n" + command_map["cl_catalog_NFSSHR"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
        return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    # get image_catalog_entries after SORT(*YES)
    # need to call get_image_catalog_info again to get reserved_field_length. Otherwise retrieve_image_catalog_entries may hang up
    rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
    if rc != 0:
        return rc, None, err, "", image_catalog_entries, success_list, fail_list
    catalog_directory_length = info_return['Catalog_Directory_Length']
    first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
    directory_offset = info_return['Catalog_Directory_Offset']
    reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))
    rc, image_catalog_entries, err = retrieve_image_catalog_entries(ibmi_module, image_catalog_name, catalog_directory_length, str(reserved_field_length))
    if rc != 0:
        return rc, None, err, "", image_catalog_entries, success_list, fail_list

    # step 7: Ensure that the NFS user has the correct authority.
    module.log("Run CL Command: " + command_map["cl_catalog_authorities"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_catalog_authorities"])
    command_log = command_log + "\n" + command_map["cl_catalog_authorities"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
        return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log, image_catalog_entries, success_list, fail_list


def rmvimgclge_operation(ibmi_module, module, image_catalog_name, opt_device_name, dir_target,
                         fix_file_name_remove_list, remove_image_files, is_rollback, PTF_sort):
    image_catalog_entries = []
    command_map = {}
    command_log = "Command log of rmvimgclge operation."
    command_map["unload_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + image_catalog_name + ")  OPTION(*UNLOAD)"
    command_map["lod_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + image_catalog_name + ") DEV("\
                                       + opt_device_name + ") OPTION(*LOAD)"
    command_map["cl_catalog_in_order"] = "QSYS/VFYIMGCLG IMGCLG(" + image_catalog_name + ") TYPE(*PTF) SORT(*YES)"
    command_map["cl_catalog_NFSSHR"] = "QSYS/VFYIMGCLG IMGCLG(" + image_catalog_name + ") TYPE(*PTF) NFSSHR(*YES)"
    command_map["cl_catalog_authorities"] = "QSYS/CHGAUT OBJ('" + dir_target + "') USER(*PUBLIC) DTAAUT(*RX) SUBTREE(*ALL)"

    success_list = []
    fail_list = []

    # step 1: inital fail_list
    rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
    if rc != 0:
        return rc, None, err, "", image_catalog_entries, success_list, fail_list
    catalog_directory_length = info_return['Catalog_Directory_Length']
    first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
    directory_offset = info_return['Catalog_Directory_Offset']
    reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))
    entry_rc, image_catalog_existing_entries, err = retrieve_image_catalog_entries(ibmi_module, image_catalog_name,
                                                                                   catalog_directory_length, str(reserved_field_length))
    if entry_rc != 0:
        return entry_rc, None, err, "", image_catalog_entries, success_list, fail_list

    todo_remove_entries = []
    for fix_file_name in fix_file_name_remove_list:
        entry_file_name = fix_file_name.strip()
        if entry_file_name == '*ALL':
            if len(image_catalog_existing_entries) != 0:
                for each_entry in image_catalog_existing_entries:
                    entry_index = tuple(each_entry.values())[0]
                    entry_file = tuple(each_entry.keys())[0]
                    fail_list.append({"remove": entry_file})
                    todo_remove_entries.append({entry_file: entry_index})
        else:
            if len(image_catalog_existing_entries) != 0:
                # check if the image file already exists in the image catalog
                # if not, skip this file
                entry_index = get_entry_index_in_image_catalog(image_catalog_existing_entries, entry_file_name)
                if entry_index != '0':
                    fail_list.append({"remove": entry_file_name})
                    todo_remove_entries.append({entry_file_name: entry_index})

    # step 2: unload the image catalog for the RMVIMGCLGE operation
    # if image catalog is unloaded already, skip this step
    current_imgclg_status = info_return['Image_Catalog_Status']
    if current_imgclg_status == '1':
        module.log("Run CL Command: " + command_map["unload_image_catalog"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["unload_image_catalog"])
        command_log = command_log + "\n" + command_map["unload_image_catalog"]
        command_log = command_log + "\n" + out
        if rc > 0:
            return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    # step 3: RMVIMGCLGE
    already_removed_entries = []
    fail_list_rollback = fail_list.copy()
    for todo_remove_entry in todo_remove_entries:
        entry_index = tuple(todo_remove_entry.values())[0]
        entry_file_name = tuple(todo_remove_entry.keys())[0]
        cl_catalog_entry_removing = "QSYS/RMVIMGCLGE IMGCLG(" + image_catalog_name + ") IMGCLGIDX("\
                                    + entry_index + ") KEEP(*"
        if remove_image_files:
            cl_catalog_entry_removing = cl_catalog_entry_removing + "NO)"
        else:
            cl_catalog_entry_removing = cl_catalog_entry_removing + "YES)"
        module.log("Run CL Command: " + cl_catalog_entry_removing)
        rc, out, err = itoolkit_run_command(ibmi_module, cl_catalog_entry_removing)
        command_log = command_log + "\n" + cl_catalog_entry_removing
        command_log = command_log + "\n" + out
        if rc > 0:
            if is_rollback:
                # add all the newly removed entries
                # index unknown
                rc_rollback, command_log_rollback = rollback_imgclg_entries(ibmi_module, module, image_catalog_name, already_removed_entries, "add")
                success_list.clear()
                return rc, out, err, command_log + command_log_rollback, image_catalog_entries, success_list, fail_list_rollback
            else:
                return rc, out, err, command_log, image_catalog_entries, success_list, fail_list
        else:
            already_removed_entries.append({entry_file_name: entry_index})
            success_list.append({"remove": entry_file_name})
            fail_list.remove({"remove": entry_file_name})

    # if the image catalog is empty, skip step 3,4 and 5
    rc_api, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
    if rc_api > 0:
        return rc, out, err, command_log, image_catalog_entries, success_list, fail_list
    entries_count = int(info_return['Total_Number_Of_Entries'])

    if entries_count > 0:
        # step 3: load the image catalog
        module.log("Run CL Command: " + command_map["lod_image_catalog"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["lod_image_catalog"])
        command_log = command_log + "\n" + command_map["lod_image_catalog"]
        command_log = command_log + "\n" + out
        if rc > 0:
            if is_rollback:
                # add all the newly removed entries
                # index unknown
                rc_rollback, command_log_rollback = rollback_imgclg_entries(ibmi_module, module, image_catalog_name, already_removed_entries, "add")
                success_list.clear()
                if current_imgclg_status == '1':
                    run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
                return rc, out, err, command_log + command_log_rollback, image_catalog_entries, success_list, fail_list_rollback
            else:
                return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

        if PTF_sort:
            # step 4: Verify that the images are in the correct order
            module.log("Run CL Command: " + command_map["cl_catalog_in_order"])
            rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_catalog_in_order"])
            command_log = command_log + "\n" + command_map["cl_catalog_in_order"]
            command_log = command_log + "\n" + out
            if rc > 0:
                if is_rollback:
                    run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
                return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

            # step 5: verify the image catalog to create a volume list file (VOLUME_LIST).
            module.log("Run CL Command: " + command_map["cl_catalog_NFSSHR"])
            rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_catalog_NFSSHR"])
            command_log = command_log + "\n" + command_map["cl_catalog_NFSSHR"]
            command_log = command_log + "\n" + out
            if rc > 0:
                if is_rollback:
                    run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
                return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    # get image_catalog_entries after SORT(*YES)
    rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
    if rc != 0:
        return rc, None, err, "", image_catalog_entries, success_list, fail_list
    catalog_directory_length = info_return['Catalog_Directory_Length']
    first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
    directory_offset = info_return['Catalog_Directory_Offset']
    reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))
    rc, image_catalog_entries, err = retrieve_image_catalog_entries(ibmi_module, image_catalog_name, catalog_directory_length, str(reserved_field_length))
    if rc != 0:
        return rc, None, err, "", image_catalog_entries, success_list, fail_list

    # step 6: Ensure that the NFS user has the correct authority.
    module.log("Run CL Command: " + command_map["cl_catalog_authorities"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_catalog_authorities"])
    command_log = command_log + "\n" + command_map["cl_catalog_authorities"]
    command_log = command_log + "\n" + out
    if rc > 0:
        if is_rollback:
            run_a_list_of_commands(ibmi_module, ["unload_image_catalog"], command_map)
        return rc, out, err, command_log, image_catalog_entries, success_list, fail_list

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log, image_catalog_entries, success_list, fail_list


def uninstall_operation(ibmi_module, module, image_catalog_name, opt_device_name, remove_image_files, is_rollback):
    db_conn = ibmi_module.get_connection()

    command_map = {}
    command_log = "Command log of uninstall operation."
    command_map["cl_vary_off_device"] = "QSYS/VRYCFG CFGOBJ(" + opt_device_name + ") CFGTYPE(*DEV) STATUS(*OFF)"

    if remove_image_files:
        command_map["cl_delete_image_catalog"] = "QSYS/DLTIMGCLG IMGCLG(" + image_catalog_name + ") KEEP(*NO)"
    else:
        command_map["cl_delete_image_catalog"] = "QSYS/DLTIMGCLG IMGCLG(" + image_catalog_name + ") KEEP(*YES)"

    command_map["unload_image_catalog"] = "QSYS/LODIMGCLG IMGCLG(" + image_catalog_name + ")  OPTION(*UNLOAD)"
    command_map["cl_dlt_device"] = "QSYS/DLTDEVD DEVD(" + opt_device_name + ")"

    # check the optical device and image catalog exist or not
    device_exist = check_object_existence(db_conn, "QSYS", "*DEVD", opt_device_name)
    imgclg_exist = check_object_existence(db_conn, "QUSRSYS", "*IMGCLG", image_catalog_name)

    if imgclg_exist != 0:
        # step 1: unload the image catalog
        rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
        if rc != 0:
            return rc, None, err, ""
        # if image catalog is unloaded already, skip this step
        if info_return['Image_Catalog_Status'] == '1':
            module.log("Run CL Command: " + command_map["unload_image_catalog"])
            rc, out, err = itoolkit_run_command(ibmi_module, command_map["unload_image_catalog"])
            command_log = command_log + "\n" + command_map["unload_image_catalog"]
            command_log = command_log + "\n" + out
            if rc > 0:
                return rc, out, err, command_log

    if device_exist != 0:
        # step 2: vary off the optical device
        module.log("Run CL Command: " + command_map["cl_vary_off_device"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_vary_off_device"])
        command_log = command_log + "\n" + command_map["cl_vary_off_device"]
        command_log = command_log + "\n" + out
        if rc > 0:
            return rc, out, err, command_log

    if imgclg_exist != 0:
        # step 3: delete the image catalog
        module.log("Run CL Command: " + command_map["cl_delete_image_catalog"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_delete_image_catalog"])
        command_log = command_log + "\n" + command_map["cl_delete_image_catalog"]
        command_log = command_log + "\n" + out
        if rc > 0:
            return rc, out, err, command_log

    if device_exist != 0:
        # step 4: delete the device
        module.log("Run CL Command: " + command_map["cl_dlt_device"])
        rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_dlt_device"])
        command_log = command_log + "\n" + command_map["cl_dlt_device"]
        command_log = command_log + "\n" + out
        if rc > 0:
            return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    if (device_exist == 0) and (imgclg_exist == 0):
        return rc, None, "The optical device and image catalog do not exist", ""
    else:
        return rc, out, err, command_log


def retrieve_operation(ibmi_module, module, image_catalog_name, opt_device_name, image_catalog_directory, is_rollback):
    image_catalog_entries = []

    rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
    if rc != 0:
        return rc, None, err, "Failure in retrieving image catalog entries.", image_catalog_entries

    catalog_directory_length = info_return['Catalog_Directory_Length']
    first_entry_offset = info_return['Offset_To_First_Catalog_Entry']
    directory_offset = info_return['Catalog_Directory_Offset']
    reserved_field_length = int(first_entry_offset) - (int(directory_offset) + int(catalog_directory_length))

    rc, image_catalog_entries, err = retrieve_image_catalog_entries(ibmi_module, image_catalog_name, catalog_directory_length, str(reserved_field_length))
    if rc != 0:
        return rc, None, err, "Failure in retrieving image catalog entries.", image_catalog_entries

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, None, "", "Image catalog entries are retrieved successfully.", image_catalog_entries


def NFSServer_operation(ibmi_module, module):
    command_map = {}
    command_log = "Command log of restart NFS server operation."
    command_map["cl_start_NFS_service"] = "QSYS/STRNFSSVR *ALL"
    command_map["cl_end_NFS_service"] = "QSYS/ENDNFSSVR *ALL"

    # step 1: end NFS service
    module.log("Run CL Command: " + command_map["cl_end_NFS_service"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_end_NFS_service"])
    command_log = command_log + "\n" + command_map["cl_end_NFS_service"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    # step 2: start NFS service
    module.log("Run CL Command: " + command_map["cl_start_NFS_service"])
    rc, out, err = itoolkit_run_command(ibmi_module, command_map["cl_start_NFS_service"])
    command_log = command_log + "\n" + command_map["cl_start_NFS_service"]
    command_log = command_log + "\n" + out
    if rc > 0:
        return rc, out, err, command_log

    rc = IBMi_COMMAND_RC_SUCCESS
    return rc, out, err, command_log


def return_valid_name(dir_name_input):
    dir_name = dir_name_input

    if dir_name_input.find('~') >= 1:
        return 1, dir_name_input

    if dir_name_input.startswith('~'):
        home_path = os.getenv('HOME', None)
        if home_path is None:
            return 2, dir_name_input
        dir_name = os.path.join(home_path, os.path.relpath(dir_name_input, '~/'))

    return 0, dir_name


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', default='setup_only', choices=['setup_only',
                                                                      'setup_and_addimgclge',
                                                                      'addimgclge_only',
                                                                      'rmvimgclge_only',
                                                                      'rmvimgclge_and_addimgclge',
                                                                      'uninstall',
                                                                      'retrieve_image_catalog_entries',
                                                                      'restart_NFS_server']),
            image_catalog_directory_name=dict(type='str', default='/etc/ibmi_ansible/fix_management/network_install'),
            virtual_image_name_list=dict(type='list', elements='str', default=['*ALL']),
            virtual_image_name_remove_list=dict(type='list', elements='str', default=['*ALL']),
            remove_image_files=dict(type='bool', default=True),
            image_catalog_name=dict(type='str', default='REPOSVRCLG'),
            device_name=dict(type='str', default='REPOSVROPT'),
            rollback=dict(type='bool', default=True),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    operation = module.params['operation']
    image_catalog_directory_input = module.params['image_catalog_directory_name']
    fix_file_name_list_input = module.params['virtual_image_name_list']
    fix_file_name_remove_list = module.params['virtual_image_name_remove_list']
    remove_image_files = module.params['remove_image_files']
    image_catalog_name = module.params['image_catalog_name']
    device_name = module.params['device_name']
    rollback = module.params['rollback']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    # return valid directory for image_catalog_directory and virtual_image_name_list(check dir part)
    rc, image_catalog_directory = return_valid_name(image_catalog_directory_input)
    if rc == 1:
        return module.fail_json(msg="The value specified in image_catalog_directory_name is not a valid directory. The value is "
                                    + image_catalog_directory_input)
    if rc == 2:
        return module.fail_json(msg="getenv 'HOME' failed.")

    fix_file_name_list = []
    for each_fix_name_list in fix_file_name_list_input:
        rc, each_fix_name_list_valid = return_valid_name(each_fix_name_list)
        if rc == 1:
            return module.fail_json(msg="The value specified in virtual_image_name_list is not a valid file name. The value is " + each_fix_name_list)
        if rc == 2:
            return module.fail_json(msg="getenv 'HOME' failed.")
        fix_file_name_list.append(each_fix_name_list_valid)

    if not os.path.exists(image_catalog_directory):
        # create the image catalog
        os.makedirs(image_catalog_directory)

    if not os.path.isdir(image_catalog_directory):
        return module.fail_json(msg="The value specified in image_catalog_directory_name is not a valid directory. The value is " + image_catalog_directory)

    startd = datetime.datetime.now()

    ibmi_module = imodule.IBMiModule(become_user_name=become_user,
                                     become_user_password=become_user_password)

    # make sure the image catalog name is in upper case
    image_catalog_name = image_catalog_name.upper()
    # make sure the optical device name is in upper case
    device_name = device_name.upper()

    # check if the input values of device name and image catalog directory name are correct
    if operation in ['addimgclge_only',
                     'rmvimgclge_only',
                     'rmvimgclge_and_addimgclge',
                     'retrieve_image_catalog_entries',
                     'uninstall']:
        rc, info_return, err = get_image_catalog_info(ibmi_module, image_catalog_name)
        if rc != 0:
            module.fail_json(msg='Failure in retrieving image catalog')

        catalog_directory_length = info_return['Catalog_Directory_Length']
        current_image_directory_hex = (info_return['Directory'])[0: int(catalog_directory_length) * 2]
        current_image_directory = binascii.a2b_hex(current_image_directory_hex).decode("utf-16")
        if (current_image_directory.strip('/').upper() != image_catalog_directory.strip('/').upper()):
            module.fail_json(msg="Incorrect image_catalog_directory_name input: " + image_catalog_directory)

        # do not check device name if the device name is blank
        # Because the device is not loaded to the image catalog
        current_device_name = (info_return['Virtual_Device_Name']).strip()
        if ((current_device_name != "") and (current_device_name.upper() != device_name.strip().upper())):
            module.fail_json(msg="Incorrect device_name input: " + device_name)

    if operation == 'setup_only':
        rc, out, err, command_log = setup_operation(ibmi_module, module, image_catalog_name, device_name, image_catalog_directory, rollback)
    elif operation == 'addimgclge_only':
        rc, out, err, command_log, image_catalog_entries, success_list, fail_list = addimgclge_operation(ibmi_module, module, image_catalog_name,
                                                                                                         device_name, image_catalog_directory,
                                                                                                         fix_file_name_list, rollback)
    elif operation == 'setup_and_addimgclge':
        rc, out, err, command_log = setup_operation(ibmi_module, module, image_catalog_name, device_name, image_catalog_directory, rollback)
        success_list = []
        fail_list = []
        if rc == IBMi_COMMAND_RC_SUCCESS:
            rc, out, err, command_log, image_catalog_entries, success_list, fail_list = addimgclge_operation(ibmi_module, module, image_catalog_name,
                                                                                                             device_name, image_catalog_directory,
                                                                                                             fix_file_name_list, rollback)
    elif operation == 'rmvimgclge_only':
        # Do issue VFYIMGCLG IMGCLG(REPOSVRCLG) TYPE(*PTF) SORT(*YES) after rmvimgclge
        PTF_sort = True
        rc, out, err, command_log, image_catalog_entries, success_list, fail_list = rmvimgclge_operation(ibmi_module, module, image_catalog_name, device_name,
                                                                                                         image_catalog_directory, fix_file_name_remove_list,
                                                                                                         remove_image_files, rollback, PTF_sort)
    elif operation == 'rmvimgclge_and_addimgclge':
        # Do not issue VFYIMGCLG IMGCLG(REPOSVRCLG) TYPE(*PTF) SORT(*YES) after rmvimgclge. Do it after addimgclge
        PTF_sort = False
        rc, out, err, command_log, image_catalog_entries, rmv_success_list, rmv_fail_list = rmvimgclge_operation(ibmi_module, module, image_catalog_name,
                                                                                                                 device_name, image_catalog_directory,
                                                                                                                 fix_file_name_remove_list, remove_image_files,
                                                                                                                 rollback, PTF_sort)
        success_list = rmv_success_list.copy()
        fail_list = rmv_fail_list.copy()
        if rc == IBMi_COMMAND_RC_SUCCESS:
            rc, out, err, command_log, image_catalog_entries, add_success_list, add_fail_list = addimgclge_operation(ibmi_module, module, image_catalog_name,
                                                                                                                     device_name, image_catalog_directory,
                                                                                                                     fix_file_name_list, rollback)
            success_list.extend(add_success_list)
            fail_list.extend(add_fail_list)
    elif operation == 'uninstall':
        rc, out, err, command_log = uninstall_operation(ibmi_module, module, image_catalog_name, device_name, remove_image_files, rollback)
    elif operation == 'retrieve_image_catalog_entries':
        rc, out, err, command_log, image_catalog_entries = retrieve_operation(ibmi_module, module, image_catalog_name,
                                                                              device_name, image_catalog_directory, rollback)
    elif operation == 'restart_NFS_server':
        # if OPT1605 from command "WRKIMGCLGE IMGCLG(*DEV) DEV(DEVNAME) " on the client, INSPTF will fail.
        # Need restart NFS service on the server
        rc, out, err, command_log = NFSServer_operation(ibmi_module, module)
    else:
        module.fail_json(msg='Invalid operation input')

    endd = datetime.datetime.now()
    delta = endd - startd

    if joblog or (rc != IBMi_COMMAND_RC_SUCCESS):
        job_log = ibmi_module.itoolkit_get_job_log(startd)
    else:
        job_log = []

    if rc != 0:
        if operation in ['addimgclge_only', 'setup_and_addimgclge', 'rmvimgclge_only', 'rmvimgclge_and_addimgclge']:
            result_failed = dict(
                stderr=err,
                stdout=command_log,
                rc=rc,
                job_log=job_log,
                fail_list=fail_list,
                success_list=success_list
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
        if operation in ['retrieve_image_catalog_entries']:
            result_success = dict(
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                stdout=command_log,
                stderr=err,
                rc=rc,
                job_log=job_log,
                image_catalog_name=image_catalog_name,
                device_name=device_name,
                image_catalog_directory_name=image_catalog_directory,
                image_catalog_entries=image_catalog_entries,
            )
        elif operation in ['addimgclge_only', 'setup_and_addimgclge', 'rmvimgclge_only', 'rmvimgclge_and_addimgclge']:
            result_success = dict(
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                stdout=command_log,
                stderr=err,
                rc=rc,
                job_log=job_log,
                image_catalog_name=image_catalog_name,
                device_name=device_name,
                image_catalog_directory_name=image_catalog_directory,
                image_catalog_entries=image_catalog_entries,
                success_list=success_list,
                fail_list=fail_list
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
                image_catalog_name=image_catalog_name,
                device_name=device_name,
                image_catalog_directory_name=image_catalog_directory,
            )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
