# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zengyu <pzypeng@cn.ibm.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import datetime

from ansible.errors import AnsibleError, AnsibleActionFail
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils.six import string_types
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.utils.hashing import checksum
__ibmi_module_version__ = "1.1.2"
display = Display()


class ActionModule(ActionBase):

    TRANSFERS_FILES = True

    _VALID_ARGS = frozenset((
        'src',
        'asp_group',
        'type',
        'parameters',
        'severity_level',
    ))

    def run(self, tmp=None, task_vars=None):

        display.debug("version: " + __ibmi_module_version__)

        if task_vars is None:
            task_vars = dict()

        # _tmp_args is used for ibmi_sync module
        _tmp_args = self._task.args.copy()

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try:
            startd = datetime.datetime.now()
            result = dict(
                stderr="",
                stdout="",
                stdout_lines='',
                stderr_lines='',
                delta="",
                rc=255,
                failed=False,
                job_log=[]
            )

            if self._play_context.check_mode:
                result['skipped'] = True
                result['stderr'] = 'check mode not (yet) supported for this module'
                return result

            src = self._task.args.get('src', None)
            type = self._task.args.get('type', None)

            if src is None:
                result['stderr'] = "src is required."
            elif type is None:
                result['stderr'] = "type is required."
            elif type not in ['CL', 'SQL']:
                result['stderr'] = "type must be 'CL' or 'SQL'."
            # validate src are strings FIXME: use basic.py and module specs
            elif not isinstance(src, string_types):
                result['stderr'] = "Invalid type supplied for src option, it must be a string."

            if result.get('stderr'):
                result['failed'] = True
                return result

            re_raise = False  # workaround to pass the raise-missing-from pylint issue
            inst = None
            try:
                src = self._loader.get_real_file(self._find_needle('files', src))
            except AnsibleError as e:
                re_raise = True
                inst = e
            if re_raise:
                raise AnsibleActionFail(to_native(inst))

            tmp_src = self._connection._shell.join_path(self._connection._shell.tmpdir, os.path.basename(src))
            display.debug("ibm i debug: transfer script file {p_src} to {p_tmp_src}".format(p_src=src, p_tmp_src=tmp_src))
            self._transfer_file(src, tmp_src)

            local_checksum = checksum(src)
            if not self._connection.become:
                remote_checksum = self._remote_checksum(tmp_src, all_vars=task_vars, follow=True)

            if remote_checksum in ('1', '2', None):
                result['stderr'] += "The permissions are lacking or privilege is needed. remote_checksum:{p_remote_checksum}".format(
                    p_remote_checksum=remote_checksum)
            elif local_checksum != remote_checksum:
                result['stderr'] += "local_checksum doesn't match remote_checksum."
                result['failed'] = True
                return result

            _tmp_args['src'] = tmp_src
            result.update(self._execute_module('ibmi_script_execute', module_args=_tmp_args))
            endd = datetime.datetime.now()
            delta = endd - startd

            if result['rc']:
                result['failed'] = True
                result.update(dict(stderr=(u"Failed to execute script file {p_src}.".format(p_src=src)) + result['stderr'],
                                   delta=str(delta)))
            else:
                result.update(dict(stdout=u"Successfully execute script file {p_src}.".format(p_src=src), delta=str(delta)))

        except Exception as e:
            result['stderr'] += "{p_to_text}".format(p_to_text=to_text(e))
            result['failed'] = True
            return result
        finally:
            self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
