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
module: ibmi_sql_execute
short_description: Executes a SQL non-DQL(Data Query Language) statement
version_added: '2.8.0'
description:
     - The C(ibmi_sql_execute) module takes the SQL non-DQL(Data Query Language) statement as argument.
options:
  sql:
    description:
      - The C(ibmi_sql_execute) module takes a IBM i SQL non-DQL(Data Query Language) statement to run.
    type: str
    required: yes
  database:
    description:
      - Specified database name, usually, its the iasp name, use WRKRDBDIRE to check Relational Database Directory Entries
      - Default to use the C(*LOCAL) entry
    type: str
    default: '*SYSBAS'
  joblog:
    description:
      - If set to C(true), output the JOBLOG even success.
    type: bool
    default: False
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
    - This module can only run one SQL statement at a time.
seealso:
- module: IBMi_sql_query

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Insert one record to table Persons
  ibmi_sql_execute:
    sql: "INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
start:
    description: The sql statement execution start time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The sql statement execution end time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The sql statement execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The sql statement standard output.
    returned: always
    type: str
    sample: "+++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
stderr:
    description: The sql statement standard error.
    returned: always
    type: str
    sample: ''
sql:
    description: The sql statement executed by the task.
    returned: always
    type: str
    sample: "INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
rc:
    description: The sql statement return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 0
stdout_lines:
    description: The sql statement standard output split in lines.
    returned: When rc as non-zero(failure)
    type: list
    sample: ["+++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"]
stderr_lines:
    description: The sql statement standard error split in lines.
    returned: When rc as non-zero(failure)
    type: list
    sample: ['']
job_log:
    description: The IBM i job log of the task executed.
    returned: when rc as non-zero(failure) or rc as success(0) but joblog set to true.
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

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql=dict(type='str', required=True),
            database=dict(type='str', default='*SYSBAS'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    sql = module.params['sql'].strip().upper()
    database = module.params['database'].strip().upper()
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()
    try:
        ibmi_module = imodule.IBMiModule(
            db_name=database, become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(sql)

    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        sql=sql,
        stdout=out,
        stderr=err,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
        job_log=job_log,
    )

    if rc:
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
