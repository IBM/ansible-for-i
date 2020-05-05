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
module: ibmi_display_subsystem
short_description: display all currently active subsystems or currently active jobs in a subsystem
description:
    - the C(ibmi_display_subsystem) module all currently active subsystems or currently active jobs in a subsystem of the target ibmi node.
    - In some ways it has equivalent results of WRKSBS if subsystem is '*ALL', otherwise, it has equivalent results of WRKSBSJOB
version_added: "1.1"
options:
  subsystem:
    description:
      - Specifies the name of the subsystem
    type: str
    default: '*ALL'
  user:
    description:
      - Specifies the name of the user whose jobs are displayed('*ALL' for all user names). If subsystem is '*ALL', this option is ignored
    type: str
    default: '*ALL'
seealso:
- module: ibmi_end_subsystem, ibmi_start_subsystem
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Display all the active subsystems in this system
  ibmi_display_subsystem:

- name: Display all the active jobs of subsystem QINTER
  ibmi_display_subsystem:
    subsystem: QINTER

- name: Display With One User's Job of subsystem QBATCH
  ibmi_display_subsystem:
    subsystem: QBATCH
    user: 'JONES'
'''

RETURN = r'''
stdout:
    description: The standard output of the display subsystem job results set
    type: str
    sample: ''
    returned: When rc as non-zero(failure)
stderr:
    description: The standard error the the display subsystem job
    type: str
    sample: ''
    returned: When rc as non-zero(failure)
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines
    type: list
    sample: ['']
    returned: When rc as non-zero(failure)
stderr_lines:
    description: The standard error split in lines
    type: list
    sample: ['']
    returned: When rc as non-zero(failure)
subsystems:
    description: The result set
    returned: When rc as 0(success) and subsystem is '*ALL'
    type: list
    sample: [
        "QCMN",
        "QCTL",
        "QHTTPSVR",
        "QINTER",
        "QSERVER",
        "QSPL",
        "QSYSWRK",
        "QUSRWRK"
    ]
active_jobs:
    description: The result set
    returned: When rc as 0(success) and subsystem is not '*ALL'
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

import datetime

from ansible.module_utils.basic import AnsibleModule

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit.transport import DatabaseTransport
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
IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT = 258
IBMi_COMMAND_RC_INVALID_EXPECTED_ROW_COUNT = 259


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
    else:
        return "Unknown error"


def itoolkit_run_sql(sql):
    conn = dbi.connect()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()

    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFetch('fetch'))
    itool.add(iSqlFree('free'))

    itool.call(itransport)

    command_output = itool.dict_out('fetch')

    out_list = []
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
            if 'Row not found' in err:
                rc = 0  # treat as success but also indicate the Row not found message in stderr
    else:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['row']
        if isinstance(out, dict):
            out_list.append(out)
        elif isinstance(out, list):
            out_list = out

    return rc, out_list, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            subsystem=dict(type='str', default='*ALL'),
            user=dict(type='str', default='*ALL'),
        ),
        supports_check_mode=True,
    )
    if HAS_ITOOLKIT is False:
        module.fail_json(rc=999, msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(rc=999, msg="ibm_db package is required")
    subsystem = module.params['subsystem'].upper()
    user = module.params['user'].upper()
    if len(subsystem) > 10:
        module.fail_json(rc=256, msg="Value of subsystem exceeds 10 characters")
    if len(user) > 10:
        module.fail_json(rc=256, msg="Value of user exceeds 10 characters")
    if subsystem == '*JOBQ' or subsystem == '*OUTQ':
        module.fail_json(rc=256, msg="Value of option subsystem can not be {subsystem_pattern}".format(subsystem_pattern=subsystem))

    if subsystem == '*ALL':
        sql = "SELECT J.SUBSYSTEM FROM TABLE (QSYS2.ACTIVE_JOB_INFO()) J WHERE JOB_TYPE = 'SBS'"
        rc, out, err = itoolkit_run_sql(sql)
        rc_msg = interpret_return_code(rc)

        if rc != IBMi_COMMAND_RC_SUCCESS:
            result_failed = dict(
                stdout=out,
                stderr=err,
                rc=rc,
            )
            message = 'non-zero return code:{rc},{rc_msg}'.format(
                rc=rc, rc_msg=rc_msg)
            module.fail_json(msg=message, **result_failed)
        else:
            formatted_out = []
            for item in out:
                formatted_out.append(item['SUBSYSTEM'])
            result_success = dict(
                subsystems=formatted_out,
                rc=rc,
            )
            module.exit_json(**result_success)
    else:
        sql = "SELECT J.SUBSYSTEM FROM TABLE (QSYS2.ACTIVE_JOB_INFO()) J WHERE JOB_TYPE = 'SBS'"
        rc, out, err = itoolkit_run_sql(sql)
        rc_msg = interpret_return_code(rc)

        if rc != IBMi_COMMAND_RC_SUCCESS:
            result_failed = dict(
                stdout=out,
                stderr=err,
                rc=rc,
            )
            message = 'Failed to retrieve subsystem {subsystem_pattern} status, non-zero return code:{rc},{rc_msg}'.format(
                subsystem_pattern=subsystem, rc=rc, rc_msg=rc_msg)
            module.fail_json(msg=message, **result_failed)
        else:
            is_active = False
            for items in out:
                if subsystem == items['SUBSYSTEM']:
                    is_active = True
            if not is_active:
                module.fail_json(rc=256, msg="Subsystem {subsystem_pattern} is not active".format(subsystem_pattern=subsystem))

            if user == '*ALL':
                sql = "SELECT J.* FROM TABLE (QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => '{subsystem_pattern}')) J \
                  WHERE JOB_TYPE NOT IN ('SBS', 'SYS')".format(subsystem_pattern=subsystem)
            else:
                sql = "SELECT J.* FROM TABLE (QSYS2.ACTIVE_JOB_INFO(\
                    SUBSYSTEM_LIST_FILTER => '{subsystem_pattern}', \
                    CURRENT_USER_LIST_FILTER => '{user_pattern}')) J WHERE JOB_TYPE NOT IN ('SBS', 'SYS')".format(
                    subsystem_pattern=subsystem, user_pattern=user)
            rc, out, err = itoolkit_run_sql(sql)
            rc_msg = interpret_return_code(rc)
            if rc != IBMi_COMMAND_RC_SUCCESS:
                result_failed = dict(
                    stdout=out,
                    stderr=err,
                    rc=rc,
                )
                message = 'non-zero return code:{rc},{rc_msg}'.format(
                    rc=rc, rc_msg=rc_msg)
                module.fail_json(msg=message, **result_failed)
            else:
                result_success = dict(
                    active_jobs=out,
                    rc=rc,
                )
                module.exit_json(**result_success)


if __name__ == '__main__':
    main()
