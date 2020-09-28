#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Yi Fan Jin <jinyifan@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_query_job_log
short_description: Query the specfic job log.
version_added: '2.8.0'
description:
  - Query the specfic job log.
options:
  job_number:
    description:
      - Job number
    type: str
    required: yes
  job_user:
    description:
      - job user
    type: str
    required: yes
  job_name:
    description:
      - job name
    type: str
    required: yes
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str
author:
- Jin Yi Fan(@jinyifan)
'''

EXAMPLES = r'''
- name: Query the specfic job log
  ibmi_query_job_log:
    job_number: "025366"
    job_user: "QUSER"
    job_name: "QZDASOINIT"
'''

RETURN = r'''
job_log:
    description: The IBM i job log of the task executed.
    returned: always
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
sql:
    description: the sql executed
    returned: always
    type: str
    sample: "SELECT ORDINAL_POSITION, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, SEVERITY,
             MESSAGE_TIMESTAMP, FROM_LIBRARY, FROM_PROGRAM, FROM_MODULE, FROM_PROCEDURE, FROM_INSTRUCTION,
             TO_LIBRARY, TO_PROGRAM, TO_MODULE, TO_PROCEDURE, TO_INSTRUCTION, FROM_USER, MESSAGE_FILE,
             MESSAGE_LIBRARY, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT FROM TABLE(QSYS2.JOBLOG_INFO('025366/QUSER/QZDASOINIT'))"
start:
    description: The command execution start time
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The command execution end time
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The command execution delta time
    returned: always
    type: str
    sample: '0:00:00.307534'
stderr:
    description: The command standard error
    returned: always
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
rc:
    description: The command return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
stderr_lines:
    description: The command standard error split in lines
    returned: always
    type: list
    sample: []
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            job_number=dict(type='str', required=True),
            job_name=dict(type='str', required=True),
            job_user=dict(type='str', required=True),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    job_number = module.params['job_number']
    job_name = module.params['job_name']
    job_user = module.params['job_user']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    sql = "SELECT ORDINAL_POSITION, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, SEVERITY, \
        MESSAGE_TIMESTAMP, FROM_LIBRARY, FROM_PROGRAM, FROM_MODULE, FROM_PROCEDURE, FROM_INSTRUCTION, \
        TO_LIBRARY, TO_PROGRAM, TO_MODULE, TO_PROCEDURE, TO_INSTRUCTION, FROM_USER, MESSAGE_FILE, \
        MESSAGE_LIBRARY, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT \
        FROM TABLE(QSYS2.JOBLOG_INFO('{p_job_number}/{p_job_user}/{p_job_name}')) A".format(
        p_job_number=job_number,
        p_job_user=job_user,
        p_job_name=job_name)

    startd = datetime.datetime.now()
    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)
    job_log = []
    rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)

    endd = datetime.datetime.now()
    delta = endd - startd
    if rc:
        result_failed = dict(
            sql=sql,
            job_log=job_log,
            stderr=err,
            stdout=out,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
        )
        message = 'non-zero return code {rc}'.format(rc=rc)
        module.fail_json(msg=message, **result_failed)

    result = dict(
        sql=sql,
        job_log=out,
        stderr=err,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
    )

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
