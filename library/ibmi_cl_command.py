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
  - For Pase or Qshell(Unix/Linux-liked) commands run on IBMi targets, like 'ls'，'chmod' etc, use the M(command) module instead.
  - Only run one command at a time.
options:
  cmd:
    description:
      - The IBM i CL command to run.
    type: str
    required: yes
  joblog:
    description:
      - If set to C(true), append JOBLOG to stderr/stderr_lines.
    type: bool
    default: false

notes:
    - Please do not set joblog to true for IBM i CL command with OUTPUT parameter, e.g. DSPLIBL OUTPUT(*), DSPHDWRSC TYPE(*AHW) OUTPUT(*).
    - With joblog as false, the available message text together with message ID will be dumped to stderr/stderr_lines.
    - With joblog as true, the available message text together with message ID and the available message help information which includes
      the Cause and Recovery part will be dumped to stderr/stderr_lines.
    - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)

seealso:
- module: command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Create a library by using CL command CRTLIB
  ibmi_cl_command:
    command: 'CRTLIB LIB(TESTLIB)'
    joblog: false
'''

RETURN = r'''
joblog:
    description: Append JOBLOG to stderr/stderr_lines or not.
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
'''

import datetime
from ansible.module_utils.basic import AnsibleModule

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iCmd
    # from itoolkit.db2.idb2call import iDB2Call
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


def interpret_return_code(rc):
    if rc == IBMi_COMMAND_RC_SUCCESS:
        return 'Success'
    elif rc == IBMi_COMMAND_RC_ERROR:
        return 'Generic failure'
    elif rc == IBMi_COMMAND_RC_UNEXPECTED:
        return 'Unexpected error'
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG:
        return "iToolKit result dict does not have key 'joblog'"
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR:
        return "iToolKit result dict does not have key 'error'"
    else:
        return "Unknown error"


def itoolkit_run_command(command):
    conn = dbi.connect()
    # itransport = iDB2Call(conn)
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(iCmd('command', command, {'error': 'on'}))
    itool.call(itransport)

    rc = IBMi_COMMAND_RC_UNEXPECTED
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
            cmd=dict(type='str', required=True),
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    command = module.params['cmd']
    joblog = module.params['joblog']

    startd = datetime.datetime.now()

    if joblog:
        if HAS_ITOOLKIT is False:
            module.fail_json(msg="itoolkit package is required")

        if HAS_IBM_DB is False:
            module.fail_json(msg="ibm_db package is required")

        rc, out, err = itoolkit_run_command(command)
    else:
        args = ['system', command]
        rc, out, err = module.run_command(args, use_unsafe_shell=False)

    endd = datetime.datetime.now()
    delta = endd - startd

    rc_msg = interpret_return_code(rc)

    result = dict(
        cmd=command,
        joblog=joblog,
        stdout=out,
        stderr=err,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
        # changed=True,
    )

    if rc != IBMi_COMMAND_RC_SUCCESS:
        message = 'non-zero return code:{rc},{rc_msg}'.format(rc=rc, rc_msg=rc_msg)
        module.fail_json(msg=message, **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
