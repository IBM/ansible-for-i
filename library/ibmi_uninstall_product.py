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
module: ibmi_uninstall_product
short_description: delete the objects that make up the licensed program(product)
description:
    - the C(ibmi_uninstall_product) module delete the objects that make up the product on the target ibmi node.
version_added: "1.1"
options:
  product:
    description:
      - Specifies the seven-character identifier of the licensed program that is deleted
    type: str
    required: yes
  option:
    description:
      - Specifies which of the parts of the licensed program specified on the Product prompt (LICPGM parameter) are deleted
    type: str
    default: '*ALL'
  release:
    description:
      - Specifies which version, release, and modification level of the licensed program is deleted
    type: str
    default: '*ONLY'
  language:
    description:
      - Specifies which national language version (NLV) objects are deleted for the licensed program specified on the LICPGM parameter
      - It's the IBM-supplied language feature codes, like German is 2924, English is 2924
    type: str
    default: '*ALL'
seealso:
- module: ibmi_install_product_from_savf, ibmi_save_product_to_savf
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Deleting all Licensed Program Objects
  ibmi_uninstall_product:
    product: 5770QU1

- name: Deleting only the German (NLV 2929) objects for all options of the licensed program 5770QU1
  ibmi_uninstall_product:
    product: 5770QU1
    language: 2929
'''

RETURN = r'''
stdout:
    description: The standard output
    type: str
    sample: 'Product 5733D10 option 11 release *ONLY language *ALL deleted.'
    returned: always
stderr:
    description: The standard error
    type: str
    sample: 'Product 5733D10 option *ALL release *ONLY language *ALL not installed'
    returned: When rc as non-zero(failure)
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    sample: 255
    returned: always
stdout_lines:
    description: The standard output split in lines
    type: list
    sample: [
        "Product 5733D10 option 11 release *ONLY language *ALL deleted."
    ]
    returned: always
stderr_lines:
    description: The standard error split in lines
    type: list
    sample: [
        "Product 5733D10 option *ALL release *ONLY language *ALL not installed"
    ]
    returned: always
'''

import datetime
from ansible.module_utils.basic import AnsibleModule

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iCmd
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257


def itoolkit_run_command(command):
    conn = dbi.connect()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(iCmd('command', command, {'error': 'on'}))
    itool.call(itransport)

    out = ''
    err = ''

    command_output = itool.dict_out('command')

    if 'success' in command_output:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['success']
    elif 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    else:
        # should not be here, must xmlservice has internal error
        rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
        err = "iToolKit result dict does not have key 'error', the output is %s" % command_output

    return rc, out, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            product=dict(type='str', required=True),
            option=dict(type='str', default='*ALL'),
            release=dict(type='str', default='*ONLY'),
            language=dict(type='str', default='*ALL'),
        ),
        supports_check_mode=True,
    )

    product = module.params['product'].upper()
    option = module.params['option'].upper()
    release = module.params['release'].upper()
    language = module.params['language'].upper()

    if len(product) > 7:
        module.fail_json(rc=256, msg="Value of product exceeds 7 characters")
    if len(option) > 4:
        module.fail_json(rc=256, msg="Value of option exceeds 4 characters")
    if len(release) > 6:
        module.fail_json(rc=256, msg="Value of release exceeds 6 characters")
    if len(language) > 4:
        module.fail_json(rc=256, msg="Value of language exceeds 4 characters")

    command = 'QSYS/DLTLICPGM LICPGM({pattern_product}) \
      OPTION({pattern_option}) RLS({pattern_release}) LNG({pattern_language})'.format(
        pattern_product=product,
        pattern_option=option,
        pattern_release=release,
        pattern_language=language)

    if HAS_ITOOLKIT is False:
        module.fail_json(rc=999, msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(rc=999, msg="ibm_db package is required")

    rc, out, err = itoolkit_run_command(command)

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
