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

__ibmi_module_version__ = "1.1.2"


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
        'install_ptf_device',
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
        return {'name': 'ibmi', 'version': '', 'family': ''}

    def validate_int(self):
        for int_key in self._INT_ARGS:
            key_value = self._task.args.get(int_key, 1)
            re_raise = False  # workaround to pass the raise-missing-from pylint issue
            try:
                validation.check_type_int(key_value)
                if key_value < 0:
                    raise AnsibleError('The value of %s must not be less than 0' % (int_key))
            except (TypeError, ValueError):
                re_raise = True  # workaround to pass the raise-missing-from pylint issue
            if re_raise:
                raise AnsibleError("The value of argument %s is %s which can't be converted to int" % (int_key, key_value))
        return None

    def get_shutdown_command(self, task_vars, distribution):
        return self.DEFAULT_SHUTDOWN_COMMAND

    def get_system_boot_time(self, distribution):
        display.vvv('{action}: get_system_boot_time: version: {version}'.format(action=self._task.action, version=__ibmi_module_version__))
        become_user = self._task.args.get('become_user')
        display.vvv('{action}: get_system_boot_time: become to user: {user}'.format(action=self._task.action, user=become_user))
        become_user_password = self._task.args.get('become_user_password')
        re_raise = False  # workaround to pass the raise-missing-from pylint issue
        inst = None
        try:
            sql = "SELECT JOB_ENTERED_SYSTEM_TIME FROM TABLE \
                (QSYS2.JOB_INFO(JOB_STATUS_FILTER => '*ACTIVE', JOB_USER_FILTER => 'QSYS')) \
                    X WHERE JOB_NAME = '000000/QSYS/SCPF'"
            sql = ' '.join(sql.split())  # keep only one space between adjacent strings
            command_result = self._execute_module(
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
            raise AnsibleError("{action}: failed to run module ibmi_sql_query to get boot time info: {exp}".format(
                action=self._task.action,
                exp=str(inst)))
        display.vvv("{action}: command_output: {boot_time}".format(action=self._task.action, boot_time=str(command_result)))
        if command_result['rc'] != 0:
            if 'msg' in command_result:
                stderr = command_result['msg']
                stdout = ''
            else:
                stderr = command_result['stderr']
                stdout = command_result['job_log']
            raise AnsibleError("{action}: failed to get host boot time info, rc: {rc}, stdout: {out}, stderr: {err}".format(
                action=self._task.action,
                rc=command_result['rc'],
                out=stdout,
                err=stderr))
        last_boot_time = command_result['row'][0]['JOB_ENTERED_SYSTEM_TIME']
        display.vvv("{action}: last boot time: {boot_time}".format(action=self._task.action, boot_time=last_boot_time))
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
            raise AnsibleError('Invalid options for reboot_commad: {0}'.format(output['msg']).strip())

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
        display.vvv('{action}: perform_reboot: version: {version}'.format(action=self._task.action, version=__ibmi_module_version__))
        become_user = self._task.args.get('become_user')
        display.vvv('{action}: perform_reboot: become to user: {user}'.format(action=self._task.action, user=become_user))
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
        reboot_command = "{0} {1}".format(shutdown_command, shutdown_command_args)
        reboot_command = ' '.join(reboot_command.split())  # keep only one space between adjacent strings

        display.vvv("{action}: rebooting server...".format(action=self._task.action))
        delay_time = self._task.args.get('pre_reboot_delay', self.DEFAULT_PRE_REBOOT_DELAY)
        notify_message = self._task.args.get('msg', self.DEFAULT_MSG)
        send_message_command = "QSYS/SNDBRKMSG MSG('{notify_message}, SYSTEM GOING DOWN IN {delay_time} SECONDS') TOMSGQ(*ALLWS)".format(
            notify_message=notify_message, delay_time=delay_time)
        display.vvv("{action}: send rebooting notice message to all users...".format(action=self._task.action))
        try:
            self._execute_module(
                module_name='ibmi_cl_command',
                module_args={
                    "cmd": send_message_command,
                    "become_user": become_user,
                    "become_user_password": become_user_password
                }
            )
        except Exception as inst:
            display.vvv("{action}: send rebooting notice message failed: '{exp}'".format(action=self._task.action, exp=str(inst)))

        display.vvv("{action}: Waiting for {delay_time} seconds to reboot".format(action=self._task.action, delay_time=delay_time))
        time.sleep(int(delay_time))
        display.vvv("{action}: rebooting server with command '{command}'".format(action=self._task.action, command=reboot_command))
        result['start'] = datetime.utcnow()
        try:
            module_output = self._execute_module(
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
                result['msg'] = "Reboot command failed, stdout: {stdout}, stderr: {stderr}, job_log: {job_log}".format(
                    stdout=stdout.strip(),
                    stderr=stderr.strip(),
                    job_log=job_log)
            else:
                result['failed'] = False
                result['rc'] = 0
                result['msg'] = reboot_result['stdout']
        except AnsibleConnectionFailure as e:
            display.vvv('{action}: AnsibleConnectionFailure caught and handled: {error}'.format(action=self._task.action, error=to_text(e)))
            result['failed'] = False
            result['rc'] = 0
            result['msg'] = to_text(e)

        return result
