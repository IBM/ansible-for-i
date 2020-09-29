# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zengyu <pzypeng@cn.ibm.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import constants as C
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
__ibmi_module_version__ = "1.1.2"
display = Display()


class ActionModule(ActionBase):
    # check args for both ibmi_synchronize plugin and ibmi_sync module, ibmi_synchronize passes args to ibmi_sync
    _VALID_ARGS = frozenset((
        'src',
        'dest',
        'remote_user',
        'private_key'
    ))

    def run(self, tmp=None, task_vars=None):

        display.debug("version: " + __ibmi_module_version__)

        if task_vars is None:
            task_vars = dict()

        # _tmp_args is used for ibmi_sync module
        _tmp_args = self._task.args.copy()

        result = super().run(tmp, task_vars)
        del tmp

        result = dict(
            stdout='',
            stderr='',
            stdout_lines='',
            stderr_lines='',
            rc=0,
            delta='',
            failed=False
        )

        src = _tmp_args.get('src', None)
        remote_user = _tmp_args.get('remote_user', None)

        if src is None:
            result.update(dict(failed=True, stderr="src is required. "))
            return result

        # Store remote connection type
        self._remote_transport = self._connection.transport

        # Get the delegate_to. delegate_to is required on ibm i.
        try:
            delegate_to = self._task.delegate_to
        except (AttributeError, KeyError):
            result.update(dict(failed=True, stderr="delegate_to is required. "))
            return result

        inventory_hostname = task_vars.get('inventory_hostname')
        dest_host_inventory_vars = task_vars['hostvars'].get(inventory_hostname)
        try:
            dest_host = dest_host_inventory_vars['ansible_host']
        except KeyError:
            dest_host = dest_host_inventory_vars.get('ansible_ssh_host', inventory_hostname)

        dest_host_ids = [hostid for hostid in (dest_host_inventory_vars.get('inventory_hostname'),
                                               dest_host_inventory_vars.get('ansible_host'),
                                               dest_host_inventory_vars.get('ansible_ssh_host'))
                         if hostid is not None]
        _tmp_args['remote_host'] = dest_host

        # Don't support src and dest are the same.
        if delegate_to in dest_host_ids:
            result.update(dict(failed=True, stderr="The src host can't be the same as dest host. "))
            return result

        if not remote_user:
            remote_user = task_vars.get('ansible_ssh_user') or self._play_context.remote_user
            if not remote_user:
                remote_user = C.DEFAULT_REMOTE_USER
        _tmp_args['remote_user'] = remote_user

        display.debug("ibm i debug: args for ibmi_sync {p_tmp_args}".format(p_tmp_args=_tmp_args))
        # run the module and store the result
        result.update(self._execute_module('ibmi_sync', module_args=_tmp_args))
        result['failed'] = result['rc']

        if 'SyntaxError' in result.get('exception', result.get('msg', '')):
            result['exception'] = result['msg']
            result['msg'] = ('SyntaxError parsing module.  Perhaps invoking "python" on delegate_to machine invokes python3. '
                             'You can set ansible_python_interpreter for the delegate_to machine to the location of python2 to fix this')
        return result
