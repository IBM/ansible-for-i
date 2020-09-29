#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_ethernet_port
short_description: Retrieves all the ethernet ports(both virtual and physical)information on the system.
version_added: '2.8.0'
description:
  - The C(ibmi_ethernet_port) module lists the ethernet ports information of the system.
options:
  operation:
    description:
      - The ethernet port operation.
    choices: ['display']
    type: str
    default: 'display'
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
  - The following PTFs are required for getting the default MAC address of a port,
    V7R1M0 SI64305, MF63437, MF63430
    V7R2M0 SI63691, MF99106
    V7R3M0 SI63671, MF99202
  - Field Descriptions refer to
    https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/apis/qgyrhri.htm

seealso:
- module: ibmi_cl_command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: list all the ethernet port information
  ibmi_ethernet_port:
'''

RETURN = r'''
msg:
    description: The message that descript the error or success
    returned: always
    type: str
    sample: 'Error occurred when retrieving the mirror state'
ethernet_ports:
    description: the ethernet ports information
    returned: when rc as 0
    type: str
    sample: [
        {
            "ADAPTER_ADDRESS": "2",
            "CARD_POSITION": "",
            "DEFAULT_MAC_ADDRESS": "FAB7D940D220",
            "EXPANDED_SERIAL_NUMBER": "00-00000",
            "FRAME_ID": "",
            "IO_BUS_ADDRESS": "208",
            "LAN speed": "0000000000000003",
            "LOCATION_CODE": "U8286.42A.10C4DAT-V14-C2-T1",
            "PART_NUMBER": "",
            "PORT_NUMBER": "0",
            "RESOURCE_NAME": "CMN06",
            "SERIAL_NUMBER": "00-00000",
            "SUPPORTS_LINK_AGGREGATION": "02",
            "SYSTEM_BOARD_NUMBER": "2",
            "SYSTEM_BUS_NUMBER": "255",
            "SYSTEM_CARD_NUMBER": "2"
        },
        {
            "ADAPTER_ADDRESS": "3",
            "CARD_POSITION": "",
            "DEFAULT_MAC_ADDRESS": "0AF685E6D2C4",
            "EXPANDED_SERIAL_NUMBER": "00-00000",
            "FRAME_ID": "",
            "IO_BUS_ADDRESS": "208",
            "LAN speed": "0000000000000003",
            "LOCATION_CODE": "U8286.42A.10C4DAT-V14-C3-T1",
            "PART_NUMBER": "",
            "PORT_NUMBER": "0",
            "RESOURCE_NAME": "CMN05",
            "SERIAL_NUMBER": "00-00000",
            "SUPPORTS_LINK_AGGREGATION": "02",
            "SYSTEM_BOARD_NUMBER": "3",
            "SYSTEM_BUS_NUMBER": "255",
            "SYSTEM_CARD_NUMBER": "3"
        }
    ]
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 0
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import sys

HAS_ITOOLKIT = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSrvPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

kKindVirtEthernet = '0000000000000008000000000000000400000800000004'
kKindPhysEthernet = '0000000000000008000000000000000400000000000004'

SUCCESS = 0
ERROR = -1

__ibmi_module_version__ = "1.1.2"


def get_info_from_resource_name(imodule, resource_name):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qgyrhr', 'QGYRHR', 'QgyRtvHdwRscInfo')
        .addParm(
            iDS('RHRI0100_t', {'len': 'rhrlen'})
            .addData(iData('rhrRet', '10i0', ''))
            .addData(iData('rhrAvl', '10i0', ''))
            .addData(iData('sysBusNum', '10i0', ''))
            .addData(iData('sysBdNum', '10i0', ''))
            .addData(iData('sysCdNum', '10i0', ''))
            .addData(iData('IOBusAdd', '10i0', ''))
            .addData(iData('AdaptAdd', '10i0', ''))
            .addData(iData('PortNum', '10i0', ''))
            .addData(iData('srNum', '10a', ''))
            .addData(iData('partNum', '12a', ''))
            .addData(iData('frmID', '4a', ''))
            .addData(iData('cdPst', '5a', ''))
            .addData(iData('locCd', '79a', ''))
            .addData(iData('expSrNum', '15a', ''))
            .addData(iData('LANSpeed', '8a', '', {'hex': 'on'}))
            .addData(iData('LinkAgg', '1a', '', {'hex': 'on'}))
            .addData(iData('MAC', '6a', '', {'hex': 'on'}))
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'rhrlen'}))
        .addParm(iData('fmtnam', '8a', 'RHRI0100'))
        .addParm(iData('resnam', '10a', resource_name))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )

    resoure_info = dict()
    itool.call(itransport)
    qgyrhr = itool.dict_out('qgyrhr')
    ibmi_util.log_debug("qgyrhr output: " + str(qgyrhr), sys._getframe().f_code.co_name)
    if 'success' in qgyrhr:
        rhri0100_t = qgyrhr['RHRI0100_t']
        if int(rhri0100_t['rhrAvl']) > 0:
            resoure_info = {"RESOURCE_NAME": resource_name,
                            "SYSTEM_BUS_NUMBER": rhri0100_t['sysBusNum'],
                            "SYSTEM_BOARD_NUMBER": rhri0100_t['sysCdNum'],
                            "SYSTEM_CARD_NUMBER": rhri0100_t['sysCdNum'],
                            "IO_BUS_ADDRESS": rhri0100_t['IOBusAdd'],
                            "ADAPTER_ADDRESS": rhri0100_t['AdaptAdd'],
                            "PORT_NUMBER": rhri0100_t['PortNum'],
                            "SERIAL_NUMBER": rhri0100_t['srNum'],
                            "PART_NUMBER": rhri0100_t['partNum'],
                            "FRAME_ID": rhri0100_t['frmID'],
                            "CARD_POSITION": rhri0100_t['cdPst'],
                            "LOCATION_CODE": rhri0100_t['locCd'],
                            "EXPANDED_SERIAL_NUMBER": rhri0100_t['expSrNum'],
                            "LAN_SPEED": rhri0100_t['LANSpeed'],
                            "SUPPORTS_LINK_AGGREGATION": rhri0100_t['LinkAgg'],
                            "DEFAULT_MAC_ADDRESS": rhri0100_t['MAC'],
                            }
        return SUCCESS, resoure_info, qgyrhr['success']
    else:
        return ERROR, resoure_info, qgyrhr['error']


