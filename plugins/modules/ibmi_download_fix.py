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
module: ibmi_download_fix
short_description: Download fix through SNDPTFORD
version_added: '2.8.0'
description:
     - The C(ibmi_download_fix) module download fix through SNDPTFORD.
     - The supported fixs are individual PTFs, cumulative PTF package and PTF Groups.
options:
  ptf_id:
    description:
      - Specify the identifier of the PTF information being ordered.
      - For Cumulative PTF package and PTF group ID, please see
      - C(*CUMPKG)
        Order the latest level of the Cumulative PTF package group (SF99vrm) for the operating system release that is installed
        on the system. The HIPER and DB2 for IBM i PTF groups are automatically included when the Cumulative PTF package PTF
        group is specified. This value cannot be specified with any other PTF identifier or special value.
      - C(*ALLGRP)
        Order the latest level of all PTF groups for the installed operating system release, except the Cumulative PTF package group.
      - C(*HIPERGRP)
        Order the latest level of the HIPER PTF group for the operating system release that is installed on the system.
      - C(*DB2GRP)
        Order the latest level of the DB2 for IBM i PTF group for the operating system release that is installed on the system.
      - C(*BRSGRP)
        Order the latest level of the Backup Recovery Solutions PTF group for the operating system release that is installed on the system.
      - C(*HTTPGRP)
        Order the latest level of the IBM HTTP Server for i PTF group for the operating system release that is installed on the system.
      - C(*JVAGRP)
        Order the latest level of the Java PTF group for the operating system release that is installed on the system.
      - C(*PFRGRP)
        Order the latest level of the Performance Tools PTF group for the operating system release that is installed on the system.
    type: str
    required: yes
  product:
    description:
      - Specifies the product ID associated with the PTF.
    type: str
    default: '*ONLYPRD'
  release:
    description:
      - Specifies the release level of the PTF in one of the following formats,
        VxRyMz, where Vx is the version number, Ry is the release number, and Mz is the modification level.
        The variables x and y can be a number from 0 through 9, and the variable z can be a number from 0 through 9 or a letter
        from A through Z.
        vvrrmm, where version vv and release rr must be a number from 00 through 35, and modification mm must be a number from
        00 through 09 or a letter from 0A through 0Z.  The leading zeros are required.  This format must be used if the version
        or release of the product is greater than 9.
    type: str
    default: '*ONLYRLS'
  delivery_format:
    description:
      - Specifies the format of the delivered PTFs.
    type: str
    default: '*SAVF'
    choices: ['*SAVF', '*IMAGE']
  order:
     description:
       - Specifies if requisite PTFs should be included with the ordered PTFs.
     type: str
     default: '*REQUIRED'
     choices: ['*REQUIRED', '*PTFID']
  reorder:
     description:
       - Specifies whether a PTF that is currently loaded, applied, or on order should be ordered again.
     type: str
     default: '*YES'
     choices: ['*NO', '*YES']
  check_PTF:
     description:
       - Specifies whether checking is performed on the service requester system to determine if PTFs are ordered based on
         whether or not the PTF product is installed or supported.
     type: str
     default: '*NO'
     choices: ['*NO', '*YES']
  image_directory:
     description:
       - Specifies the directory where the optical image files are stored. If IMGCLG parameter is specified, the directory
         specified will be associated with the image catalog.
     type: str
     default: '*DFT'
  time_out:
     description:
       - The max time that the module waits for the SNDPTFORD command complete.
       - The unit can be 's', 'm', 'h', 'd' and 'w'.
     type: str
     default: '15m'
  wait:
    description:
      - Only works when delivery_format is C(*SAVF).
      - If delivery_format is C(*SAVF), and C(wait) set to C(true), module will wait until all PTF save files are delivered or
        time is up.
    type: bool
    default: True
  parameters:
    description:
      - The parameters that SNDPTFORD command will take. Other than options above, all other parameters need to be specified here.
      - The default values of parameters for SNDPTFORD will be taken if not specified.
    type: str
    default: ' '
  joblog:
    description:
      - If set to C(true), output the available joblog even the rc is 0(success).
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

notes:
    - Only support English language ibm i system, language ID 2924.
    - See SNDPTFORD command for more information.

