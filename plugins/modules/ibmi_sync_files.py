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
module: ibmi_sync_files
short_description: Synchronize a list of files from current IBM i node A to another IBM i node B.
version_added: '1.1.0'
description:
     - The C(ibmi_sync_files) module synchronize a list of files from current IBM i node to another IBM i node.
     - Only supports SAVF(.file) and MBR(only supports "database" subtype Physical files(PF-DTA attribute)) format synchronize between QSYS and QSYS.
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
    - Dependency PTFs
      7.2 MF65149
      7.3 MF65148
    - Doesn't support IASP by now.

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Synchronize a list of different types of files to host.com.
  ibm.power_ibmi.ibmi_sync_files:
    src_list:
      - {'src': '/tmp/c1.file', 'dest': '/qsys.lib/test.lib/'}
      - {'src': '/qsys.lib/test.lib/test.file', 'dest': '/qsys.lib/test.lib'}
      - {'src': '/tmp/c2.SAVF', 'dest': '/qsys.lib/test.lib/'}
      - {'src': '/tmp/c3.bin', 'dest': '/test/dir'}
      - {'src': '/qsys.lib/c4.file/test.mbr', 'dest': '/qsys.lib/test.lib/c5.file'}
      - {'src': '~/c6.txt', 'dest': '~/testfolder'}
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
msg:
    description: The general message returned.
    returned: always
    type: str
    sample: 'No files were successfully transferred.'
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

import os
import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_bytes, to_text
from tempfile import mkdtemp
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
__ibmi_module_version__ = "2.0.1"
HAS_PARAMIKO = True

try:
    import paramiko
except ImportError:
    HAS_PARAMIKO = False


