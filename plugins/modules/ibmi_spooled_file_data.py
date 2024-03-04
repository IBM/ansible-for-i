#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Chang Le <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_spooled_file_data
short_description: Returns the content of a spooled file.
version_added: '1.2.0'
description:
  - The C(ibmi_spooled_file_data) returns the content of a spooled file.
options:
  job_name:
    description:
      - A character string containing a qualified job name.
    type: str
    required: yes
  spooled_file_name:
    description:
      - A character string containing the name of the spooled file.
        If this parameter is an incorrect value or the spooled file is not existed, nothing will return to spooled_data.
    type: str
    required: yes
  spooled_file_number:
    description:
      - A character string containing the number of the spooled file for current job.
        If this parameter is omitted, the spooled file with the highest number matching spooled-file-name is used.
    type: str
    default: '*LAST'
  spooled_data_filter:
    description:
      - If supplied, only return lines that match this shell-style (fnmatch) wildcard.
        If this parameter is omitted, all the spooled file content is returned.
    type: str
    default: '*'
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str

seealso:
- module: ibmi_submit_job

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: print the spooled file data
  ibm.power_ibmi.ibmi_spooled_file_data:
    job_name: '024800/CHANGLE/QDFTJOBD'
    spooled_file_name: 'QPSECUSR'
'''

RETURN = r'''
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
msg:
    description: Simple description of the error.
    returned: when rc as non-zero(failure)
    type: str
    sample: 255
spooled_data:
    description: The spooled file content split in lines.
    returned: when rc as 0(success)
    type: list
    sample: [
        "5770SS1 V7R4M0  190621                                 MIRRORS   11/25/20  10:08:37 CST ",
        " Report type  . . . . . . . . . :   *PWDLVL                                             ",
        " Select by  . . . . . . . . . . :   *SPCAUT                                             ",
        " Special authorities  . . . . . :   *ALL                                                ",
        "                Password      Password      Password                                    ",
        " User           for level     for level        for                                      ",
        " Profile         0 or 1        2 or 3       NetServer                                   ",
        " CHANGLE          *YES          *YES          *YES                                      ",
        " DHQB             *NO           *YES          *NO                                       ",
        " QANZAGENT        *NO           *NO           *NO                                       ",
        " QAUTPROF         *NO           *NO           *NO                                       ",
        " QBRMS            *NO           *NO           *NO                                       ",

    ]
job_log:
    description: The IBM i job log of the task executed.
    returned: when rc as non-zero(failure) and error happened for CL command CPYSPLF used in this module.
    type: list
    sample: [{
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
        }]
'''

import os
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import fnmatch

__ibmi_module_version__ = "2.0.1"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            job_name=dict(type='str', required=True),
            spooled_file_name=dict(type='str', required=True),
            spooled_file_number=dict(type='str', default='*LAST'),
            spooled_data_filter=dict(type='str', default='*'),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    job_name = module.params['job_name'].strip().upper()
    spooled_file_name = module.params['spooled_file_name'].upper()
    spooled_file_number = module.params['spooled_file_number']
    spooled_data_filter = module.params['spooled_data_filter']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    spooled_data = []

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = f'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    ifs_spooled_file_path = f"/TMP/ANSIBLE_{spooled_file_name}_{job_name.replace('/', '_')}.TXT"
    if os.path.exists(ifs_spooled_file_path):
        os.remove(ifs_spooled_file_path)
    command = f"QSYS/CPYSPLF FILE({spooled_file_name}) TOFILE(*TOSTMF) JOB({job_name}) \
      SPLNBR({spooled_file_number}) TOSTMF('{ifs_spooled_file_path}') STMFOPT(*REPLACE)"
    rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)
    if rc:
        message = f'non-zero return code {rc} when run command {command}, check if the job name and spooled file information are correct'
        result = dict(
            rc=rc,
            job_log=job_log,
        )
        module.fail_json(msg=message, **result)

    try:
        ccsid = 'IBM-037'  # default CCSID
        # get file CCSID
        command = f'attr {ifs_spooled_file_path} CCSID'
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_info(
            f"run command: {command}, rc={rc}, out={out}, err={err}", module._name)
        if not rc:
            # convert to format like IBM-037, IBM-1399, IBM-500 etc....
            ccsid = 'IBM-' + out.strip().rjust(3, '0')
        rc, out, err = module.run_command(command, use_unsafe_shell=False)

        # convert file content to utf-8
        command = f'iconv -f {ccsid} -t UTF-8 {ifs_spooled_file_path}'
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_info(
            f"run command: {command}, rc={rc}, out={out}, err={err}", module._name)
        if not rc:
            spooled_data = out.splitlines()
            if spooled_data_filter != '*':
                spooled_data_temp = []
                for line in spooled_data:
                    if (fnmatch.fnmatch(line, spooled_data_filter)) or (spooled_data_filter in line):
                        spooled_data_temp.append(line)
                spooled_data = spooled_data_temp
        else:
            message = f'Error occurred when run command:{command}, error:{str(err)}'
            module.fail_json(rc=rc, msg=message)
        os.remove(ifs_spooled_file_path)
    except Exception as inst:
        message = f'Exception occurred:{str(inst)}'
        module.fail_json(rc=999, msg=message)

    result = dict(
        rc=rc,
        spooled_data=spooled_data,
    )

    module.exit_json(**result)


if __name__ == '__main__':
    main()
