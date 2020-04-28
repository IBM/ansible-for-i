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
module: ibmi_at
short_description: Schedule a batch job on a remote IBMi node
version_added: 1.0
description:
     - The ibmi_at module schedule a batch job on a remote IBMi node
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
      - The valid value are '*NONE', '*ALL', '*MON', '*TUE', '*WED', '*THU', '*FRI', '*SAT', '*SUN'.
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
      - The parameters that ADDJOBSCDE command will take. Other than options above, all other parameters need to be specified here.
        The default values of parameters for ADDJOBSCDE will be taken if not specified.
    type: str
    default: ''
  joblog:
    description:
      - If set to C(true), append JOBLOG to stderr/stderr_lines.
    type: bool
    default: False

notes:
    - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)

author:
    - Peng Zeng Yu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Add a job schedule entry test
  ibmi_at:
    job_name: 'test'
    cmd: 'QSYS/WRKSRVAGT TYPE(*UAK)'
    frequency: '*WEEKLY'
    scddate: '*CURRENT'
    text: 'Test job schedule'
'''

RETURN = r'''
command:
    description: The execution command
    returned: always
    type: str
    sample: "QSYS/ADDJOBSCDE JOB(fish) CMD(QBLDSYSR/CHGSYSSEC OPTION(*CHGPW)) FRQ(*WEEKLY) SCDDATE(*CURRENT) SCDDAY(*NONE) \
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
    description: The standard output
    returned: always
    type: str
    sample: 'CPC1238: Job schedule entry TEST number 000074 added.'
stderr:
    description: The standard error
    returned: always
    type: str
    sample: 'CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n'
rc:
    description: The action return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The standard output split in lines
    returned: always
    type: list
    sample: [
        "CPC1238: Job schedule entry TEST number 000074 added."
    ]
stderr_lines:
    description: The standard error split in lines
    returned: always
    type: list
    sample: [
        "CPF5813: File archive in library archlib already exists.",
        "CPF7302: File archive not created in library archlib."
    ]
'''

import datetime

from ansible.module_utils.basic import AnsibleModule

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit import iCmd
    from itoolkit.transport import DirectTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_PARAM_NOT_VALID = 259
scdday_list = ['*NONE', '*ALL', '*MON', '*TUE', '*WED', '*THU', '*FRI', '*SAT', '*SUN']


def itoolkit_run_command(command):
    conn = dbi.connect()
    itransport = DirectTransport()
    itool = iToolKit()
    itool.add(iCmd('command', command, {'error': 'on'}))
    itool.call(itransport)

    rc = IBMi_COMMAND_RC_UNEXPECTED
    out = ''
    err = ''

    command_output = itool.dict_out('command')

    if 'success' in command_output:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['success']

    elif 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output \
                  is %s" % command_output
    else:
        # should not be here, must xmlservice has internal error
        rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
        err = "iToolKit result dict does not have key 'error', the output is \
              %s" % command_output

    return rc, out, err


def run_command(module, command, joblog):
    if joblog is True:
        rc, out, err = itoolkit_run_command(command)
    else:
        rc, out, err = module.run_command(['system', command], use_unsafe_shell=False)
    return rc, out, err


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
            joblog=dict(type='bool', default=False)
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    job_name = module.params['job_name']
    cmd = module.params['cmd']
    frequency = module.params['frequency']
    scddate = module.params['scddate']
    scdday = module.params['scdday']
    schtime = module.params['schtime']
    text = module.params['text']
    parameters = module.params['parameters']
    joblog = module.params['joblog']

    if scddate not in ["*CURRENT", "*MONTHSTR", "*MONTHEND", "*NONE"]:
        scddate = "'" + scddate + "'"
    if schtime != "*CURRENT":
        schtime = "'" + schtime + "'"
    if text != "*BLANK":
        text = "'" + text + "'"
    result = dict(
        command='',
        stdout='',
        stderr='',
        rc='',
        delta='',
    )

    if set(scdday) < set(scdday_list):
        pass
    else:
        result.update({'msg': 'Value specified for scdday is not valid. Valid values are ' + ", ".join(scdday_list),
                       'stderr': 'Parameter passed is not valid.', 'rc': IBMi_PARAM_NOT_VALID})
        module.fail_json(**result)

    scdday = " ".join(scdday)
    if scddate != '*NONE' and scdday != '*NONE':
        result['msg'] = 'Either scddate or scdday need to be *NONE.'

    if scddate == '*NONE' and scdday == '*NONE':
        result['msg'] = 'scddate and scdday cannot be *NONE at the sametime.'

    if result.get('msg'):
        module.fail_json(**result)

    startd = datetime.datetime.now()
    command = 'QSYS/ADDJOBSCDE JOB(%s) CMD(%s) FRQ(%s) SCDDATE(%s) SCDDAY(%s) SCDTIME(%s) TEXT(%s) %s' % (job_name, cmd,
                                                                                                          frequency, scddate,
                                                                                                          scdday, schtime, text,
                                                                                                          parameters)
    rc, out, err = run_command(module, command, joblog)
    endd = datetime.datetime.now()
    delta = endd - startd

    result.update({'command': command, 'stdout': out, 'stderr': err,
                   'rc': rc, 'delta': str(delta)})

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result['msg'] = 'Failed to add Job schedule entry %s. Please double check the input.' % job_name
        module.fail_json(**result)

    result['msg'] = 'Job schedule entry %s is successfully added.' % job_name
    module.exit_json(**result)


if __name__ == '__main__':
    main()
