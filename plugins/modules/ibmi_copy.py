#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zengyu <pzypeng@cn.ibm.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_copy
short_description: Copy a save file from local to a remote IBM i node
version_added: '2.8.0'
description:
     - The C(ibmi_copy) copies a save file from local to a remote IBM i node.
     - C(ibmi_copy) will not restore save file on IBM i node.
     - For non-IBMi native targets, use the copy module instead.
options:
  src:
    description:
    - Local path to a save file to copy to the remote server.
    - This can be absolute or relative.
    type: str
    required: yes
  lib_name:
    description:
      - Remote library where the save file should be copied to.
    type: str
    required: yes
  force:
    description:
      - Influence whether the remote save file must always be replaced.
      - If C(yes), the remote save file will be replaced.
      - If C(no), the save file will only be transferred if the destination does not exist.
    type: bool
    default: False
  backup:
    description:
      - If set force C(true) and save file already exists on remote, rename the exists remote save file so you can get the
        original file back.
      - The backup save file name will be the original file name+number[1:9]. For example, the origial file name is obja, then
        rename the original file to obja1. If obja1 already exists, then rename the original file to obja2... util obja9, then
        report error.
      - Only works when force is C(True).
    type: bool
    default: False

notes:
    - ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under[defaults] section
seealso:
    - module: copy
author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Copy test.file on local to a remote IBM i.
  ibmi_copy:
    src: '/backup/test.file'
    lib_name: 'testlib'
    force: True
    backup: True
'''

RETURN = r'''
delta:
    description: The copy execution delta time when file is renewed.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The copy standard output.
    returned: always
    type: list
    sample: 'File TEST in library TESTLIB already exists.'
stderr:
    description: The copy standard error.
    returned: always
    type: list
    sample: [
        "CPF5813: File TEST in library TESTLIB already exists.",
        "CPF7302: File TEST not created in library TESTLIB."
    ]
src:
    description: Local absolute path to a save file to copy to the remote server.
    returned: always
    type: str
    sample: '/backup/test.file'
msg:
    description: The fetch execution message.
    returned: always
    type: str
    sample: 'File is successfully copied.'
dest:
    description: Remote absolute path where the file is copied to.
    returned: always
    type: str
    sample: '/QSYS.LIB/TESTLIB.LIB/TEST.FILE'
rc:
    description: The action return code. 0 means success.
    returned: always
    type: int
    sample: 255
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "149",
            "FROM_LIBRARY": "QSHELL",
            "FROM_MODULE": "QZSHRUNC",
            "FROM_PROCEDURE": "main",
            "FROM_PROGRAM": "QZSHRUNC",
            "FROM_USER": "TESTER",
            "MESSAGE_FILE": "QZSHMSGF",
            "MESSAGE_ID": "QSH0005",
            "MESSAGE_LIBRARY": "QSHELL",
            "MESSAGE_SECOND_LEVEL_TEXT": "",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Command ended normally with exit status 0.",
            "MESSAGE_TIMESTAMP": "2020-05-25-13.06.35.019371",
            "MESSAGE_TYPE": "COMPLETION",
            "ORDINAL_POSITION": "12",
            "SEVERITY": "0",
            "TO_INSTRUCTION": "5829",
            "TO_LIBRARY": "QXMLSERV",
            "TO_MODULE": "PLUGILE",
            "TO_PROCEDURE": "ILECMDEXC",
            "TO_PROGRAM": "XMLSTOREDP"
        }]
'''
