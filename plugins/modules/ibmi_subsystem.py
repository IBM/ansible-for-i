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
module: ibmi_subsystem
short_description: Manage a subsystem with various operations.
version_added: '3.3.0'
description:
    - The C(ibmi_subsystem) module allows managing a subsystem with operations for start, end, restart, and display.
    - The C(start) operation starts an inactive subsystem.
    - The C(end) operation ends an active subsystem.
    - The C(restart) operation restarts a subsystem.
    - The C(display) operation displays all currently active subsystems or currently active jobs in a subsystem.
      In some ways it has equivalent results of WRKSBS if subsystem is C(*ALL), otherwise, it has equivalent results of WRKSBSJOB.
    - Idempotency applies to relevant operations, e.g., a start operation on an already active subystem or an end operation on an inactive subsystem
      performs no action and returns success.
options:
  operation:
    description:
      - The subsystem management operations include
      - Start a subsystem.
      - End a subsystem.
      - Restart a subsystem.
      - Display a subsystem.
    choices: ['start', 'end', 'restart', 'display']
    type: str
    required: yes
  subsystem:
    description:
      - The name of the subsystem description.
      - May use '*ALL' for the display operation.
    type: str
    required: yes
  how_to_end:
    description:
      - Specifies whether jobs in the subsystem are ended in a controlled manner or immediately.
      - This option is only applicable to the end and restart operations.
    type: str
    default: '*CNTRLD'
    choices: ['*IMMED', '*CNTRLD']
  controlled_end_delay_time:
    description:
      - Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation.
        If this amount of time is exceeded and the end operation is not complete,
        any jobs still being processed in the subsystem are ended immediately.
        If the value is greater than 99999, C(*NOLIMIT) will be used in ENDSBS command DELAY parameter.
      - This option is only applicable to the end and restart operations.
    type: int
    default: 100000
  end_subsystem_option:
    description:
      - Specifies the options to take when ending the active subsystems.
      - This option is only applicable to the end and restart operations.
    type: list
    elements: str
    default: ['*DFT']
    choices: ['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL']
  parameters:
    description:
      - The parameters that ENDSBS command will take.
        Other than the options above, all other parameters need to be specified here.
        The default values of parameters for ENDSBS will be taken if not specified.
      - This option is only applicable to the end and restart operations.
    type: str
    default: ''
  library:
    description:
      - Specify the library where the subsystem description is located.
      - This option is only applicable to the start and restart operations.
    type: str
    default: '*LIBL'
  user:
    description:
      - Specifies the name of the user whose jobs are displayed, C(*ALL) for all users.
        If subsystem is C(*ALL), this option is ignored.
      - This option is only applicable to the display operation.
    type: str
    default: '*ALL'
  joblog:
    description:
      - If set to C(true), output the available job log even when the rc is 0 (success).
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
    - This end or restart operation is NOT ALLOWED to end ALL subsystems (*ALL); use the C(ibmi_cl_command) module for this instead.
    - This module is non-blocking for the start and end operations, so the subsystem may still be in transition after module completion, and
      the C(ibmi_display_subsystem) module should be used to check the subsystem status.
    - Note that the restart operation blocks to wait for the subsystem to end, while it is non-blocking for resuming/starting the subsystem.
      The controlled_end_delay_time parameter should be used with restart to limit the wait time for subsystem end.
    - Due to the non-atomic and asynchronous nature of various operations that change the subsystem state, an error may occur with this type of operation
      if the subsystem is currently in a transition state from active to inactive or vice-versa.
seealso:
- module: ibmi_cl_command
author:
- Rob Gjertsen (@gjertsen)
'''

EXAMPLES = r'''
- name: Start the subsystem QBATCH.
  ibm.power_ibmi.ibmi_subsystem:
    operation: start
    subsystem: QBATCH

- name: Start a user defined subsystem, which the subsystem description is MYSBS, located at library MYLIB.
  ibm.power_ibmi.ibmi_subsystem:
    operation: start
    subsystem: MYSBS
    library: MYLIB
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: End the subsystem QBATCH with another user.
  ibm.power_ibmi.ibmi_subsystem:
    operation: end
    subsystem: QBATCH
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: End the QBATCH subsystem with options.
  ibm.power_ibmi.ibmi_subsystem:
    operation: end
    subsystem: QBATCH
    how_to_end: '*IMMED'

- name: Restart the subsystem QBATCH.
  ibm.power_ibmi.ibmi_subsystem:
    operation: restart
    subsystem: QBATCH

