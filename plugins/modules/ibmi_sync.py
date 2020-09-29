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
module: ibmi_sync
short_description: Synchronize a save file from current IBM i node A to another IBM i node B.
version_added: '2.8.0'
description:
     - The C(ibmi_sync) module synchronize a save file from current IBM i node to another IBM i node.
     - Only support to synchronize save file by now.
     - For non-IBMi native targets, use the synchronize module instead.
options:
  src:
    description:
      - Save file path on the source host that will be synchronized to the destination.
      - The path must be absolute, and src must be a IBM i native library. For example, /qsys.lib/test.lib/c1.file.
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
      - The user name to connect to the remote IBM i node.
    type: str
    required: yes
  remote_host:
    description:
      - The remote IBM i node address.
      - Can be IP or host name.
    type: str
    required: yes
  private_key:
    description:
      - Specifies SSH private key used to connect to remote IBM i host.
      - The path can be absolute or relative.
    type: path
    default: '~/.ssh/id_rsa'

notes:
    - Need install paramiko package on target IBM i.
    - Make sure ssh passwordless login works from IBM i node A to IBM i node B.
    - private_key must be a rsa key in the legacy PEM private key format.
    - Doesn't support IASP by now.

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Synchronize c1 save file to host.com.
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

import os
import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_text
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
__ibmi_module_version__ = "1.1.2"
HAS_PARAMIKO = True

try:
    import paramiko
except ImportError:
    HAS_PARAMIKO = False

ifs_dir = '/tmp/.ansible/'


def return_error(module, error, result):
    result['stderr'] = error
    result['rc'] = ibmi_util.IBMi_COMMAND_RC_ERROR
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
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    result = dict(
        stdout='',
        stderr='',
        rc=0,
        delta='',
    )

    try:
        if HAS_PARAMIKO is False:
            module.fail_json(msg="paramiko package is required", rc=ibmi_util.IBMi_COMMAND_RC_ERROR)

        src = module.params['src']
        dest = module.params['dest']
        remote_user = module.params['remote_user']
        remote_host = module.params['remote_host']
        private_key = module.params['private_key']

        startd = datetime.datetime.now()
        if os.path.splitext(os.path.basename(src))[-1].upper() != '.FILE':
            return_error(module, "src {p_src} is not a save file. src must be end with '.FILE'.".format(p_src=src), result)
        if src[0:9].upper() != '/QSYS.LIB':
            return_error(module, "src {p_src} path should be absolute, start with /QSYS.LIB.".format(p_src=src), result)

        if dest == '':
            dest = src
        if dest[0:9].upper() != '/QSYS.LIB':
            return_error(module, "dest {p_dest} path should be absolute, start with /QSYS.LIB.".format(p_dest=dest), result)

        # Check if the savefile exists
        if not os.path.isfile(src):
            return_error(module, "src doesn't exist. {p_src}".format(p_src=src), result)

        ibmi_util.log_debug("mkdir " + ifs_dir, module._name)
        rc, out, err = module.run_command(['mkdir', ifs_dir], use_unsafe_shell=False)
        if rc == 0 or 'File exists' in err:
            ibmi_util.log_debug("cp " + src + " " + ifs_dir, module._name)
            rc, out, err = module.run_command(['cp', src, ifs_dir], use_unsafe_shell=False)
            if rc == 0:
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
                stdin, stdout, stderr = ssh.exec_command('mkdir {p_ifs_dir}'.format(p_ifs_dir=ifs_dir))
                line = stderr.readlines()
                if line != [] and 'File exists' not in "".join(line):
                    return_error(module, "Failed to mkdir on remote host, dir = {p_ifs_dir}. {p_line}".format(
                        p_ifs_dir=ifs_dir,
                        p_line=line), result)
                try:
                    ibmi_util.log_debug("sftp: put " + ifs_name + " " + ifs_name, module._name)
                    sftp.put(ifs_name, ifs_name)
                except Exception as e:
                    return_error(module, "Put {p_to_text} to remote host exception. Use -vvv for more information.".format(
                        p_to_text=to_text(e)), result)

                ibmi_util.log_debug("mv " + ifs_name + " " + dest, module._name)
                stdin, stdout, stderr = ssh.exec_command('mv {p_ifs_name} {p_dest}'.format(p_ifs_name=ifs_name, p_dest=dest))
                line = stderr.readlines()
                if line != []:
                    return_error(module, "Failed to mv file to qsys. qsys dir = {p_dest}. {p_line}".format(
                        p_dest=dest, p_line=line), result)
            else:
                return_error(module,
                             "Copy file to current host tmp dir failed. cp {p_src} {p_ifs_dir}. {p_err}".format(
                                 p_src=src, p_ifs_dir=ifs_dir, p_err=err), result)
        else:
            return_error(module, "mkdir on current host failed. dir = {p_ifs_dir}. {p_err}".format(
                p_ifs_dir=ifs_dir, p_err=err), result)

        endd = datetime.datetime.now()
        delta = endd - startd
        result['stdout'] = "Successfully synchronize file {p_src} to remote host {p_remote_host}:{p_dest}".format(
            p_src=src, p_remote_host=remote_host, p_dest=dest)
        result.update({'stderr': err, 'rc': rc, 'delta': str(delta)})
        module.exit_json(**result)

    except Exception as e:
        return_error(module, "Unexpected exception happens. error: {p_to_text}. Use -vvv for more information.".format(
            p_to_text=to_text(e)), result)
    finally:
        if 'ssh' in vars():
            ssh.close()
        if 'sftp' in vars():
            sftp.close()


if __name__ == '__main__':
    main()
