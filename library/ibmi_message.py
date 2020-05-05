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
module: ibmi_message
short_description: Search or reply message on a remote IBMi node
version_added: 2.10
description:
  - Search or reply message on a remote IBMi node
  - For non-IBMi targets, no need
options:
  operation:
    description:
      - the operation of the messgae
    type: str
    required: yes
    choices: [ "find" ]
  message_type:
    description:
      - the type of the message
      - INFORMATIONAL, A message that conveys information about the condition of a function.
      - COMPLETION, A message that conveys completion status of work.
      - DIAGNOSTIC, A message about errors in the processing of a system function, in an application program, or in input data.
      - ESCAPE, A message that describes a condition for which a procedure or program must end abnormally. A procedure or program can
        monitor for the arrival of escape messages from the program or procedure it calls or from the machine. Control does not
        return to the sending program after an escape message is sent.
      - INQUIRY, A message that conveys information but also asks for a reply.
      - REPLY, A message that is a response to a received inquiry or notify message.
      - NOTIFY, A message that describes a condition for which a procedure or program requires corrective action or a reply from its calling
        procedure or program. A procedure or program can monitor for the arrival of notify messages from the programs or procedures it calls.
      - REQUEST, A message that requests a function from the receiving procedure or program. (For example, a CL command is a request message.)
      - SENDER, an inquiry or notify message that is kept by the sender.
      - NO_REPLY, a message that type is "INQUIRY" and has not been replied.
    type: str
    choices: [ "INFORMATIONAL", "COMPLETION", "DIAGNOSTIC", "ESCAPE",
               "INQUIRY", "REPLY", "NOTIFY", "REQUEST", "SENDER", "NO_REPLY"]
    required: yes
  message_queue:
    description:
      - the queue of the message
    type: list
    elements: str
  message_lib:
    description:
      - the library name which contains message queue
    type: str
    required: yes
  message_id:
    description:
      - the id of the message
    type: list
    elements: str
  message_text:
    description:
      - the message text of the message
    type: str

seealso:
- module: service

author:
- Jin Yi Fan(@jinyifan)
'''

EXAMPLES = r'''
- name: find a message with message type, message_lib, message_queue and message_id
  ibmi_message:
    operation: 'find'
    message_type: 'INFORMATIONAL'
    message_lib: 'QUSRSYS'
    message_queue: ['QPGMR', 'QSECOFR']
    message_id: ['CPF1241', 'CPF1240']

- name: find all un-reply message with message type, message_lib and message_queue
  ibmi_message:
    operation: 'find'
    message_type: 'NO_REPLY'
    message_lib: 'QUSRSYS'
    message_queue: ['QPGMR', 'QSECOFR']
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
    sample: 'Success'
stderr:
    description: The command standard error
    returned: always
    type: str
    sample: 'Generic failure'
sql:
    description: The sql executed by the task
    returned: always
    type: str
    sample: "SELECT MESSAGE_QUEUE_LIBRARY, MESSAGE_QUEUE_NAME, MESSAGE_ID, MESSAGE_TYPE,
             MESSAGE_SUBTYPE, MESSAGE_TEXT, SEVERITY, MESSAGE_TIMESTAMP, MESSAGE_KEY,
             ASSOCIATED_MESSAGE_KEY, FROM_USER, FROM_JOB, FROM_PROGRAM, MESSAGE_FILE_LIBRARY,
             MESSAGE_FILE_NAME, MESSAGE_SECOND_LEVEL_TEXT
             FROM QSYS2.MESSAGE_QUEUE_INFO
             WHERE MESSAGE_QUEUE_LIBRARY = 'QUSRSYS'
             AND MESSAGE_QUEUE_NAME = 'CHANGLE' OR MESSAGE_QUEUE_NAME = 'QHQB'
             AND MESSAGE_ID = 'CPF1241' OR MESSAGE_ID = 'CPF1240' AND MESSAGE_TYPE = 'INFORMATIONAL'"
rc:
    description: The command return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