def return_error(module, error, result):
    result['stderr'] = error
    result['rc'] = ibmi_util.IBMi_COMMAND_RC_ERROR
    module.fail_json(**result)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src_list=dict(type='list', required=True, elements='dict'),
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
        success_list=[],
        fail_list=[],
        msg=''
    )

    try:
        if HAS_PARAMIKO is False:
            module.fail_json(msg="paramiko package is required", rc=ibmi_util.IBMi_COMMAND_RC_ERROR)

        src_list = module.params['src_list']
        dest = module.params['dest']
        remote_user = module.params['remote_user']
        remote_host = module.params['remote_host']
        private_key = module.params['private_key']
        success_list = []
        fail_list = []
        startd = datetime.datetime.now()

        ifs_dir = mkdtemp("", "ansible_for_i_temp", None)
        ibmi_util.log_debug("mkdtemp " + ifs_dir, module._name)
        if not os.path.isdir(ifs_dir):
            return_error(module, f"mkdtemp on current host failed. dir = {ifs_dir}.", result)

        try:
            private_key = to_bytes(private_key, errors='surrogate_or_strict')
            p_key = paramiko.RSAKey.from_private_key_file(private_key)
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=remote_host, port=22, username=remote_user, pkey=p_key)
            transport = paramiko.Transport((remote_host, 22))
            transport.connect(username=remote_user, pkey=p_key)
            sftp = paramiko.SFTPClient.from_transport(transport)
        except Exception as e:
            for i in range(len(src_list)):
                src_list[i]['fail_reason'] = f"{to_text(e)}. "
            result.update({'fail_list': src_list})
            return_error(module, f"Exception. {to_text(e)}. Use -vvv for more information.", result)

        if dest:
            if dest.startswith('~'):
                stdin1, stdout1, stderr1 = ssh.exec_command("echo $HOME")
                dest_home_path = stdout1.read().decode('utf-8')
                if dest_home_path is None:
                    return_error(module, "Get the dest 'HOME' path failed. ", result)
                dest = os.path.join(dest_home_path.strip(), os.path.relpath(dest, '~/'))
            try:
                sftp.stat(dest)
            except Exception as e:
                if 'No such file' in to_text(e):
                    return_error(module, f"dest: {dest} is not a directory.", result)
                return_error(module, f"Exception. {to_text(e)}. Use -vvv for more information.", result)

        for i in range(len(src_list)):
            final_dest = dest
            src_basename = os.path.basename(src_list[i]['src'])
            if final_dest == '':
                if 'dest' in src_list[i]:
                    final_dest = src_list[i]['dest']
            if final_dest == '':
                final_dest = os.path.dirname(os.path.realpath(src_list[i]['src']))

            if final_dest[0:9].upper() == '/QSYS.LIB' and not os.path.isdir(src_list[i]['src']):
                if os.path.splitext(src_basename)[-1].upper() == '.MBR':
                    final_dest = (final_dest + '/' + src_basename).replace("//", "/")
                else:
                    final_dest = (final_dest + '/' + os.path.splitext(src_basename)[0] + '.FILE').replace("//", "/")
            else:
                final_dest = (final_dest + '/' + src_basename).replace("//", "/")

            if final_dest.startswith('~'):
                stdin1, stdout1, stderr1 = ssh.exec_command("echo $HOME")
                dest_home_path = stdout1.read().decode('utf-8')
                if dest_home_path is None:
                    return_error(module, "Get the dest 'HOME' path failed. ", result)
                final_dest = os.path.join(dest_home_path.strip(), os.path.relpath(final_dest, '~/'))

            if src_list[i]['src'][0:9].upper() == '/QSYS.LIB' and os.path.splitext(src_basename)[-1].upper() != '.MBR':
                ibmi_util.log_debug("cp " + src_list[i]['src'] + " " + ifs_dir, module._name)
                rc, out, err = module.run_command(['cp', src_list[i]['src'], ifs_dir], use_unsafe_shell=False)
                if rc == 0:
                    final_src = ifs_dir + "/" + src_basename
                else:
                    src_list[i]['fail_reason'] = f"Copy file to current host tmp dir failed. cp {src_list[i]['src']} {ifs_dir}. {err}"
                    fail_list.append(src_list[i])
                    continue
            elif src_list[i]['src'].startswith('~'):
                src_home_path = os.getenv('HOME', None)
                if src_home_path is None:
                    return_error(module, "getenv 'HOME' failed. ", result)
                final_src = os.path.join(src_home_path, os.path.relpath(src_list[i]['src'], '~/'))
            else:
                final_src = src_list[i]['src']

            try:
                ibmi_util.log_debug("sftp: put " + final_src + " " + final_dest, module._name)
                if final_dest[0:9].upper() != '/QSYS.LIB':
                    try:
                        sftp.mkdir(os.path.dirname(final_dest))
                    except Exception as e:
                        ibmi_util.log_debug(f"sftp: mkdir failed. Dir may be exist. Error: {to_text(e)}")
                sftp.put(final_src, final_dest)
                success_list.append(src_list[i])
            except Exception as e:
                if 'size mismatch' in to_text(e):
                    src_list[i]['fail_reason'] = f"Can't sync file to /QSYS.LIB. Put {final_src} to remote host fail. Error message: {to_text(e)}"
                else:
                    src_list[i]['fail_reason'] = f"{to_text(e)}. Put {final_src} to remote host exception."
                fail_list.append(src_list[i])

        endd = datetime.datetime.now()
        delta = endd - startd
        if success_list:
            result['msg'] = f"Complete synchronize file list to remote host {remote_host}"
            result.update({'stderr': '', 'rc': 0, 'delta': str(delta), 'success_list': success_list, 'fail_list': fail_list})
            module.exit_json(**result)
        else:
            result['msg'] = "No files were successfully transferred."
            result.update({'stderr': '', 'rc': 255, 'delta': str(delta), 'success_list': success_list, 'fail_list': fail_list})
            module.fail_json(**result)

    except Exception as e:
        return_error(module, f"Exception. {to_text(e)}. Use -vvv for more information.", result)
    finally:
        if 'ssh' in vars():
            ssh.close()
        if 'sftp' in vars():
            sftp.close()
        rc, out, err = module.run_command(['rm', '-rf', ifs_dir], use_unsafe_shell=False)


if __name__ == '__main__':
    main()
