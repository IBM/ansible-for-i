#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Chang Le <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
module: ibmi_start_subsystem
short_description: Start an inactive subsystem
version_added: '2.8.0'
description:
    - the C(ibmi_start_subsystem) module start an inactive subsystem.
options:
  subsystem:
    description:
      - The name of the subsystem description.
    type: str
    required: yes
  library:
    description:
      - Specify the library where the subsystem description is located.
    type: str
    default: '*LIBL'
  joblog:
    description:
      - If set to C(true), output the avaiable job log even the rc is 0(success).
    type: bool
    default: False
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str
seealso:
- module: ibmi_end_subsystem
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Start the subsystem QBATCH.
  ibmi_start_subsystem:
    subsystem: QBATCH

- name: Start a user defined subsystem, which the subsystem description is MYSBS, located at library MYLIB.
  ibmi_start_subsystem:
    subsystem: MYSBS
    library: MYLIB
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
stdout:
    description: The standard output of the start subsystem command.
    type: str
    sample: 'CPF0902: Subsystem QBATCH in library QSYS being started.'
    returned: always
stderr:
    description: The standard error the start subsystem command.
    type: str
    sample: 'CPF1010: Subsystem name QBATCH active.'
    returned: always
rc:
    description: The task return code (0 means success, non-zero means failure).
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines.
    type: list
    sample: [
        "CPF0902: Subsystem QINTER in library QSYS being started."
    ]
    returned: always
stderr_lines:
    description: The standard error split in lines.
    type: list
    sample: [
        "CPF1080: Library MYLIB not found."
    ]
    returned: always
job_log:
    description: The IBM i job log of the task executed.
    type: list
    sample: [{
            "FROM_INSTRUCTION": "318F",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "",
            "FROM_PROCEDURE": "",
            "FROM_PROGRAM": "QWTCHGJB",
            "FROM_USER": "CHANGLE",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPD0912",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Printer device PRT01 not found.",
            "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897",
            "MESSAGE_TYPE": "DIAGNOSTIC",
            "ORDINAL_POSITION": "5",
            "SEVERITY": "20",
            "TO_INSTRUCTION": "9369",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
        }]
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            subsystem=dict(type='str', required=True),
            library=dict(type='str', default='*LIBL'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    subsystem = module.params['subsystem'].strip().upper()
    library = module.params['library'].strip().upper()
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if len(subsystem) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of subsystem exceeds 10 characters")
    if len(library) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of library exceeds 10 characters")
    command = 'QSYS/STRSBS SBSD({library}/{subsystem})'.format(library=library, subsystem=subsystem)

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)

    result = dict(
        command=command,
        stdout=out,
        stderr=err,
        rc=rc,
        job_log=job_log,
        changed=True,
    )

    if rc != 0:
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
