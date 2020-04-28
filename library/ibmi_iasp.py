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
short_description: Control IASP on target IBMi node
version_added: 2.10
description:
  - Control IASP on target IBMi node
  - For non-IBMi targets, no need
options:
  name:
    description:
      - The name of the iasp
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
      - The list of the unconfigure disks
    type: list
    elements: str
  asp_type:
    description:
      - The asp_type of new create iasp
    type: str
    default: '*PRIMARY'
    choices: ['*PRIMARY', '*SECONDARY', '*UDFS']
  primary_asp:
    description:
      - The primary_asp of new create iasp
    type: str
  extra_parameters:
    description:
      - extra parameter is appended at the end of create operation
    type: str
    default: ' '
  synchronous:
    description:
      - synchronous execute the iasp command
    type: bool
    default: true

author:
- Jin Yi Fan(@jinyifan)
'''

EXAMPLES = r'''
- name: start host server service
  ibmi_iasp:
    name: 'IASP1'
    operation: 'create'
    disks: ['DMP002', 'DMP019']
'''

RETURN = r'''
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
    sample: 'CPCB719: Configure Device ASP *DELETE request completed.'
stderr:
    description: The command standard error
    returned: always
    type: str
    sample: 'Generic failure'
cmd:
    description: The command executed by the task
    returned: always
    type: str
    sample: 'CFGDEVASP ASPDEV(YFTEST) ACTION(*DELETE) CONFIRM(*NO)'
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
asp_info:
    description: the asp_info of the identify iasp
    returned: always
    type: str
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
    description: The command standard output split in lines
    returned: always
    type: list
    sample: [
        "CPCB719: Configure Device ASP *DELETE request completed."
    ]
stderr_lines:
    description: The command standard error split in lines
    returned: always
    type: list
    sample: [
        "Generic failure"
    ]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ibmi import ibmi_util


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
        ),
        required_if=[
            ["operation", "create", ["disks", "asp_type"]],
            ["operation", "add_disks", ["disks"]],
            ["asp_type", "*SECONDARY", ["primary_asp"]]
        ],
        supports_check_mode=True,
    )

    name = module.params['name']
    operation = module.params['operation']
    disks = module.params['disks']
    asp_type = module.params['asp_type']
    primary_asp = module.params['primary_asp']
    extra_parameters = module.params['extra_parameters']
    synchronous = module.params['synchronous']

    startd = datetime.datetime.now()
    command = ''
    rc = ''
    rc_msg = ''
    out = ''
    state = ''
    asp_number = '000'
    asp_info = ''
    sql = "SELECT * FROM QSYS2.ASP_INFO WHERE RESOURCE_NAME = '" + name.upper() + "'"
    rc, rc_msg, asp_info, error = ibmi_util.itoolkit_run_sql_once(sql)
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
            rc_msg = ibmi_util.interpret_return_code(rc)
            out = "ASP " + name + " already exsit."
            error = out
    elif operation == "add_disks":
        if not state:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            rc_msg = ibmi_util.interpret_return_code(rc)
            out = "ASP " + name + " does not exsit"
            error = out
        else:
            command = "CALL PGM(QSYS/QAENGADDDU) PARM('"
            command = command + ibmi_util.fmtTo10(name) + "' '" + asp_number + "' "
            command = command + "'0' "
            for disk in disks:
                command = command + "'" + ibmi_util.fmtTo10(disk) + "' "
            command = command + ")"
    elif operation == "delete":
        if state:
            command = "QSYS/CFGDEVASP ASPDEV(" + name + ") ACTION(*DELETE) CONFIRM(*NO)"
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            rc_msg = ibmi_util.interpret_return_code(rc)
            out = "ASP " + name + " already deleted."
    elif operation == 'display':
        if state:
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            rc_msg = ibmi_util.interpret_return_code(rc)
            out = rc_msg
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            rc_msg = ibmi_util.interpret_return_code(rc)
            out = "ASP " + name + " does not exsit."
            error = out
    if command:
        if not synchronous:
            command = "SBMJOB CMD(" + command + ")"
        rc, rc_msg, out, error = ibmi_util.itoolkit_run_command_once(command)

    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        cmd=command,
        stdout=out,
        stderr=error,
        asp_info=asp_info,
        rc=rc,
        rc_msg=rc_msg,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
    )

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