- name: Display all the active subsystems in this system.
  ibm.power_ibmi.ibmi_subsystem:
    operation: display
    subsystem: '*ALL'

- name: Display all the active jobs of subsystem QINTER.
  ibm.power_ibmi.ibmi_subsystem:
    operation: display
    subsystem: QINTER

- name: Display With One User's Job of subsystem QBATCH.
  ibm.power_ibmi.ibmi_subsystem:
    operation: display
    subsystem: QBATCH
    user: 'JONES'
'''

RETURN = r'''
stdout:
    description: The standard output of the subsystem command.
    type: str
    sample: 'CPF0943: Ending of subsystem QBATCH in progress.'
    returned: always except for a display operation that has a zero rc (success).
stderr:
    description: The standard error the subsystem command.
    type: str
    sample: 'CPF1054: No subsystem MYJOB active.'
    returned: always except for a display operation that has a zero rc (success).
rc:
    description: The task return code (0 means success, non-zero means failure).
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines.
    type: list
    sample: [
        "CPF0943: Ending of subsystem QBATCH in progress."
    ]
    returned: always except for a display operation that has a zero rc (success).
stderr_lines:
    description: The standard error split in lines.
    type: list
    sample: [
        "CPF1054: No subsystem MYJOB active."
    ]
    returned: always except for a display operation that has a zero rc (success).
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
    returned: Only for a display operation when the rc is zero (success) and all subsystems, C(*ALL), are specified.
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
    returned: Only for a display operation when the rc is zero (success) and subsystem is not C(*ALL).
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
import time

