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
module: ibmi_object_restore
short_description: Restore one or more objects
version_added: '2.8.0'
description:
     - The C(ibmi_object_restore) module restore an save file on a remote IBM i nodes
     - The restored objects and save file are on the remote host.
     - Only support C(*SAVF) as the save file's format by now.
options:
  object_names:
    description:
      - The objects need to be restored.
      - One or more object names can be specified. Use space as separator.
    type: str
    default: '*ALL'
  object_lib:
    description:
      - The library that contains the saved objects.
    type: str
    required: yes
  object_types:
    description:
      - The object types.
      - One or more object types can be specified. Use space as separator.
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
      - The parameters that RSTOBJ command will take. Other than options above, all other parameters need to be specified here.
        The default values of parameters for RSTOBJ will be taken if not specified.
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
- name: Restore test1.pgm test2.srvpgm in savedlib libary from archive.savf in archlib libary with become user.
  ibmi_object_restore:
    object_names: 'test1 test2'
    object_lib: 'savedlib'
    object_types: '*PGM *SRVPGM'
    savefile_name: 'archive'
    savefile_lib: 'archlib'
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
start:
    description: The restore execution start time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The restore execution end time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The restore execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The restore standard output.
    returned: always
    type: str
    sample: 'CPC3703: 2 objects restored from C1 to C1.'
stderr:
    description: The restore standard error.
    returned: always
    type: str
    sample: 'CPF9812: File file1 in library C1 not found..\'
object_names:
    description: The objects need to be restored.
    returned: always
    type: str
    sample: 'test1 test2'
object_lib:
    description: The library that contains the saved objects.
    returned: always
    type: str
    sample: 'objectlib'
object_types:
    description: The objects types.
    returned: always
    type: str
    sample: '*PGM *SRVPGM'
savefile_name:
    description: The save file name.
    returned: always
    type: str
    sample: c1
savefile_lib:
    description: The save file library.
    returned: always
    type: str
    sample: c1lib
format:
    description: The save file's format. Only support C(*SAVF) by now.
    returned: always
    type: str
    sample: '*SAVF'
command:
    description: The last excuted command.
    returned: always
    type: str
    sample: 'RSTOBJ OBJ(OBJA) SAVLIB(TESTLIB) DEV(*SAVF) OBJTYPE(*ALL) SAVF(TEST/ARCHLIB)'
joblog:
    description: Append JOBLOG to stderr/stderr_lines or not.
    returned: always
    type: bool
    sample: False
rc:
    description: The restore action return code. 0 means success.
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The restore standard output split in lines.
    returned: always
    type: list
    sample: [
        "CPC3703: 2 objects restored from C1 to C1."
    ]
stderr_lines:
    description: The restore standard error split in lines.
    returned: always
    type: list
    sample: [
        "CPF9812: File file1 in library C1 not found."
    ]
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "8873",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "QSQSRVR",
            "FROM_PROCEDURE": "QSQSRVR",
            "FROM_PROGRAM": "QSQSRVR",
            "FROM_USER": "TESTER",
            "MESSAGE_FILE": "",
            "MESSAGE_ID": "",
            "MESSAGE_LIBRARY": "",
            "MESSAGE_SECOND_LEVEL_TEXT": "",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "User Profile = TESTER",
            "MESSAGE_TIMESTAMP": "2020-05-25-13.09.36.988652",
            "MESSAGE_TYPE": "COMPLETION",
            "ORDINAL_POSITION": "8",
            "SEVERITY": "0",
            "TO_INSTRUCTION": "8873",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
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
            joblog=dict(type='bool', default=False),
            asp_group=dict(type='str', default='*SYSBAS'),
            parameters=dict(type='str', default=' '),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    object_names = module.params['object_names']
    object_lib = module.params['object_lib']
    object_types = module.params['object_types']
    savefile_name = module.params['savefile_name']
    savefile_lib = module.params['savefile_lib']
    format = module.params['format']
    joblog = module.params['joblog']
    asp_group = module.params['asp_group'].strip().upper()
    parameters = module.params['parameters']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()
    # crtsavf
    command = 'QSYS/RSTOBJ OBJ({p_object_names}) SAVLIB({p_object_lib}) DEV({p_format}) OBJTYPE({p_object_types}) \
        SAVF({p_savefile_lib}/{p_savefile_name}) {p_parameters}'.format(
        p_object_names=object_names,
        p_object_lib=object_lib,
        p_format=format,
        p_object_types=object_types,
        p_savefile_lib=savefile_lib,
        p_savefile_name=savefile_name,
        p_parameters=parameters)
    try:
        ibmi_module = imodule.IBMiModule(
            db_name=asp_group, become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    rc, out, error, job_log = ibmi_module.itoolkit_run_command_once(' '.join(command.split()))
    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        object_names=object_names,
        object_lib=object_lib,
        object_types=object_types,
        savefile_name=savefile_name,
        savefile_lib=savefile_lib,
        joblog=joblog,
        format=format,
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


if __name__ == '__main__':
    main()
