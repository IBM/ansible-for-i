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
module: ibmi_end_subsystem
short_description: End an active subsystem.
version_added: '2.8.0'
description:
    - The C(ibmi_end_subsystem) module ends an active subsystem.
options:
  subsystem:
    description:
      - The name of the subsystem description.
    type: str
    required: yes
  how_to_end:
    description:
      - Specifies whether jobs in the subsystem are ended in a controlled manner or immediately.
    type: str
    default: '*CNTRLD'
    choices: ['*IMMED', '*CNTRLD']
  controlled_end_delay_time:
    description:
      - Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation.
        If this amount of time is exceeded and the end operation is not complete,
        any jobs still being processed in the subsystem are ended immediately.
        If the value is greater than 99999, C(*NOLIMIT) will be used in ENDSBS command DELAY parameter.
    type: int
    default: 100000
  end_subsystem_option:
    description:
      - Specifies the options to take when ending the active subsystems.
    type: list
    elements: str
    default: ['*DFT']
    choices: ['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL']
  parameters:
    description:
      - The parameters that ENDSBS command will take.
        Other than the options above, all other parameters need to be specified here.
        The default values of parameters for ENDSBS will be taken if not specified.
    type: str
    default: ''
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
notes:
    - This module is NOT ALLOWED to end ALL subsystems, use the C(ibmi_cl_command) module instead.
    - This module is non-blocking, the ending subsystem may still be in progress, use C(ibmi_display_subsystem) module to check the status.
seealso:
- module: ibmi_display_subsystem, ibmi_start_subsystem
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: End the subsystem QBATCH with another user.
  ibmi_end_subsystem:
    subsystem: QBATCH
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: End a subsystem with options.
  ibmi_end_subsystem:
    subsystem: QBATCH
    how_to_end: '*IMMED'
'''

RETURN = r'''
stdout:
    description: The standard output of the end subsystem command.
    type: str
    sample: 'CPF0943: Ending of subsystem QBATCH in progress.'
    returned: always
stderr:
    description: The standard error the end subsystem command.
    type: str
    sample: 'CPF1054: No subsystem MYJOB active.'
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
        "CPF0943: Ending of subsystem QBATCH in progress."
    ]
    returned: always
stderr_lines:
    description: The standard error split in lines.
    type: list
    sample: [
        "CPF1054: No subsystem MYJOB active."
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
            how_to_end=dict(type='str', default='*CNTRLD', choices=['*IMMED', '*CNTRLD']),
            controlled_end_delay_time=dict(type='int', default=100000),
            end_subsystem_option=dict(type='list', default=['*DFT'], choices=['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL'], elements='str'),
            parameters=dict(type='str', default=''),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    subsystem = module.params['subsystem'].strip().upper()
    how_to_end = module.params['how_to_end']
    controlled_end_delay_time_seconds = module.params['controlled_end_delay_time']
    end_subsystem_option_list = module.params['end_subsystem_option']
    parameters = module.params['parameters'].upper()
    joblog = module.params['joblog']
    if len(subsystem) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of subsystem exceeds 10 characters")
    if controlled_end_delay_time_seconds > 99999:
        controlled_end_delay_time = '*NOLIMIT'
    else:
        controlled_end_delay_time = controlled_end_delay_time_seconds
    if subsystem == '*ALL' or subsystem == '*all':
        module.fail_json(rc=ibmi_util.IBMi_END_ALL_SUBSYSTEM_NOT_ALLOWED, msg="End all subsystems is NOT allowed")
    end_subsystem_option = ''
    for item in end_subsystem_option_list:
        end_subsystem_option = end_subsystem_option + item + ' '
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    command = 'QSYS/ENDSBS SBS({subsystem}) \
        OPTION({how_to_end}) DELAY({controlled_end_delay_time}) ENDSBSOPT({end_subsystem_option}) \
        {parameters}'.format(
        subsystem=subsystem,
        how_to_end=how_to_end,
        controlled_end_delay_time=controlled_end_delay_time,
        end_subsystem_option=end_subsystem_option,
        parameters=parameters)

    command = ' '.join(command.split())  # keep only one space between adjacent strings
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
