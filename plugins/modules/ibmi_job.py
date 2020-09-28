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
module: ibmi_job
short_description: Returns job information according to inputs.
version_added: '2.8.0'
description:
     - The C(ibmi_job) module returns information associated with one or more jobs.
options:
  name:
    description:
      - The qualified job name.
      - If this parameter is specified, the other parameters will be ignored.
    type: str
    required: false
  status:
    description:
      - The job status filter.
    type: str
    default: "*ALL"
    choices: ["*ALL", "*ACTIVE", "*JOBQ", "*OUTQ"]
  type:
    description:
      - The job type filter.
    type: str
    default: "*ALL"
    choices: ["*ALL", "*BATCH", "*INTERACT"]
  subsystem:
    description:
      - The job subsystem filter. A valid subsystem name can be specified. Valid values are C(*ALL) or subsystem name.
    type: str
    default: "*ALL"
  user:
    description:
      - The user profile name to use as the job user filtering criteria.
      - Valid values are user profile name, C(*USER) or C(*ALL).
    type: str
    default: "*ALL"
  submitter:
    description:
      - The type of submitted jobs to return.
    type: str
    default: "*ALL"
    choices: ["*ALL", "*JOB", "*USER", "*WRKSTN"]
  joblog:
    description:
      - The job log of the job executing the task will be returned even rc is zero if it is set to true.
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
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
seealso:
- module: ibmi_submit_job

author:
    - Wang Yun (@airwangyun)
'''

EXAMPLES = r'''
- name: Get status of a list of jobs
  ibmi_job:
    user: "WANGYUN"
    type: "*BATCH"

- name: List job information
  ibmi_job:
    name: "556235/WANGYUN/TEST"
'''

RETURN = r'''
start:
    description: The task execution start time
    type: str
    sample: '2019-12-02 11:07:53.757435'
    returned: When job has been submitted and task has waited for the job status for some time
end:
    description: The task execution end time
    type: str
    sample: '2019-12-02 11:07:54.064969'
    returned: When job has been submitted and task has waited for the job status for some time
delta:
    description: The task execution delta time
    type: str
    sample: '0:00:00.307534'
    returned: When job has been submitted and task has waited for the job status for some time
stdout:
    description: The task standard output
    type: str
    sample: 'CPC2102: Library TESTLIB created'
    returned: When rc as non-zero(failure)
stderr:
    description: The task standard error
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
    returned: When rc as non-zero(failure)
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The task standard output split in lines
    type: list
    sample: [
        "CPC2102: Library TESTLIB created."
    ]
    returned: When rc as non-zero(failure)
