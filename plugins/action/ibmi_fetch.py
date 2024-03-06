# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zengyu <pzypeng@cn.ibm.com>
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import os
import base64
import datetime

from ansible.errors import AnsibleError
from ansible.module_utils._text import to_text
from ansible.module_utils._text import to_bytes
from ansible.module_utils.six import string_types
from ansible.module_utils.parsing.convert_bool import boolean
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display
from ansible.utils.hashing import checksum, checksum_s, md5, secure_hash
from ansible.utils.path import makedirs_safe
__ibmi_module_version__ = "2.0.1"

ifs_dir = '/tmp/.ansible'
display = Display()


class ActionModule(ActionBase):
    _VALID_ARGS = frozenset((
        'object_names',
        'lib_name',
        'object_types',
        'is_lib',
        'savefile_name',
        'force_save',
        'backup',
        'format',
        'target_release',
        'dest',
        'flat',
        'validate_checksum',
    ))

    def _calculate_savf_path(self, object_names, lib_name):
        # Calculate savf path when object is a *FILE
        if lib_name != 'QSYS':
            savf_path = f'/QSYS.LIB/{lib_name}.LIB/{object_names}.FILE'
        else:
            savf_path = f'/QSYS.LIB/{object_names}.FILE'

        return savf_path

    def _calculate_savf_name(self, object_names, lib_name, is_lib, savefile_name, task_vars, result):
        # Calculate savf name and path
        savf_name = lib_name
        original_savf_name = lib_name

        if savefile_name is None:
            if is_lib is not True and object_names != '*ALL':
                if (object_names.split())[0][-1] == '*':
                    original_savf_name = (object_names.split())[0][0:-1]
                else:
                    original_savf_name = (object_names.split())[0]
                savf_name = original_savf_name

            if lib_name != 'QSYS':
                savf_path = f'/QSYS.LIB/{lib_name}.LIB/{original_savf_name}.FILE'
            else:
                savf_path = f'/QSYS.LIB/{original_savf_name}.FILE'
            i = 1
            while (self._execute_remote_stat(savf_path, all_vars=task_vars, follow=False))['exists']:
                if i > 9:
                    result['msg'] = f'SAVF names ({savf_path} range(1,9)) are already exist on IBMi. Failed'
                    result['failed'] = True
                    return result
                if len(original_savf_name + str(i)) <= 10:
                    if lib_name != 'QSYS':
                        savf_path = f'/QSYS.LIB/{lib_name}.LIB/{original_savf_name + str(i)}.FILE'
                    else:
                        savf_path = f'/QSYS.LIB/{original_savf_name + str(i)}.FILE'
                    savf_name = original_savf_name + str(i)
                else:
                    if lib_name != 'QSYS':
                        savf_path = f'/QSYS.LIB/{lib_name}.LIB/{original_savf_name[0:9] + str(i)}.FILE'
                    else:
                        savf_path = f'/QSYS.LIB/{original_savf_name[0:9] + str(i)}.FILE'
                    savf_name = original_savf_name[0:9] + str(i)
                i += 1
        else:
            savf_name = savefile_name
            if lib_name != 'QSYS':
                savf_path = f'/QSYS.LIB/{lib_name}.LIB/{savefile_name}.FILE'
            else:
                savf_path = f'/QSYS.LIB/{savefile_name}.FILE'
        return savf_name, savf_path

    def run(self, tmp=None, task_vars=None):

        display.debug("version: " + __ibmi_module_version__)
        ''' handler for fetch operations '''
        if task_vars is None:
            task_vars = {}

        result = super().run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        ifs_created = False
        try:
            result = dict(
                msg="",
                stderr="",
                stdout="",
                file="",
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
            savf_name = ''
            created = False
            is_savf = False
            savf = ''
            backup = False
            is_lib = False
            force_save = False
            flat = False
            if self._play_context.check_mode:
                result['skipped'] = True
                result['msg'] = 'check mode not (yet) supported for this module'
                return result

            object_names = self._task.args.get('object_names', '*ALL')
            lib_name = self._task.args.get('lib_name', None)
            object_types = self._task.args.get('object_types', '*ALL')
            is_lib = boolean(self._task.args.get('is_lib', False), strict=True)
            savefile_name = self._task.args.get('savefile_name', None)
            force_save = boolean(self._task.args.get('force_save', False), strict=True)
            backup = boolean(self._task.args.get('backup', False), strict=True)
            format = self._task.args.get('format', '*SAVF')
            target_release = self._task.args.get('target_release', '*CURRENT')
            dest = self._task.args.get('dest', None)
            flat = boolean(self._task.args.get('flat', False), strict=True)
            validate_checksum = boolean(self._task.args.get('validate_checksum', True), strict=True)

            # validate dest are strings FIXME: use basic.py and module specs
            if not isinstance(dest, string_types):
                result['msg'] = "Invalid type supplied for dest option, it must be a string. "

            if lib_name is None or dest is None:
                result['msg'] = "lib_name and dest are required. "

            object_names = object_names.upper()
            object_types = object_types.upper()
            format = format.upper()
            target_release = target_release.upper()

            if lib_name is not None:
                lib_name = lib_name.upper()

            if savefile_name is not None:
                savefile_name = savefile_name.upper()

            if lib_name == 'QSYS' and (is_lib is True or (object_names == '*ALL' and object_types == '*ALL')):
                result['msg'] = "QSYS can't be saved."

            if format != "*SAVF":
                result['msg'] = "format can only be *SAVF."

            if result.get('msg'):
                result['failed'] = True
                return result

            startd = datetime.datetime.now()

            if len(object_names.split()) == 1 and is_lib is not True:
                if object_types == '*ALL' or object_types == '*FILE':
                    if (object_names.split())[0][-1] == '*':
                        module_args = {'object_name': object_names[0:-1] + '+', 'lib_name': lib_name, 'use_regex': True}
                        module_output = self._execute_module(module_name='ibmi_object_find', module_args=module_args, task_vars=task_vars)
                        save_result = module_output
                        if not save_result.get('failed'):
                            if len(save_result['object_list']) == 1 and save_result['object_list'][0]['OBJTYPE'] == '*FILE' \
                               and save_result['object_list'][0]['OBJATTRIBUTE'] == 'SAVF':
                                result['msg'] += "Object is a save file, fetch it directly."
                                savf_path = self._calculate_savf_path(save_result['object_list'][0]['OBJNAME'], lib_name)
                                savf_name = save_result['object_list'][0]['OBJNAME']
                                is_savf = True
                    else:
                        module_args = {'object_name': object_names, 'lib_name': lib_name}
                        module_output = self._execute_module(module_name='ibmi_object_find', module_args=module_args, task_vars=task_vars)
                        save_result = module_output
                        if not save_result.get('failed'):
                            if len(save_result['object_list']) == 1 and save_result['object_list'][0]['OBJTYPE'] == '*FILE' and \
                               save_result['object_list'][0]['OBJATTRIBUTE'] == 'SAVF':
                                result['msg'] += "Object is a save file, fetch it directly."
                                savf_path = self._calculate_savf_path(object_names, lib_name)
                                savf_name = object_names
                                is_savf = True

                    if save_result.get('failed'):
                        result.update(save_result)
                        return result
            if is_savf is False:
                savf_name, savf_path = self._calculate_savf_name(object_names, lib_name, is_lib, savefile_name, task_vars,
                                                                 result)
                if is_lib is True:
                    omitfile = f'OMITOBJ(({lib_name}/{savf_name} *FILE))'
                    module_args = {'lib_name': lib_name, 'savefile_name': savf_name, 'savefile_lib': lib_name,
                                   'target_release': target_release, 'force_save': force_save, 'joblog': True,
                                   'parameters': omitfile}
                    display.debug(f"ibm i debug: call ibmi_lib_save {module_args}")
                    module_output = self._execute_module(module_name='ibmi_lib_save', module_args=module_args, task_vars=task_vars)
                else:
                    omitfile = f'OMITOBJ(({lib_name}/{savf_name} *FILE))'
                    module_args = {'object_names': object_names, 'object_lib': lib_name, 'object_types': object_types,
                                   'savefile_name': savf_name, 'savefile_lib': lib_name, 'target_release': target_release,
                                   'force_save': force_save, 'joblog': True, 'parameters': omitfile}
                    display.debug(f"ibm i debug: call ibmi_object_save {module_args}")
                    module_output = self._execute_module(module_name='ibmi_object_save', module_args=module_args, task_vars=task_vars)

                save_result = module_output
                rc = save_result['rc']
                if rc != 0 or ('CPC3708' in str(save_result['job_log'])):
                    result['msg'] = 'Create SAVF failed. See job_log.'
                    result['failed'] = True
                    result['stderr'] = save_result['stderr_lines']
                    result['stdout'] = save_result['stdout_lines']
                    result['job_log'] = save_result['job_log']
                    result['rc'] = save_result['rc']
                    return result
                created = True

            source = savf_path
            commandmk = f'mkdir {ifs_dir}'
            command = f'cp {savf_path} {ifs_dir}'

            module_output = self._execute_module(module_name='command', module_args={'_raw_params': commandmk}, task_vars=task_vars)
            save_result = module_output
            rc = save_result['rc']
            if rc != 0 and ('exists' not in save_result['stderr']):
                result['msg'] = save_result['msg']
                result['stderr'] = save_result['stderr_lines']
                result['rc'] = save_result['rc']
                result['failed'] = True
                return result
            module_output = self._execute_module(module_name='command', module_args={'_raw_params': command}, task_vars=task_vars)
            save_result = module_output
            rc = save_result['rc']
            if rc != 0:
                result['msg'] = save_result['msg']
                result['failed'] = True
                result['stderr'] = save_result['stderr_lines']
                result['stdout'] = save_result['stdout_lines']
                result['rc'] = save_result['rc']
                return result
            ifs_created = True

            source = f'{ifs_dir}/{os.path.basename(savf_path)}'
            if not isinstance(source, string_types):
                result['msg'] = "Invalid type supplied for source option, it must be a string"
                result['failed'] = True
                return result
            source = self._connection._shell.join_path(source)
            source = self._remote_expand_user(source)
            remote_stat = None
            remote_checksum = None
            if not self._connection.become:
                # calculate checksum for the remote file, don't bother if using become as slurp will be used
                # Force execute_remote_stat to follow symlinks because fetch always follows symlinks
                remote_stat = self._execute_remote_stat(source, all_vars=task_vars, follow=True)
                remote_checksum = remote_stat['checksum']

            # use slurp if permissions are lacking or another issue
            remote_data = None
            if remote_checksum in ('1', '', None):
                slurpres = self._execute_module(module_name='slurp', module_args=dict(src=source), task_vars=task_vars)
                if slurpres.get('failed'):
                    if (slurpres.get('msg').startswith('file not found') or remote_checksum == '1'):
                        result['msg'] = "the remote file does not exist, not transferring"
                        result['file'] = source
                        result['changed'] = False
                    else:
                        result.update(slurpres)
                    return result
                else:
                    if slurpres['encoding'] == 'base64':
                        remote_data = base64.b64decode(slurpres['content'])
                    if remote_data is not None:
                        remote_checksum = checksum_s(remote_data)
                    else:
                        # Unexpected error case
                        remote_checksum = None
                    # the source path may have been expanded on the
                    # target system, so we compare it here and use the
                    # expanded version if it's different
                    remote_source = slurpres.get('source')
                    if remote_source and remote_source != source:
                        source = remote_source

            # calculate the destination name
            if os.path.sep not in self._connection._shell.join_path('a', ''):
                source = self._connection._shell._unquote(source)
                qsys_source = self._connection._shell._unquote(savf_path)
                source_local = qsys_source.replace('\\', '/')
            else:
                source_local = savf_path

            dest = os.path.expanduser(dest)
            if flat:
                if not dest.startswith("/"):
                    # if dest does not start with "/", we'll assume a relative path
                    dest = self._loader.path_dwim(dest)
                base = os.path.basename(source_local)
                dest = os.path.join(dest, base)
            else:
                # files are saved in dest dir, with a subdir for each host, then the filename
                if 'inventory_hostname' in task_vars:
                    target_name = task_vars['inventory_hostname']
                else:
                    target_name = self._play_context.remote_addr
                dest = f"{self._loader.path_dwim(dest)}/{target_name}/{source_local}"

            dest = os.path.normpath(dest)
            if remote_checksum is None:
                result['changed'] = False
                result['file'] = source
                result['msg'] = "unexpected error: unable to calculate the checksum of the remote file"
                result['failed'] = True
                return result

            # calculate checksum for the local file
            local_checksum = checksum(dest)
            if remote_checksum != local_checksum:
                # create the containing directories, if needed
                makedirs_safe(os.path.dirname(dest))

                # fetch the file and check for changes
                display.debug(f"ibm i debug: fetch {source} {dest}")
                if remote_data is None:
                    self._connection.fetch_file(source, dest)
                else:
                    re_raise = False  # workaround to pass the raise-missing-from pylint issue
                    inst = None
                    try:
                        with open(to_bytes(dest, errors='surrogate_or_strict'), 'wb') as f:
                            f.write(remote_data)
                    except (IOError, OSError) as e:
                        re_raise = True
                        inst = e
                    if re_raise:
                        raise AnsibleError(f"Failed to fetch the file: {inst}")
                new_checksum = secure_hash(dest)
                # For backwards compatibility. We'll return None on FIPS enabled systems
                try:
                    new_md5 = md5(dest)
                except ValueError:
                    new_md5 = None

                if validate_checksum and new_checksum != remote_checksum:
                    result.update(dict(failed=True, md5sum=new_md5,
                                       msg="checksum mismatch", file=savf, dest=dest, remote_md5sum=None,
                                       checksum=new_checksum, remote_checksum=remote_checksum))
                else:
                    endd = datetime.datetime.now()
                    delta = endd - startd
                    if (created is True and backup is True) or is_savf is True:
                        savf = savf_path
                    result['msg'] += " File is renewed on local."
                    result.update({'changed': True, 'md5sum': new_md5, 'dest': dest,
                                   'remote_md5sum': None, 'checksum': new_checksum,
                                   'remote_checksum': remote_checksum, 'delta': str(delta), 'file': savf, 'rc': 0})
            else:
                # For backwards compatibility. We'll return None on FIPS enabled systems
                try:
                    local_md5 = md5(dest)
                except ValueError:
                    local_md5 = None
                endd = datetime.datetime.now()
                delta = endd - startd
                if (created is True and backup is True) or is_savf is True:
                    savf = savf_path
                result.update(dict(changed=False, md5sum=local_md5, file=savf, delta=str(delta), dest=dest,
                                   checksum=local_checksum, rc=0))

        except Exception as e:
            result['msg'] += f"{to_text(e)}"
            result['failed'] = True
            return result
        finally:
            if ((backup is False and is_savf is False) or result['failed'] is True) and created is True:
                cmd = f'QSYS/DLTOBJ OBJ({lib_name}/{savf_name}) OBJTYPE(*FILE)'
                module_output = self._execute_module(module_name='ibmi_cl_command', module_args={'cmd': cmd}, task_vars=task_vars)
                save_result = module_output
                rc = save_result['rc']
                if rc != 0 and ('CPF2105' not in save_result['stderr']):
                    result['msg'] += "Failed to delete SAVF on remote when cleanup."
            if ifs_created is True:
                cmd = f'rm {ifs_dir}/{os.path.basename(savf_path)}'
                try:
                    module_output = self._execute_module(module_name='command', module_args={'_raw_params': cmd}, task_vars=task_vars)
                    save_result = module_output
                    rc = save_result['rc']
                    if rc != 0:
                        result['msg'] += "Failed to delete IFS on remote when cleanup."
                except Exception as e:
                    result['msg'] += f"exception happens when delete IFS file. error: {to_text(e)}"

            self._remove_tmp_path(self._connection._shell.tmpdir)

        return result
