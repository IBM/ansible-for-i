# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zeng Yu <pzypeng@cn.ibm.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import base64
import datetime

from ansible.errors import AnsibleError, AnsibleActionFail
from ansible.module_utils._text import to_text, to_native
from ansible.module_utils._text import to_bytes
from ansible.module_utils.six import string_types
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.utils.hashing import checksum, checksum_s, md5, secure_hash
from ansible.utils.path import makedirs_safe

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255

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
            savf_path = '/QSYS.LIB/%s.LIB/%s.FILE' % (lib_name, savefile_name)
        else:
            savf_path = '/QSYS.LIB/%s.FILE' % (savefile_name)

        return savf_path

    def _calculate_savf_name(self, savefile_name, lib_name, task_vars):
        # Calculate savf name and path
        savf_name = savefile_name
        original_savf_name = savefile_name
        msg = ''

        if lib_name != 'QSYS':
            savf_path = '/QSYS.LIB/%s.LIB/%s.FILE' % (lib_name, original_savf_name)
        else:
            savf_path = '/QSYS.LIB/%s.FILE' % (original_savf_name)
        i = 1
        while (self._execute_remote_stat(savf_path, all_vars=task_vars, follow=False))['exists']:
            if i > 9:
                msg = 'Rename failure. SAVF names (%s range(1,%s)) are already exist on IBMi. Failed' % (savf_path, str(i))
                return savf_name, savf_path, msg
            if len(original_savf_name + str(i)) <= 10:
                if lib_name != 'qsys':
                    savf_path = '/QSYS.LIB/%s.LIB/%s.FILE' % (lib_name, original_savf_name + str(i))
                else:
                    savf_path = '/QSYS.LIB/%s.FILE' % (original_savf_name + str(i))
                savf_name = original_savf_name + str(i)
            else:
                if lib_name != 'qsys':
                    savf_path = '/QSYS.LIB/%s.LIB/%s.FILE' % (lib_name, original_savf_name[0:9] + str(i))
                else:
                    savf_path = '/QSYS.LIB/%s.FILE' % (original_savf_name[0:9] + str(i))
                savf_name = original_savf_name[0:9] + str(i)
            i += 1

        return savf_name, savf_path, msg

    def run(self, tmp=None, task_vars=None):
        ''' handler for fetch operations '''
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
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
                failed=False
            )
            savf_name = ''
            created = False
            is_savf = False
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

            try:
                src = self._loader.get_real_file(self._find_needle('files', src))
            except AnsibleError as e:
                raise AnsibleActionFail(to_native(e))

            lib_name = lib_name.upper()
            startd = datetime.datetime.now()

            # Get the file name without extention
            savefile_name = os.path.splitext(os.path.basename(src))[0]
            savefile_path = self._calculate_savf_path(savefile_name, lib_name)
            display.debug("savefile_name = %s, savf_path = %s" % (savefile_name, savefile_path))

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
                            cmd = "QSYS/REN OBJ('%s') NEWOBJ(%s.file)" % (savefile_path, rename_savf_name)
                            module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
                            save_result = module_output
                            rc = save_result['rc']
                            if rc != IBMi_COMMAND_RC_SUCCESS:
                                result['msg'] += "Failed to rename original SAVF on remote. "
                                result['stderr'] = save_result['stderr_lines']
                                result['stdout'] = save_result['stdout_lines']
                                result['failed'] = True
                                return result
                        display.debug("The original save file is successfully renamed to %s" % (savefile_path))
                    else:
                        cmd = 'QSYS/DLTOBJ OBJ(%s/%s) OBJTYPE(*FILE)' % (lib_name, savefile_name)
                        module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
                        save_result = module_output
                        rc = save_result['rc']
                        if rc != IBMi_COMMAND_RC_SUCCESS:
                            result['msg'] += "Failed to delete original SAVF on remote. "
                            result['stderr'] = save_result['stderr_lines']
                            result['stdout'] = save_result['stdout_lines']
                            result['failed'] = True
                            return result
                        display.debug("The original save file is deleted.")
                else:
                    result['msg'] += "File with the Same name already exists on remote. If still want to copy, set force True. "
                    result['failed'] = True
                    return result

            # Create the save file
            cmd = 'QSYS/CRTSAVF FILE(%s/%s)' % (lib_name, savefile_name)
            module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
            save_result = module_output
            rc = save_result['rc']
            if rc != IBMi_COMMAND_RC_SUCCESS:
                result['msg'] += "Failed to create SAVF: %s on remote." % savefile_path
                result['stderr'] = save_result['stderr_lines']
                result['stdout'] = save_result['stdout_lines']
                result['failed'] = True
                return result
            dir = os.path.dirname(savefile_path)

            display.debug("Start to copy file. src = %s, savefile_path = %s, savefile_path= %s " % (src, savefile_path,
                                                                                                    savefile_path))
            self._transfer_file(src, savefile_path)

            local_checksum = checksum(src)
            remote_data = None
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

            result.update(dict(msg="File is successfully copied.", src=src, delta=str(delta), dest=savefile_path))

        except Exception as e:
            result['msg'] += "%s" % to_text(e)
            result['failed'] = True
            return result
        finally:
            if created is True and result['failed'] is True:
                cmd = 'QSYS/DLTOBJ OBJ(%s/%s) OBJTYPE(*FILE)' % (lib_name, savefile_name)
                module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd})
                save_result = module_output
                rc = save_result['rc']
                if rc != 0 and ('CPF2105' not in save_result['stderr']):
                    result['msg'] += "Failed to delete the new created save file %s on remote when copy fails. " % savefile_path

        return result
