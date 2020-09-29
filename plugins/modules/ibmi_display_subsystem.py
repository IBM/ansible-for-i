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
module: ibmi_display_subsystem
short_description: Displays all currently active subsystems or currently active jobs in a subsystem
version_added: '2.8.0'
description:
    - The C(ibmi_display_subsystem) module displays all currently active subsystems or currently active jobs in a subsystem.
    - In some ways it has equivalent results of WRKSBS if subsystem is C(*ALL), otherwise, it has equivalent results of WRKSBSJOB.
options:
  subsystem:
    description:
      - Specifies the name of the subsystem.
    type: str
    default: '*ALL'
  user:
    description:
      - Specifies the name of the user whose jobs are displayed, C(*ALL) for all users.
        If subsystem is C(*ALL), this option is ignored.
    type: str
    default: '*ALL'
  joblog:
    description:
      - If set to C(true), output the avaiable job log even the rc is 0(success).
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
seealso:
- module: ibmi_end_subsystem, ibmi_start_subsystem
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Display all the active subsystems in this system.
  ibmi_display_subsystem:

- name: Display all the active jobs of subsystem QINTER.
  ibmi_display_subsystem:
    subsystem: QINTER

- name: Display With One User's Job of subsystem QBATCH.
  ibmi_display_subsystem:
    subsystem: QBATCH
    user: 'JONES'
'''

RETURN = r'''
stdout:
    description: The standard output of the display subsystem job results set.
    type: str
    sample: ''
    returned: When rc as non-zero(failure).
stderr:
    description: The standard error the the display subsystem job.
    type: str
    sample: ''
    returned: When rc as non-zero(failure).
rc:
    description: The task return code (0 means success, non-zero means failure).
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines.
    type: list
    sample: ['']
    returned: When rc as non-zero(failure)
stderr_lines:
    description: The standard error split in lines.
    type: list
    sample: ['']
    returned: When rc as non-zero(failure)
job_log:
    description: The IBM i job log of the task executed.
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
    returned: always
subsystems:
    description: The list of the currently active subsystems.
    returned: When rc as 0(success) and subsystem is C(*ALL).
    type: list
    sample: [
        "                                      Work with Subsystems                                       5/25/20 19:55:04        Page 0001",
        "                          Subsystem        Active                          Total         -----------Subsystem Pools-----------------",
        "      Subsystem             Number          Jobs        Status          Storage (M)       1   2   3   4   5   6   7   8   9  10",
        "      QBATCH                018647              0       ACTIVE                     .00    2",
        "      QCMN                  018651              7       ACTIVE                     .00    2",
        "      QCTL                  018621              1       ACTIVE                     .00    2",
        "      QHTTPSVR              018742              8       ACTIVE                     .00    2",
        "      QINTER                018642              0       ACTIVE                     .00    2   3",
        "      QSERVER               018631             16       ACTIVE                     .00    2",
        "      QSPL                  018652              0       ACTIVE                     .00    2   4",
        "      QSYSWRK               018622            111       ACTIVE                     .00    2",
        "      QUSRWRK               018633             27       ACTIVE                     .00    2",
        "                          * * * * *  E N D  O F  L I S T I N G  * * * * *"
    ]