def list_ethernet_ports_info(imodule):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qgyrhr', 'QGYRHR', 'QgyRtvHdwRscList')
        .addParm(
            iDS('RHRL0100_t', {'len': 'rhrlen'})
            .addData(iData('rhrRet', '10i0', ''))
            .addData(iData('rhrAvl', '10i0', ''))
            .addData(iData('rhrNbr', '10i0', '', {'enddo': 'mycnt'}))
            .addData(iData('rhrLen', '10i0', ''))
            .addData(iDS('res_t', {'dim': '999', 'dou': 'mycnt'})
                     .addData(iData('resCat', '10i0', ''))
                     .addData(iData('resLvl', '10i0', ''))
                     .addData(iData('resLin', '10i0', ''))
                     .addData(iData('resNam', '10a', ''))
                     .addData(iData('resTyp', '4a', ''))
                     .addData(iData('resMod', '3a', ''))
                     .addData(iData('resSts', '1a', ''))
                     .addData(iData('resSys', '8a', ''))
                     .addData(iData('resAdp', '12a', ''))
                     .addData(iData('resDsc', '50h', ''))
                     .addData(iData('resKnd', '24b', ''))
                     )
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'rhrlen'}))
        .addParm(iData('fmtnam', '10a', 'RHRL0100'))
        .addParm(iData('rescat', '10i0', '2'))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )
    itool.call(itransport)
    qgyrhr = itool.dict_out('qgyrhr')
    ibmi_util.log_debug("qgyrhr output: " + str(qgyrhr), sys._getframe().f_code.co_name)
    res_list = []
    if 'success' in qgyrhr:
        rhrl0100_t = qgyrhr['RHRL0100_t']
        if int(rhrl0100_t['rhrNbr']) > 0:
            res_t = rhrl0100_t['res_t']
            res_info = dict()
            for rec in res_t:
                if rec['resKnd'] == kKindVirtEthernet or rec['resKnd'] == kKindPhysEthernet:
                    ibmi_util.log_debug(
                        "resource name is " + rec['resNam'], sys._getframe().f_code.co_name)
                    rc, res_info, result = get_info_from_resource_name(
                        imodule, rec['resNam'])
                    ibmi_util.log_debug(
                        "resource info is " + str(res_info), sys._getframe().f_code.co_name)
                    ibmi_util.log_debug(
                        "get resource info result is " + result, sys._getframe().f_code.co_name)
                    if rc == SUCCESS:
                        res_list.append(res_info)
        return SUCCESS, res_list, qgyrhr['success']
    else:
        return ERROR, res_list, qgyrhr['error']


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', choices=['display'], default='display'),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    rc = SUCCESS
    ethernet_ports = []
    result = ''
    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    rc, ethernet_ports, result = list_ethernet_ports_info(ibmi_module)
    ibmi_util.log_debug(
        "list_ethernet_ports_info result is: {0}".format(result), module._name)
    ibmi_util.log_debug("list_ethernet_ports_info resources information are: {0}".format(
        ethernet_ports), module._name)

    if rc:
        module.fail_json(
            rc=rc, msg="Error when getting ethernet ports information: {0}".format(result))

    module.exit_json(
        rc=SUCCESS, msg="Success to get ethernet ports information", ethernet_ports=ethernet_ports)


if __name__ == '__main__':
    main()
