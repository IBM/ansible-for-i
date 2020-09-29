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
module: ibmi_script_execute
short_description: Execute a cl/sql script file
version_added: '2.8.0'
description:
     - The C(ibmi_script_execute) module execute a cl/sql script file on a remote ibm i node.
     - Only support cl/sql script file by now.
     - For sql script, use RUNSQLSTM to process.
     - For non-cl/sql script, use the script plugin instead.
options:
  src:
    description:
      - Script file path on the remote ibm i node.
      - The path can be absolute or relative.
    type: path
    required: yes
  type:
    description:
      - Specify the script file type.
      - Only support C(CL) or C(SQL) script by now.
    type: str
    required: yes
    choices: ["CL", "SQL"]
  asp_group:
     description:
       - Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.
       - The ASP group name is the name of the primary ASP device within the ASP group.
     type: str
     default: '*SYSBAS'
  severity_level:
     description:
       - When run sql script, specifies whether the processing is successful, based on the severity of the messages generated
         by the processing of the SQL statements.
       - If errors that are greater than the value specified for this parameter occur during processing, no more statements are
         run and the statements are rolled back if they are running under commitmentcontrol.
       - Only works for sql script.
     type: int
     default: 10
  parameters:
    description:
      - The parameters that RUNSQLSTM command will take. All other parameters need to be specified here.
      - The default values of parameters for RUNSQLSTM will be taken if not specified.
      - Only works for sql script.
    type: str
    default: ' '
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str

notes:
    - For cl script, the command supports line breaks.
    - When a command ends, add ':' at the end of each command or empty the next line.
    - Otherwise program will not consider it is the end of a command.

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Execute test.cl on a remote IBM i node with become user.
  ibmi_script_execute:
    src: '/home/test.cl'
    type: 'CL'
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: Execute testsql.sql on a remote IBM i node.
  ibmi_script_execute:
    src: '/home/testsql.sql'
    type: 'SQL'
    severity_level: 40
    parameters: 'DATFMT(*USA)'
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
    sample: 'Successfully execute script file /home/test.cl'
stderr:
    description: The standard error.
    returned: always
    type: str
    sample: 'Execute command %s failed.'
rc:
    description: The action return code. 0 means success.
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The standard output split in lines.
    returned: always
    type: list
    sample: ['Successfully execute script file /home/test.cl']
stderr_lines:
    description: The standard error split in lines.
    returned: always
    type: list
    sample: ['Execute command %s failed.']
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
            "MESSAGE_TIMESTAMP": "2020-05-27-16.17.43.738571",
            "MESSAGE_TYPE": "COMPLETION",
            "ORDINAL_POSITION": "13",
            "SEVERITY": "0",
            "TO_INSTRUCTION": "5829",
            "TO_LIBRARY": "QXMLSERV",
            "TO_MODULE": "PLUGILE",
            "TO_PROCEDURE": "ILECMDEXC",
            "TO_PROGRAM": "XMLSTOREDP"
        }]
'''

import os
import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
__ibmi_module_version__ = "1.1.2"


def return_error(module, ibmi_module, error, out, startd, result):
    job_log = ibmi_module.itoolkit_get_job_log(startd)
    result.update({'rc': ibmi_util.IBMi_COMMAND_RC_ERROR, 'stderr': error, 'stdout': out, 'job_log': job_log})
    module.exit_json(**result)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='path', required=True),
            asp_group=dict(type='str', default='*SYSBAS'),
            severity_level=dict(type='int', default=10),
            type=dict(type='str', required=True, choices=['CL', 'SQL']),
            parameters=dict(type='str', default=' '),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    result = dict(
        stdout='',
        stderr='',
        rc=0,
        delta='',
        job_log=[]
    )

    try:
        src = module.params['src']
        type = module.params['type']
        severity_level = module.params['severity_level']
        asp_group = module.params['asp_group'].strip().upper()
        parameters = module.params['parameters']
        become_user = module.params['become_user']
        become_user_password = module.params['become_user_password']

        startd = datetime.datetime.now()

        try:
            ibmi_module = imodule.IBMiModule(
                db_name=asp_group, become_user_name=become_user, become_user_password=become_user_password)
        except Exception as inst:
            message = 'Exception occurred: {0}'.format(str(inst))
            module.fail_json(rc=999, msg=message)

        src = os.path.realpath(src)
        if not os.path.isfile(src):
            return_error(module, ibmi_module, "src {p_src} doesn't exist.".format(p_src=src), '', startd, result)

        f = open(src, "r")
        if not f:
            return_error(module, ibmi_module, "Can't open src {p_src}.".format(p_src=src), '', startd, result)

        command = ''
        if type == 'CL':
            for line in f:
                line_command = line.strip()
                if line_command != '':
                    if not line_command.endswith(":"):
                        command = command + line_command + ' '
                    else:
                        if line_command.endswith(":"):
                            command = command + line_command[:-1]
                        else:
                            command = command + line_command
                        rc, out, error = ibmi_module.itoolkit_run_command(command)
                        if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                            break
                        command = ''
                elif command != '':
                    rc, out, error = ibmi_module.itoolkit_run_command(command)
                    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                        break
                    command = ''
            if command != '':
                rc, out, error = ibmi_module.itoolkit_run_command(command)
                ibmi_util.log_debug("run command: " + command, module._name)
        else:
            command = "QSYS/RUNSQLSTM SRCSTMF('{p_src}') ERRLVL({p_severity_level}) {p_parameters}".format(
                p_src=src,
                p_severity_level=severity_level,
                p_parameters=parameters)
            rc, out, error = ibmi_module.itoolkit_run_command(command)
            ibmi_util.log_debug("RUNSQLSTM: " + command, module._name)
            if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
                return_error(module, ibmi_module, "Execute sql statement file {p_command} failed. err: \n {p_err}".format(
                    p_command=command,
                    p_err=error),
                    out,
                    startd,
                    result)

        endd = datetime.datetime.now()
        delta = endd - startd
        if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
            return_error(module, ibmi_module, "Execute command {p_command} failed. err: {p_err}".format(
                p_command=command,
                p_err=error),
                out,
                startd,
                result)
        result['stdout'] = "Successfully execute script file."
        result.update({'rc': rc, 'delta': str(delta)})
        module.exit_json(**result)

    except Exception as e:
        result.update({'rc': ibmi_util.IBMi_COMMAND_RC_ERROR,
                      'stderr': "Unexpected exception happens. error: {p_to_text}. Use -vvv for more information.".format(
                          p_to_text=to_text(e))})
        module.fail_json(**result)


if __name__ == '__main__':
    main()