stderr_lines:
    description: The task standard error split in lines
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
    returned: When rc as non-zero(failure)
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
job_info:
    description: The information of the job(s)
    type: list
    returned: When rc is zero
    sample: [
        {
            "CCSID": "0",
            "COMPLETION_STATUS": "ABNORMAL",
            "JOB_ACCOUNTING_CODE": "*SYS",
            "JOB_ACTIVE_TIME": "",
            "JOB_DATE": "",
            "JOB_DESCRIPTION": "",
            "JOB_DESCRIPTION_LIBRARY": "",
            "JOB_END_REASON": "",
            "JOB_END_SEVERITY": "10",
            "JOB_END_TIME": "2020-02-14-00.36.35",
            "JOB_ENTERED_SYSTEM_TIME": "2020-02-14-00.36.35",
            "JOB_INFORMATION": "YES",
            "JOB_NAME": "514647/WANGYUN/QPRTJOB",
            "JOB_QUEUE_LIBRARY": "",
            "JOB_QUEUE_NAME": "",
            "JOB_QUEUE_PRIORITY": "0",
            "JOB_QUEUE_STATUS": "",
            "JOB_SCHEDULED_TIME": "",
            "JOB_STATUS": "OUTQ",
            "JOB_SUBSYSTEM": "",
            "JOB_TYPE": "BCH",
            "JOB_TYPE_ENHANCED": "ALTERNATE_SPOOL_USER",
            "SUBMITTER_JOB_NAME": "",
            "SUBMITTER_MESSAGE_QUEUE": "",
            "SUBMITTER_MESSAGE_QUEUE_LIBRARY": ""
        },
        {
            "CCSID": "65535",
            "COMPLETION_STATUS": "ABNORMAL",
            "JOB_ACCOUNTING_CODE": "*SYS",
            "JOB_ACTIVE_TIME": "2020-03-23-22.07.18",
            "JOB_DATE": "",
            "JOB_DESCRIPTION": "QDFTJOBD",
            "JOB_DESCRIPTION_LIBRARY": "QGPL",
            "JOB_END_REASON": "JOB ENDED DUE TO A DEVICE ERROR",
            "JOB_END_SEVERITY": "30",
            "JOB_END_TIME": "2020-03-24-11.06.44",
            "JOB_ENTERED_SYSTEM_TIME": "2020-03-23-22.07.18",
            "JOB_INFORMATION": "YES",
            "JOB_NAME": "547343/WANGYUN/QPADEV0001",
            "JOB_QUEUE_LIBRARY": "",
            "JOB_QUEUE_NAME": "",
            "JOB_QUEUE_PRIORITY": "0",
            "JOB_QUEUE_STATUS": "",
            "JOB_SCHEDULED_TIME": "",
            "JOB_STATUS": "OUTQ",
            "JOB_SUBSYSTEM": "",
            "JOB_TYPE": "INT",
            "JOB_TYPE_ENHANCED": "INTERACTIVE_GROUP",
            "SUBMITTER_JOB_NAME": "",
            "SUBMITTER_MESSAGE_QUEUE": "",
            "SUBMITTER_MESSAGE_QUEUE_LIBRARY": ""
        }
    ]
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_JOB_STATUS_NOT_EXPECTED = 258
IBMi_PARAM_NOT_VALID = 259
IBMi_JOB_STATUS_LIST = ["*NONE", "*ACTIVE", "*COMPLETE", "*JOBQ", "*OUTQ"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=False),
            status=dict(type='str', default='*ALL', choices=["*ALL", "*ACTIVE", "*JOBQ", "*OUTQ"]),
            type=dict(type='str', default="*ALL", choices=["*ALL", "*BATCH", "*INTERACT"]),
            subsystem=dict(type='str', default='*ALL'),
            user=dict(type='str', default='*ALL'),
            submitter=dict(type='str', default='*ALL', choices=["*ALL", "*JOB", "*USER", "*WRKSTN"]),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    job_name = module.params['name']
    job_status = module.params['status']
    job_type = module.params['type']
    job_subsystem = module.params['subsystem']
    job_user = module.params['user']
    job_submitter = module.params['submitter']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()

    ibmi_module = imodule.IBMiModule(become_user_name=become_user,
                                     become_user_password=become_user_password)

    # connection_id = ibmi_module.get_connection()

    sql_job_columns = "SELECT JOB_NAME, JOB_INFORMATION, JOB_STATUS, JOB_TYPE, JOB_TYPE_ENHANCED, JOB_SUBSYSTEM, " \
                      " JOB_DATE, JOB_DESCRIPTION_LIBRARY, JOB_DESCRIPTION, JOB_ACCOUNTING_CODE, SUBMITTER_JOB_NAME, " \
                      " SUBMITTER_MESSAGE_QUEUE_LIBRARY, SUBMITTER_MESSAGE_QUEUE, JOB_ENTERED_SYSTEM_TIME, " \
                      " JOB_SCHEDULED_TIME, JOB_ACTIVE_TIME, JOB_END_TIME, JOB_END_SEVERITY, COMPLETION_STATUS, " \
                      " JOB_END_REASON, JOB_QUEUE_LIBRARY, JOB_QUEUE_NAME, JOB_QUEUE_STATUS, JOB_QUEUE_PRIORITY, " \
                      " CCSID "

    if (job_name is None) or (job_name == ""):
        sql_where = ""
    else:
        sql_where = " AND UPPER(JOB_NAME) = '" + job_name.upper() + "'"
        job_status = "*ALL"
        job_type = "*ALL"
        job_subsystem = "*ALL"
        job_user = "*ALL"
        job_submitter = "*ALL"

    sql_job_status_filter = " JOB_STATUS_FILTER => '" + job_status + "', "
    sql_job_type_filter = " JOB_TYPE_FILTER => '" + job_type + "', "
    sql_job_subsystem_filter = " JOB_SUBSYSTEM_FILTER => '" + job_subsystem.upper() + "', "
    sql_job_user_filter = " JOB_USER_FILTER => '" + job_user.upper() + "', "
    sql_job_submitter_filter = " JOB_SUBMITTER_FILTER => '" + job_submitter + "' "

    sql_from = " FROM TABLE(QSYS2.JOB_INFO(" + sql_job_status_filter + sql_job_type_filter + \
               sql_job_subsystem_filter + \
               sql_job_user_filter + sql_job_submitter_filter + ")) X WHERE 1 = 1 "

    sql_to_run = sql_job_columns + sql_from + sql_where

    rc, out, err_msg, job_log = ibmi_module.itoolkit_run_sql_once(sql_to_run)
    rt_job_log = []
    if joblog or (rc != IBMi_COMMAND_RC_SUCCESS):
        rt_job_log = job_log

    endd = datetime.datetime.now()
    delta = endd - startd

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            stderr=err_msg,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            job_log=rt_job_log,
        )
        module.fail_json(msg='Non-zero return code.', **result_failed)
    else:
        result_success = dict(
            job_info=out,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            job_log=rt_job_log,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
