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
module: ibmi_end_subsystem
short_description: end a subsystem
description:
    - the C(ibmi_end_subsystem) module end a subsystem of the target ibmi node.
version_added: "1.1"
options:
  subsystem:
    description:
      - The name of the subsystem description
    type: str
    required: yes
  how_to_end:
    description:
      - Specifies whether jobs in the subsystem are ended in a controlled manner or immediately
    type: str
    default: '*CNTRLD'
    choices: ['*IMMED', '*CNTRLD']
  controlled_end_delay_time:
    description:
      - Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation
      - If this amount of time is exceeded and the end operation is not complete,
      - any jobs still being processed in the subsystem are ended immediately
      - If the value is greater than 99999, '*NOLIMIT' will be used in ENDSBS commnad
    type: int
    default: 100000
  end_subsystem_option:
    description:
      - Specifies the options to take when ending the active subsystems
    type: list
    elements: str
    default: ['*DFT']
    choices: ['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL']
  parameters:
    description:
      - The parameters that ENDSBS command will take
      - Other than options above, all other parameters need to be specified here
      - The default values of parameters for ENDSBS will be taken if not specified
    type: str
    default: ''
  joblog:
    description:
      - If set to C(true), output the avaiable JOBLOG even the rc is 0(success).
    type: bool
    default: false
notes:
- This module is NOT ALLOWED to end ALL subsystems, use the C(ibmi_cl_command) module instead
- This module is non-blocking, the end subsystem may still be in progress, use C(ibmi_display_subsystem_job) module to check the status
seealso:
- module: ibmi_end_subsystem
author:
- Chang Le (@changlexc)
'''

EXAMPLES = r'''
- name: End the subsystem QBATCH
  ibmi_end_subsystem:
    subsystem: QBATCH

- name: End a subsystem with options
  ibmi_end_subsystem:
    subsystem: QBATCH
    how_to_end: '*IMMED'
'''

RETURN = r'''
stdout:
    description: The standard output of the end subsystem command
    type: str
    sample: 'CPF0943: Ending of subsystem QBATCH in progress.'
    returned: always
stderr:
    description: The standard error the end subsystem command
    type: str
    sample: 'CPF1054: No subsystem MYJOB active.'
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
        "CPF0943: Ending of subsystem QBATCH in progress."
    ]
    returned: always
stderr_lines:
    description: The standard error split in lines
    type: list
    sample: [
        "CPF1054: No subsystem MYJOB active."
    ]
    returned: always
job_log:
    description: the job_log
    type: str
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

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ibmi import ibmi_util


def main():
    module = AnsibleModule(
        argument_spec=dict(
            subsystem=dict(type='str', required=True),
            how_to_end=dict(type='str', default='*CNTRLD', choices=['*IMMED', '*CNTRLD']),
            controlled_end_delay_time=dict(type='int', default=100000),
            end_subsystem_option=dict(type='list', default=['*DFT'], choices=['*DFT', '*NOJOBLOG', '*CHGPTY', '*CHGTSL'], elements='str'),
            parameters=dict(type='str', default=''),
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    subsystem = module.params['subsystem']
    how_to_end = module.params['how_to_end']
    controlled_end_delay_time_seconds = module.params['controlled_end_delay_time']
    end_subsystem_option_list = module.params['end_subsystem_option']
    parameters = module.params['parameters']
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

    command = 'QSYS/ENDSBS SBS({subsystem}) \
        OPTION({how_to_end}) DELAY({controlled_end_delay_time}) ENDSBSOPT({end_subsystem_option}) \
        {parameters}'.format(
        subsystem=subsystem,
        how_to_end=how_to_end,
        controlled_end_delay_time=controlled_end_delay_time,
        end_subsystem_option=end_subsystem_option,
        parameters=parameters)

    command = ' '.join(command.split())  # keep only one space between adjacent strings
    rc, out, err, job_log = ibmi_util.itoolkit_run_command_once(command)

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