author:
    - Peng Zengyu (@pengzengyufish)
'''

EXAMPLES = r'''
- name: Download a single PTF
  ibmi_download_fix:
    ptf_id: 'SI63556'
    reorder: '*YES'
    order: '*PTFID'

- name: Download a PTF group with become user
  ibmi_download_fix:
    ptf_id: 'SF99740'
    delivery_format: '*IMAGE'
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
delta:
    description: The module execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
stdout:
    description: The command standard output.
    returned: always
    type: str
    sample: 'PTF 5770UME-SI63556 V1R4M0 received and stored in library QGPL.'
stderr:
    description: The command standard error.
    returned: always
    type: str
    sample: 'CPD0043: Keyword LOGOUTPUT not valid for this command.\n'
command:
    description: The excuted SNDPTFORD command.
    returned: always
    type: str
    sample: 'QSYS/SBMJOB CMD(SNDPTFORD PTFID((SI63556 *ONLYPRD *ONLYRLS)) DLVRYFMT(*SAVF) ORDER(*PTFID) REORDER(*YES) CHKPTF(*NO))'
rc:
    description: The command action return code. 0 means success.
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The command standard output split in lines.
    returned: always
    type: list
    sample: [
        "CPC3703: 2 objects restored from test to test."
    ]
stderr_lines:
    description: The command standard error split in lines.
    returned: always
    type: list
    sample: [
        "CPD0043: Keyword LOGOUTPUT not valid for this command.",
        "CPD0099: Previous 1 errors found in embedded command SNDPTFORD.",
    ]
download_list:
    description: The successful downloaded fix list.
    returned: always
    type: list
    sample: [
        {
            "download_time": "2020-07-30T22:55:11.754388",
            "file_name": "QSI63556",
            "file_path": "/qsys.lib/qgpl.lib/QSI63556.FILE",
            "ptf_id": "SI63556",
            "product": "5770UME",
            "release": "V1R4M0",
            "order_id": "2348376546"
        }
    ]
order_id:
    description: The order identifier of the PTF order.
    returned: always
    type: int
    sample: 2021278656
