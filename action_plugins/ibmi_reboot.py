# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time
from datetime import datetime

from ansible.errors import AnsibleError
from ansible.errors import AnsibleConnectionFailure
from ansible.module_utils._text import to_text
from ansible.plugins.action import ActionBase
from ansible.plugins.action.reboot import ActionModule as RebootActionModule
from ansible.utils.display import Display

display = Display()


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
    ))

    DEFAULT_SUDOABLE = False
    DEFAULT_SHUTDOWN_COMMAND_ARGS = 'OPTION({how_to_end}) \
        DELAY({controlled_end_delay_time}) \
        RESTART(*YES {reboot_type}) \
        IPLSRC({ipl_source}) \
        ENDSBSOPT({end_subsystem_option}) \
        TIMOUTOPT({timeout_option}) \
        CONFIRM(*NO) \
        INSPTFDEV({install_ptf_device})'
    DEFAULT_SHUTDOWN_COMMAND = 'PWRDWNSYS'
    DEFAULT_PRE_REBOOT_DELAY = 60
    DEFAULT_POST_REBOOT_DELAY = 60
    DEFAULT_REBOOT_TIMEOUT = 900
    DEFAULT_REBOOT_TIMEOUT_SEC = 15
    DEFAULT_CONNECT_TIMEOUT = 900
    DEFAULT_CONNECT_TIMEOUT_SEC = 15
    DEFAULT_TEST_COMMAND = 'uname'
    DEFAULT_MSG = 'Reboot initiated by Ansible'
    DEFAULT_HOW_TO_END = '*CNTRLD'
    DEFAULT_CONTROLLED_END_DELAY_TIME = 3600
    DEFAULT_REBOOT_TYPE = '*IPLA'
    DEFAULT_IPL_SOURCE = '*PANEL'
    DEFAULT_END_SUBSYSTEM_OPTION = '*DFT'
    DEFAULT_TIMEOUT_OPTION = '*CONTINUE'
    DEFAULT_INSTALL_PTF_DEVICE = '*NONE'

    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)

    def get_distribution(self, task_vars):
        return {'name': 'ibmi', 'version': '', 'family': ''}

    def get_shutdown_command(self, task_vars, distribution):
        return self.DEFAULT_SHUTDOWN_COMMAND

    def get_system_boot_time(self, distribution):
        module_output = self._execute_module(
            module_name='ibmi_sql_query',
            module_args={
                "sql": "SELECT job_entered_system_time FROM TABLE \
                    (qsys2.job_info(job_status_filter => '*ACTIVE', job_user_filter => 'QSYS')) x \
                    WHERE job_name = '000000/QSYS/SCPF'",
                "expected_row_count": 1})
        try:
            if module_output['rc'] != 0:
                raise AnsibleError('Failed to determine system last boot time. {0}'.format(
                    module_output['stderr']).strip())
            last_boot_time = module_output['row'][0]['JOB_ENTERED_SYSTEM_TIME']
            display.debug("{action}: last boot time: {boot_time}".format(action=self._task.action, boot_time=last_boot_time))
            display.vvv("{action}: last boot time: {boot_time}".format(action=self._task.action, boot_time=last_boot_time))
            return last_boot_time
        except KeyError as ke:
            raise AnsibleError('Failed to get last boot time information. Missing "{0}" in output.'.format(ke.args[0]))
        return None

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
        if not isinstance(how_to_end, str):
            output['msg'] = "Invalid type supplied for how_to_end option, it must be a string"
        elif how_to_end not in ['*IMMED', '*CNTRLD']:
            output['msg'] = "Invalid value for how_to_end option, it must be '*IMMED' or '*CNTRLD'"

        reboot_type = self._task.args.get('reboot_type', self.DEFAULT_REBOOT_TYPE)
        if not isinstance(reboot_type, str):
            output['msg'] = "Invalid type supplied for reboot_type option, it must be a string"
        elif reboot_type not in ['*IPLA', '*SYS', '*FULL']:
            output['msg'] = "Invalid value for reboot_type option, it must be '*IPLA', '*SYS' or '*FULL'"

        ipl_source = self._task.args.get('ipl_source', self.DEFAULT_IPL_SOURCE)
        if not isinstance(ipl_source, str):
            output['msg'] = "Invalid type supplied for ipl_source option, it must be a string"
        elif ipl_source not in ['*PANEL', 'A', 'B', 'D']:
            output['msg'] = "Invalid value for ipl_source option, it must be '*PANEL', 'A', 'B' or 'D'"

        end_subsystem_option = self._task.args.get('end_subsystem_option', self.DEFAULT_END_SUBSYSTEM_OPTION)
        if not isinstance(end_subsystem_option, str):
            output['msg'] = "Invalid type supplied for end_subsystem_option option, it must be a string"
        elif end_subsystem_option not in ['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL']:
            output['msg'] = "Invalid value for end_subsystem_option option, it must be '*DFT', '*NOJOBLOG', '*CHGPTY' or '*CHGTSL'"

        timeout_option = self._task.args.get('timeout_option', self.DEFAULT_TIMEOUT_OPTION)
        if not isinstance(timeout_option, str):
            output['msg'] = "Invalid type supplied for timeout_option option, it must be a string"
        elif timeout_option not in ['*CONTINUE', '*MSD', '*SYSREFCDE']:
            output['msg'] = "Invalid value for timeout_option option, it must be '*CONTINUE', '*MSD' or '*SYSREFCDE'"

        install_ptf_device = self._task.args.get('install_ptf_device', self.DEFAULT_INSTALL_PTF_DEVICE)
        if not isinstance(install_ptf_device, str):
            output['msg'] = "Invalid type supplied for install_ptf_device option, it must be a string"

        if output.get('msg'):
            raise AnsibleError('Invalid options for reboot_commad: {0}'.format(output['msg']).strip())

        return args.format(
            how_to_end=how_to_end,
            controlled_end_delay_time=controlled_end_delay_time,
            reboot_type=reboot_type,
            ipl_source=ipl_source,
            end_subsystem_option=end_subsystem_option,
            timeout_option=timeout_option,
            install_ptf_device=install_ptf_device
        )

    def perform_reboot(self, task_vars, distribution):
        shutdown_command = self.get_shutdown_command(task_vars, distribution)
        result = {}
        try:
            shutdown_command_args = self.get_shutdown_command_args(distribution)
        except AnsibleError as e:
            result['start'] = datetime.utcnow()
            result['failed'] = True
            result['rebooted'] = False
            result['msg'] = to_text(e)
            return result
        reboot_command = "{0} {1}".format(shutdown_command, shutdown_command_args)

        display.vvv("{action}: rebooting server...".format(action=self._task.action))
        delay_time = self._task.args.get('pre_reboot_delay', self.DEFAULT_PRE_REBOOT_DELAY)
        notify_message = self._task.args.get('msg', self.DEFAULT_MSG)
        send_message_command = "SNDBRKMSG MSG('{notify_message}, system going down in {delay_time} seconds') TOMSGQ(*ALLWS)".format(
            notify_message=notify_message, delay_time=delay_time)
        self._execute_module(
            module_name='ibmi_cl_command',
            module_args={"cmd": send_message_command})

        time.sleep(int(delay_time))
        display.debug("{action}: rebooting server with command '{command}'".format(action=self._task.action, command=reboot_command))
        display.vvv("{action}: rebooting server with command '{command}'".format(action=self._task.action, command=reboot_command))
        try:
            module_output = self._execute_module(
                module_name='ibmi_cl_command',
                module_args={"cmd": reboot_command})
            reboot_result = module_output
            stdout = reboot_result['stdout']
            stderr = reboot_result['stderr']
            result['start'] = datetime.utcnow()

            if reboot_result['stdout'].startswith('CPF0901'):
                result['failed'] = False
                result['rc'] = 0
                result['msg'] = reboot_result['stdout']
            else:
                result['failed'] = True
                result['rebooted'] = False
                result['msg'] = "Reboot command failed, error was: {stdout} {stderr}".format(
                    stdout=stdout.strip(),
                    stderr=stderr.strip())
        except AnsibleConnectionFailure as e:
            display.vvv('{action}: AnsibleConnectionFailure caught and handled: {error}'.format(action=self._task.action, error=to_text(e)))
            result['failed'] = False
            result['rc'] = 0
            result['msg'] = to_text(e)
            result['start'] = datetime.utcnow()

        return result
