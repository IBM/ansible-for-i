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
---
module: ibmi_rtv_command
short_description: Executes a command which is valid only within a CL program or REXX procedure
version_added: '2.8.0'
description:
  - The C(ibmi_rtv_command) module executes command which used in a CL program or REXX procedure.
  - Usually, this kind of commands can not run directly from the 5250 console, like RTVJOBA, RTVNETA.
options:
  cmd:
    description:
      - The RTV command to run.
    type: str
    required: yes
  char_vars:
    description:
      - Specifies the name of the CL variable that receives character value.
        In the command's help, indicated as Character value.
    type: list
    elements: str
  number_vars:
    description:
      - Specifies the name of the CL variable that receives digit value.
        In the command's help, indicated as Number.
    type: list
    elements: str
  joblog:
    description:
      - If set to C(true), output the avaiable job log even the rc is 0(success).
      - Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL, DSPHDWRSC.
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

notes:
    - The vars name and type for the rtv command must be correctly.
    - F1 or F4 in 5250 console can help determine the vars name and type.
    - Or check it with the command's url in Knowledge Center,
      e.g. RTVJOBA refers to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/rtvjoba.htm

seealso:
- module: ibmi_cl_command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Call RTVJOBA to get job information
  ibmi_rtv_command:
    cmd: 'RTVJOBA'
    char_vars:
      - 'JOB'
      - 'USER'
    number_vars:
      - 'LOGSEV'
      - 'JOBMSGQMX'

- name: Call RTVAUTLE to get information of the authority list
  ibmi_rtv_command:
    cmd: 'RTVAUTLE AUTL(PAYROLL) USER(TOM)'
    char_vars:
      - 'USE'
      - 'OBJOPR'
      - 'AUTLMGT'

- name: Call RTVDTAARA to get content of a data area
  ibmi_rtv_command:
    cmd: 'RTVDTAARA DTAARA(QSYS/QAENGWTTM)'
    char_vars:
      - 'RTNVAR'
'''

RETURN = r'''
msg:
    description: The result message of the rtv command.
    returned: always
    type: str
    sample: "Error occurred when call RTVJOBA: {u'dftccsid': u'37', u'error1': u'CPF7CFD'}"
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
output:
    description: The RTV command output.
    returned: when rc as 0(success)
    type: dict
    sample: {
        "JOB": "QSQSRVR",
        "LOGSEV": "0",
        "USER": "QUSER"
    }
job_log:
    description: The IBM i job log of the task executed.
    returned: always
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
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(type='str', required=True),
            char_vars=dict(type='list', elements='str'),
            number_vars=dict(type='list', elements='str'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    command = module.params['cmd'].strip().upper()
    char_vars = module.params['char_vars']
    args_dict = dict()
    if char_vars:
        char_vars = [item.strip().upper() for item in char_vars]
        for item in char_vars:
            args_dict.update({item: 'chars'})
    number_vars = module.params['number_vars']
    if number_vars:
        number_vars = [item.strip().upper() for item in number_vars]
        for item in number_vars:
            args_dict.update({item: 'number'})
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    out = dict()
    if (not char_vars) and (not number_vars):
        module.fail_json(msg='At least one of the option char_vars or number_vars must contain value')
    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    job_log = []
    rc, out, err, job_log = ibmi_module.itoolkit_run_rtv_command_once(command, args_dict)

    result = dict(
        rc=rc,
        output=out,
        args_dict=args_dict,
        job_log=job_log
    )

    if rc:
        message = 'non-zero return code:{rc}, error: {err}'.format(rc=rc, err=err)
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(msg='Success', **result)


if __name__ == '__main__':
    main()
