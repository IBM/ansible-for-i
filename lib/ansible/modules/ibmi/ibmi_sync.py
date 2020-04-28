#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Peng Zeng Yu <pzypeng@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_sync
short_description: Synchronize a save file from current ibm i node A to another ibm i node B.
version_added: 1.0
description:
     - The ibmi_sync module synchronize a save file from current ibm i node to another ibm i node.
     - Only support to synchronize save file by now.
     - For non-IBMi native targets, use the synchronize module instead.
options:
  src:
    description:
      - Save file path on the source host that will be synchronized to the destination.
      - The path must be absolute, and src must be a ibm i native library. For example, /qsys.lib/test.lib/c1.file.
    type: str
    required: yes
  dest:
    description:
      - Path on the destination host that will be synchronized from the source.
      - The path must be absolute, and dest must be a ibm i native library. For example, /qsys.lib/test.lib.
      - If not specify, dest will be equal to src.
    type: str
    default: ''
  remote_user:
    description:
      - The user name to connect to the remote ibm i node.
    type: str
    required: yes
  remote_host:
    description:
      - The remote ibm i node address.
      - Can be IP or host name.
    type: str
    required: yes
  private_key:
    description:
      - Specifies SSH private key used to connect to remote ibm i host.
      - The path can be absolute or relative.
    type: path
    default: '~/.ssh/id_rsa'

notes:
    - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3
    - Make sure ssh passwordless login works from ibm i node A to ibm i node B
    - private_key must be a rsa key in the legacy PEM private key format
    - Doesn't support IASP by now

author:
    - Peng Zeng Yu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Synchronize c1 save file to host.com
  ibmi_sync:
    src: '/qsys.lib/test.lib/c1.file'
    remote_host: 'host.com'
    remote_user: 'user'
    private_key: '/home/test/id_rsa'
'''

RETURN = r'''
delta:
    description: The execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The standard output
    returned: always
    type: str
    sample: 'Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com'
stderr:
    description: The standard error
    returned: always
    type: str
    sample: 'Failed to mv file to qsys. Make sure library exists.'
rc:
    description: The action return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The standard output split in lines
    returned: always
    type: list
    sample: ['Successfully synchronize file /QSYS.LIB/TEST.LIB/C1.FILE to remote host host.com']
stderr_lines:
    description: The standard error split in lines
    returned: always
    type: list
    sample: ['Failed to mv file to qsys. Make sure library exists.']
'''

import os
import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_native, to_text

HAS_PARAMIKO = True

try:
    import paramiko
except ImportError:
    HAS_PARAMIKO = False

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255

ifs_dir = '/tmp/.ansible/'


def return_error(module, error, result):
    result['stderr'] = error
    result['rc'] = IBMi_COMMAND_RC_ERROR
    module.exit_json(**result)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='str', required=True),
            dest=dict(type='str', default=''),
            remote_user=dict(type='str', required=True),
            remote_host=dict(type='str', required=True),
            private_key=dict(type='path', default='~/.ssh/id_rsa')
        ),
        supports_check_mode=True,
    )
    result = dict(
        stdout='',
        stderr='',
        rc=0,
        delta='',
    )

    try:
        if HAS_PARAMIKO is False:
            module.fail_json(msg="paramiko package is required", rc=IBMi_COMMAND_RC_ERROR)

        src = module.params['src']
        dest = module.params['dest']
        remote_user = module.params['remote_user']
        remote_host = module.params['remote_host']
        private_key = module.params['private_key']

        startd = datetime.datetime.now()
        if os.path.splitext(os.path.basename(src))[-1].upper() != '.FILE':
            return_error(module, "src %s is not a save file. src must be end with '.FILE'." % src, result)
        if src[0:9].upper() != '/QSYS.LIB':
            return_error(module, "src %s must be a ibm i native save file, the path should be absolute, start with /QSYS.LIB."
                         % src, result)

        if dest == '':
            dest = src
        if dest[0:9].upper() != '/QSYS.LIB':
            return_error(module, "dest %s path should be absolute, start with /QSYS.LIB."
                         % dest, result)

        # Check if the savefile exists
        if not os.path.isfile(src):
            return_error(module, "src doesn't exist. %s" % src, result)

        rc, out, err = module.run_command(['mkdir', ifs_dir], use_unsafe_shell=False)
        if rc is 0 or 'File exists' in err:
            rc, out, err = module.run_command(['cp', src, ifs_dir], use_unsafe_shell=False)
            if rc is 0:
                src_basename = os.path.basename(src)
                ifs_name = ifs_dir + src_basename
                private_key = to_bytes(private_key, errors='surrogate_or_strict')
                p_key = paramiko.RSAKey.from_private_key_file(private_key)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(hostname=remote_host, port=22, username=remote_user, pkey=p_key)

                transport = paramiko.Transport((remote_host, 22))
                transport.connect(username=remote_user, pkey=p_key)
                sftp = paramiko.SFTPClient.from_transport(transport)
                stdin, stdout, stderr = ssh.exec_command('mkdir %s' % ifs_dir)
                line = stderr.readlines()
                if line != [] and 'File exists' not in "".join(line):
                    return_error(module, "Failed to mkdir on remote host, dir = %s. %s" % (ifs_dir, line), result)
                try:
                    sftp.put(ifs_name, ifs_name)
                except Exception as e:
                    return_error(module, "Put %s to remote host exception. Use -vvv for more information." % to_text(e), result)

                stdin, stdout, stderr = ssh.exec_command('mv %s %s' % (ifs_name, dest))
                line = stderr.readlines()
                if line != []:
                    return_error(module,
                                 "Failed to mv file to qsys. Make sure library exists and savf is not in use. qsys dir = %s. %s"
                                 % (dest, line), result)
            else:
                return_error(module, "Copy file to current host tmp dir failed. Make sure file is not in use. cp %s %s. %s" %
                             (src, ifs_dir, err), result)
        else:
            return_error(module, "mkdir on current host failed. dir = %s. %s" % (ifs_dir, err), result)

        endd = datetime.datetime.now()
        delta = endd - startd
        result['stdout'] = "Successfully synchronize file %s to remote host %s:%s" % (src, remote_host, dest)
        result.update({'stderr': err, 'rc': rc, 'delta': str(delta)})
        module.exit_json(**result)

    except Exception as e:
        return_error(module, "Unexpected exception happens. error: %s. Use -vvv for more information." % to_text(e), result)
    finally:
        if 'ssh' in vars():
            ssh.close()
        if 'sftp' in vars():
            sftp.close()


if __name__ == '__main__':
    main()
