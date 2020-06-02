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
---
module: ibmi_cl_command
short_description: Executes a CL command on a remote IBMi node
version_added: 2.10
description:
  - The C(ibmi_cl_command) module takes the CL command name followed by a list of space-delimited arguments.
  - The given CL command will be executed on all selected nodes.
  - For Pase or Qshell(Unix/Linux-liked) commands run on IBMi targets, like 'ls', 'chmod' etc, use the M(command) module instead.
  - Only run one command at a time.
options:
  cmd:
    description:
      - The IBM i CL command to run.
    type: str
    required: yes
  asp_group:
    description:
      - Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.
      - The ASP group name is the name of the primary ASP device within the ASP group.
      - Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*).
    type: str
    default: '*SYSBAS'
  joblog:
    description:
      - If set to C(true), output the avaiable JOBLOG even the rc is 0(success).
      - Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*).
    type: bool
    default: false

notes:
    - IBM i CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*) don't have joblog returned.
    - IBM i CL command can also be run by command module with quite simple result messages, add a prefix 'system' to the CL command.
    - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2).

seealso:
- module: command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Create a library by using CL command CRTLIB
  ibmi_cl_command:
    command: 'CRTLIB LIB(TESTLIB)'
    asp_group: 'IASP1'
'''

RETURN = r'''
joblog:
    description: Print JOBLOG or not when using itoolkit to run the CL command.
    returned: always
    type: bool
    sample: false
start:
    description: The command execution start time
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The command execution end time
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The command execution delta time
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The command standard output
    returned: always
    type: str
    sample: 'CPC2102: Library TESTLIB created'
stderr:
    description: The command standard error
    returned: always
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
cmd:
    description: The command executed by the task
    returned: always
    type: str
    sample: 'CRTLIB LIB(TESTLIB)'
rc:
    description: The command return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The command standard output split in lines
    returned: always
    type: list
    sample: [
        "CPC2102: Library TESTLIB created."
    ]
stderr_lines:
    description: The command standard error split in lines
    returned: always
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
job_log:
    description: the job_log
    returned: always
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
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util


def main():
    module = AnsibleModule(
        argument_spec=dict(
            cmd=dict(type='str', required=True),
            asp_group=dict(type='str', default='*SYSBAS'),
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    command = module.params['cmd'].strip().upper()
    asp_group = module.params['asp_group'].strip().upper()
    joblog = module.params['joblog']

    startd = datetime.datetime.now()
    job_log = []

    is_cmd5250 = False
    if command.startswith('DSP'):
        is_cmd5250 = True
    if command.startswith('QSYS/DSP'):
        is_cmd5250 = True
    if command.startswith('WRK'):
        is_cmd5250 = True
    if command.startswith('QSYS/WRK'):
        is_cmd5250 = True
    if 'OUTPUT(*)' in command:
        is_cmd5250 = True

    if is_cmd5250:
        args = ['system', command]
        rc, out, err = module.run_command(args, use_unsafe_shell=False)
    else:
        rc, out, err, job_log = ibmi_util.itoolkit_run_command_once(command, asp_group)

    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        cmd=command,
        joblog=joblog,
        rc=rc,
        stdout=out,
        stderr=err,
        job_log=job_log,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
    )

    if rc:
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
