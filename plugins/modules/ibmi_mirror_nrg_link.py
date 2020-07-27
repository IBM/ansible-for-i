#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Chang Le <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_mirror_nrg_link
short_description: Manages NRGs(Network Redundancy Groups) links
version_added: '2.8'
description:
  - The C(ibmi_mirror_nrg_link) module adds or removes a link to one or all of the Db2 Mirror Network Redundancy Groups (NRGs).
options:
  operation:
    description:
      - NRGs link operation.
    type: str
    choices: ['ADD', 'REMOVE']
    required: yes
  nrg_name:
    description:
      - A string that contains the name of the NRG where the link is to be added.
        If the NRG does not exist, it will be created.
    type: str
    choices: ['*MIRROR', 'MIRROR_DATABASE', 'MIRROR_ENGINE', 'MIRROR_IFS', 'MIRROR_OTHER', 'MIRROR_RESYNC']
    default: '*MIRROR'
  source_address:
    description:
      - A string that contains the local IP address for the link to add. Either an IPv4 or an IPv6 address can be specified.
      - When the operation is C('REMOVE'), Can also contain the following special value C(*ALL) to remove all links for this NRG.
    type: str
    required: yes
  target_address:
    description:
      - A string that contains the remote IP address for the link to add. Either an IPv4 or an IPv6 address can be specified.
      - Ignored when the operation is C('REMOVE')
    type: str
  link_priority:
    description:
      - A string that contains an integer value set as the priority of the link.
        The range of priorities is from 1 to 16, where 1 is the highest priority. Priority values do not need to be unique.
      - Ignored when the operation is C('REMOVE')
    type: str
  change_load_balance_link_count:
    description:
      - Indicates whether to increment the load balance link count when C('ADD') a new link to the NRG or
        decrement the load balance link count when C('REMOVE') a link from the NRG.
    type: bool
    default: True
  line_description:
    description:
      - A string that contains the local system line description associated with this link.
        This parameter is required when source-address is an IPv6 link-local address and is used to identify a unique local interface.
        It is ignored for all other addresses.
    type: str
    default: ''
  virtual_lan_id:
    description:
      - A string that contains an integer value for the local virtual LAN identifier associated with this link.
        This parameter is required when source-address is an IPv6 link-local address and is used to identify a unique local interface.
        It is ignored for all other addresses.
    type: str
    default: ''

seealso:
- module: command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: add a link to the db2 mirror configuration
  ibmi_mirror_nrg_link:
    operation: ADD
    source_address: 10.0.0.1
    target_address: 10.0.0.2
    link_priority: 1
'''

RETURN = r'''
msg:
    description: The message that descript the error or success
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
import datetime

__ibmi_module_version__ = "9.9.9"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', choices=[
                           'ADD', 'REMOVE'], required=True),
            nrg_name=dict(type='str', choices=['*MIRROR', 'MIRROR_DATABASE', 'MIRROR_ENGINE',
                                               'MIRROR_IFS', 'MIRROR_OTHER', 'MIRROR_RESYNC'], default='*MIRROR'),
            source_address=dict(type='str', required=True),
            target_address=dict(type='str'),
            link_priority=dict(type='str'),
            change_load_balance_link_count=dict(type='bool', default=True),
            line_description=dict(type='str', default=''),
            virtual_lan_id=dict(type='str', default=''),
        ),
        supports_check_mode=True,
        required_if=[
            ['operation', 'ADD', ['target_address', 'link_priority']],
        ],
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    operation = module.params['operation'].upper().strip()
    nrg_name = module.params['nrg_name']
    source_address = module.params['source_address']
    target_address = module.params['target_address']
    link_priority = module.params['link_priority']
    change_load_balance_link_count = module.params['change_load_balance_link_count']
    line_description = module.params['line_description']
    virtual_lan_id = module.params['virtual_lan_id']

    if change_load_balance_link_count:
        change_load_balance_link_count_str = 'YES'
    else:
        change_load_balance_link_count_str = 'NO'

    if operation == 'ADD':
        try:
            link_priority_int = int(link_priority)
            if link_priority_int < 1 or link_priority_int > 16:
                module.fail_json(
                    rc=255, msg="The value of argument link_priority is {0} which out of range from 1 to 16".format(link_priority_int))
        except (TypeError, ValueError):
            module.fail_json(
                rc=255, msg="The value of argument link_priority is {0} which can't be converted to int".format(link_priority))
        if source_address == '*ALL':
            module.fail_json(
                rc=255, msg="The value of argument source_address can not be '*ALL' when the operation is 'ADD'")

        sql = "CALL QSYS2.ADD_NRG_LINK(NRG_NAME => '{p_name}', SOURCE_ADDRESS => '{s_addr}', TARGET_ADDRESS => '{t_addr}', \
            LINK_PRIORITY => {p_linkp}, INCREMENT_LOAD_BALANCE_LINK_COUNT => '{p_load}'".format(
            p_name=nrg_name, s_addr=source_address, t_addr=target_address,
            p_linkp=link_priority_int, p_load=change_load_balance_link_count_str)
        if line_description:
            sql = sql + \
                ", LINE_DESCRIPTION => '{p_lined}'".format(
                    p_lined=line_description)
        if virtual_lan_id:
            sql = sql + \
                ", VIRTUAL_LAN_ID => '{p_vlan_id}'".format(
                    p_vlan_id=virtual_lan_id)
        sql = sql + ")"

        ibmi_util.log_info("Run sql statement: " + sql, module._name)
        rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(sql)
        if rc:
            module.fail_json(
                rc=rc, msg="Error occurred when add NRG link, see job log for detail", job_log=job_log)

        sql = "CALL QSYS2.CHANGE_NRG(NRG_NAME => '{p_name}', NRG_DESCRIPTION => 'DB2MIRROR GROUP')".format(p_name=nrg_name)
        ibmi_util.log_info("Run sql statement: " + sql, module._name)
        rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(sql)
        if rc:
            module.fail_json(
                rc=rc, msg="Error occurred when change NRG deescription, see job log for detail", job_log=job_log)

        module.exit_json(
            rc=0, msg="Success to add NRG link")
    else:
        sql = "CALL QSYS2.REMOVE_NRG_LINK(NRG_NAME => '{p_name}', SOURCE_ADDRESS => '{s_addr}', \
            DECREMENT_LOAD_BALANCE_LINK_COUNT => '{p_load}'".format(
            p_name=nrg_name, s_addr=source_address, p_load=change_load_balance_link_count_str)
        if line_description:
            sql = sql + \
                ", LINE_DESCRIPTION => '{p_lined}'".format(
                    p_lined=line_description)
        if virtual_lan_id:
            sql = sql + \
                ", VIRTUAL_LAN_ID => '{p_vlan_id}'".format(
                    p_vlan_id=virtual_lan_id)
        sql = sql + ")"

        ibmi_util.log_info("Run sql statement: " + sql, module._name)
        rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(sql)
        if rc:
            module.fail_json(
                rc=rc, msg="Error occurred when remove NRG link, see job log for detail", job_log=job_log)
        module.exit_json(
            rc=0, msg="Success to remove NRG link")


if __name__ == '__main__':
    main()
