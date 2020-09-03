#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Yi Fan Jin <jinyifan@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_device_vary
short_description: Vary on or off target device
version_added: '2.8.0'
description:
  - Vary on or off target device.
  - For non-IBM i targets, no need.
options:
  device_list:
    description:
      - The name of the device.
    type: list
    elements: str
    required: yes
  status:
    description:
      - C(on)/C(off) are idempotent actions that will not run
        commands unless necessary.
      - C(reset) will always bounce the service.
      - B(At least one of status are required.)
    type: str
    choices: [ "*ON", "*OFF", "*RESET", "*ALLOCATE", "UNPROTECTED", "*DEALLOCATE"]
    required: yes
  extra_parameters:
    description:
      - Extra parameter is appended at the end of VARYCFG command.
    type: str
    default: ' '
  joblog:
    description:
      - If set to C(true), append JOBLOG to stderr/stderr_lines.
    type: bool
    default: False

seealso:
- module: service

author:
- Jin Yifan(@jinyifan)
'''

EXAMPLES = r'''
- name: start host server service
  ibmi_device_vary:
    device_list: ['IASP1', 'IASP2']
    status: '*ON'
    joblog: True
'''

RETURN = r'''
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
start:
    description: The command execution start time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The command execution end time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The command execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The command standard output.
    returned: always
    type: str
    sample: '+++ success VRYCFG CFGOBJ(IASP1) CFGTYPE(*DEV) STATUS(*ON)'
stderr:
    description: The command standard error.
    returned: always
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
cmd:
    description: The command executed by the task.
    returned: always
    type: str
    sample: 'VRYCFG CFGOBJ(IASP1) CFGTYPE(*DEV) STATUS(*ON) '
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The command standard output split in lines.
    returned: always
    type: list
    sample: [
        "+++ success VRYCFG CFGOBJ(IASP1) CFGTYPE(*DEV) STATUS(*ON)"
    ]
stderr_lines:
    description: The command standard error split in lines.
    returned: always
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util

__ibmi_module_version__ = "1.0.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            device_list=dict(type='list', elements='str', required=True),
            status=dict(type='str',
                        choices=["*ON", "*OFF", "*RESET",
                                 "*ALLOCATE", "UNPROTECTED", "*DEALLOCATE"],
                        required=True),
            extra_parameters=dict(type='str', default=' '),
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    device_list = module.params['device_list']
    status = module.params['status']
    extra_parameters = module.params['extra_parameters']
    joblog = module.params['joblog']

    startd = datetime.datetime.now()
    if status in ["*OFF", "*DEALLOCATE"]:
        command = "QSYS/VRYCFG CFGOBJ(" + " ".join(device_list) + ") CFGTYPE(*DEV) STATUS(" + status + ") FRCVRYOFF(*YES) " + extra_parameters
    else:
        command = "QSYS/VRYCFG CFGOBJ(" + " ".join(device_list) + ") CFGTYPE(*DEV) STATUS(" + status + ") " + extra_parameters

    job_log = []
    if joblog:
        rc, out, error, job_log = ibmi_util.itoolkit_run_command_once(command)
    else:
        args = ['system', command]
        rc, out, error = module.run_command(args, use_unsafe_shell=False)

    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        cmd=command,
        job_log=job_log,
        stdout=out,
        stderr=error,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
    )

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
