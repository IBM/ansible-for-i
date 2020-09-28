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
module: ibmi_at
short_description: Schedule a batch job
version_added: '2.8.0'
description:
     - The C(ibmi_at) module schedule a batch job.
options:
  job_name:
    description:
      - Specifies the name of the job schedule entry.
    type: str
    required: yes
  cmd:
    description:
      - Specifies the command that runs in the submitted job.
    type: str
    required: yes
  frequency:
    description:
      - Specifies how often the job is submitted.
    type: str
    required: yes
    choices: ['*ONCE', '*WEEKLY', '*MONTHLY']
  scddate:
    description:
      - Specifies the date on which the job is submitted.
    type: str
    default: '*CURRENT'
  scdday:
    description:
      - Specifies the day of the week on which the job is submitted.
      - The valid value are C(*NONE), C(*ALL), C(*MON), C(*TUE), C(*WED), C(*THU), C(*FRI), C(*SAT), C(*SUN).
    type: list
    elements: str
    default: "*NONE"
  schtime:
    description:
      - Specifies the time on the scheduled date at which the job is submitted.
    type: str
    default: '*CURRENT'
  text:
    description:
      - Specifies text that briefly describes the job schedule entry.
    type: str
    default: '*BLANK'
  parameters:
    description:
      - The parameters that ADDJOBSCDE command will take. Other than options above, all other parameters need to be specified
        here.
      - The default values of parameters for ADDJOBSCDE will be taken if not specified.
    type: str
    default: ''
  joblog:
    description:
      - If set to C(true), output the avaiable JOBLOG even the rc is 0(success).
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
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Add a job schedule entry test with become user.
  ibmi_at:
    job_name: 'test'
    cmd: 'QSYS/WRKSRVAGT TYPE(*UAK)'
    frequency: '*WEEKLY'
    scddate: '*CURRENT'
    text: 'Test job schedule'
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
command:
    description: The execution command.
    returned: always
    type: str
    sample: "QSYS/ADDJOBSCDE JOB(RUNCOM) CMD(QBLDSYSR/CHGSYSSEC OPTION(*CHGPW)) FRQ(*WEEKLY) SCDDATE(*CURRENT) SCDDAY(*NONE) \
             SCDTIME(*CURRENT) TEXT(*BLANK) "
msg:
    description: The execution message.
    returned: always
    type: str
    sample: 'Either scddate or scdday need to be *NONE.'
delta:
    description: The execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The standard output.
    returned: always
    type: str
    sample: 'CPC1238: Job schedule entry TEST number 000074 added.'
stderr:
    description: The standard error.
    returned: always
    type: str
    sample: 'CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n'
rc:
    description: The action return code. 0 means success.
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The standard output split in lines.
    returned: always
    type: list
    sample: [
        "CPC1238: Job schedule entry TEST number 000074 added."
    ]
stderr_lines:
    description: The standard error split in lines.
    returned: always
    type: list
    sample: [
        "CPF5813: File archive in library archlib already exists.",
        "CPF7302: File archive not created in library archlib."
    ]
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "8873",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "QSQSRVR",
            "FROM_PROCEDURE": "QSQSRVR",
            "FROM_PROGRAM": "QSQSRVR",
            "FROM_USER": "TESTER",
            "MESSAGE_FILE": "",
            "MESSAGE_ID": "",
            "MESSAGE_LIBRARY": "",
            "MESSAGE_SECOND_LEVEL_TEXT": "",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "User Profile = TESTER",
            "MESSAGE_TIMESTAMP": "2020-05-25-12.40.00.690270",
            "MESSAGE_TYPE": "COMPLETION",
            "ORDINAL_POSITION": "8",
            "SEVERITY": "0",
            "TO_INSTRUCTION": "8873",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
        }]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
__ibmi_module_version__ = "1.1.2"
scdday_list = ['*NONE', '*ALL', '*MON', '*TUE', '*WED', '*THU', '*FRI', '*SAT', '*SUN']


