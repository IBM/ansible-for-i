#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) International Business Machines Corp. 2019
# All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_submit_job
short_description: Submit a job on IBM i system. This module functions like SBMJOB.
version_added: 1.0
description:
     - The C(ibmi_submit_job) module submits a job on IBM i system.
     - It waits until the submitted job turns into expected status that is specified.
options:
  cmd:
    description:
      - A command that runs in the batch job.
    type: str
    required: true
  time_out:
    description:
      - The max time that the module waits for the submitted job is turned into expected status.
        It returns if the status of the submitted job is not turned into the expected status within the time_out time.
        This option will be ignored if *NONE is specified for option status.
    type: str
    default: "1m"
    required: false
  status:
    description:
      - The expect status list. The module will wait for the job to be turned into one of the expected status specified.
        If one of the expect status specified matches the status of submitted job, it will return.
        If *NONE is specified, the module will not wait for anything and return right after the job is submitted.
        The valid options are "*NONE", "*ACTIVE", "*COMPLETE", "*JOBQ", "*OUTQ".
    type: list
    elements: str
    default: ["*NONE"]
  check_interval:
    description:
      - The time interval between current and next checks of the expected status of the submitted job.
        This option will be ignored if *NONE is specified for option status.
    type: str
    default: "1m"
    required: false
  parameters:
    description:
      - The parameters that SBMJOB will take. Other than CMD, all other parameters need to be specified here.
        The default values of parameters for SBMJOB will be taken if not specified.
    type: str
    required: false
    default: ""

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
sbmjob_cmd:
    description: The SBMJOB CL command that has been used.
    type: str
    sample: 'SBMJOB CMD(CRTLIB LIB(TESTLIB))'
    returned: always
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
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
import re
import time
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


# def retrieve_job_attribute(job_number, job_user, job_name):
#     conn = dbi.connect()
#     itool = iToolKit()
#     itool.add(iCmd('rtvjoba', 'RTVJOBA JOB(' + job_name + ') USER(' + job_user + ') NBR(' + job_number + ') '
#                    'USRLIBL(?) SYSLIBL(?) CCSID(?N) OUTQ(?)'))
#     # itransport = DatabaseTransport(conn)
#     itransport = DirectTransport()
#     itool.call(itransport)
#
#     # output
#     rtvjoba = itool.dict_out('rtvjoba')
#     print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
#     print(rtvjoba)
#     if 'error' in rtvjoba:
#         print(rtvjoba['error'])
#         exit()
#     elif 'row' in rtvjoba:
#         rtvjoba_vals = rtvjoba['row']
#
#         for item_dict in rtvjoba_vals:
#             for key in item_dict:
#                 print(item_dict[key])
#
#         print('hahahahahahhahahahahhaah')
#
#         # print('value:' + rtvjoba)
#         # print('USRLIBL = ' + rtvjoba_vals['USRLIBL'])
#         # print('SYSLIBL = ' + rtvjoba_vals['SYSLIBL'])
#         # print('CCSID   = ' + rtvjoba_vals['CCSID'])
#         # print('OUTQ    = ' + rtvjoba_vals['OUTQ'])
#     else:
#         print('ERRORRRRRRRRRRRRRRRRRRR')
#     print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(type='str', required=True),
            time_out=dict(type='str', default='1m'),
            status=dict(type='list', default=["*NONE"], elements='str'),
            check_interval=dict(type='str', default='1m'),
            parameters=dict(type='str', default=''),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    command = module.params['cmd']
    time_out = module.params['time_out']
    check_interval = module.params['check_interval']
    wait_for_job_status = module.params['status']
    parameters = module.params['parameters']

    cl_sbmjob = "SBMJOB CMD(" + command + ") " + parameters

    if set(wait_for_job_status) < set(IBMi_JOB_STATUS_LIST):
        # this is expected
        pass
    else:
        rc = IBMi_PARAM_NOT_VALID
        result_failed_parameter_check = dict(
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            stderr="Parameter passed is not valid. ",
            rc=rc,
            sbmjob_cmd=cl_sbmjob,
            # changed=True,
        )
        module.fail_json(msg='Value specified for status option is not valid. Valid values are '
                             '*NONE, *ACTIVE, *COMPLETE, *JOBQ, *OUTQ', **result_failed_parameter_check)

    startd = datetime.datetime.now()

    args = ['system', cl_sbmjob]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            stderr=err,
            rc=rc,
            sbmjob_cmd=cl_sbmjob,
            # changed=True,
        )
        module.fail_json(msg='Submit job failed. ', **result_failed)
    elif '*NONE' in wait_for_job_status:
        submitted_job = re.search(r'\d{6}/[A-Za-z0-9#_]{1,10}/[A-Za-z0-9#_]{1,10}', out)
        job_submitted = submitted_job.group()

        result_success = dict(
            rc=rc,
            job_submitted=job_submitted,
            sbmjob_cmd=cl_sbmjob,
            # changed=True,
        )
        module.exit_json(**result_success)

    submitted_job = re.search(r'\d{6}/[A-Za-z0-9#_]{1,10}/[A-Za-z0-9#_]{1,10}', out)
    job_submitted = submitted_job.group()

    sql_get_job_info = "SELECT V_JOB_STATUS as \"job_status\", " \
                       "V_ACTIVE_JOB_STATUS as \"active_job_status\", " \
                       "V_ACTIVE_JOB_TYPE as \"active_job_type\", " \
                       "V_RUN_PRIORITY as \"run_priority\", " \
                       "V_SBS_NAME as \"sbs_name\", " \
                       "V_CLIENT_IP_ADDRESS as \"ip_address\"" \
                       " FROM TABLE(QSYS2.GET_JOB_INFO('" + job_submitted + "')) A"
    rc, out, err_msg = itoolkit_run_sql(sql_get_job_info)

    time_out_in_seconds = convert_wait_time_to_seconds(time_out)

    while out['job_status'] not in wait_for_job_status:
        rc, out, err_msg = itoolkit_run_sql(sql_get_job_info)
        wait_for_certain_time(check_interval)
        current_time = datetime.datetime.now()
        running_time = (current_time - startd).seconds
        if running_time > time_out_in_seconds:
            break

    if out['job_status'] not in wait_for_job_status:
        rc = IBMi_JOB_STATUS_NOT_EXPECTED

    endd = datetime.datetime.now()
    delta = endd - startd

    rc_msg = interpret_return_code(rc)

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            job_info=out,
            stderr=err,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            job_submitted=job_submitted,
            sbmjob_cmd=cl_sbmjob,
            # changed=True,
        )
        module.fail_json(msg='non-zero return code: ' + rc_msg, **result_failed)
    else:
        result_success = dict(
            job_info=out,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            job_submitted=job_submitted,
            sbmjob_cmd=cl_sbmjob,
            # changed=True,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
