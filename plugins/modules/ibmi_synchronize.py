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
module: ibmi_synchronize
short_description: Synchronize a save file from IBM i node A to another IBM i node B
version_added: '2.8.0'
description:
     - The C(ibmi_synchronize) plugin synchronize a save file from IBM i node A to another IBM i node B.
     - C(ibmi_synchronize) plugin calls ibmi_sync module.
     - Only support to synchronize save file by now.
     - For non-IBMi native targets, use the synchronize module instead.
     - delegate_to must be set to IBM i node A, and set hosts to IBM i node B.
     - Be careful to set delegate_to or hosts to node groups. The synchronized data may be overridden.
options:
  src:
    description:
      - Save file path on the source host that will be synchronized to the destination.
      - The path must be absolute. For example, /qsys.lib/test.lib/c1.file.
    type: str
    required: yes
  dest:
    description:
      - Path on the destination host that will be synchronized from the source.
      - The path must be absolute, and dest must be a IBM i native library. For example, /qsys.lib/test.lib.
      - If not specify, dest will be equal to src.
    type: str
    default: ''
  remote_user:
    description:
      - The user name to connect to the remote IBM i node B.
      - If not specify, remote_user will be the ansible_ssh_user of IBM i node B, which stored in ansible inventory.
    type: str
    default: ''
  private_key:
    description:
      - Specifies SSH private key path on IBM i node A used to connect to remote IBM i node B.
      - The path can be absolute or relative.
    type: str
    default: '~/.ssh/id_rsa'

notes:
    - ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under [defaults] section.
    - delegate_to must be set to IBM i node A.
    - Make sure ssh passwordless login works from IBM i node A to IBM i node B.
    - private_key must be a rsa key in the legacy PEM private key format.
    - Doesn't support IASP by now.

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Synchronize c1 save file from IBM i node A to another IBM i node B.
  ibmi_synchcronize:
    src: '/qsys.lib/test.lib/c1.file'
    remote_user: 'user'
    private_key: '/home/test/id_rsa'
  delegate_to: nodeA
'''

RETURN = r'''
delta:
    description: The execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The standard output.
    returned: always
    type: str
    sample: 'Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com'
stderr:
    description: The standard error.
    returned: always
    type: str
    sample: 'Failed to mv file to qsys. Make sure library exists.'
rc:
    description: The action return code. 0 means success.
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The standard output split in lines.
    returned: always
    type: list
    sample: ['Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com']
stderr_lines:
    description: The standard error split in lines.
    returned: always
    type: list
    sample: ['Failed to mv file to qsys. Make sure library exists.']
'''
