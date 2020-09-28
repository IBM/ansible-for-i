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
module: ibmi_nrg_link
short_description: Manages NRGs(Network Redundancy Groups) links
version_added: '2.8.0'
description:
  - The C(ibmi_nrg_link) module adds or removes a link to one or all of the Db2 Mirror Network Redundancy Groups (NRGs).
options:
  operation:
    description:
      - NRGs link operation.
    type: str
    choices: ['add', 'remove']
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
      - When the operation is C(remove), it can also contain the following special value C(*ALL) to remove all links for this NRG.
    type: str
    required: yes
  target_address:
    description:
      - A string that contains the remote IP address for the link to add. Either an IPv4 or an IPv6 address can be specified.
      - Required when the operation is C(add)
      - Ignored when the operation is C(remove)
    type: str
  link_priority:
    description:
      - A string that contains an integer value set as the priority of the link.
        The range of priorities is from 1 to 16, where 1 is the highest priority. Priority values do not need to be unique.
      - Required when the operation is C(add)
      - Ignored when the operation is C(remove)
    type: str
  change_load_balance_link_count:
    description:
      - Indicates whether to increment the load balance link count when C(add) a new link to the NRG or
        decrement the load balance link count when C(remove) a link from the NRG.
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
  - This module supports IBMi 7.4 and above release, and 5770SS1 option 48 is required.
  - NRG_INFO and NRG_LINK_INFO view can be used to retrieve the NRG and NRG links information by using module ibmi_sql_query.
  - More information about NRG releated services refer to
    https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/db2mi/db2mservicesnrg.htm

seealso:
- module: ibmi_sql_query

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: add a link to the db2 mirror nrg
  ibmi_nrg_link:
    operation: add
    source_address: 10.0.0.1
    target_address: 10.0.0.2
    link_priority: 1

- name: remove a link from the db2 mirror nrg with become user
  ibmi_nrg_link:
    operation: remove
    source_address: 10.0.0.1
    become_user: 'USER1'
    become_user_password: 'yourpassword'
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
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', choices=[
                           'add', 'remove'], required=True),
            nrg_name=dict(type='str', choices=['*MIRROR', 'MIRROR_DATABASE', 'MIRROR_ENGINE',
                                               'MIRROR_IFS', 'MIRROR_OTHER', 'MIRROR_RESYNC'], default='*MIRROR'),
            source_address=dict(type='str', required=True),
            target_address=dict(type='str'),
            link_priority=dict(type='str'),
            change_load_balance_link_count=dict(type='bool', default=True),
            line_description=dict(type='str', default=''),
            virtual_lan_id=dict(type='str', default=''),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
        required_if=[
            ['operation', 'add', ['target_address', 'link_priority']],
        ],
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)
    operation = module.params['operation']
    nrg_name = module.params['nrg_name']
    source_address = module.params['source_address']
    target_address = module.params['target_address']
    link_priority = module.params['link_priority']
    change_load_balance_link_count = module.params['change_load_balance_link_count']
    line_description = module.params['line_description']
    virtual_lan_id = module.params['virtual_lan_id']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if change_load_balance_link_count:
        change_load_balance_link_count_str = 'YES'
    else:
        change_load_balance_link_count_str = 'NO'

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    if operation == 'add':
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
                rc=255, msg="The value of argument source_address can not be '*ALL' when the operation is 'add'")

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
        rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(sql)
        ibmi_util.log_debug("out={0}, err={1} ".format(str(out), str(err)), module._name)
        if rc:
            if (rc == ibmi_util.IBMi_PACKAGES_NOT_FOUND) or (rc == ibmi_util.IBMi_DB_CONNECTION_ERROR):
                msg = "Error occurred when add NRG link: {0}".format(err)
            else:
                msg = "Error occurred when add NRG link, see job log for detail"
            module.fail_json(
                rc=rc, msg=msg, job_log=job_log)

        sql = "CALL QSYS2.CHANGE_NRG(NRG_NAME => '{p_name}', NRG_DESCRIPTION => 'DB2MIRROR GROUP')".format(p_name=nrg_name)
        ibmi_util.log_info("Run sql statement: " + sql, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(sql)
        ibmi_util.log_debug("out={0}, err={1} ".format(str(out), str(err)), module._name)
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
        rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(sql)
        ibmi_util.log_debug("out={0}, err={1} ".format(str(out), str(err)), module._name)
        if rc:
            module.fail_json(
                rc=rc, msg="Error occurred when remove NRG link, see job log for detail", job_log=job_log)
        module.exit_json(
            rc=0, msg="Success to remove NRG link")


if __name__ == '__main__':
    main()