__ibmi_module_version__ = "3.3.0"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', choices=['start', 'end', 'restart', 'display'], required=True),
            subsystem=dict(type='str', required=True),
            library=dict(type='str', default='*LIBL'),
            how_to_end=dict(type='str', default='*CNTRLD', choices=['*IMMED', '*CNTRLD']),
            controlled_end_delay_time=dict(type='int', default=100000),
            end_subsystem_option=dict(type='list', default=['*DFT'], choices=['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL'], elements='str'),
            parameters=dict(type='str', default=''),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
            user=dict(type='str', default='*ALL'),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    operation = module.params['operation'].strip()
    subsystem = module.params['subsystem'].strip().upper()
    library = module.params['library'].strip().upper()
    how_to_end = module.params['how_to_end']
    controlled_end_delay_time_seconds = module.params['controlled_end_delay_time']
    end_subsystem_option_list = module.params['end_subsystem_option']
    parameters = module.params['parameters'].upper()
    joblog = module.params['joblog']
    user = module.params['user'].strip().upper()

    if len(subsystem) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of subsystem exceeds 10 characters")

    if operation == 'start' or operation == 'restart':
        if len(library) > 10:
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of library exceeds 10 characters")
    if operation == 'end' or operation == 'restart':
        if controlled_end_delay_time_seconds > 99999:
            controlled_end_delay_time = '*NOLIMIT'
        else:
            controlled_end_delay_time = controlled_end_delay_time_seconds
        if subsystem == '*ALL' or subsystem == '*all':
            module.fail_json(rc=ibmi_util.IBMi_END_ALL_SUBSYSTEM_NOT_ALLOWED, msg="End all subsystems is NOT allowed")
        end_subsystem_option = ''
        for item in end_subsystem_option_list:
            end_subsystem_option = end_subsystem_option + item + ' '
    if operation == 'display':
        if len(user) > 10:
            module.fail_json(rc=256, msg="Value of user exceeds 10 characters")
        if subsystem == '*JOBQ' or subsystem == '*OUTQ':
            module.fail_json(rc=256, msg=f"Value of option subsystem can not be {subsystem}")

    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    # Idempotent case: we will note when the operation was already performed and return success in that situation
    operation_done = False

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    if operation == 'start':
        command = f'QSYS/STRSBS SBSD({library}/{subsystem})'
        # Query depends on whether providing specific library versus library list or current library
        if library == '*LIBL' or library == '*CURLIB':
            sql = f"SELECT * FROM QSYS2.SUBSYSTEM_INFO WHERE SUBSYSTEM_DESCRIPTION = '{subsystem}'"
        else:
            sql = f"SELECT * FROM QSYS2.SUBSYSTEM_INFO WHERE SUBSYSTEM_DESCRIPTION = '{subsystem}' AND SUBSYSTEM_DESCRIPTION_LIBRARY = '{library}'"
        ibmi_util.log_info("Command to run: " + sql, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
        if rc != 0:
            message = f'Non-zero return code for SQL query on subsystem state: {rc}'
            module.fail_json(rc=ibmi_util.IBMi_SQL_RC_ERROR, msg=message)
        # Note number of entries for inactive case
        row_count = -1
        if isinstance(out, list):
            row_count = len(out)

        is_active = False
        is_ending = False
        is_starting = False
        is_restricted = False
        is_inactive = False
        # There may be multiple entries with one being inactive, so verify state for all
        for items in out:
            if items['STATUS'] == 'ACTIVE':
                is_active = True
            if items['STATUS'] == 'ENDING':
                is_ending = True
            if items['STATUS'] == 'STARTING':
                is_starting = True
            if items['STATUS'] == 'RESTRICTED':
                is_restricted = True
        if not (is_active or is_ending or is_starting or is_restricted) and row_count > 0:
            is_inactive = True
        # Idempotent case: when active or already starting up, then nothing to do and success.
        if (is_active or is_starting):
            operation_done = True
            result = dict(
                command=command,
                stdout='',
                stderr='',
                rc=0,
                job_log=[],
                changed=False,
            )
        # else perform operation below
        # raise Exception(f'subsystem: "{subsystem} sql: "{sql}" rc: "{rc}" out:"{out}"')

    elif operation == 'end':
        command = f'QSYS/ENDSBS SBS({subsystem}) OPTION({how_to_end}) DELAY({controlled_end_delay_time}) ENDSBSOPT({end_subsystem_option}) {parameters}'
        command = ' '.join(command.split())  # keep only one space between adjacent strings
        sql = f"SELECT * FROM QSYS2.SUBSYSTEM_INFO WHERE SUBSYSTEM_DESCRIPTION = '{subsystem}'"
        ibmi_util.log_info("Command to run: " + sql, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
        if rc != 0:
            message = f'Non-zero return code for SQL query on subsystem state: {rc}'
            module.fail_json(rc=ibmi_util.IBMi_SQL_RC_ERROR, msg=message)
        # Note number of entries for inactive case
        row_count = -1
        if isinstance(out, list):
            row_count = len(out)

        is_active = False
        is_ending = False
        is_starting = False
        is_restricted = False
        is_inactive = False
        # There may be multiple entries with one being inactive, so verify state for all
        for items in out:
            if items['STATUS'] == 'ACTIVE':
                is_active = True
            if items['STATUS'] == 'ENDING':
                is_ending = True
            if items['STATUS'] == 'STARTING':
                is_starting = True
            if items['STATUS'] == 'RESTRICTED':
                is_restricted = True
        if not (is_active or is_ending or is_starting or is_restricted) and row_count > 0:
            is_inactive = True
        # Idempotent case: when inactive, then nothing to do and success.
        # Note: currently not treating the ending or restricted transition states as inactive because the command may have different parameters
        # than the in-progress operation, e.g., an immediate end versus controlled end. There is the accepted risk of an error in such a scenario.
        if (is_inactive):
            operation_done = True
            result = dict(
                command=command,
                stdout='',
                stderr='',
                rc=0,
                job_log=[],
                changed=False,
            )
        # else perform operation below

    elif operation == 'restart':
        # End the subsystem and then wait until inactive
        command = f'QSYS/ENDSBS SBS({subsystem}) OPTION({how_to_end}) DELAY({controlled_end_delay_time}) ENDSBSOPT({end_subsystem_option}) {parameters}'
        command = ' '.join(command.split())  # keep only one space between adjacent strings
        sql = f"SELECT * FROM QSYS2.SUBSYSTEM_INFO WHERE SUBSYSTEM_DESCRIPTION = '{subsystem}'"
        ibmi_util.log_info("Command to run: " + sql, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
        if rc != 0:
            message = f'Non-zero return code for SQL query on subsystem state: {rc}'
            module.fail_json(rc=ibmi_util.IBMi_SQL_RC_ERROR, msg=message)
        # Note number of entries for inactive case
        row_count = -1
        if isinstance(out, list):
            row_count = len(out)
        is_active = False
        is_ending = False
        is_starting = False
        is_restricted = False
        is_inactive = False
        # There may be multiple entries with one being inactive, so verify state for all
        for items in out:
            if items['STATUS'] == 'ACTIVE':
                is_active = True
            if items['STATUS'] == 'ENDING':
                is_ending = True
            if items['STATUS'] == 'STARTING':
                is_starting = True
            if items['STATUS'] == 'RESTRICTED':
                is_restricted = True
        if not (is_active or is_ending or is_starting or is_restricted) and row_count > 0:
            is_inactive = True
        # Idempotent case: when inactive, then nothing to do and success for end portion.
        # Note: currently not treating the ending or restricted transition states as inactive because the command may have different parameters
        # than the in-progress operation, e.g., an immediate end versus controlled end. There is the accepted risk of an error in such a scenario.
        if (not is_inactive):
            rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)
            if (rc != 0):
                result = dict(
                    command=command,
                    stdout=out,
                    stderr=err,
                    rc=rc,
                    job_log=job_log,
                    changed=True,
                )
                message = f'non-zero return code:{rc}'
                module.fail_json(msg=message, **result)
        # Wait for subsystem to be inactive if not already
        # TODO: Perhaps we should have a timeout option in addition to currently relying on controlled_end_delay_time to handle longer than expected end.
        time.sleep(1)
        seconds = 1
        while not is_inactive:
            sql = f"SELECT * FROM QSYS2.SUBSYSTEM_INFO WHERE SUBSYSTEM_DESCRIPTION = '{subsystem}'"
            ibmi_util.log_info("Command to run: " + sql, module._name)
            rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
            if rc != 0:
                message = f'Non-zero return code for SQL query on subsystem state: {rc}'
                module.fail_json(rc=ibmi_util.IBMi_SQL_RC_ERROR, msg=message)
            is_active = False
            is_ending = False
            is_starting = False
            is_restricted = False
            # There may be multiple entries with one being inactive, so verify state for all
            for items in out:
                if items['STATUS'] == 'ACTIVE':
                    is_active = True
                if items['STATUS'] == 'ENDING':
                    is_ending = True
                if items['STATUS'] == 'STARTING':
                    is_starting = True
                if items['STATUS'] == 'RESTRICTED':
                    is_restricted = True
            # TODO: May add timeout here in the future
            # if (seconds > restart_timeout):
            #   Failure actions
            if not (is_active or is_ending or is_starting or is_restricted):
                is_inactive = True
            elif is_starting:
                # This is a problem state if we requested the subsystem to end, so we have to abort the operation
                message = 'Unexpected subsystem starting state encountered after requesting subsystem to end, so aborting the operation'
                module.fail_json(rc=ibmi_util.IBMi_COMMAND_RC_ERROR, msg=message)
            else:
                time.sleep(1)
                seconds += 1
        # Start the inactive subsystem (perform command below)
        command = f'QSYS/STRSBS SBSD({library}/{subsystem})'

    elif operation == 'display':
        # Perform command/operation here for display due to different success return values than other operations
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
                message = f'non-zero return code:{rc}'
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
                message = f'Failed to retrieve subsystem {subsystem} status, non-zero return code:{rc}'
                module.fail_json(msg=message, **result_failed)
            else:
                is_active = False
                for items in out:
                    if subsystem == items['SUBSYSTEM']:
                        is_active = True
                if not is_active:
                    module.fail_json(rc=ibmi_util.IBMi_SUBSYSTEM_NOT_ACTIVE, msg=f"Subsystem {subsystem} is not active")

                if user == '*ALL':
                    sql = f"SELECT J.* FROM TABLE (QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => '{subsystem}')) J WHERE JOB_TYPE NOT IN ('SBS', 'SYS')"
                else:
                    sql = f"SELECT J.* FROM TABLE (QSYS2.ACTIVE_JOB_INFO(SUBSYSTEM_LIST_FILTER => '{subsystem}', \
                        CURRENT_USER_LIST_FILTER => '{user}')) J WHERE JOB_TYPE NOT IN ('SBS', 'SYS')"
                ibmi_util.log_info("Command to run: " + sql, module._name)
                rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
                if rc:
                    result_failed = dict(
                        stdout=out,
                        stderr=err,
                        job_log=job_log,
                        rc=rc,
                    )
                    message = f'non-zero return code:{rc}'
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
    else:
        module.fail_json(rc=256, msg=f"Operation {operation} is not valid")

    # Perform operation except when idempotent case
    if not operation_done:
        rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)
        result = dict(
            command=command,
            stdout=out,
            stderr=err,
            rc=rc,
            job_log=job_log,
            changed=True,
        )

    if rc != 0:
        message = f'non-zero return code:{rc}'
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})
    module.exit_json(**result)


if __name__ == '__main__':
    main()
