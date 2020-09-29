#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zengyu <pzypeng@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_object_save
short_description: Save one or more objects
version_added: '2.8.0'
description:
     - The C(ibmi_object_save) module create an save file on a remote IBM i nodes.
     - The saved objects and save file are on the remote host, and the save file is not copied to the local host.
     - Only support C(*SAVF) as the save file's format by now.
options:
  object_names:
    description:
      - The objects need to be saved.
        One or more object names can be specified. Use space as separator.
    type: str
    default: '*ALL'
  object_lib:
    description:
      - The library contains the objects.
    type: str
    required: yes
  object_types:
    description:
      - The object types.
        One or more object types can be specified. Use space as separator.
    type: str
    default: '*ALL'
  savefile_name:
    description:
      - The save file name.
    type: str
    required: yes
  savefile_lib:
    description:
      - The save file library.
    type: str
    required: yes
  format:
    description:
      - The save file's format. Only support C(*SAVF) by now.
    type: str
    default: '*SAVF'
    choices: ["*SAVF"]
  force_save:
    description:
      - If save file already exists or contains data, whether to clear data or not.
    type: bool
    default: False
  target_release:
    description:
      - The release of the operating system on which you intend to restore and use the object.
    type: str
    default: '*CURRENT'
  joblog:
    description:
      - If set to C(true), output the avaiable JOBLOG even the rc is 0(success).
    type: bool
    default: False
  asp_group:
     description:
       - Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.
       - The ASP group name is the name of the primary ASP device within the ASP group.
     type: str
     default: '*SYSBAS'
  parameters:
    description:
      - The parameters that SAVOBJ command will take. Other than options above, all other parameters need to be specified here.
        The default values of parameters for SAVOBJ will be taken if not specified.
    type: str
    default: ' '
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Force to save test1.pgm and test2.srvpgm in objlib libary to archive.savf in archlib libary with become user.
  ibmi_object_save:
    object_names: 'test1 test2'
    object_lib: 'objlib'
    object_types: '*PGM *SRVPGM'
    savefile_name: 'archive'
    savefile_lib: 'archlib'
    force_save: True
    target_release: 'V7R2M0'
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
start:
    description: The save execution start time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The save execution end time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The save execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The save standard output.
    returned: always
    type: str
    sample: 'CPC3722: 2 objects saved from library objlib.'
stderr:
    description: The save standard error.
    returned: always
    type: str
    sample: 'CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n'
object_names:
    description: The objects need to be saved.
    returned: always
    type: str
    sample: 'test1 test2'
object_lib:
    description: The library contains the object.
    returned: always
    type: str
    sample: 'objlib'
object_types:
    description: The object types.
    returned: always
    type: str
    sample: '*PGM *SRVPGM'
savefile_name:
    description: The save file name.
    returned: always
    type: str
    sample: 'c1'
savefile_lib:
    description: The save file library.
    returned: always
    type: str
    sample: 'c1lib'
format:
    description: The save file's format. Only support C(*SAVF) by now.
    returned: always
    type: str
    sample: '*SAVF'
force_save:
    description: If save file already exists or contains data, whether to clear data or not.
    returned: always
    type: bool
    sample: True
target_release:
    description: The release of the operating system on which you intend to restore and use the object.
    returned: always
    type: str
    sample: 'V7R1M0'
command:
    description: The last excuted command.
    returned: always
    type: str
    sample: 'SAVOBJ OBJ(*ALL) LIB(TESTLIB) DEV(*SAVF) OBJTYPE(*ALL) SAVF(TEST/ARCHLIB) TGTRLS(V7R1M0)'
joblog:
    description: Append JOBLOG to stderr/stderr_lines or not.
    returned: always
    type: bool
    sample: False
rc:
    description: The save action return code. 0 means success.
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The save standard output split in lines.
    returned: always
    type: list
    sample: [
        "CPC3722: 2 objects saved from library objlib."
    ]
