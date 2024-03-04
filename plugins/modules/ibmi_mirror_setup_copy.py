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
module: ibmi_mirror_setup_copy
short_description: Configures the Db2 Mirror on the target node.
version_added: '1.2.0'
description:
  - The C(ibmi_mirror_setup_copy) module configures the Db2 Mirror on the target node after the clone.
options:
  ip_address:
    description:
      - The setup copy system IP address.
    type: str
    required: yes
  rdma_subnet_mask:
    description:
      - Sets the subnet mask if the RDMA links subnet is different than the system IP address.
        If set to C(*SAME), will retrieve the subnet mask from the system IP address.
    type: str
    default: '*SAME'
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str

seealso:
- module: ibmi_mirror_setup_source

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: config the db2 mirror on the copy node
  ibm.power_ibmi.ibmi_mirror_setup_copy:
    ip_address: 192.168.100.2
    rdma_subnet_mask: 255.255.252.0
'''

RETURN = r'''
msg:
    description: The message that describes the error or success
    returned: always
    type: str
    sample: 'Error occurred when retrieving the mirror state'
job_log:
    description: the job_log
    returned: always
    type: str
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
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 0
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import json
import re
import os
import sys

HAS_ITOOLKIT = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSrvPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport as BaseDatabaseTransport

    class DatabaseTransport(BaseDatabaseTransport):
        def _close(self):
            """Don't close connection, we'll manage it ourselves"""
            pass

except ImportError:
    HAS_ITOOLKIT = False


CLOUDINIT_METADATA_DIR = '/QOpenSys/pkgs/lib/cloudinit/cloud/seed/config_drive/openstack/latest'
DB2MTOOL_METADATA_DIR = '/QIBM/UserData/QDB2MIR/MRDB/TOOLS'

kKindVirtEthernet = '0000000000000008000000000000000400000800000004'
kKindPhysEthernet = '0000000000000008000000000000000400000000000004'

SUCCESS = 0
ERROR = -1

__ibmi_module_version__ = "2.0.1"


def _is_ipv4_addr(ip):
    p = re.compile(
        r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def _is_ipv6_addr(addr):
    ip6_regex = (r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,6}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,5}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4}){1,4}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]{1,4}){1,3}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,5}(:[0-9a-f]{1,4}){1,2}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,6}(:[0-9a-f]{1,4}){1,1}\Z)|'
                 r'(\A(([0-9a-f]{1,4}:){1,7}|:):\Z)|(\A:(:[0-9a-f]{1,4})'
                 r'{1,7}\Z)|(\A((([0-9a-f]{1,4}:){6})(25[0-5]|2[0-4]\d|[0-1]'
                 r'?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
                 r'(\A(([0-9a-f]{1,4}:){5}[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3})\Z)|'
                 r'(\A([0-9a-f]{1,4}:){5}:[0-9a-f]{1,4}:(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)|'
                 r'(\A([0-9a-f]{1,4}:){1,1}(:[0-9a-f]{1,4}){1,4}:(25[0-5]|'
                 r'2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d))'
                 r'{3}\Z)|(\A([0-9a-f]{1,4}:){1,2}(:[0-9a-f]{1,4}){1,3}:'
                 r'(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?'
                 r'\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,3}(:[0-9a-f]{1,4})'
                 r'{1,2}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)){3}\Z)|(\A([0-9a-f]{1,4}:){1,4}(:[0-9a-f]'
                 r'{1,4}){1,1}:(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|'
                 r'2[0-4]\d|[0-1]?\d?\d)){3}\Z)|(\A(([0-9a-f]{1,4}:){1,5}|:):'
                 r'(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?'
                 r'\d?\d)){3}\Z)|(\A:(:[0-9a-f]{1,4}){1,5}:(25[0-5]|2[0-4]\d|'
                 r'[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\Z)')
    return bool(re.match(ip6_regex, addr))


