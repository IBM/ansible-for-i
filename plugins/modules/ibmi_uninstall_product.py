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
module: ibmi_uninstall_product
short_description: Delete the objects that make up the licensed program(product)
version_added: '2.8.0'
description:
    - the C(ibmi_uninstall_product) module deletes the objects that make up the product.
options:
  product:
    description:
      - Specifies the seven-character identifier of the licensed program that is deleted.
    type: str
    required: yes
  option:
    description:
      - Specifies which of the parts of the licensed program specified on the Product prompt (LICPGM parameter) are deleted.
    type: str
    default: '*ALL'
  release:
    description:
      - Specifies which version, release, and modification level of the licensed program is deleted.
    type: str
    default: '*ONLY'
  language:
    description:
      - Specifies which national language version (NLV) objects are deleted for the licensed program specified on the LICPGM parameter.
      - It's the IBM-supplied language feature codes, like German is 2924, English is 2924.
    type: str
    default: '*ALL'
  joblog:
    description:
      - If set to C(true), output the avaiable JOBLOG even the rc is 0(success).
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
- module: ibmi_install_product_from_savf, ibmi_save_product_to_savf
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Deleting all Licensed Program Objects, run as USER1.
  ibmi_uninstall_product:
    product: 5770QU1
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: Deleting only the German (NLV 2929) objects for all options of the licensed program 5770QU1.
  ibmi_uninstall_product:
    product: 5770QU1
    language: 2929
'''

RETURN = r'''
stdout:
    description: The standard output.
    type: str
    sample: 'Product 5733D10 option 11 release *ONLY language *ALL deleted.'
    returned: always
stderr:
    description: The standard error
    type: str
    sample: 'Product 5733D10 option *ALL release *ONLY language *ALL not installed'
    returned: When rc as non-zero(failure)
rc:
    description: The task return code (0 means success, non-zero means failure).
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines.
    type: list
    sample: [
        "Product 5733D10 option 11 release *ONLY language *ALL deleted."
    ]
    returned: always
stderr_lines:
    description: The standard error split in lines.
    type: list
    sample: [
        "Product 5733D10 option *ALL release *ONLY language *ALL not installed"
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
            product=dict(type='str', required=True),
            option=dict(type='str', default='*ALL'),
            release=dict(type='str', default='*ONLY'),
            language=dict(type='str', default='*ALL'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    product = module.params['product'].upper()
    option = module.params['option'].upper()
    release = module.params['release'].upper()
    language = module.params['language'].upper()
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if len(product) > 7:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of product exceeds 7 characters")
    if len(option) > 4:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of option exceeds 4 characters")
    if len(release) > 6:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of release exceeds 6 characters")
    if len(language) > 4:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of language exceeds 4 characters")

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    command = 'QSYS/DLTLICPGM LICPGM({pattern_product}) \
      OPTION({pattern_option}) RLS({pattern_release}) LNG({pattern_language})'.format(
        pattern_product=product,
        pattern_option=option,
        pattern_release=release,
        pattern_language=language)

    command = ' '.join(command.split())  # keep only one space between adjacent strings
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
