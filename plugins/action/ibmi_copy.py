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
__ibmi_module_version__ = "1.1.2"

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
            savf_path = '/QSYS.LIB/{p_lib_name}.LIB/{p_savefile_name}.FILE'.format(
                p_lib_name=lib_name,
                p_savefile_name=savefile_name)
        else:
            savf_path = '/QSYS.LIB/{p_savefile_name}.FILE'.format(p_savefile_name=savefile_name)

        return savf_path

    def _calculate_savf_name(self, savefile_name, lib_name, task_vars):
        # Calculate savf name and path
        savf_name = savefile_name
        original_savf_name = savefile_name
        msg = ''

        if lib_name != 'QSYS':
            savf_path = '/QSYS.LIB/{p_lib_name}.LIB/{p_original_savf_name}.FILE'.format(
                p_lib_name=lib_name,
                p_original_savf_name=original_savf_name)
        else:
            savf_path = '/QSYS.LIB/{p_original_savf_name}.FILE'.format(p_original_savf_name=original_savf_name)
        i = 1
        while (self._execute_remote_stat(savf_path, all_vars=task_vars, follow=False))['exists']:
            if i > 9:
                msg = 'Rename failure. SAVF names ({p_savf_path} range(1,{p_str})) are already exist on IBMi. Failed'.format(
                    p_savf_path=savf_path,
                    p_str=str(i))
                return savf_name, savf_path, msg
            if len(original_savf_name + str(i)) <= 10:
                if lib_name != 'qsys':
                    savf_path = '/QSYS.LIB/{p_lib_name}.LIB/{p_original_savf_name}.FILE'.format(
                        p_lib_name=lib_name,
                        p_original_savf_name=original_savf_name + str(i))
                else:
                    savf_path = '/QSYS.LIB/{p_original_savf_name}.FILE'.format(p_original_savf_name=original_savf_name + str(i))
                savf_name = original_savf_name + str(i)
            else:
                if lib_name != 'qsys':
                    savf_path = '/QSYS.LIB/{p_lib_name}.LIB/{p_original_savf_name}.FILE'.format(
                        p_lib_name=lib_name,
                        p_original_savf_name=original_savf_name[0:9] + str(i))
                else:
                    savf_path = '/QSYS.LIB/{p_original_savf_name}.FILE'.format(
                        p_original_savf_name=original_savf_name[0:9] + str(i))
                savf_name = original_savf_name[0:9] + str(i)
            i += 1

        return savf_name, savf_path, msg

    def run(self, tmp=None, task_vars=None):

        display.debug("version: " + __ibmi_module_version__)
        ''' handler for fetch operations '''
        if task_vars is None:
            task_vars = dict()

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

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
            created = False
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
                            cmd = "QSYS/REN OBJ('{p_savefile_path}') NEWOBJ({p_rename_savf_name}.file)".format(
                                p_savefile_path=savefile_path,
                                p_rename_savf_name=rename_savf_name)
                            module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
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
                        display.debug("ibm i debug: The original save file is successfully renamed to {p_rename_savf_name}".format(
                            p_rename_savf_name=rename_savf_name))
                    else:
                        cmd = 'QSYS/DLTOBJ OBJ({p_lib_name}/{p_savefile_name}) OBJTYPE(*FILE)'.format(
                            p_lib_name=lib_name,
                            p_savefile_name=savefile_name)
                        module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
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
            cmd = 'QSYS/CRTSAVF FILE({p_lib_name}/{p_savefile_name})'.format(
                p_lib_name=lib_name,
                p_savefile_name=savefile_name)
            module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
            save_result = module_output
            rc = save_result['rc']
            if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                result['msg'] += "Failed to create SAVF: {p_savefile_path} on remote.".format(p_savefile_path=savefile_path)
                result['stderr'] = save_result['stderr_lines']
                result['stdout'] = save_result['stdout_lines']
                result['job_log'] = save_result['job_log']
                result['rc'] = save_result['rc']
                result['failed'] = True
                return result
            display.debug("ibm i debug: transfer {p_src} to {p_savefile_path}".format(p_src=src, p_savefile_path=savefile_path))
            self._transfer_file(src, savefile_path)

            local_checksum = checksum(src)
            if not self._connection.become:
                remote_checksum = self._remote_checksum(savefile_path, all_vars=task_vars, follow=True)

            if remote_checksum in ('1', '2', None):
                result['msg'] += "remote_checksum error. The permissions are lacking or privilege escalation is needed. "
            elif local_checksum != remote_checksum:
                result['msg'] += "local_checksum doesn't match remote_checksum. "
                result['failed'] = True
                return result

            endd = datetime.datetime.now()
            delta = endd - startd

            result.update(dict(msg="File is successfully copied.", src=src, delta=str(delta), dest=savefile_path), rc=0)

        except Exception as e:
            result['msg'] += "{p_to_text}".format(p_to_text=to_text(e))
            result['failed'] = True
            return result
        finally:
            if created is True and result['failed'] is True:
                cmd = 'QSYS/DLTOBJ OBJ({p_lib_name}/{p_savefile_name}) OBJTYPE(*FILE)'.format(
                    p_lib_name=lib_name,
                    p_savefile_name=savefile_name)
                module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
                save_result = module_output
                rc = save_result['rc']
                if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS and ('CPF2105' not in save_result['stderr']):
                    result['msg'] += "Failed to delete the new created save file {p_savefile_path} on remote. ".format(
                        p_savefile_path=savefile_path)
                    result['job_log'] = save_result['job_log']

        return result