def load_meta_data(meta_data_file_path):
    with open(meta_data_file_path, 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def save_meta_data(meta_data_file_path, json_dict):
    with open(meta_data_file_path, 'w', encoding='utf-8') as dump_f:
        json.dump(json_dict, dump_f)


def get_system_name(json_dict):
    return json_dict['name']


def get_host_name(json_dict):
    return json_dict['hostname']


def get_nrg_ip_pairs(json_dict):
    return json_dict['nrgs'][0]['nrgIPAddrPairs']


def get_network_config_details(json_dict):
    return json_dict['network_config']['details']


def reverse_nrg_ip_pairs(json_dict):
    nrgs = json_dict['nrgs']
    for nrg in nrgs:
        nrg_ip_addr_pairs = nrg['nrgIPAddrPairs']
        if 'groupDesc' not in nrg:
            nrg.setdefault('groupDesc', 'DB2MIRROR')
        for nrg_ip_addr_pair in nrg_ip_addr_pairs:
            local_ip_addr = nrg_ip_addr_pair['localAddr']
            remote_ip_addr = nrg_ip_addr_pair['remoteAddr']
            nrg_ip_addr_pair.update({'localAddr': remote_ip_addr})
            nrg_ip_addr_pair.update({'remoteAddr': local_ip_addr})
            if 'localLind' not in nrg_ip_addr_pair:
                nrg_ip_addr_pair.setdefault('localLind', 'default')


def updata_system_name(json_dict, system_name):
    json_dict.update({'name': system_name})


def updata_host_name(json_dict, host_name):
    json_dict.update({'hostname': host_name})


def add_rdma_ip_address(json_dict, ip_addr, cmn_location, subnet_mask='255.255.255.0'):
    ip_addr_list = []
    ip_addr_list.append(ip_addr)
    ip_detail = {"broadcast": "",
                 "vlanID": "*NONE",
                 "auto": True,
                 "address": [],
                 "dns_nameservers": ["", "", ""],
                 "dns_search": ["", ""],
                 "gateway": "",
                 "hwaddress": "ff: ff: ff: ff: ff: ff",
                 "prefixLen": "64",
                 "netmask": "255.255.255.0",
                 "bootproto": "static",
                 "cmnlocation": "",
                 "ipv6": False,
                 "device": "eth0",
                 "ipv4": True}
    ip_detail['address'] = ip_addr_list
    ip_detail['cmnlocation'] = cmn_location
    ip_detail['netmask'] = subnet_mask
    if _is_ipv4_addr(ip_addr):
        ip_detail['ipv4'] = True
        ip_detail['ipv6'] = False
    else:
        ip_detail['ipv4'] = False
        ip_detail['ipv6'] = True

    details = json_dict['network_config']['details']
    details.append(ip_detail)


def get_location_code_from_resource_name(imodule, resource_name):
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

    loccode = ''
    itool.call(itransport)
    qgyrhr = itool.dict_out('qgyrhr')
    ibmi_util.log_debug("qgyrhr output: " + str(qgyrhr),
                        sys._getframe().f_code.co_name)
    if 'success' in qgyrhr:
        rhri0100_t = qgyrhr['RHRI0100_t']
        if int(rhri0100_t['rhrAvl']) > 0:
            loccode = rhri0100_t['locCd']
        return SUCCESS, loccode, qgyrhr['success']
    else:
        return ERROR, loccode, qgyrhr['error']


def list_rdma_location_code(imodule):
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
    ibmi_util.log_debug("qgyrhr output: " + str(qgyrhr),
                        sys._getframe().f_code.co_name)
    location = []
    if 'success' in qgyrhr:
        rhrl0100_t = qgyrhr['RHRL0100_t']
        if int(rhrl0100_t['rhrNbr']) > 0:
            res_t = rhrl0100_t['res_t']
            cur_loc = None
            for rec in res_t:
                if rec['resKnd'] == kKindVirtEthernet or rec['resKnd'] == kKindPhysEthernet:
                    ibmi_util.log_debug(
                        "resource name is " + rec['resNam'], sys._getframe().f_code.co_name)
                    rc, cur_loc, result = get_location_code_from_resource_name(
                        imodule, rec['resNam'])
                    ibmi_util.log_debug(
                        "location code is " + cur_loc, sys._getframe().f_code.co_name)
                    ibmi_util.log_debug(
                        f"get location code rc is {rc}", sys._getframe().f_code.co_name)
                    ibmi_util.log_debug(
                        "get location code result is " + result, sys._getframe().f_code.co_name)
                    location.append(cur_loc)
        return SUCCESS, location, qgyrhr['success']
    else:
        return ERROR, location, qgyrhr['error']


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ip_address=dict(type='str', required=True),
            rdma_subnet_mask=dict(type='str', default='*SAME'),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    ip_address = module.params['ip_address']
    rdma_subnet_mask = module.params['rdma_subnet_mask']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if not HAS_ITOOLKIT:
        module.fail_json(rc=999, msg="itoolkit package is required.")

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = f'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    # check special authority *IOSYSCFG
    # get current user's special authority
    command = 'RTVUSRPRF'
    if become_user:
        command = command + f' USRPRF({become_user})'
    rc, out, err, job_log = ibmi_module.itoolkit_run_rtv_command_once(
        command, {'SPCAUT': 'char'})
    if rc:
        module.fail_json(
            rc=rc, msg=f"Error occurred when call RTVUSRPRF to special authority: {str(err)}")
    special_authority = out['SPCAUT']
    ibmi_util.log_info(f"Special authority is {special_authority}", module._name)

    if '*IOSYSCFG' not in special_authority:
        module.fail_json(
            rc=rc, msg="Special authority *IOSYSCFG is needed")

    # Generate the meta_data base on the system snapshot
    command = "db2mtool action=snapshot"
    rc, out, err = module.run_command(command, use_unsafe_shell=False)
    ibmi_util.log_debug(
        f"Run command={command}, rc={rc}, stdout={out}, stderr={err}", module._name)
    if rc or ("INFO Save to file /QIBM/UserData/QDB2MIR/MRDB/TOOLS/meta_data" not in out):
        module.fail_json(
            rc=rc, msg=f"Error occurred when generate system snapshot: stdout={out}, stderr={err}")

    json_file = None
    for line in out.splitlines():
        if "INFO Save to file /QIBM/UserData/QDB2MIR/MRDB/TOOLS/meta_data" in line:
            temp_list = line.split()
            for item in temp_list:
                if "/QIBM/UserData/QDB2MIR/MRDB/TOOLS/meta_data" in item:
                    json_file = item

    ibmi_util.log_debug("json_file path is " + json_file, module._name)

    if (json_file is None) or (not os.path.exists(json_file)):
        module.fail_json(
            rc=255, msg=f"Mirror configuration meta data not found, path={json_file}")

    # Load the meta_data.json as dict
    json_dict = load_meta_data(json_file)
    ibmi_util.log_debug(f"Current meta data: {str(json_dict)}", module._name)

    # Prepare the system name and hostname
    sql = "SELECT SECONDARY_NODE, SECONDARY_HOSTNAME FROM QSYS2.MIRROR_INFO"
    rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
    if rc:
        module.fail_json(
            rc=255, msg="Unable retrieve the secondary node information from QSYS2.MIRROR_INFO", job_log=job_log)
    secondary_system_name = ''
    sencodary_host_name = ''
    if isinstance(out, list) and len(out) > 0:
        first_row = out[0]
        secondary_system_name = first_row['SECONDARY_NODE']
        sencodary_host_name = first_row['SECONDARY_HOSTNAME']
    ibmi_util.log_debug(
        f"Secondary system name and hostname in QSYS2.MIRROR_INFO is: {secondary_system_name}, {sencodary_host_name}", module._name)

    # Prepare the RDMA address
    sql = "SELECT TARGET_ADDRESS FROM QSYS2.NRG_LINK_INFO WHERE NRG_NAME = 'MIRROR_DATABASE'"
    rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
    if rc:
        module.fail_json(
            rc=255, msg="Unable retrieve NRG link information from QSYS2.NRG_LINK_INFO", job_log=job_log)
    target_address = []
    for item in out:
        target_address.append(item['TARGET_ADDRESS'])
    # Remove the duplicate
    target_address = list(set(target_address))
    ibmi_util.log_debug(
        f"Target address in QSYS2.NRG_LINK_INFO is: {target_address}", module._name)

    rc, location, result = list_rdma_location_code(ibmi_module)
    ibmi_util.log_debug(
        f"list_rdma_location_code result is: {result}", module._name)
    if rc:
        module.fail_json(
            rc=rc, msg=f"Error when list RDMA location code: {result}")
    # Remove the duplicate
    location = list(set(location))
    ibmi_util.log_debug(
        f"RDMA resources location are: {location}", module._name)

    network_config_details_list = get_network_config_details(json_dict)
    already_configured_ip_list = []
    already_configured_cmn_list = []
    for item in network_config_details_list:
        ip_address_list = item['address']
        for ip in ip_address_list:
            already_configured_ip_list.append(ip)
        already_configured_cmn_list.append(item['cmnlocation'])
    ibmi_util.log_debug(
        f"Already configured IP addresses are: {already_configured_ip_list}", module._name)
    ibmi_util.log_debug(
        f"Already configured cmnlocation are: {already_configured_cmn_list}", module._name)

    for item in already_configured_ip_list:
        if item in target_address:
            target_address.remove(item)
    ibmi_util.log_debug(
        f"Non-configured IP addresses are: {target_address}", module._name)
    for item in already_configured_cmn_list:
        if item in location:
            location.remove(item)
    ibmi_util.log_debug(
        f"Non-configured cmnlocation are: {location}", module._name)

    if len(location) < len(target_address):
        module.fail_json(
            rc=255, msg=f"Not enough RDMA comunication resource ports({len(location)}) for RDMA links({len(target_address)})")

    if rdma_subnet_mask == '*SAME':
        sql = f"SELECT SUBNET_MASK from QSYS2.NETSTAT_INTERFACE_INFO \
            WHERE (INTERFACE_LINE_TYPE = 'ELAN' OR INTERFACE_LINE_TYPE = 'VETH') \
            AND INTERNET_ADDRESS  NOT IN ('*IP6SAC', '*IP4DHCP') AND INTERNET_ADDRESS = '{ip_address}'"
        ibmi_util.log_debug(
            f"Retrieve RDMA subnet mask sql is: {sql}", module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)
        if rc:
            module.fail_json(
                rc=255, msg="Error occured when retrieving subnet mask information from QSYS2.NETSTAT_INTERFACE_INFO", job_log=job_log)
        else:
            if isinstance(out, list) and len(out) == 1:
                rdma_subnet_mask = out[0]['SUBNET_MASK']
            else:
                module.fail_json(
                    rc=255, msg=f"Row incorrect when retrieving subnet mask information from QSYS2.NETSTAT_INTERFACE_INFO: row={out}")
    ibmi_util.log_debug(
        f"RDMA subnet mask is: {rdma_subnet_mask}", module._name)

    i = 0
    for ip in target_address:
        add_rdma_ip_address(json_dict, ip, location[i], rdma_subnet_mask)
        i = i + 1

    updata_system_name(json_dict, secondary_system_name)
    updata_host_name(json_dict, sencodary_host_name)
    reverse_nrg_ip_pairs(json_dict)
    if not os.path.exists(CLOUDINIT_METADATA_DIR):
        os.makedirs(CLOUDINIT_METADATA_DIR)
    ibmi_util.log_debug(
        f"Write meta data to seed: {str(json_dict)}", module._name)
    save_meta_data(CLOUDINIT_METADATA_DIR + "/meta_data.json", json_dict)
    save_meta_data(DB2MTOOL_METADATA_DIR + "/meta_data_" +
                   secondary_system_name + "_ansible.json", json_dict)

    args = ['system', 'CALL PGM(QSYS/QAENGCHG) PARM(*ENABLECI)']
    rc, out, err = module.run_command(args, use_unsafe_shell=False)
    if rc and ('ACTIVATION ENGINE OR CLOUD-INIT IS ALREADY ENABLED' not in err):
        module.fail_json(
            rc=255, msg=f"Error occurred when enable Activation Engine: stdout={out}, stderr={err}")

    module.exit_json(
        rc=SUCCESS, msg="Success to configure Db2Mirror copy node, reboot to make the nodes synchronized")


if __name__ == '__main__':
    main()
