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
module: ibmi_install_product_from_savf
short_description: Install the licensed program(product) from a save file.
version_added: '2.8.0'
description:
    - The C(ibmi_install_product_from_savf) module installs the product from a save file.
options:
  product:
    description:
      - Specifies the seven-character identifier of the licensed program that is restored.
    type: str
    required: yes
  option:
    description:
      - Specifies which one of the optional parts of the licensed program given in the Product prompt (LICPGM parameter) is to be restored.
    type: str
    default: '*BASE'
  object_type:
    description:
      - Specifies the type of licensed program objects to be restored.
    type: str
    default: '*ALL'
    choices: ['*ALL', '*PGM', '*LNG']
  language:
    description:
      - Specifies which national language version (NLV) objects to be used for restoring the licensed program.
        It's the IBM-supplied language feature codes, like German is 2924, English is 2924.
    type: str
    default: '*PRIMARY'
  release:
    description:
      - Specifies the version, release, and modification level of the licensed program being restored.
    type: str
    default: '*FIRST'
  replace_release:
    description:
      - Specifies the version, release, and modification level of the licensed program being replaced.
    type: str
    default: '*ONLY'
  savf_name:
    description:
      - Specify the name of the save file.
    type: str
    required: yes
  savf_library:
    description:
      - Specify the name of the library where the save file is located.
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
      - The Accept Software Agreement command records the acceptance of the software agreement for a product.
        It is assumed that the caller of this command has previously displayed and obtained acceptance for the terms of the agreement.
        This command cannot be used to accept the Licensed Internal Code or the IBM i C(*Base) software agreements.
        If invalid command specificed, message CPDB6D5 with following reason will be received,
        'Product cannot be installed in a batch request because the software agreement has not been previously accepted'.
        In general, a command or program should be implemented by QLPACAGR API, consult the product support if you don't know the command.
    type: str
    default: ' '
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
- module: ibmi_uninstall_product, ibmi_save_product_to_savf
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: Restoring Program with become user.
  ibmi_install_product_from_savf:
    product: 5770WDS
    savf_name: MYFILE
    savf_library: MYLIB
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: Restoring Program with acceptance command.
  ibmi_install_product_from_savf:
    product: 5733D10
    option: 11
    savf_name: MYFILE
    savf_library: MYLIB
    acceptance_cmd: "CALL PGM(QSYS/QLPACAGR) PARM('5733D10' '100001' '0011' X'00000010000000000000000000000000')"
'''

RETURN = r'''
stdout:
    description: The standard output.
    type: str
    sample: "+++ success RSTLICPGM LICPGM(5733D10) DEV(*SAVF) OPTION(*BASE) RSTOBJ(*ALL)"
    returned: When rc as 0(success)
stderr:
    description: The standard error.
    type: str
    sample: 'CPF9801: Object QNOTE in library L10010125P not found'
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
        "+++ success RSTLICPGM LICPGM(5733D10) DEV(*SAVF) OPTION(*BASE) RSTOBJ(*ALL)"
    ]
    returned: When rc as 0(success)
stderr_lines:
    description: The standard error split in lines.
    type: list
    sample: [
        "CPF9801: Object QNOTE in library L10010125P not found"
    ]
    returned: When rc as non-zero(failure).
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
            option=dict(type='str', default='*BASE'),
            object_type=dict(type='str', default='*ALL', choices=['*ALL', '*PGM', '*LNG']),
            language=dict(type='str', default='*PRIMARY'),
            release=dict(type='str', default='*FIRST'),
            replace_release=dict(type='str', default='*ONLY'),
            savf_name=dict(type='str', required=True),
            savf_library=dict(type='str', required=True),
            parameters=dict(type='str', default=' '),
            acceptance_cmd=dict(type='str', default=' '),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

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
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if len(product) > 7:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of product exceeds 7 characters")
    if len(option) > 5:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of option exceeds 5 characters")
    if len(release) > 6:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of release exceeds 6 characters")
    if len(replace_release) > 6:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of replace_release exceeds 6 characters")
    if len(language) > 8:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of language exceeds 8 characters")
    if len(savf_name) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of savf_name exceeds 10 characters")
    if len(savf_library) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of savf_library exceeds 10 characters")

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    command = 'QSYS/CHKOBJ OBJ({pattern_savf_library}/{pattern_savf_name}) OBJTYPE(*FILE)'.format(
        pattern_savf_name=savf_name.strip(),
        pattern_savf_library=savf_library.strip())
    # Check to see if the savf is existed
    ibmi_util.log_info("Command to run: " + command, module._name)
    rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)
    if rc != 0:
        result = dict(
            command=command,
            stderr=err,
            rc=rc,
            job_log=job_log,
        )
        module.fail_json(msg="File {pattern_savf_name} in library {pattern_savf_library} not found".format(
            pattern_savf_name=savf_name.strip(),
            pattern_savf_library=savf_library.strip()), **result)

    # Call the The Accept Software Agreement command
    if acceptance_cmd.strip():
        command = acceptance_cmd.strip()
        ibmi_util.log_info("Acceptance command to run: " + command, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)
        if rc != 0:
            result = dict(
                command=command,
                stderr=err,
                rc=rc,
                job_log=job_log,
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

    command = ' '.join(command.split())  # keep only one space between adjacent strings
    rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)

    if rc:
        result = dict(
            command=command,
            stderr=err,
            rc=rc,
            job_log=job_log,
        )
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    result = dict(
        command=command,
        stdout=out,
        rc=rc,
        job_log=job_log,
        changed=True,
    )

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
