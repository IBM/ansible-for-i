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
short_description: Get all nonconfigure disks on target IBMi node
version_added: 2.10
description:
  - Get all nonconfigure disks on target IBMi node
  - For non-IBMi targets, no need

author:
- Jin Yi Fan(@jinyifan)
'''

EXAMPLES = r'''
- name: get all nonconfigure disks
  ibmi_get_nonconfigure_disks:
'''

RETURN = r'''
start:
    description: The command execution start time
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The command execution end time
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The command execution delta time
    returned: always
    type: str
    sample: '0:00:00.307534'
disks:
    description: all un-configure disks
    returned: always
    type: str
    sample: 'DMP002 DMP019 DMP005 DMP014 DMP031 DMP012 '
rc:
    description: The command return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 0
rc_msg:
    description: Meaning of the return code
    returned: always
    type: str
    sample: 'Success to get all un-configure disks.'
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ibmi import ibmi_util
try:
    from itoolkit import iToolKit
    from itoolkit.db2.idb2call import iDB2Call
    from itoolkit import iPgm
    from itoolkit import iData
    from itoolkit import iDS
except ImportError:
    HAS_ITOOLKIT = False


def getNonconfigureDisk():
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
    return diskList


def main():
    module = AnsibleModule(
        argument_spec=dict(),
        supports_check_mode=True,
    )

    startd = datetime.datetime.now()
    disk_list = getNonconfigureDisk()
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
        rc_msg=rc_msg,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
    )

    if rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS:
        module.fail_json(msg='non-zero return code', **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
