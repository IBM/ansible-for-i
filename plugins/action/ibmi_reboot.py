# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time
from datetime import datetime

from ansible.errors import AnsibleError
from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.module_utils.common import validation
from ansible.plugins.action import ActionBase
from ansible.plugins.action.reboot import ActionModule as RebootActionModule
from ansible.utils.display import Display

display = Display()

__ibmi_module_version__ = "2.0.1"


class TimedOutException(Exception):
    pass


class ActionModule(RebootActionModule, ActionBase):
    TRANSFERS_FILES = False
    _VALID_ARGS = frozenset((
        'pre_reboot_delay',
        'post_reboot_delay',
        'reboot_timeout',
        'reboot_timeout_sec',
        'connect_timeout',
        'connect_timeout_sec',
        'test_command',
        'msg',
        'how_to_end',
        'controlled_end_delay_time',
        'reboot_type',
        'ipl_source',
        'end_subsystem_option',
        'timeout_option',
        'parameters',
        'become_user',
        'become_user_password',
    ))

    _INT_ARGS = (
        'post_reboot_delay',
        'pre_reboot_delay',
        'reboot_timeout',
        'reboot_timeout_sec',
        'connect_timeout',
        'connect_timeout_sec'
    )

    DEFAULT_SUDOABLE = False
    DEFAULT_SHUTDOWN_COMMAND_ARGS = 'OPTION({how_to_end}) \
        DELAY({controlled_end_delay_time}) \
        RESTART(*YES {reboot_type}) \
        IPLSRC({ipl_source}) \
        ENDSBSOPT({end_subsystem_option}) \
        TIMOUTOPT({timeout_option}) \
        CONFIRM(*NO) \
        {parameters}'
    DEFAULT_SHUTDOWN_COMMAND = 'QSYS/PWRDWNSYS'
    DEFAULT_PRE_REBOOT_DELAY = 60
    DEFAULT_POST_REBOOT_DELAY = 60
    DEFAULT_REBOOT_TIMEOUT = 1800
    DEFAULT_REBOOT_TIMEOUT_SEC = 15
    DEFAULT_CONNECT_TIMEOUT = 300
    DEFAULT_CONNECT_TIMEOUT_SEC = 5
    DEFAULT_TEST_COMMAND = 'uname'
    DEFAULT_MSG = 'Reboot initiated by Ansible'
    DEFAULT_HOW_TO_END = '*IMMED'
    DEFAULT_CONTROLLED_END_DELAY_TIME = 600
    DEFAULT_REBOOT_TYPE = '*IPLA'
    DEFAULT_IPL_SOURCE = '*PANEL'
    DEFAULT_END_SUBSYSTEM_OPTION = '*DFT'
    DEFAULT_TIMEOUT_OPTION = '*CONTINUE'
    DEFAULT_PARAMETERS = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_distribution(self, task_vars):
        # Also return the task_vars so that _execute_module in get_system_boot_time can use it
        return {'name': 'ibmi', 'version': '', 'family': '', 'task_vars': task_vars}

    def validate_int(self):
        for int_key in self._INT_ARGS:
            key_value = self._task.args.get(int_key, 1)
            re_raise = False  # workaround to pass the raise-missing-from pylint issue
            try:
                validation.check_type_int(key_value)
                if key_value < 0:
                    raise AnsibleError(f'The value of {int_key} must not be less than 0')
            except (TypeError, ValueError):
                re_raise = True  # workaround to pass the raise-missing-from pylint issue
            if re_raise:
                raise AnsibleError(f"The value of argument {int_key} is {key_value} which can't be converted to int")
        return None

    def get_shutdown_command(self, task_vars, distribution):
        return self.DEFAULT_SHUTDOWN_COMMAND

    def get_system_boot_time(self, distribution):
        display.vvv(f'{self._task.action}: get_system_boot_time: version: {__ibmi_module_version__}')
        become_user = self._task.args.get('become_user')
        display.vvv(f'{self._task.action}: get_system_boot_time: become to user: {become_user}')
        become_user_password = self._task.args.get('become_user_password')
        re_raise = False  # workaround to pass the raise-missing-from pylint issue
        inst = None
        try:
            sql = "SELECT JOB_ENTERED_SYSTEM_TIME FROM TABLE \
                (QSYS2.JOB_INFO(JOB_STATUS_FILTER => '*ACTIVE', JOB_USER_FILTER => 'QSYS')) \
                    X WHERE JOB_NAME = '000000/QSYS/SCPF'"
            sql = ' '.join(sql.split())  # keep only one space between adjacent strings
            # A workaround to use task_vars. RebootActionModule get_system_boot_time doesn't make task_var as the input parm
            task_vars = distribution['task_vars']
            command_result = self._execute_module(
                task_vars=task_vars,
                module_name='ibmi_sql_query',
                module_args={
                    "sql": sql,
                    "expected_row_count": 1,
                    "become_user": become_user,
                    "become_user_password": become_user_password
                }
            )
        except Exception as e:
            re_raise = True  # workaround to pass the raise-missing-from pylint issue
            inst = e
        if re_raise:
            raise AnsibleError(f"{self._task.action}: failed to run module ibmi_sql_query to get boot time info: {inst}")
        display.vvv(f"{self._task.action}: command_output: {command_result}")
        if command_result['rc'] != 0:
            if 'msg' in command_result:
                stderr = command_result['msg']
                stdout = ''
            else:
                stderr = command_result['stderr']
                stdout = command_result['job_log']
            raise AnsibleError(f"{self._task.action}: failed to get host boot time info, rc: {command_result['rc']}, stdout: {stdout}, stderr: {stderr}")
        last_boot_time = command_result['row'][0]['JOB_ENTERED_SYSTEM_TIME']
        display.vvv(f"{self._task.action}: last boot time: {last_boot_time}")
        return last_boot_time

    def get_shutdown_command_args(self, distribution):
        args = self._get_value_from_facts('SHUTDOWN_COMMAND_ARGS', distribution, 'DEFAULT_SHUTDOWN_COMMAND_ARGS')
        output = {}
        controlled_end_delay_time_seconds = self._task.args.get('controlled_end_delay_time', self.DEFAULT_CONTROLLED_END_DELAY_TIME)
        try:
            if int(controlled_end_delay_time_seconds) > 99999:
                controlled_end_delay_time = '*NOLIMIT'
            else:
                controlled_end_delay_time = controlled_end_delay_time_seconds
                if int(controlled_end_delay_time_seconds) < 1:
                    output['msg'] = "Invalid value for controlled_end_delay_time option, it must be greater than 0"
        except ValueError:
            output['msg'] = "Invalid value for controlled_end_delay_time option, it must be a int greater than 0"

        how_to_end = self._task.args.get('how_to_end', self.DEFAULT_HOW_TO_END)
        if how_to_end not in ['*IMMED', '*CNTRLD']:
            output['msg'] = "Invalid value for how_to_end option, it must be '*IMMED' or '*CNTRLD'"

        reboot_type = self._task.args.get('reboot_type', self.DEFAULT_REBOOT_TYPE)
        if reboot_type not in ['*IPLA', '*SYS', '*FULL']:
            output['msg'] = "Invalid value for reboot_type option, it must be '*IPLA', '*SYS' or '*FULL'"

        ipl_source = self._task.args.get('ipl_source', self.DEFAULT_IPL_SOURCE)
        if ipl_source not in ['*PANEL', 'A', 'B', 'D']:
            output['msg'] = "Invalid value for ipl_source option, it must be '*PANEL', 'A', 'B' or 'D'"

        end_subsystem_option = self._task.args.get('end_subsystem_option', self.DEFAULT_END_SUBSYSTEM_OPTION)
        if end_subsystem_option not in ['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL']:
            output['msg'] = "Invalid value for end_subsystem_option option, it must be '*DFT', '*NOJOBLOG', '*CHGPTY' or '*CHGTSL'"

        timeout_option = self._task.args.get('timeout_option', self.DEFAULT_TIMEOUT_OPTION)
        if timeout_option not in ['*CONTINUE', '*MSD', '*SYSREFCDE']:
            output['msg'] = "Invalid value for timeout_option option, it must be '*CONTINUE', '*MSD' or '*SYSREFCDE'"

        parameters = self._task.args.get('parameters', self.DEFAULT_PARAMETERS)

        if output.get('msg'):
            msg_string = output['msg'].strip()
            raise AnsibleError(f'Invalid options for reboot_commad: {msg_string}')

        return args.format(
            how_to_end=how_to_end,
            controlled_end_delay_time=controlled_end_delay_time,
            reboot_type=reboot_type,
            ipl_source=ipl_source,
            end_subsystem_option=end_subsystem_option,
            timeout_option=timeout_option,
            parameters=parameters
        )

    def perform_reboot(self, task_vars, distribution):
        display.vvv(f'{self._task.action}: perform_reboot: version: {__ibmi_module_version__}')
        become_user = self._task.args.get('become_user')
        display.vvv(f'{self._task.action}: perform_reboot: become to user: {become_user}')
        become_user_password = self._task.args.get('become_user_password')
        result = {}
        result['start'] = datetime.utcnow()
        try:
            self.validate_int()
            shutdown_command_args = self.get_shutdown_command_args(distribution)
        except AnsibleError as e:
            result['failed'] = True
            result['rebooted'] = False
            result['msg'] = to_text(e)
            return result
        shutdown_command = self.get_shutdown_command(task_vars, distribution)
        reboot_command = f"{shutdown_command} {shutdown_command_args}"
        reboot_command = ' '.join(reboot_command.split())  # keep only one space between adjacent strings

        display.vvv(f"{self._task.action}: rebooting server...")
        delay_time = self._task.args.get('pre_reboot_delay', self.DEFAULT_PRE_REBOOT_DELAY)
        notify_message = self._task.args.get('msg', self.DEFAULT_MSG)
        send_message_command = f"QSYS/SNDBRKMSG MSG('{notify_message}, SYSTEM GOING DOWN IN {delay_time} SECONDS') TOMSGQ(*ALLWS)"
        display.vvv(f"{self._task.action}: send rebooting notice message to all users...")
        try:
            self._execute_module(
                task_vars=task_vars,
                module_name='ibmi_cl_command',
                module_args={
                    "cmd": send_message_command,
                    "become_user": become_user,
                    "become_user_password": become_user_password
                }
            )
        except Exception as inst:
            display.vvv(f"{self._task.action}: send rebooting notice message failed: '{inst}'")

        display.vvv(f"{self._task.action}: Waiting for {delay_time} seconds to reboot")
        time.sleep(int(delay_time))
        display.vvv(f"{self._task.action}: rebooting server with command '{reboot_command}'")
        result['start'] = datetime.utcnow()
        try:
            module_output = self._execute_module(
                task_vars=task_vars,
                module_name='ibmi_cl_command',
                module_args={
                    "cmd": reboot_command,
                    "become_user": become_user,
                    "become_user_password": become_user_password
                }
            )
            result['start'] = datetime.utcnow()
            reboot_result = module_output
            if reboot_result['rc'] != 0:
                stdout = reboot_result['stdout']
                stderr = reboot_result['stderr']
                job_log = reboot_result['job_log']
                result['failed'] = True
                result['rebooted'] = False
                result['msg'] = f"Reboot command failed, stdout: {stdout.strip()}, stderr: {stderr.strip()}, job_log: {job_log}"
            else:
                result['failed'] = False
                result['rc'] = 0
                result['msg'] = reboot_result['stdout']
        except AnsibleConnectionFailure as e:
            display.vvv(f'{self._task.action}: AnsibleConnectionFailure caught and handled: {to_text(e)}')
            result['failed'] = False
            result['rc'] = 0
            result['msg'] = to_text(e)

        return result
