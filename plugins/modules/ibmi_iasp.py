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
module: ibmi_iasp
short_description: Control IASP
version_added: '2.8.0'
description:
  - Control IASP.
  - For IBM i V7R2, PTF SI72162 is required.
  - For IBM i V7R3, PTF SI72161 is required.
  - For non-IBM i targets, no need.
options:
  name:
    description:
      - The name of the iasp.
    type: str
    required: yes
  operation:
    description:
      - C(create)/C(delete)/C(add_disks) are idempotent actions that will not run
        commands unless necessary.
      - C(view) will return the iasp state
      - B(At least one of operation are required.)
    type: str
    choices: [ "create", "add_disks", "delete", "display" ]
    required: yes
  disks:
    description:
      - The list of the unconfigure disks.
    type: list
    elements: str
  asp_type:
    description:
      - The asp_type of new create iasp.
    type: str
    default: '*PRIMARY'
    choices: ['*PRIMARY', '*SECONDARY', '*UDFS']
  primary_asp:
    description:
      - The primary_asp of new create iasp.
    type: str
  extra_parameters:
    description:
      - Extra parameter is appended at the end of create operation.
    type: str
    default: ' '
  synchronous:
    description:
      - Synchronous execute the iasp command.
    type: bool
    default: true
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

author:
- Jin Yifan(@jinyifan)
'''

EXAMPLES = r'''
- name: create an IASP
  ibmi_iasp:
    name: 'IASP1'
    operation: 'create'
    disks: ['DMP002', 'DMP019']
    become_user: 'USER1'
    become_user_password: 'yourpassword'
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
    sample: 'CPCB719: Configure Device ASP *DELETE request completed.'
stderr:
    description: The command standard error.
    returned: always
    type: str
    sample: 'Generic failure'
cmd:
    description: The command executed by the task.
    returned: always
    type: str
    sample: 'CFGDEVASP ASPDEV(YFTEST) ACTION(*DELETE) CONFIRM(*NO)'
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
asp_info:
    description: The asp_info of the identify iasp.
    returned: always
    type: list
    sample: [{
            "ASP_NUMBER": "144",
            "ASP_STATE": "VARIED OFF",
            "ASP_TYPE": "PRIMARY",
            "BALANCE_DATA_MOVED": "0",
            "BALANCE_DATA_REMAINING": "0",
            "BALANCE_STATUS": "",
            "BALANCE_TIMESTAMP": "",
            "BALANCE_TYPE": "",
            "CHANGES_WRITTEN_TO_DISK": "YES",
            "COMPRESSED_DISK_UNITS": "NONE",
            "COMPRESSION_RECOVERY_POLICY": "OVERFLOW IMMEDIATE",
            "DEVICE_DESCRIPTION_NAME": "",
            "DISK_UNITS_PRESENT": "ALL",
            "END_IMMEDIATE": "",
            "ERROR_LOG_SPACE": "0",
            "MACHINE_LOG_SPACE": "0",
            "MACHINE_TRACE_SPACE": "0",
            "MAIN_STORAGE_DUMP_SPACE": "0",
            "MICROCODE_SPACE": "0",
            "MULTIPLE_CONNECTION_DISK_UNITS": "YES",
            "NUMBER_OF_DISK_UNITS": "1",
            "OVERFLOW_RECOVERY_RESULT": "",
            "OVERFLOW_STORAGE": "0",
            "PRIMARY_ASP_RESOURCE_NAME": "",
            "PROTECTED_CAPACITY": "0",
            "PROTECTED_CAPACITY_AVAILABLE": "0",
            "RDB_NAME": "IASP1",
            "RESOURCE_NAME": "IASP1",
            "STORAGE_THRESHOLD_PERCENTAGE": "90",
            "SYSTEM_STORAGE": "2",
            "TOTAL_CAPACITY": "0",
            "TOTAL_CAPACITY_AVAILABLE": "0",
            "TRACE_DURATION": "0",
            "TRACE_STATUS": "",
            "TRACE_TIMESTAMP": "",
            "UNPROTECTED_CAPACITY": "0",
            "UNPROTECTED_CAPACITY_AVAILABLE": "0"
        }]
stdout_lines:
    description: The command standard output split in lines.
    returned: always
    type: list
    sample: [
        "CPCB719: Configure Device ASP *DELETE request completed."
    ]
stderr_lines:
    description: The command standard error split in lines.
    returned: always
    type: list
    sample: [
        "Generic failure"
    ]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(type='str', required=True),
            operation=dict(type='str', required=True, choices=['create', 'add_disks', 'delete', 'display']),
            disks=dict(type='list', elements='str'),
            asp_type=dict(type='str', default="*PRIMARY", choices=['*PRIMARY', '*SECONDARY', '*UDFS']),
            primary_asp=dict(type='str'),
            extra_parameters=dict(type='str', default=' '),
            synchronous=dict(type='bool', default=True),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        required_if=[
            ["operation", "create", ["disks", "asp_type"]],
            ["operation", "add_disks", ["disks"]],
            ["asp_type", "*SECONDARY", ["primary_asp"]]
        ],
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    name = module.params['name']
    operation = module.params['operation']
    disks = module.params['disks']
    asp_type = module.params['asp_type']
    primary_asp = module.params['primary_asp']
    extra_parameters = module.params['extra_parameters']
    synchronous = module.params['synchronous']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()
    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    command = ''
    rc = ''
    rc_msg = ''
    out = ''
    state = ''
    asp_number = '000'
    asp_info = ''
    job_log = []
    sql = "SELECT * FROM QSYS2.ASP_INFO WHERE RESOURCE_NAME = '" + name.upper() + "'"
    rc, asp_info, error, job_log = ibmi_module.itoolkit_run_sql_once(sql)
    if asp_info:
        state = asp_info[0]['ASP_STATE']
        asp_number = asp_info[0]['ASP_NUMBER']
    error = ''
    if operation == "create":
        if not state:
            command = "QSYS/CFGDEVASP ASPDEV(" + name + ") ACTION(*CREATE) TYPE(" + asp_type + ") "
            if asp_type == "*SECONDARY":
                command = command + "PRIASPDEV(" + primary_asp + ") "
            command = command + "UNITS(" + " ".join(disks) + ") CONFIRM(*NO) " + extra_parameters
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            out = "ASP " + name + " already exsit."
            error = out
    elif operation == "add_disks":
        if not state:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            out = "ASP " + name + " does not exsit"
            error = out
        else:
            command = "CALL PGM(QSYS/QAENGADDDU) PARM('{p_name}' '{p_asp_number}' '0' ".format(
                p_name=ibmi_util.fmtTo10(name),
                p_asp_number=asp_number)
            for disk in disks:
                command = command + "'" + ibmi_util.fmtTo10(disk) + "' "
            command = command + ")"
    elif operation == "delete":
        if state:
            command = "QSYS/CFGDEVASP ASPDEV(" + name + ") ACTION(*DELETE) CONFIRM(*NO)"
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            out = "ASP " + name + " already deleted."
    elif operation == 'display':
        if state:
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            out = rc_msg
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            out = "ASP " + name + " does not exsit."
            error = out
    if command:
        if not synchronous:
            command = "SBMJOB CMD(" + command + ")"
        rc, out, error, job_log = ibmi_module.itoolkit_run_command_once(command)

    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        cmd=command,
        stdout=out,
        stderr=error,
        asp_info=asp_info,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
        job_log=job_log,
    )

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