msg:
    description: The general message returned.
    returned: always
    type: str
    sample: 'PTF order cannot be processed. See joblog'
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "54",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "QESECARE",
            "FROM_PROCEDURE": "SendMsg__FPcT1iT1",
            "FROM_PROGRAM": "QESECARE",
            "FROM_USER": "QSECOFR",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPI35F1",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "&N Cause . . . . . :   The cover letter has been copied to file QAPZCOVER in library
            QGPL with member name of QSI63556 from file *N member *N. &N Recovery  . . . :   Use the Display Program Temporary
            Fix (DSPPTF) command to display the cover letter. Specify product 5770UME, PTF SI63556, release  and request cover
            letter only.",
            "MESSAGE_SUBTYPE": null,
            "MESSAGE_TEXT": "Cover letter has been copied to file QAPZCOVER member QSI63556.",
            "MESSAGE_TIMESTAMP": "2020-07-30T22:55:12.865122",
            "MESSAGE_TYPE": "INFORMATIONAL",
            "ORDINAL_POSITION": 7,
            "SEVERITY": 0,
            "TO_INSTRUCTION": "54",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QESECARE",
            "TO_PROCEDURE": "SendMsg__FPcT1iT1",
            "TO_PROGRAM": "QESECARE"
        },
        {
            "FROM_INSTRUCTION": "54",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "QESECARE",
            "FROM_PROCEDURE": "SendMsg__FPcT1iT1",
            "FROM_PROGRAM": "QESECARE",
            "FROM_USER": "QSECOFR",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPZ8C12",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "&N Cause . . . . . :   Program temporary fix (PTF) SI63556 product 5770UME at release
            V1R4M0 was received and is stored in library QGPL.  Use the Display PTF (DSPPTF) command to view the status of the
            PTF on your system.",
            "MESSAGE_SUBTYPE": null,
            "MESSAGE_TEXT": "PTF 5770UME-SI63556 V1R4M0 received and stored in library QGPL.",
            "MESSAGE_TIMESTAMP": "2020-07-30T22:55:11.754388",
            "MESSAGE_TYPE": "INFORMATIONAL",
            "ORDINAL_POSITION": 6,
            "SEVERITY": 0,
            "TO_INSTRUCTION": "54",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QESECARE",
            "TO_PROCEDURE": "SendMsg__FPcT1iT1",
            "TO_PROGRAM": "QESECARE"
        },
]
'''

import datetime
import re
import time
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
__ibmi_module_version__ = "1.1.2"

HAS_ITOOLKIT = True

try:
    from itoolkit import iToolKit
    from itoolkit import iPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False


def remove_pending_joblog(conn, job_name, user_name, job_number):
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iPgm('qwtrmvjl', 'QWTRMVJL')
        .addParm(
            iDS('RJLS0100_t', {'len': 'rhrlen'})
            .addData(iData('length', '10i0', '44'))
            .addData(iData('day_since', '10i0', '0'))
            .addData(iData('job_name', '10A', job_name))
            .addData(iData('user_name', '10A', user_name))
            .addData(iData('job_number', '6A', job_number))
            .addData(iData('job_log_output', '10A', '*ALL'))
        )
        .addParm(iData('fmtnam', '8A', 'RJLS0100'))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )
    itool.call(itransport)
    qwtrmvjl = itool.dict_out('qwtrmvjl')
    if 'success' in qwtrmvjl:
        return 0, qwtrmvjl['success']
    else:
        return -1, qwtrmvjl['error']


def return_error(module, conn, error, out, msg, job_log, rc, job_submitted_split, wait, delivery_format, result):
    if (job_submitted_split and job_log) and (wait is True or delivery_format == '*IMAGE'):
        ret, message = remove_pending_joblog(conn, job_submitted_split[2], job_submitted_split[1], job_submitted_split[0])
        if ret != 0:
            error = 'Failed to clear the job in joblog pending state.' + message

    result['stderr'] = error
    result['stdout'] = out
    result['msg'] = msg
    result['job_log'] = job_log
    result['rc'] = rc
    module.fail_json(**result)


def convert_wait_time_to_seconds(input_wait_time):
    m = re.match(r"^(-?\d+)([smhdw])?$", input_wait_time.lower())
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if m:
        wait_time = int(m.group(1)) * seconds_per_unit.get(m.group(2), 1)
    else:
        wait_time = 0
    return wait_time


def wait_for_certain_time(input_wait_time):
    wait_time = convert_wait_time_to_seconds(input_wait_time)
    time.sleep(wait_time)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ptf_id=dict(type='str', required=True),
            product=dict(type='str', default='*ONLYPRD'),
            release=dict(type='str', default='*ONLYRLS'),
            delivery_format=dict(type='str', default='*SAVF', choices=['*SAVF', '*IMAGE']),
            order=dict(type='str', default='*REQUIRED', choices=['*REQUIRED', '*PTFID']),
            reorder=dict(type='str', default='*YES', choices=['*NO', '*YES']),
            check_PTF=dict(type='str', default='*NO', choices=['*NO', '*YES']),
            image_directory=dict(type='str', default='*DFT'),
            joblog=dict(type='bool', default=False),
            parameters=dict(type='str', default=' '),
            time_out=dict(type='str', default='15m'),
            wait=dict(type='bool', default=True),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    ptf_id = module.params['ptf_id']
    product = module.params['product']
    release = module.params['release']
    delivery_format = module.params['delivery_format']
    order = module.params['order']
    reorder = module.params['reorder']
    check_PTF = module.params['check_PTF']
    image_directory = module.params['image_directory']
    joblog = module.params['joblog']
    parameters = module.params['parameters']
    time_out = module.params['time_out']
    wait = module.params['wait']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    result = dict(
        stdout='',
        stderr='',
        rc=0,
        delta='',
        command='',
        download_list=[],
        job_log=[],
        msg='',
        order_id=0,
        job_info=''
    )
    error = ''
    out = ''
    returned_job_status = ''
    job_log = []
    download_list = []
    time_up = False
    success = False
    job_submitted = ''
    job_submitted_split = ''
    order_id = 0
    order_start_time = 0
    order_end_time = 0
    file_path = ''

    try:
        ibmi_module = imodule.IBMiModule(become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    conn = ibmi_module.get_connection()

    if image_directory != "*DFT":
        image_directory = "'{p_image_directory}'".format(p_image_directory=image_directory)

    command = 'SNDPTFORD PTFID(({p_ptf_id} {p_product} {p_release})) DLVRYFMT({p_delivery_format}) ORDER({p_order}) \
    REORDER({p_reorder}) CHKPTF({p_check_PTF}) IMGDIR({p_image_directory}) {p_parameters}'.format(
        p_ptf_id=ptf_id,
        p_product=product,
        p_release=release,
        p_delivery_format=delivery_format,
        p_order=order,
        p_reorder=reorder,
        p_check_PTF=check_PTF,
        p_image_directory=image_directory,
        p_parameters=parameters)

    cl_sbmjob = "QSYS/SBMJOB CMD(" + ' '.join(command.split()) + ") " + 'LOG(4 *JOBD *SECLVL) ' + 'LOGOUTPUT(*PND) ' + parameters
    startd = datetime.datetime.now()
    message_description = ''
    rc, out, error = ibmi_module.itoolkit_run_command(cl_sbmjob)

    current_job_log = ibmi_module.itoolkit_get_job_log(startd)
    for i in current_job_log:
        if i["MESSAGE_ID"] == "CPC1221":
            message_description = i["MESSAGE_TEXT"]
            break

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        return_error(module, conn, message_description, out, 'Submit job failed.', current_job_log, ibmi_util.IBMi_COMMAND_RC_ERROR, job_submitted_split, wait,
                     delivery_format, result)

    submitted_job = re.search(r'\d{6}/[A-Za-z0-9#_]{1,10}/[A-Za-z0-9#_]{1,10}', message_description)
    job_submitted = submitted_job.group()
    job_submitted_split = job_submitted.split("/")
    sql_get_job_info = "SELECT V_JOB_STATUS as \"job_status\", " \
                       "V_ACTIVE_JOB_STATUS as \"active_job_status\"" \
                       " FROM TABLE(QSYS2.GET_JOB_INFO('" + job_submitted + "')) A"
    try:
        time_out_in_seconds = convert_wait_time_to_seconds(time_out)
        if wait or delivery_format == '*IMAGE':
            rc, out, error = ibmi_module.itoolkit_run_sql(sql_get_job_info)
            if isinstance(out, list) and len(out) == 1:
                returned_job_status = out[0]['job_status'].strip()

            while returned_job_status != '*UNKNOWN' and returned_job_status != '*OUTQ':
                wait_for_certain_time('1s')
                current_time = datetime.datetime.now()
                running_time = (current_time - startd).seconds
                if running_time > time_out_in_seconds:
                    time_up = True
                    break
                rc, out, error = ibmi_module.itoolkit_run_sql(sql_get_job_info)
                returned_job_status = ''
                if isinstance(out, list) and len(out) == 1:
                    returned_job_status = out[0]['job_status'].strip()
                ibmi_util.log_debug("job_status: " + returned_job_status, module._name)

        if rc == ibmi_util.IBMi_COMMAND_RC_SUCCESS:
            job_log = db2i_tools.get_job_log(conn, job_submitted, startd)
        else:
            return_error(module, conn, error, out, 'itoolkit_run_sql failed', [], ibmi_util.IBMi_COMMAND_RC_ERROR, job_submitted_split,
                         wait, delivery_format, result)

        if time_up is True:
            return_error(module, conn, error, '', 'Time up when waiting for SNDPTFORD complete.', job_log, ibmi_util.IBMi_COMMAND_RC_ERROR,
                         job_submitted_split, wait, delivery_format, result)

        if delivery_format == '*SAVF':
            j = 0
            while order_id == 0:
                for i in range(len(job_log) - 1, -1, -1):
                    if job_log[i]['MESSAGE_ID'] == 'CPF8C07':
                        return_error(module, conn, '', '', job_log[i]['MESSAGE_TEXT'], job_log,
                                     ibmi_util.IBMi_COMMAND_RC_ERROR, job_submitted_split, wait, delivery_format, result)
                    elif job_log[i]['MESSAGE_ID'] == 'CPZ8C38':
                        order_id = job_log[i]['MESSAGE_TEXT'][18:28]
                        order_start_time = job_log[i]['MESSAGE_TIMESTAMP']
                    elif job_log[i]['MESSAGE_ID'] == 'CPZ8C12':
                        download_list.append({})
                        download_list[j]['product'] = (job_log[i]['MESSAGE_TEXT'])[4:11]
                        download_list[j]['ptf_id'] = job_log[i]['MESSAGE_TEXT'][12:19]
                        download_list[j]['release'] = job_log[i]['MESSAGE_TEXT'][20:26]
                        download_list[j]['download_time'] = job_log[i]['MESSAGE_TIMESTAMP']
                        download_list[j]['file_name'] = 'Q' + download_list[j]['ptf_id']
                        download_list[j]['file_path'] = '/qsys.lib/qgpl.lib/' + download_list[j]['file_name'] + '.FILE'
                        download_list[j]['order_id'] = order_id
                        j = j + 1
                        success = True
                    elif job_log[i]['MESSAGE_ID'] == 'CPF1164':
                        order_end_time = job_log[i]['MESSAGE_TIMESTAMP']
                    elif job_log[i]['MESSAGE_ID'] == 'CPI8C02':
                        return_error(module, conn, '', '', job_log[i]['MESSAGE_TEXT'], job_log,
                                     ibmi_util.IBMi_COMMAND_RC_ERROR, job_submitted_split, wait, delivery_format, result)
                    elif job_log[i]['MESSAGE_ID'] == 'CPF8C32':
                        return_error(module, conn, '', '', 'PTF order cannot be processed. See joblog', job_log,
                                     ibmi_util.IBMi_COMMAND_RC_ERROR, job_submitted_split, wait, delivery_format, result)
                job_log = db2i_tools.get_job_log(conn, job_submitted, startd)
        elif delivery_format == '*IMAGE':
            if job_log:
                for i in range(len(job_log)):
                    if job_log[i]['MESSAGE_ID'] == 'CPZ8C38':
                        order_id = job_log[i]['MESSAGE_TEXT'][18:28]
                        order_start_time = job_log[i]['MESSAGE_TIMESTAMP']
                        success = True
                    elif job_log[i]['MESSAGE_ID'] == 'CPF8C32':
                        return_error(module, conn, '', '', 'PTF order cannot be processed. See joblog', job_log,
                                     ibmi_util.IBMi_COMMAND_RC_ERROR, job_submitted_split, wait, delivery_format, result)
            else:
                return_error(module, conn, error, out, 'No joblog returned.', job_log, ibmi_util.IBMi_COMMAND_RC_ERROR,
                             job_submitted_split, wait, delivery_format, result)

        if wait is True or delivery_format == '*IMAGE':
            ret, message = remove_pending_joblog(conn, job_submitted_split[2], job_submitted_split[1], job_submitted_split[0])
            if ret != 0:
                error = error + '/n remove pending joblog fail.' + message

        endd = datetime.datetime.now()
        delta = endd - startd

        if delivery_format == '*IMAGE':
            if image_directory == '*DFT':
                file_path = '/QIBM/UserData/OS/Service/ECS/PTF/' + str(order_id)
            else:
                file_path = image_directory.strip("'")

        result.update({'job_log': job_log if joblog or rc or success is False else [], 'stdout': '', 'stderr': error,
                       'download_list': download_list, 'rc': rc, 'delta': str(delta), 'order_id': order_id,
                       'msg': 'SNDPTFORD successfully ended.', 'job_info': job_submitted, 'command': cl_sbmjob,
                       'order_start_time': order_start_time, 'order_end_time': order_end_time, 'file_path': file_path})

        module.exit_json(**result)

    except ImportError as e_import:
        return_error(module, conn, str(e_import), '', '', '', ibmi_util.IBMi_PACKAGES_NOT_FOUND, job_submitted_split, wait,
                     delivery_format, result)
    except Exception as e_db_connect:
        return_error(module, conn, str(e_db_connect), '', '', '', ibmi_util.IBMi_DB_CONNECTION_ERROR, job_submitted_split, wait,
                     delivery_format, result)


if __name__ == '__main__':
    main()
