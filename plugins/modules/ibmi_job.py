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
version_added: 1.0
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
      - The job subsystem filter. A valid subsystem name can be specified. Valid values are "*ALL" or subsystem name.
    type: str
    default: "*ALL"
  user:
    description:
      - The user profile name to use as the job user filtering criteria.
      - Valid values are user profile name, "*USER" or "*ALL".
    type: str
    default: "*USER"
  submitter:
    description:
      - The type of submitted jobs to return.
    type: str
    default: "*ALL"
    choices: ["*ALL", "*JOB", "*USER", "*WRKSTN"]

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

try:
    from itoolkit import iToolKit
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
IBMi_PARAM_NOT_VALID = 259
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=False),
            status=dict(type='str', default='*ALL', choices=["*ALL", "*ACTIVE", "*JOBQ", "*OUTQ"]),
            type=dict(type='str', default="*ALL", choices=["*ALL", "*BATCH", "*INTERACT"]),
            subsystem=dict(type='str', default='*ALL'),
            user=dict(type='str', default='*USER'),
            submitter=dict(type='str', default='*ALL', choices=["*ALL", "*JOB", "*USER", "*WRKSTN"]),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    job_name = module.params['name']
    job_status = module.params['status']
    job_type = module.params['type']
    job_subsystem = module.params['subsystem']
    job_user = module.params['user']
    job_submitter = module.params['submitter']

    startd = datetime.datetime.now()

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

    rc, out, err_msg = itoolkit_run_sql(sql_to_run)

    endd = datetime.datetime.now()
    delta = endd - startd

    rc_msg = interpret_return_code(rc)

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            stderr=err_msg,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
        )
        module.fail_json(msg='non-zero return code: ' + rc_msg, **result_failed)
    else:
        result_success = dict(
            job_info=out,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
