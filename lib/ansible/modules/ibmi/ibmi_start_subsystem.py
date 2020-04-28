#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
module: ibmi_start_subsystem
short_description: start a subsystem
description:
    - the C(ibmi_start_subsystem) module start a subsystem of the target ibmi node.
version_added: "1.1"
options:
  subsystem:
    description:
      - The name of the subsystem description
    type: str
    required: yes
  library:
    description:
      - Specify the library where the subsystem description is located
    type: str
    default: '*LIBL'
seealso:
- module: ibmi_end_subsystem
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Start the subsystem QBATCH
  ibmi_start_subsystem:
    subsystem: QBATCH

- name: Start a user defined subsystem, which the subsystem description is MYSBS, located at library MYLIB
  ibmi_start_subsystem:
    subsystem: MYSBS
    library: MYLIB
'''

RETURN = r'''
stdout:
    description: The standard output of the start subsystem command
    type: str
    sample: 'CPF0902: Subsystem QBATCH in library QSYS being started.'
    returned: always
stderr:
    description: The standard error the start subsystem command
    type: str
    sample: 'CPF1010: Subsystem name QBATCH active.'
    returned: always
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines
    type: list
    sample: [
        "CPF0902: Subsystem QINTER in library QSYS being started."
    ]
    returned: always
stderr_lines:
    description: The standard error split in lines
    type: list
    sample: [
        "CPF1080: Library MYLIB not found."
    ]
    returned: always
'''

import datetime
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            subsystem=dict(type='str', required=True),
            library=dict(type='str', default='*LIBL'),
        ),
        supports_check_mode=True,
    )

    subsystem = module.params['subsystem']
    library = module.params['library']
    if len(subsystem) > 10:
        module.fail_json(rc=256, msg="Value of subsystem exceeds 10 characters")
    if len(library) > 10:
        module.fail_json(rc=256, msg="Value of library exceeds 10 characters")
    command = 'QSYS/STRSBS SBSD({library}/{subsystem})'.format(library=library, subsystem=subsystem)
    args = ['system', command]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)

    result = dict(
        command=command,
        stdout=out,
        stderr=err,
        rc=rc,
        changed=True,
    )

    if rc != 0:
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
