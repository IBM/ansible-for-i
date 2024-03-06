# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zengyu <pzypeng@cn.ibm.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import datetime

from ansible.errors import AnsibleError, AnsibleActionFail
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils.six import string_types
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.utils.hashing import checksum
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
__ibmi_module_version__ = "2.0.1"

display = Display()


class ActionModule(ActionBase):
    _VALID_ARGS = frozenset((
        'src',
        'lib_name',
        'force',
        'backup',
    ))

    def _calculate_savf_path(self, savefile_name, lib_name):
        # Calculate savf path when object is a *FILE
        if lib_name != 'QSYS':
            savf_path = f'/QSYS.LIB/{lib_name}.LIB/{savefile_name}.FILE'
        else:
            savf_path = f'/QSYS.LIB/{savefile_name}.FILE'

        return savf_path

    def _calculate_savf_name(self, savefile_name, lib_name, task_vars):
        # Calculate savf name and path
        savf_name = savefile_name
        original_savf_name = savefile_name
        msg = ''

        if lib_name != 'QSYS':
            savf_path = f'/QSYS.LIB/{lib_name}.LIB/{original_savf_name}.FILE'
        else:
            savf_path = f'/QSYS.LIB/{original_savf_name}.FILE'
        i = 1
        while (self._execute_remote_stat(savf_path, all_vars=task_vars, follow=False))['exists']:
            if i > 9:
                msg = f'Rename failure. SAVF names ({savf_path} range(1,{str(i)})) are already exist on IBMi. Failed'
                return savf_name, savf_path, msg
            if len(original_savf_name + str(i)) <= 10:
                if lib_name != 'qsys':
                    savf_path = f'/QSYS.LIB/{lib_name}.LIB/{original_savf_name + str(i)}.FILE'
                else:
                    savf_path = f'/QSYS.LIB/{original_savf_name + str(i)}.FILE'
            else:
                if lib_name != 'qsys':
                    savf_path = f'/QSYS.LIB/{lib_name}.LIB/{original_savf_name[0:9] + str(i)}.FILE'
                else:
                    savf_path = f'/QSYS.LIB/{original_savf_name[0:9] + str(i)}.FILE'
                savf_name = original_savf_name[0:9] + str(i)
            i += 1

        return savf_name, savf_path, msg

    def run(self, tmp=None, task_vars=None):

        display.debug("version: " + __ibmi_module_version__)
        ''' handler for fetch operations '''
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        created = False
        try:
            result = dict(
                msg="",
                stderr="",
                stdout="",
                src="",
                md5sum="",
                dest="",
                remote_md5sum="",
                remote_checksum="",
                checksum="",
                delta="",
                job_log=[],
                rc=255,
                failed=False
            )
            if self._play_context.check_mode:
                result['skipped'] = True
                result['msg'] = 'check mode not (yet) supported for this module'
                return result

            src = self._task.args.get('src', None)
            lib_name = self._task.args.get('lib_name', None)
            force = boolean(self._task.args.get('force', False), strict=True)
            backup = boolean(self._task.args.get('backup', False), strict=True)

            if lib_name is None:
                result['msg'] = "lib_name is required."
            elif src is None:
                result['msg'] = "src is required."
            # validate dest are strings FIXME: use basic.py and module specs
            elif not isinstance(src, string_types):
                result['msg'] = "Invalid type supplied for src option, it must be a string."

            if result.get('msg'):
                result['failed'] = True
                return result

            re_raise = False
            inst = None
            try:
                src = self._loader.get_real_file(self._find_needle('files', src))
            except AnsibleError as e:
                re_raise = True
                inst = e
            if re_raise:
                raise AnsibleActionFail(to_native(inst))

            lib_name = lib_name.upper()
            startd = datetime.datetime.now()

            # Get the file name without extention
            savefile_name = os.path.splitext(os.path.basename(src))[0]
            savefile_path = self._calculate_savf_path(savefile_name, lib_name)

            if self._execute_remote_stat(savefile_path, all_vars=task_vars, follow=False)['exists']:
                if force is True:
                    if backup is True:
                        # Rename original save file
                        rename_savf_name, rename_savf_path, msg = self._calculate_savf_name(savefile_name, lib_name, task_vars)
                        if msg:
                            result['msg'] += msg
                            result['failed'] = True
                            return result
                        else:
                            cmd = f"QSYS/REN OBJ('{savefile_path}') NEWOBJ({rename_savf_name}.file)"
                            module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd}, task_vars=task_vars)
                            save_result = module_output
                            rc = save_result['rc']
                            if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                                result['msg'] += "Failed to rename original SAVF on remote. "
                                result['stderr'] = save_result['stderr_lines']
                                result['stdout'] = save_result['stdout_lines']
                                result['job_log'] = save_result['job_log']
                                result['rc'] = save_result['rc']
                                result['failed'] = True
                                return result
                        display.debug(f"ibm i debug: The original save file is successfully renamed to {rename_savf_name}")
                    else:
                        cmd = f'QSYS/DLTOBJ OBJ({lib_name}/{savefile_name}) OBJTYPE(*FILE)'
                        module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd}, task_vars=task_vars)
                        save_result = module_output
                        rc = save_result['rc']
                        if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                            result['msg'] += "Failed to delete original SAVF on remote. "
                            result['stderr'] = save_result['stderr_lines']
                            result['stdout'] = save_result['stdout_lines']
                            result['job_log'] = save_result['job_log']
                            result['rc'] = save_result['rc']
                            result['failed'] = True
                            return result
                        display.debug("ibm i debug: The original save file is deleted.")
                else:
                    result['msg'] += "File with the Same name already exists on remote. If still want to copy, set force True. "
                    result['failed'] = True
                    return result

            # Create the save file
            cmd = f'QSYS/CRTSAVF FILE({lib_name}/{savefile_name})'
            module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd}, task_vars=task_vars)
            save_result = module_output
            rc = save_result['rc']
            if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                result['msg'] += f"Failed to create SAVF: {savefile_path} on remote."
                result['stderr'] = save_result['stderr_lines']
                result['stdout'] = save_result['stdout_lines']
                result['job_log'] = save_result['job_log']
                result['rc'] = save_result['rc']
                result['failed'] = True
                return result
            display.debug(f"ibm i debug: transfer {src} to {savefile_path}")
            self._transfer_file(src, savefile_path)

            local_checksum = checksum(src)
            remote_stat = None
            remote_checksum = None
            if not self._connection.become:
                remote_stat = self._execute_remote_stat(savefile_path, all_vars=task_vars, follow=True)
                remote_checksum = remote_stat['checksum']

            if remote_checksum in ('1', '', None):
                result['msg'] += "File does not exist, permissions are lacking, or another issue. remote_checksum:{remote_checksum}"
            elif local_checksum != remote_checksum:
                result['msg'] += "local_checksum doesn't match remote_checksum. "
                result['failed'] = True
                return result

            endd = datetime.datetime.now()
            delta = endd - startd

            result.update(dict(msg="File is successfully copied.", src=src, delta=str(delta), dest=savefile_path), rc=0)

        except Exception as e:
            result['msg'] += f"{to_text(e)}"
            result['failed'] = True
            return result
        finally:
            if created is True and result['failed'] is True:
                cmd = f'QSYS/DLTOBJ OBJ({lib_name}/{savefile_name}) OBJTYPE(*FILE)'
                module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd}, task_vars=task_vars)
                save_result = module_output
                rc = save_result['rc']
                if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS and ('CPF2105' not in save_result['stderr']):
                    result['msg'] += f"Failed to delete the new created save file {savefile_path} on remote. "
                    result['job_log'] = save_result['job_log']

        return result