def main():
    module = AnsibleModule(
        argument_spec=dict(
            job_name=dict(type='str', required=True),
            cmd=dict(type='str', required=True),
            frequency=dict(type='str', required=True, choices=['*ONCE', '*WEEKLY', '*MONTHLY']),
            scddate=dict(type='str', default='*CURRENT'),
            scdday=dict(type='list', elements='str', default='*NONE'),
            schtime=dict(type='str', default='*CURRENT'),
            text=dict(type='str', default='*BLANK'),
            parameters=dict(type='str', default=''),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    job_name = module.params['job_name']
    cmd = module.params['cmd']
    frequency = module.params['frequency']
    scddate = module.params['scddate']
    scdday = module.params['scdday']
    schtime = module.params['schtime']
    text = module.params['text']
    parameters = module.params['parameters']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if scddate not in ["*CURRENT", "*MONTHSTR", "*MONTHEND", "*NONE"]:
        scddate = "'{p_scddate}'".format(p_scddate=scddate)
    if schtime != "*CURRENT":
        schtime = "'{p_schtime}'".format(p_schtime=schtime)
    if text != "*BLANK":
        text = "'{p_text}'".format(p_text=text)
    result = dict(
        command='',
        stdout='',
        stderr='',
        rc='',
        delta='',
        msg='',
        job_log=[]
    )

    if set(scdday) < set(scdday_list):
        pass
    else:
        result.update({'msg': 'Value specified for scdday is not valid. Valid values are {p_scdday_list}'.format(
            p_scdday_list=", ".join(scdday_list)),
            'stderr': 'Parameter passed is not valid.',
            'rc': ibmi_util.IBMi_PARAM_NOT_VALID})
        module.fail_json(**result)

    scdday = " ".join(scdday)
    if scddate != '*NONE' and scdday != '*NONE':
        result['msg'] = 'Either scddate or scdday need to be *NONE.'

    if scddate == '*NONE' and scdday == '*NONE':
        result['msg'] = 'scddate and scdday cannot be *NONE at the sametime.'

    if result.get('msg'):
        module.fail_json(**result)

    startd = datetime.datetime.now()
    command = 'QSYS/ADDJOBSCDE JOB({p_job_name}) CMD({p_cmd}) FRQ({p_frequency}) SCDDATE({p_scddate}) SCDDAY({p_scdday}) \
        SCDTIME({p_schtime}) TEXT({p_text}) {p_parameters}'.format(
        p_job_name=job_name,
        p_cmd=cmd,
        p_frequency=frequency,
        p_scddate=scddate,
        p_scdday=scdday,
        p_schtime=schtime,
        p_text=text,
        p_parameters=parameters)

    try:
        ibmi_module = imodule.IBMiModule(become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    rc, out, error, job_log = ibmi_module.itoolkit_run_command_once(command)
    endd = datetime.datetime.now()
    delta = endd - startd

    if rc:
        result.update({'msg': 'Failed to add Job schedule entry {p_job_name}. Please double check the input.'.format(
            p_job_name=job_name),
            'command': ' '.join(command.split()),
            'stdout': out,
            'stderr': error,
            'rc': rc,
            'delta': str(delta),
            'job_log': job_log})
        module.fail_json(**result)
    elif joblog:
        result.update({'msg': 'Job schedule entry {p_job_name} is successfully added.'.format(
            p_job_name=job_name),
            'command': ' '.join(command.split()),
            'stdout': out,
            'stderr': error,
            'rc': rc,
            'delta': str(delta),
            'job_log': job_log})
        module.exit_json(**result)
    else:
        result.update({'msg': 'Job schedule entry {p_job_name} is successfully added.'.format(
            p_job_name=job_name),
            'command': ' '.join(command.split()),
            'stdout': out, 'stderr': error,
            'rc': rc,
            'delta': str(delta)})
        module.exit_json(**result)


if __name__ == '__main__':
    main()
