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
module: ibmi_install_product_from_savf
short_description: Install the the licensed program(product) from a save file
description:
    - the C(ibmi_install_product_from_savf) module install the product from a save file on the target ibmi node.
version_added: "1.1"
options:
  product:
    description:
      - Specifies the seven-character identifier of the licensed program that is restored
    type: str
    required: yes
  option:
    description:
      - Specifies which one of the optional parts of the licensed program given in the Product prompt (LICPGM parameter) is to be restored
    type: str
    default: '*BASE'
  object_type:
    description:
      - Specifies the type of licensed program objects to be restored
    type: str
    default: '*ALL'
    choices: ['*ALL', '*PGM', '*LNG']
  language:
    description:
      - Specifies which national language version (NLV) objects to be used for restoring the licensed program
      - It's the IBM-supplied language feature codes, like German is 2924, English is 2924
    type: str
    default: '*PRIMARY'
  release:
    description:
      - Specifies the version, release, and modification level of the licensed program being restored
    type: str
    default: '*FIRST'
  replace_release:
    description:
      - Specifies the version, release, and modification level of the licensed program being replaced
    type: str
    default: '*ONLY'
  savf_name:
    description:
      - Specify the name of the save file
    type: str
    required: yes
  savf_library:
    description:
      - Specify the name of the library where the save file is located
    type: str
    required: yes
  parameters:
    description:
      - The parameters that RSTLICPGM command will take. Other than options above, all other parameters need to be specified here.
        The default values of parameters for RSTLICPGM will be taken if not specified.
    type: str
    default: ' '
  acceptance_cmd:
    description:
      - The Accept Software Agreement command records the acceptance of the software agreement for a product
      - It is assumed that the caller of this command has previously displayed and obtained acceptance for the terms of the agreement
      - This command cannot be used to accept the Licensed Internal Code or the IBM® i *Base software agreements
      - If invalid command specificed, message CPDB6D5 with following reason will be received,
      - 'Product cannot be installed in a batch request because the software agreement has not been previously accepted'
      - In general, a command or program should be implemented by QLPACAGR API, consult the product support if you don't know the command
    type: str
    default: ' '
seealso:
- module: ibmi_uninstall_product, ibmi_save_product_to_savf
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Restoring Program Using Defaults
  ibmi_install_product_from_savf:
    product: 5770WDS
    savf_name: MYFILE
    savf_library: MYLIB

- name: Restoring Program with acceptance command
  ibmi_install_product_from_savf:
    product: 5733D10
    option: 11
    savf_name: MYFILE
    savf_library: MYLIB
    acceptance_cmd: "CALL PGM(QSYS/QLPACAGR) PARM('5733D10' '100001' '0011' X'00000010000000000000000000000000')"
'''

RETURN = r'''
stdout:
    description: The standard output
    type: str
    sample: "+++ success RSTLICPGM LICPGM(5733D10) DEV(*SAVF) OPTION(*BASE) RSTOBJ(*ALL)"
    returned: When rc as 0(success)
stderr:
    description: The standard error
    type: str
    sample: 'CPF9801: Object QNOTE in library L10010125P not found'
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
        "+++ success RSTLICPGM LICPGM(5733D10) DEV(*SAVF) OPTION(*BASE) RSTOBJ(*ALL)"
    ]
    returned: When rc as 0(success)
stderr_lines:
    description: The standard error split in lines
    type: list
    sample: [
        "CPF9801: Object QNOTE in library L10010125P not found"
    ]
    returned: When rc as non-zero(failure)
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
            option=dict(type='str', default='*BASE'),
            object_type=dict(type='str', default='*ALL', choices=['*ALL', '*PGM', '*LNG']),
            language=dict(type='str', default='*PRIMARY'),
            release=dict(type='str', default='*FIRST'),
            replace_release=dict(type='str', default='*ONLY'),
            savf_name=dict(type='str', required=True),
            savf_library=dict(type='str', required=True),
            parameters=dict(type='str', default=' '),
            acceptance_cmd=dict(type='str', default=' '),
        ),
        supports_check_mode=True,
    )

    product = module.params['product'].upper()
    option = module.params['option'].upper()
    object_type = module.params['object_type'].upper()
    language = module.params['language'].upper()
    release = module.params['release'].upper()
    replace_release = module.params['replace_release'].upper()
    savf_name = module.params['savf_name'].upper()
    savf_library = module.params['savf_library'].upper()
    parameters = module.params['parameters'].upper()
    acceptance_cmd = module.params['acceptance_cmd'].upper()

    if len(product) > 7:
        module.fail_json(rc=256, msg="Value of product exceeds 7 characters")
    if len(option) > 5:
        module.fail_json(rc=256, msg="Value of option exceeds 5 characters")
    if len(release) > 6:
        module.fail_json(rc=256, msg="Value of release exceeds 6 characters")
    if len(replace_release) > 6:
        module.fail_json(rc=256, msg="Value of replace_release exceeds 6 characters")
    if len(language) > 8:
        module.fail_json(rc=256, msg="Value of language exceeds 8 characters")
    if len(savf_name) > 10:
        module.fail_json(rc=256, msg="Value of savf_name exceeds 10 characters")
    if len(savf_library) > 10:
        module.fail_json(rc=256, msg="Value of savf_library exceeds 10 characters")

    chkobj_cmd = 'QSYS/CHKOBJ OBJ({pattern_savf_library}/{pattern_savf_name}) OBJTYPE(*FILE)'.format(
        pattern_savf_name=savf_name.strip(),
        pattern_savf_library=savf_library.strip())
    # Check to see if the savf is existed
    args = ['system', chkobj_cmd]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc != 0:
        result = dict(
            stderr=err,
            rc=rc,
        )
        module.fail_json(msg="File {pattern_savf_name} in library {pattern_savf_library} not found".format(
            pattern_savf_name=savf_name.strip(),
            pattern_savf_library=savf_library.strip()), **result)

    # Call the The Accept Software Agreement command
    args = ['system', acceptance_cmd]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc != 0:
        result = dict(
            stderr=err,
            rc=rc,
        )
        module.fail_json(msg="The Accept Software Agreement command {acceptance_cmd} failed".format(
            acceptance_cmd=acceptance_cmd), **result)

    # run the RSTLICPGM command to install the product
    command = 'QSYS/RSTLICPGM LICPGM({pattern_product}) DEV(*SAVF) OPTION({pattern_option}) RSTOBJ({pattern_object_type}) \
        LNG({pattern_language}) RLS({pattern_release}) REPLACERLS({pattern_replace_release}) \
        SAVF({pattern_savf_library}/{pattern_savf_name}) {pattern_parameters}'.format(
        pattern_product=product,
        pattern_option=option,
        pattern_object_type=object_type,
        pattern_language=language,
        pattern_release=release,
        pattern_replace_release=replace_release,
        pattern_savf_library=savf_library.strip(),
        pattern_savf_name=savf_name.strip(),
        pattern_parameters=parameters)

    if HAS_ITOOLKIT is False:
        module.fail_json(rc=999, msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(rc=999, msg="ibm_db package is required")

    rc, out, err = itoolkit_run_command(command)

    if rc != 0:
        result = dict(
            command=command,
            stderr=err,
            rc=rc,
        )
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    result = dict(
        command=command,
        stdout=out,
        rc=rc,
        changed=True,
    )

    module.exit_json(**result)


if __name__ == '__main__':
    main()
