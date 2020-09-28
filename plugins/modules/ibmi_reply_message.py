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
module: ibmi_reply_message
short_description: Send a reply message to the sender of an inquiry message
version_added: '2.8.0'
description:
  - Send a reply message to the sender of an inquiry message.
  - For non-IBM i targets, use the M(service) module instead.
options:
  message_key:
    description:
      - Message key.
    type: str
    required: yes
  message_queue:
    description:
      - Message queue.
    type: str
    required: yes
  message_lib:
    description:
      - Message lib.
    type: str
    default: '*LIB'
  reply:
    description:
      - Reply.
    type: str
    default: '*DFT'
  remove_message:
    description:
      - Remove message.
    type: str
    choices: ["*YES", "*NO"]
    default: "*YES"
  reject_default_reply:
    description:
      - Reject default reply.
    type: str
    choices: ["*NOALWRJT", "*ALWRJT"]
    default: "*NOALWRJT"
  ccsid:
    description:
      - Coded character set ID, Vaild value are "1-65535", C(*HEX), C(*JOB).
    type: str
    default: "*JOB"
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
- name: start host server service
  ibmi_reply_message:
    message_key: 1990
    message_queue: QSECOFR
    message_lib: QUSRSYS
    reply: OK
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
    sample: '+++ success STRHOSTSVR SERVER(*ALL)'
stderr:
    description: The command standard error.
    returned: always
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
cmd:
    description: The command executed by the task.
    returned: always
    type: str
    sample: 'STRHOSTSVR SERVER(*ALL)'
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
        "+++ success STRHOSTSVR SERVER(*ALL)"
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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            message_key=dict(type='str', required=True),
            message_queue=dict(type='str', required=True),
            message_lib=dict(type='str', default='*LIB'),
            reply=dict(type='str', default='*DFT'),
            remove_message=dict(type='str', choices=['*YES', '*NO'], default='*YES'),
            reject_default_reply=dict(type='str', choices=['*NOALWRJT', '*ALWRJT'], default='*NOALWRJT'),
            ccsid=dict(type='str', default='*JOB'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    message_key = module.params['message_key']
    message_queue = module.params['message_queue']
    message_lib = module.params['message_lib']
    reply = module.params['reply']
    remove_message = module.params['remove_message']
    reject_default_reply = module.params['reject_default_reply']
    ccsid = module.params['ccsid']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    # handle the message key which more than 4 characters
    if len(message_key) > 4:
        message_key = "x'{0}'".format(message_key)

    command = "QSYS/SNDRPY MSGKEY({p_message_key}) MSGQ({p_message_lib}/{p_message_queue}) \
        RPY({p_reply}) RMV({p_remove_message}) RJTDFTRPY({p_reject_default_reply}) CCSID({p_ccsid})".format(
        p_message_key=message_key,
        p_message_queue=message_queue,
        p_message_lib=message_lib,
        p_reply=reply,
        p_remove_message=remove_message,
        p_reject_default_reply=reject_default_reply,
        p_ccsid=ccsid)

    startd = datetime.datetime.now()

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
