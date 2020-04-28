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
module: ibmi_tcp_server_service
short_description: Manage tcp server on a remote IBMi node
version_added: 2.10
description:
  - Manage and query IBMi tcp server service.
  - For non-IBMi targets, use the M(service) module instead.
options:
  name_list:
    description:
      - The name of the tcp server service.
        The valid value are "*ALL", "*AUTOSTART", "*BOOTP", "*DBG", "*DDM", "*DHCP", "*DIRSRV", "*DLFM", "*DNS",
        "*DOMINO", "*EDRSQL", "*FTP", "*HTTP", "*HOD", "*IAS", "*INETD", "*LPD", "*MGTC", "*NETSVR", "*NSLD", "*NTP",
        "*ODPA", "*OMPROUTED", "*ONDMD", "*POP", "*QOS", "*REXEC", "*ROUTED", "*SLP", "*SMTP", "*SNMP", "*SRVSPTPRX",
        "*SSHD", "*TCM", "*TELNET", "*TFTP", "*VPN", "*WEBFACING".
    type: list
    elements: str
    required: yes
  state:
    description:
      - C(started)/C(stopped) are idempotent actions that will not run
        commands unless necessary.
      - C(restarted) will always bounce the service.
      - B(At least one of state and enabled are required.)
    type: str
    choices: ["started", "stopped"]
    required: yes
  extra_parameters:
    description:
      - extra parameter is appended at the end of tcp server service command
    type: str
    default: ' '
  joblog:
    description:
      - If set to C(true), append JOBLOG to stderr/stderr_lines.
    type: bool
    default: false

seealso:
- module: service

author:
- Jin Yi Fan(@jinyifan)
'''

EXAMPLES = r'''
- name: start tcp server service
  ibmi_tcp_server_service:
    name_list: ['*SSH', '*HTTP']
    state: 'started'
    joblog: True
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
rc_msg:
    description: Meaning of the return code
    returned: always
    type: str
    sample: 'Generic failure'
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
    # from itoolkit import *
    # from itoolkit.db2.idb2call import *
    from itoolkit import iToolKit
    from itoolkit import iCmd
    from itoolkit.db2.idb2call import iDB2Call
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
IBMi_PARAM_NOT_VALID = 259
IBMi_STRSVR = "QSYS/STRTCPSVR"
IBMi_ENDSVR = "QSYS/ENDTCPSVR"
IBMi_TCP_SERVER_LIST = ["*ALL", "*AUTOSTART", "*BOOTP", "*DBG", "*DDM", "*DHCP", "*DIRSRV", "*DLFM", "*DNS",
                        "*DOMINO", "*EDRSQL", "*FTP", "*HTTP", "*IAS", "*INETD", "*LPD", "*MGTC", "*NETSVR",
                        "*NTP", "*OMPROUTED", "*POP", "*QOS", "*REXEC", "*ROUTED", "*SMTP", "*SNMP", "*SRVSPTPRX",
                        "*SSHD", "*TCM", "*TELNET", "*TFTP", "*VPN", "*WEBFACING", "*ODPA", "*ONDMD", "*SLP",
                        "*NSLD", "*HOD"]


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
    itransport = iDB2Call(conn)
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
            err = "iToolKit result dict does not have key 'joblog, the output is %s" % command_output
    else:
        # should not be here, must xmlservice has internal error
        rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
        err = "iToolKit result dict does not have key 'error', the output is %s" % command_output

    return rc, out, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name_list=dict(type='list', elements='str', required=True),
            state=dict(type='str', choices=['started', 'stopped'], required=True),
            extra_parameters=dict(type='str', default=' '),
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    name_list = module.params['name_list']
    state = module.params['state']
    extra_parameters = module.params['extra_parameters']
    joblog = module.params['joblog']

    startd = datetime.datetime.now()
    if state == 'started':
        command = IBMi_STRSVR + " SERVER(" + " ".join(i for i in name_list) + ") " + extra_parameters
    if state == 'stopped':
        command = IBMi_ENDSVR + " SERVER(" + " ".join(i for i in name_list) + ") " + extra_parameters

    if set(name_list) < set(IBMi_TCP_SERVER_LIST):
        # this is expected
        pass
    else:
        rc = IBMi_PARAM_NOT_VALID
        result_failed_parameter_check = dict(
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            stderr="Parameter passed is not valid. ",
            rc=rc,
            command=command,
            # changed=True,
        )
        module.fail_json(msg='Value specified for name_list is not valid. Valid values are ' +
                             ", ".join(i for i in IBMi_TCP_SERVER_LIST), **result_failed_parameter_check)
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
        rc_msg=rc_msg,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
    )

    if rc != IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
