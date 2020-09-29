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
short_description: Manage tcp server
version_added: '2.8.0'
description:
  - Manage and query IBMi tcp server service.
  - For non-IBMi targets, use the M(service) module instead.
options:
  name_list:
    description:
      - The name of the tcp server service.
        The valid value are C(*ALL), C(*AUTOSTART), C(*BOOTP), C(*DBG), C(*DDM), C(*DHCP), C(*DIRSRV), C(*DLFM), C(*DNS),
        C(*DOMINO), C(*EDRSQL), C(*FTP), C(*HTTP), C(*HOD), C(*IAS), C(*INETD), C(*LPD), C(*MGTC), C(*NETSVR), C(*NSLD), C(*NTP),
        C(*ODPA), C(*OMPROUTED), C(*ONDMD), C(*POP), C(*QOS), C(*REXEC), C(*ROUTED), C(*SLP), C(*SMTP), C(*SNMP), C(*SRVSPTPRX),
        C(*SSHD), C(*TCM), C(*TELNET), C(*TFTP), C(*VPN), C(*WEBFACING).
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
      - Extra parameter is appended at the end of tcp server service command.
    type: str
    default: ' '
  joblog:
    description:
      - If set to C(true), append JOBLOG to stderr/stderr_lines.
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
- module: service

author:
- Jin Yifan(@jinyifan)
'''

EXAMPLES = r'''
- name: start tcp server service
  ibmi_tcp_server_service:
    name_list: ['*SSH', '*HTTP']
    state: 'started'
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
    sample: 'CPC2102: Library TESTLIB created'
stderr:
    description: The command standard error.
    returned: always
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
cmd:
    description: The command executed by the task.
    returned: always
    type: str
    sample: 'CRTLIB LIB(TESTLIB)'
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
        "CPC2102: Library TESTLIB created."
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
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"
IBMi_STRSVR = "QSYS/STRTCPSVR"
IBMi_ENDSVR = "QSYS/ENDTCPSVR"
IBMi_TCP_SERVER_LIST = ["*ALL", "*AUTOSTART", "*BOOTP", "*DBG", "*DDM", "*DHCP", "*DIRSRV", "*DLFM", "*DNS",
                        "*DOMINO", "*EDRSQL", "*FTP", "*HTTP", "*IAS", "*INETD", "*LPD", "*MGTC", "*NETSVR",
                        "*NTP", "*OMPROUTED", "*POP", "*QOS", "*REXEC", "*ROUTED", "*SMTP", "*SNMP", "*SRVSPTPRX",
                        "*SSHD", "*TCM", "*TELNET", "*TFTP", "*VPN", "*WEBFACING", "*ODPA", "*ONDMD", "*SLP",
                        "*NSLD", "*HOD"]


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name_list=dict(type='list', elements='str', required=True),
            state=dict(type='str', choices=['started', 'stopped'], required=True),
            extra_parameters=dict(type='str', default=' '),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    name_list = module.params['name_list']
    state = module.params['state']
    extra_parameters = module.params['extra_parameters']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()
    if state == 'started':
        command = IBMi_STRSVR + " SERVER(" + " ".join(i for i in name_list) + ") " + extra_parameters
    if state == 'stopped':
        command = IBMi_ENDSVR + " SERVER(" + " ".join(i for i in name_list) + ") " + extra_parameters

    if set(name_list) < set(IBMi_TCP_SERVER_LIST):
        # this is expected
        pass
    else:
        rc = ibmi_util.IBMi_PARAM_NOT_VALID
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
    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)
    job_log = []
    rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)

    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        cmd=command,
        job_log=job_log,
        stdout=out,
        stderr=err,
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