stderr_lines:
    description: The save standard error split in lines.
    returned: always
    type: list
    sample: [
        "CPF5813: File archive in library archlib already exists.",
        "CPF7302: File archive not created in library archlib."
    ]
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "149",
            "FROM_LIBRARY": "QSHELL",
            "FROM_MODULE": "QZSHRUNC",
            "FROM_PROCEDURE": "main",
            "FROM_PROGRAM": "QZSHRUNC",
            "FROM_USER": "TESTER",
            "MESSAGE_FILE": "QZSHMSGF",
            "MESSAGE_ID": "QSH0005",
            "MESSAGE_LIBRARY": "QSHELL",
            "MESSAGE_SECOND_LEVEL_TEXT": "",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Command ended normally with exit status 0.",
            "MESSAGE_TIMESTAMP": "2020-05-25-13.06.35.019371",
            "MESSAGE_TYPE": "COMPLETION",
            "ORDINAL_POSITION": "12",
            "SEVERITY": "0",
            "TO_INSTRUCTION": "5829",
            "TO_LIBRARY": "QXMLSERV",
            "TO_MODULE": "PLUGILE",
            "TO_PROCEDURE": "ILECMDEXC",
            "TO_PROGRAM": "XMLSTOREDP"
        }]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            object_names=dict(type='str', default='*ALL'),
            object_lib=dict(type='str', required=True),
            object_types=dict(type='str', default='*ALL'),
            savefile_name=dict(type='str', required=True),
            savefile_lib=dict(type='str', required=True),
            format=dict(type='str', default='*SAVF', choices=['*SAVF']),
            force_save=dict(type='bool', default=False),
            target_release=dict(type='str', default='*CURRENT'),
            joblog=dict(type='bool', default=False),
            asp_group=dict(type='str', default='*SYSBAS'),
            parameters=dict(type='str', default=' '),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    try:
        object_names = module.params['object_names']
        object_lib = module.params['object_lib']
        object_types = module.params['object_types']
        savefile_name = module.params['savefile_name']
        savefile_lib = module.params['savefile_lib']
        format = module.params['format']
        force_save = module.params['force_save']
        target_release = module.params['target_release']
        joblog = module.params['joblog']
        asp_group = module.params['asp_group'].strip().upper()
        parameters = module.params['parameters']
        become_user = module.params['become_user']
        become_user_password = module.params['become_user_password']

        startd = datetime.datetime.now()

        try:
            ibmi_module = imodule.IBMiModule(
                db_name=asp_group, become_user_name=become_user, become_user_password=become_user_password)
        except Exception as inst:
            message = 'Exception occurred: {0}'.format(str(inst))
            module.fail_json(rc=999, msg=message)

        # crtsavf
        command = 'QSYS/CRTSAVF FILE({p_savefile_lib}/{p_savefile_name})'.format(
            p_savefile_lib=savefile_lib,
            p_savefile_name=savefile_name)
        rc, out, error = ibmi_module.itoolkit_run_command(command)
        job_log = ibmi_module.itoolkit_get_job_log(startd)
        ibmi_util.log_debug("CRTSAVF: " + command, module._name)
        if rc == ibmi_util.IBMi_COMMAND_RC_SUCCESS:
            # SAVOBJ
            command = 'QSYS/SAVOBJ OBJ({p_object_names}) LIB({p_object_lib}) DEV({p_format}) OBJTYPE({p_object_types}) \
                SAVF({p_savefile_lib}/{p_savefile_name}) TGTRLS({p_target_release}) {p_parameters}'.format(
                p_object_names=object_names,
                p_object_lib=object_lib,
                p_format=format,
                p_object_types=object_types,
                p_savefile_lib=savefile_lib,
                p_savefile_name=savefile_name,
                p_target_release=target_release,
                p_parameters=parameters)
            rc, out, error = ibmi_module.itoolkit_run_command(' '.join(command.split()))
        else:
            if 'CPF5813' in str(job_log):
                ibmi_util.log_debug("SAVF " + savefile_name + " already exists", module._name)
                if force_save is True:
                    # CLRSAVF
                    command = 'QSYS/CLRSAVF FILE({p_savefile_lib}/{p_savefile_name})'.format(
                        p_savefile_lib=savefile_lib,
                        p_savefile_name=savefile_name)
                    rc, out, error = ibmi_module.itoolkit_run_command(command)
                    ibmi_util.log_debug("CLRSAVF: " + command, module._name)
                    if rc == ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                        command = 'QSYS/SAVOBJ OBJ({p_object_names}) LIB({p_object_lib}) DEV({p_format}) OBJTYPE({p_object_types}) \
                            SAVF({p_savefile_lib}/{p_savefile_name}) TGTRLS({p_target_release}) {p_parameters}'.format(
                            p_object_names=object_names,
                            p_object_lib=object_lib,
                            p_format=format,
                            p_object_types=object_types,
                            p_savefile_lib=savefile_lib,
                            p_savefile_name=savefile_name,
                            p_target_release=target_release,
                            p_parameters=parameters)
                        rc, out, error = ibmi_module.itoolkit_run_command(' '.join(command.split()))
                else:
                    out = 'File {p_savefile_name} in library {p_savefile_lib} already exists. Set force_save to force save.'.format(
                        p_savefile_name=savefile_name,
                        p_savefile_lib=savefile_lib)

        endd = datetime.datetime.now()
        delta = endd - startd
        job_log = ibmi_module.itoolkit_get_job_log(startd)
        result = dict(
            object_names=object_names,
            object_lib=object_lib,
            object_types=object_types,
            savefile_name=savefile_name,
            savefile_lib=savefile_lib,
            joblog=joblog,
            format=format,
            force_save=force_save,
            target_release=target_release,
            command=' '.join(command.split()),
            job_log=job_log if joblog or rc else [],
            stdout=out,
            stderr=error,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
        )

        if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
            module.fail_json(msg='non-zero return code', **result)

        module.exit_json(**result)
    except Exception as e:
        module.fail_json(rc=ibmi_util.IBMi_COMMAND_RC_UNEXPECTED, msg=str(e))


if __name__ == '__main__':
    main()