message_info:
    description: the message_info
    returned: always
    type: str
    sample: [{
            "ASSOCIATED_MESSAGE_KEY": "",
            "FROM_JOB": "013447/QSYS/QINTER",
            "FROM_PROGRAM": "QWTMMDSC",
            "FROM_USER": "QSYS",
            "MESSAGE_FILE_LIBRARY": "QSYS",
            "MESSAGE_FILE_NAME": "QCPFMSG",
            "MESSAGE_ID": "CPI1131",
            "MESSAGE_KEY": "00003B70",
            "MESSAGE_QUEUE_LIBRARY": "QSYS",
            "MESSAGE_QUEUE_NAME": "QSYSOPR",
            "MESSAGE_SECOND_LEVEL_TEXT": "&N Cause . . . . . :   User QSYS performed the Disconnect Job (DSCJOB) command for the job.",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "CPI1131 Job 013659/CHANGLE/QPADEV0002 disconnected by user QSYS.",
            "MESSAGE_TIMESTAMP": "2020-04-24-09.44.35.568129",
            "MESSAGE_TYPE": "INFORMATIONAL",
            "SEVERITY": "0"
        }]
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
        "Success"
    ]
stderr_lines:
    description: The command standard error split in lines
    returned: always
    type: list
    sample: [
        "Generic failure."
    ]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ibmi import ibmi_util


def handle_list_to_sql(sql, item_list, param_name):
    if isinstance(item_list, list):
        if item_list:
            i = 1
            j = 1
            for item in item_list:
                if item and item.strip():
                    if i == 1:
                        sql = sql + "(" + param_name + " = '" + item.upper() + "'"
                        i += 1
                    else:
                        sql = sql + param_name + " = '" + item.upper() + "'"
                    if j < len(item_list):
                        sql = sql + " OR "
                    else:
                        sql = sql + ") AND "
                j += 1
    return sql


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str',
                           choices=["find"],
                           required=True),
            message_type=dict(type='str',
                              choices=["INFORMATIONAL", "COMPLETION", "DIAGNOSTIC",
                                       "ESCAPE", "INQUIRY", "REPLY", "NOTIFY", "REQUEST",
                                       "SENDER", "NO_REPLY"],
                              required=True),
            message_lib=dict(type='str', required=True),
            message_queue=dict(type='list', elements='str'),
            message_id=dict(type='list', elements='str'),
            message_text=dict(type='str'),
        ),
        supports_check_mode=True,
    )

    operation = module.params['operation']
    message_type = module.params['message_type']
    message_queue = module.params['message_queue']
    message_lib = module.params['message_lib']
    message_id = module.params['message_id']
    message_text = module.params['message_text']
    startd = datetime.datetime.now()
    if operation == "find":
        sql = "SELECT MESSAGE_QUEUE_LIBRARY, MESSAGE_QUEUE_NAME, MESSAGE_ID, MESSAGE_TYPE, " + \
              "MESSAGE_SUBTYPE, MESSAGE_TEXT, SEVERITY, MESSAGE_TIMESTAMP, MESSAGE_KEY, ASSOCIATED_MESSAGE_KEY, " + \
              "FROM_USER, FROM_JOB, FROM_PROGRAM, MESSAGE_FILE_LIBRARY, MESSAGE_FILE_NAME, MESSAGE_SECOND_LEVEL_TEXT " + \
              "FROM QSYS2.MESSAGE_QUEUE_INFO WHERE MESSAGE_QUEUE_LIBRARY = '" + message_lib.upper() + "' AND "
        sql = handle_list_to_sql(sql, message_queue, "MESSAGE_QUEUE_NAME")
        sql = handle_list_to_sql(sql, message_id, "MESSAGE_ID")
        if message_text:
            sql = sql + "(MESSAGE_TEXT LIKE '%" + message_text + "%' OR MESSAGE_SECOND_LEVEL_TEXT LIKE '%" + message_text + "%') AND "
        if message_type == "NO_REPLY":
            sql = sql + "MESSAGE_TYPE = 'INQUIRY' AND MESSAGE_KEY NOT IN " + \
                        "(SELECT ASSOCIATED_MESSAGE_KEY FROM QSYS2.MESSAGE_QUEUE_INFO WHERE MESSAGE_TYPE = 'REPLY' " + \
                        "AND MESSAGE_QUEUE_LIBRARY = '" + message_lib.upper() + "')"
        else:
            sql = sql + "MESSAGE_TYPE = '" + message_type.upper() + "'"

    rc, rc_msg, out, error = ibmi_util.itoolkit_run_sql_once(sql)
    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        sql=sql,
        stdout=rc_msg,
        stderr=error,
        message_info=out,
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
