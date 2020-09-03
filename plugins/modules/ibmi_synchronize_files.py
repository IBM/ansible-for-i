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
module: ibmi_synchronize_files
short_description: Synchronize a list of files from IBM i node A to another IBM i node B
version_added: '2.8.0'
description:
     - The C(ibmi_synchronize_files) plugin synchronize a list of files from IBM i node A to another IBM i node B.
     - C(ibmi_synchronize_files) plugin calls ibmi_sync_files module.
     - Only supports SAVF(.file) format synchronize between QSYS and QSYS.
options:
  src_list:
    description:
      - src files information list on the source host.
      - Evey src_list element should be a dict. dict can contain 'src' and 'dest'. 'dest' is optional.
      - The src key is the path to the src, and must be absolute.
      - The dest key is the path on the destination host that will be synchronized from the source.
    type: list
    elements: dict
    required: yes
  dest:
    description:
      - Path on the destination host that will be synchronized from the source.
      - The path must be absolute.
      - If specify, all the src files will be synchronized to the directory that dest speicified.
        Individual dest key in src_list will be ignored.
      - If not specify, individual dest will be the dest value inputted in src_list.
      - If both dest and dest key in src_list are not specify, individual dest will be equal to individual src in src_list.
      - Example
        '/test/dir/'
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
    - Need install paramiko package on target IBM i.
    - Make sure ssh passwordless login works from IBM i node A to IBM i node B.
    - private_key must be a rsa key in the legacy PEM private key format.
    - Doesn't support IASP by now.

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Synchronize a list of different types of files to host.com.
  ibmi_synchronize_files:
    src_list:
      - {'src': '/tmp/c1.file', 'dest': '/qsys.lib/fish.lib/'}
      - {'src': '/qsys.lib/fish.lib/test.file', 'dest': '/qsys.lib/fish.lib'}
      - {'src': '/tmp/c2.SAVF', 'dest': '/qsys.lib/fish.lib/'}
      - {'src': '/tmp/c3.bin', 'dest': '/test/dir'}
    private_key: '/home/test/id_rsa'
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
    sample: 'Complete synchronize file list to remote host host.com'
stderr:
    description: The standard error.
    returned: always
    type: str
    sample: 'Exception. not a valid RSA private key file. Use -vvv for more information.'
rc:
    description: The action return code. 0 means success.
    returned: always
    type: int
    sample: 255
success_list:
    description: The success transferred list.
    returned: always
    type: list
    sample: [
        {
            "dest": "/qsys.lib/fish.lib/",
            "src": "/tmp/c1.file"
        },
        {
            "dest": "/qsys.lib/fish.lib/",
            "src": "/tmp/c2.SAVF"
        },
        {
            "src": "/tmp/c3.log"
        }
    ]
fail_list:
    description: The fail transferred list.
    returned: always
    type: list
    sample: [
        {
            "dest": "/qsys.lib/fish.lib/",
            "fail_reason": "Can't sync file to /QSYS.LIB",
            "src": "/qsys.lib/fish.lib/test.file"
        },
        {
            "dest": "/qsys.lib/fish.lib/",
            "fail_reason": "src /qsys.lib/fish.lib/test.file doesn't exist.",
            "src": "/tmp/c4.SAVF"
        }
    ]
stdout_lines:
    description: The standard output split in lines.
    returned: always
    type: list
    sample: ['Complete synchronize file list to remote host host.com']
stderr_lines:
    description: The standard error split in lines.
    returned: always
    type: list
    sample: ['Exception. not a valid RSA private key file. Use -vvv for more information.']
'''
