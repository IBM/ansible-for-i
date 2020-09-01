#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Yi Fan Jin <jinyifan@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_get_nonconfigure_disks
short_description: Get all nonconfigure disks
version_added: '2.8.0'
description:
  - Get all nonconfigure disks.
  - For non-IBM i targets, no need.
options:
  joblog:
    description:
      - If set to C(true), append JOBLOG to stderr/stderr_lines.
    type: bool
    default: False

author:
- Jin Yifan(@jinyifan)
'''

EXAMPLES = r'''
- name: get all nonconfigure disks
  ibmi_get_nonconfigure_disks:
    joblog: True
'''

RETURN = r'''
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "318F",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "",
            "FROM_PROCEDURE": "",
            "FROM_PROGRAM": "QWTCHGJB",
            "FROM_USER": "CHANGLE",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPD0912",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Printer device PRT01 not found.",
            "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897",
            "MESSAGE_TYPE": "DIAGNOSTIC",
            "ORDINAL_POSITION": "5",
            "SEVERITY": "20",
            "TO_INSTRUCTION": "9369",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
        }]
start:
    description: The command execution start time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The command execution end time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The command execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
disks:
    description: all un-configure disks.
    returned: always
    type: str
    sample: 'DMP002 DMP019 DMP005 DMP014 DMP031 DMP012'
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 0
rc_msg:
    description: Meaning of the return code.
    returned: always
    type: str
    sample: 'Success to get all un-configure disks.'
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
try:
    from itoolkit import iToolKit
    from itoolkit.db2.idb2call import iDB2Call
    from itoolkit import iPgm
    from itoolkit import iData
    from itoolkit import iDS
except ImportError:
    HAS_ITOOLKIT = False

__ibmi_module_version__ = "1.0.2"


def getNonconfigureDisk(time):
    conn = ibmi_util.itoolkit_init()
    itransport = iDB2Call(conn)
    itool = iToolKit()
    itool.add(iPgm('qyasrdi', 'QYASRDI')
              .addParm(iDS('DMIN0100_t', {'len': 'dmilen'})
              .addData(iData('dniRet', '10i0', ''))
              .addData(iData('dmiAvl', '10i0', ''))
              .addData(iData('dmiOfset', '10i0', ''))
              .addData(iData('dmiNbr', '10i0', '', {'enddo': 'mycnt'}))
              .addData(iData('dmiLen', '10i0', ''))
              .addData(iData('dmiRes', '10i0', ''))
              .addData(iDS('res_t', {'dim': '999', 'dou': 'mycnt'})
                       .addData(iData('resDurn', '10a', ''))
                       .addData(iData('resDuff', '1a', ''))
                       .addData(iData('resTrnaswdu', '10a', ''))
                       .addData(iData('resTnawdu', '4a', ''))
                       .addData(iData('resDuaindpsf', '1a', ''))
                       .addData(iData('resDuaiedpsf', '1a', ''))
                       .addData(iData('resRes', '5a', ''))
                       .addData(iData('resDpsn', '10i0', ''))
                       .addData(iData('resCaadps', '10i0', ''))
                       )
                       )
              .addParm(iData('rcvlen', '10i0', '', {'setlen': 'dmilen'}))
              .addParm(iData('fmtnam', '10a', 'DMIN0100'))
              .addParm(iData('dmiDurna', '10a', '*UNCONFIG'))
              .addParm(iData('dmiNbr', '10i0', '1'))
              .addParm(iDS('ERRC0100_t', {'len': 'errlen'})
                       .addData(iData('errRet', '10i0', ''))
                       .addData(iData('errAvl', '10i0', ''))
                       .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                       .addData(iData('errRsv', '1A', ''))
                       )
              )
    itool.call(itransport)
    qyasrdi = itool.dict_out('qyasrdi')
    diskList = ''
    if 'success' in qyasrdi:
        DMIN0100_t = qyasrdi['DMIN0100_t']
        if int(DMIN0100_t['dmiNbr']) > 0:
            res_t = DMIN0100_t['res_t']
            if int(DMIN0100_t['dmiNbr']) == 1:
                diskList = res_t['resDurn']
            else:
                for rec in res_t:
                    diskList += rec['resDurn'] + ' '
        if diskList.endswith(' '):
            diskList = diskList[:-1]
    job_log = ibmi_util.itoolkit_get_job_log(conn, time)
    return diskList, job_log


def main():
    module = AnsibleModule(
        argument_spec=dict(
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    joblog = module.params['joblog']
    startd = datetime.datetime.now()
    disk_list, job_log = getNonconfigureDisk(startd)
    if not disk_list:
        rc_msg = "Here is no un-configure disk."
        rc = 0
    else:
        rc_msg = "Success to get all un-configure disks."
        rc = 0
    endd = datetime.datetime.now()
    delta = endd - startd

    result = dict(
        disks=disk_list,
        rc=rc,
        out=rc_msg,
        start=str(startd),
        job_log=job_log,
        end=str(endd),
        delta=str(delta),
    )

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