active_jobs:
    description: The result set
    returned: When rc as 0(success) and subsystem is not C(*ALL).
    type: list
    sample: [
        {
            "AUTHORIZATION_NAME": "QPGMR",
            "CPU_TIME": "17",
            "ELAPSED_ASYNC_DISK_IO_COUNT": "0",
            "ELAPSED_CPU_PERCENTAGE": "0.0",
            "ELAPSED_CPU_TIME": "0",
            "ELAPSED_INTERACTION_COUNT": "0",
            "ELAPSED_PAGE_FAULT_COUNT": "0",
            "ELAPSED_SYNC_DISK_IO_COUNT": "0",
            "ELAPSED_TIME": "0.000",
            "ELAPSED_TOTAL_DISK_IO_COUNT": "0",
            "ELAPSED_TOTAL_RESPONSE_TIME": "0",
            "FUNCTION": "QEZSCNEP",
            "FUNCTION_TYPE": "PGM",
            "INTERNAL_JOB_ID": "002700010041F300A432B3A44FFD7001",
            "JOB_END_REASON": "",
            "JOB_NAME": "022042/QPGMR/QSYSSCD",
            "JOB_STATUS": "EVTW",
            "JOB_TYPE": "BCH",
            "MEMORY_POOL": "BASE",
            "ORDINAL_POSITION": "2",
            "RUN_PRIORITY": "10",
            "SERVER_TYPE": "",
            "SUBSYSTEM": "QCTL",
            "SUBSYSTEM_LIBRARY_NAME": "QSYS",
            "TEMPORARY_STORAGE": "6",
            "THREAD_COUNT": "1",
            "TOTAL_DISK_IO_COUNT": "587"
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            subsystem=dict(type='str', default='*ALL'),
            user=dict(type='str', default='*ALL'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    subsystem = module.params['subsystem'].strip().upper()
    user = module.params['user'].strip().upper()
    joblog = module.params['joblog']
    if len(subsystem) > 10:
        module.fail_json(rc=256, msg="Value of subsystem exceeds 10 characters")
    if len(user) > 10:
        module.fail_json(rc=256, msg="Value of user exceeds 10 characters")
    if subsystem == '*JOBQ' or subsystem == '*OUTQ':
        module.fail_json(rc=256, msg="Value of option subsystem can not be {subsystem_pattern}".format(subsystem_pattern=subsystem))
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    job_log = []
    if subsystem == '*ALL':
        command = 'QSYS/WRKSBS'
        rc, out, err, job_log = ibmi_module.itoolkit_run_command5250_once(command)

        if rc:
            result_failed = dict(
                stdout=out,
                stderr=err,
                job_log=job_log,
                rc=rc,
            )
            message = 'non-zero return code:{rc}'.format(
                rc=rc)
            module.fail_json(msg=message, **result_failed)
        else:
            result_success = dict(
                subsystems=out.splitlines(),
                job_log=job_log,
                rc=rc,
            )
            if not joblog:
                empty_list = []
                result_success.update({'job_log': empty_list})
            module.exit_json(**result_success)
    else:
        sql = "SELECT J.SUBSYSTEM FROM TABLE (QSYS2.ACTIVE_JOB_INFO()) J WHERE JOB_TYPE = 'SBS'"
        ibmi_util.log_info("Command to run: " + sql, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)

        if rc:
            result_failed = dict(
                stdout=out,
                stderr=err,
                job_log=job_log,
                rc=rc,
            )
            message = 'Failed to retrieve subsystem {subsystem_pattern} status, non-zero return code:{rc}'.format(
                subsystem_pattern=subsystem, rc=rc)
            module.fail_json(msg=message, **result_failed)
        else:
            is_active = False
            for items in out:
                if subsystem == items['SUBSYSTEM']:
                    is_active = True
            if not is_active:
                module.fail_json(rc=ibmi_util.IBMi_SUBSYSTEM_NOT_ACTIVE, msg="Subsystem {0} is not active".format(subsystem))

            if user == '*ALL':
                sql = "SELECT J.* FROM TABLE (QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => '{subsystem_pattern}')) J \
                  WHERE JOB_TYPE NOT IN ('SBS', 'SYS')".format(subsystem_pattern=subsystem)
            else:
                sql = "SELECT J.* FROM TABLE (QSYS2.ACTIVE_JOB_INFO(\
                    SUBSYSTEM_LIST_FILTER => '{subsystem_pattern}', \
                    CURRENT_USER_LIST_FILTER => '{user_pattern}')) J WHERE JOB_TYPE NOT IN ('SBS', 'SYS')".format(
                    subsystem_pattern=subsystem, user_pattern=user)
            ibmi_util.log_info("Command to run: " + sql, module._name)
            rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
            if rc:
                result_failed = dict(
                    stdout=out,
                    stderr=err,
                    job_log=job_log,
                    rc=rc,
                )
                message = 'non-zero return code:{rc}'.format(
                    rc=rc)
                module.fail_json(msg=message, **result_failed)
            else:
                result_success = dict(
                    active_jobs=out,
                    job_log=job_log,
                    rc=rc,
                )
                if not joblog:
                    empty_list = []
                    result_success.update({'job_log': empty_list})
                module.exit_json(**result_success)


if __name__ == '__main__':
    main()
