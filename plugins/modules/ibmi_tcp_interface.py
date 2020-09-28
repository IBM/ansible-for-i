#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Wang Yun <cdlwangy@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_tcp_interface
short_description: Add, change, remove or query a tcp/ip interface.
version_added: '2.8.0'
description:
     - The C(ibmi_tcp_interface) module add, change, remove, start, end or query a tcp/ip interface.
     - This module provides the similar function of ADDTCPIFC, CHGTCPIFC, RMVTCPIFC, STRTCPIFC, ENDTCPIFC.
     - In addition, the module provides query function for a specific internet address basing on internet address
     - or alias_name.
options:
  internet_address:
    description:
      - The internet address that will be added, changed, removed or queried.
      - The internet address may be an IPv4 or IPv6 address.
      - An interface is associated with a line description.
    type: str
    required: false
  line_description:
    description:
      - the name of the line description associated with the new interface.
      - The line description must exist before the TCP/IP interface can be added.
    type: str
    required: false
  vlan_id:
    description:
      - The virtual LAN identifier of the associated line.
      - This identifies the virtual LAN to which this interface belongs according to IEEE standard 802.1Q.
      - This parameter is only valid for interfaces defined for Ethernet adapters that support the 802.1Q standard.
      - This must be used together with line_description.
    type: str
    required: false
  subnet_mask:
    description:
      - Defines the subnet mask
      - which is a bit mask that defines the part of the network where this IPv4 interface attaches.
    type: str
    required: false
  alias_name:
    description:
      - A name that can be used in place of the internet address.
      - This alias_name can be used to change, remove, start, end and query a internet interface.
    type: str
    required: false
  associated_local_interface:
    description:
      - Use this parameter to associate the IPv4 interface being added with an existing local IPv4 TCP/IP interface.
    type: str
    required: false
  type_of_service:
    description:
      - The type of service specifies how the internet hosts and routers should make trade-offs
      - between throughput, delay, reliability, and cost.
    type: str
    choices: ["*NORMAL", "*MINDELAY", "*MAXTHRPUT", "*MAXRLB", "*MINCOST"]
    required: false
  max_transmission_unit:
    description:
      - Specifies the maximum size (in bytes) of IP datagrams that can be transmitted through this interface.
    type: str
    required: false
  auto_start:
    description:
      - Specifies whether the interface is automatically started
      - when the TCP/IP stack is activated by the Start TCP/IP (STRTCP) command.
    type: str
    choices: ['*YES', '*NO']
    required: false
  preferred_interface:
    description:
      - A list of preferred IPv4 interfaces that are to be used with the IPv4 interface being added for proxy
      - Address Resolution Protocol (ARP) agent selection.
    type: list
    elements: str
    required: false
  text_description:
    description:
      - Specifies text that briefly describes the interface.
    type: str
    required: false
  sec_to_wait:
    description:
      - The number of seconds that the module waits after executing the task
      - before returning the information of the internet address.
      - Some tasks such as start and end the interface will need to wait some seconds
      - before it can return the final status.
      - If default zero is used, the returned information could be the intermediate status of
      - starting or ending the interface.
    type: int
    default: 0
  joblog:
    description:
      - The job log of the job executing the task will be returned even rc is zero if it is set to True.
    type: bool
    default: false
  extra_params:
    description:
      - The extra parameters that the user wants to pass into this module.
      - These are the additional CL parameters that the user wants to pass to execute the CL commands.
    type: str
    required: false
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str
  state:
    description:
      - The state of the interface.
      - present means to add, change or query the internet interface.
      - When the internet address does not exist on the IBM i system, present option will create the interface.
      - When the internet address exists on the IBM i system, and only internet_address or alias_name is specified,
        present option will query the specific interface.
      - When the internet address exists on the IBM i system, and internet_address option is used together
        with other options, present option will change the specific interface.
      - absent means to remove the internet interface. Either internet_address or alias_name can be used.
      - If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.
      - active means to start the internet interface. Either internet_address or alias_name can be used.
      - If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.
      - inactive means to end the internet interface. Either internet_address or alias_name can be used.
      - If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.
    type: str
    choices: ['present', 'absent', 'inactive', 'active']
    default: 'present'
notes:
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)

author:
    - Wang Yun (@airwangyun)
'''

EXAMPLES = r'''
- name: create an interface 1
  ibmi_tcp_interface:
    internet_address: '9.5.155.11'
    subnet_mask: '255.255.255.0'
    line_description: 'LIND1'
    sec_to_wait: 5
    state: 'present'

- name: create an interface 2
  ibmi_tcp_interface:
    internet_address: '9.5.155.12'
    line_description: 'LIND1'
    subnet_mask: '255.255.255.0'
    state: 'present'
    alias_name: 'alias'

- name: create an interface 3
  ibmi_tcp_interface:
    internet_address: '9.5.155.13'
    line_description: 'LIND1'
    subnet_mask: '255.255.255.0'
    preferred_interface:
      - "9.5.155.12"
    state: 'present'
    alias_name: 'alias13'

- name: create an interface 4
  ibmi_tcp_interface:
    internet_address: '9.5.155.14'
    line_description: 'LIND1'
    subnet_mask: '255.255.255.0'
    preferred_interface:
      - "9.5.155.12"
      - "9.5.155.13"
    state: 'present'
    alias_name: 'alias14'

- name: create an interface 5
  ibmi_tcp_interface:
    internet_address: '9.5.155.15'
    line_description: 'LIND1'
    vlan_id: '2'
    subnet_mask: '255.255.255.0'
    preferred_interface:
      - "9.5.155.12"
      - "9.5.155.13"
    state: 'present'
    alias_name: 'alias15'

- name: change an interface 1
  ibmi_tcp_interface:
    internet_address: '9.5.155.11'
    subnet_mask: '255.255.0.0'
    state: 'present'

- name: change an interface 2
  ibmi_tcp_interface:
    internet_address: '9.5.155.12'
    subnet_mask: '255.255.0.0'
    state: 'present'
    alias_name: 'alias2'

- name: change an interface 3
  ibmi_tcp_interface:
    internet_address: '9.5.155.11'
    preferred_interface:
      - "9.5.155.12"
      - "9.5.155.13"
    state: 'present'

- name: change an interface 4
  ibmi_tcp_interface:
    internet_address: '9.5.155.12'
    state: 'present'
    alias_name: 'alias2'

- name: query an interface by ip
  ibmi_tcp_interface:
    internet_address: '9.5.155.12'
    state: 'present'

- name: query an interface by alias name
  ibmi_tcp_interface:
    alias_name: 'alias14'
    state: 'present'

- name: remove an interface by ip
  ibmi_tcp_interface:
    internet_address: '9.5.155.11'
    state: 'absent'

- name: remove an interface by alias name
  ibmi_tcp_interface:
    alias_name: 'alias2'
    state: 'absent'
'''

RETURN = r'''
start:
    description: The task execution start time
    type: str
    sample: '2019-12-02 11:07:53.757435'
    returned: When task has been executed.
end:
    description: The task execution end time
    type: str
    sample: '2019-12-02 11:07:54.064969'
    returned: When task has been executed.
delta:
    description: The task execution delta time
    type: str
    sample: '0:00:00.307534'
    returned: When task has been executed.
stdout:
    description: The task standard output
    type: str
    sample: 'CPC2102: Library TESTLIB created'
    returned: When task has been executed.
stderr:
    description: The task standard error
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
    returned: When rc as non-zero(failure)
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    sample: 255
    returned: When task has been executed.
stdout_lines:
    description: The task standard output split in lines
    type: list
    sample: [
        "CPC2102: Library TESTLIB created."
    ]
    returned: When task has been executed.
stderr_lines:
    description: The task standard error split in lines
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
    returned: When task has been executed.
job_log:
    description: The job log of the job executes the task.
    returned: always
    type: list
    sample: [
        {
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
        }
    ]
cl_command:
    description: The CL command executed.
    type: str
    sample: "CHGTCPIFC INTNETADR('9.5.168.12') SUBNETMASK('255.255.0.0') ALIASNAME(alias2)"
    returned: When task has been executed.
interface_info:
    description: The interface information. If state is absent, empty list is returned.
    type: list
    returned: When rc is zero.
    sample: [
        {
            "ALIAS_NAME": "ALIAS2",
            "AUTOSTART": "YES",
            "CONNECTION_TYPE": "IPV4",
            "INTERFACE_LINE_TYPE": "VETH",
            "INTERFACE_STATUS": "INACTIVE",
            "INTERNET_ADDRESS": "9.5.155.12",
            "LAST_CHANGE_TIMESTAMP": "2020-04-25T11:57:26",
            "LINE_DESCRIPTION": "LINDES",
            "MAXIMUM_TRANSMISSION_UNIT": "LIND",
            "CONFIGURED_MAXIMUM_TRANSMISSION_UNIT": "1024",
            "NETWORK_ADDRESS": "9.5.0.0",
            "SERVICE_TYPE": "NORMAL",
            "SUBNET_MASK": "255.255.0.0",
            "VIRTUAL_LAN_ID": "NONE"
        }
    ]
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
import time
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_JOB_STATUS_NOT_EXPECTED = 258
IBMi_PARAM_NOT_VALID = 259
IBMi_JOB_STATUS_LIST = ["*NONE", "*ACTIVE", "*COMPLETE", "*JOBQ", "*OUTQ"]


def return_interface_information(db_connection, internet_address, alias_name):
    if internet_address is not None:
        where_condition = "WHERE INTERNET_ADDRESS = '" + internet_address + "'"
    elif alias_name is not None:
        where_condition = "WHERE UPPER(ALIAS_NAME) = '" + alias_name.upper() + "'"
    else:
        where_condition = "1 = 2"
    sql = "SELECT CONNECTION_TYPE, INTERNET_ADDRESS, NETWORK_ADDRESS, SUBNET_MASK, " \
          "LINE_DESCRIPTION, INTERFACE_LINE_TYPE, INTERFACE_STATUS, SERVICE_TYPE, VIRTUAL_LAN_ID, " \
          "MAXIMUM_TRANSMISSION_UNIT, CONFIGURED_MAXIMUM_TRANSMISSION_UNIT, AUTOSTART, ALIAS_NAME, " \
          "LAST_CHANGE_TIMESTAMP " \
          "FROM QSYS2.NETSTAT_INTERFACE_INFO " + where_condition
    out_result_set, err = db2i_tools.ibm_dbi_sql_query(db_connection, sql)

    out = []
    for result in out_result_set:
        result_map = {"CONNECTION_TYPE": result[0], "INTERNET_ADDRESS": result[1],
                      "NETWORK_ADDRESS": result[2], "SUBNET_MASK": result[3],
                      "LINE_DESCRIPTION": result[4], "INTERFACE_LINE_TYPE": result[5],
                      "INTERFACE_STATUS": result[6], "SERVICE_TYPE": result[7],
                      "VIRTUAL_LAN_ID": result[8], "MAXIMUM_TRANSMISSION_UNIT": result[9],
                      "CONFIGURED_MAXIMUM_TRANSMISSION_UNIT": result[10],
                      "AUTOSTART": result[11], "ALIAS_NAME": result[12],
                      "LAST_CHANGE_TIMESTAMP": result[13]
                      }
        out.append(result_map)
    return out, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            internet_address=dict(type='str', required=False),
            line_description=dict(type='str', required=False),
            vlan_id=dict(type='str', required=False),
            subnet_mask=dict(type='str', required=False),
            alias_name=dict(type='str', required=False),
            associated_local_interface=dict(type='str', required=False),
            type_of_service=dict(type='str', required=False, choices=["*NORMAL", "*MINDELAY",
                                                                      "*MAXTHRPUT", "*MAXRLB", "*MINCOST"]),
            max_transmission_unit=dict(type='str', required=False),
            auto_start=dict(type='str', required=False, choices=["*YES", "*NO"]),
            preferred_interface=dict(type='list', elements='str', required=False),
            text_description=dict(type='str', required=False),
            sec_to_wait=dict(type='int', default=0),
            extra_params=dict(type='str', required=False),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
            state=dict(type='str', default='present', choices=["present", "absent", "inactive", "active"])
        ),
        required_one_of=[["internet_address", "alias_name"]],
        supports_check_mode=True,
    )

    internet_address = module.params['internet_address']
    line_description = module.params['line_description']
    vlan_id = module.params['vlan_id']
    subnet_mask = module.params['subnet_mask']
    alias_name = module.params['alias_name']
    associated_local_interface = module.params['associated_local_interface']
    type_of_service = module.params['type_of_service']
    max_transmission_unit = module.params['max_transmission_unit']
    auto_start = module.params['auto_start']
    preferred_interface = module.params['preferred_interface']
    text_description = module.params['text_description']
    state = module.params['state']
    extra_params = module.params['extra_params']
    sec_to_wait = module.params['sec_to_wait']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()

    ibmi_module = imodule.IBMiModule(become_user_name=become_user,
                                     become_user_password=become_user_password)

    connection_id = ibmi_module.get_connection()

    only_query = False
    cl_command = ""

    if state == "present":
        # check options
        opt_vlan_id = "" if vlan_id is None else vlan_id
        opt_line_description = "" if line_description is None else "LIND(" + line_description + " " + opt_vlan_id + ") "
        opt_subnet_mask = "" if subnet_mask is None else "SUBNETMASK('" + subnet_mask + "') "
        opt_alias_name = "" if alias_name is None else "ALIASNAME(" + alias_name + ") "
        opt_associate = "" if associated_local_interface is None else "LCLIFC(" + associated_local_interface + ") "
        opt_type_of_service = "" if type_of_service is None else "TOS(" + type_of_service + ") "
        opt_max_transmission_unit = "" if max_transmission_unit is None else "MTU(" + max_transmission_unit + ") "
        opt_auto_start = "" if auto_start is None else "AUTOSTART(" + auto_start + ") "
        opt_preferred_ifc = "" if preferred_interface is None else "PREFIFC('" + "' '".join(preferred_interface) + "') "
        opt_text_desc = "" if text_description is None else "TEXT('" + text_description + "') "

        # options_without_alias_name = opt_line_description + opt_subnet_mask + \
        #                              opt_associate + opt_type_of_service + \
        #                              opt_max_transmission_unit + opt_auto_start + opt_preferred_ifc + opt_text_desc
        options_without_alias_name = "{0}{1}{2}{3}{4}{5}{6}{7}".format(opt_line_description, opt_subnet_mask,
                                                                       opt_associate, opt_type_of_service,
                                                                       opt_max_transmission_unit, opt_auto_start,
                                                                       opt_preferred_ifc, opt_text_desc)

        options = options_without_alias_name + opt_alias_name

        if (internet_address is not None) and (options == ""):
            # nothing to add or change means to query
            only_query = True
        elif (opt_alias_name is not None) and (internet_address is None) and (options_without_alias_name == ""):
            only_query = True
        else:
            if internet_address is None:
                module.fail_json(msg="Parameter internet_address is not specified.")

            # see if the ip address exists for present
            rs, query_err = return_interface_information(connection_id, internet_address, alias_name)
            present_operation = "QSYS/ADDTCPIFC" if len(rs) == 0 else "QSYS/CHGTCPIFC"

            cl_command = present_operation + " INTNETADR('" + internet_address + "') " + options

    elif state in ["absent", "active", "inactive"]:
        interface_action_map = {"absent": "QSYS/RMVTCPIFC", "active": "QSYS/STRTCPIFC", "inactive": "QSYS/ENDTCPIFC"}
        if internet_address is not None:
            cl_command = interface_action_map[state] + " INTNETADR('" + internet_address + "')"
        elif (alias_name is not None) and (alias_name != '*NONE'):
            cl_command = interface_action_map[state] + " ALIASNAME(" + alias_name + ")"
        else:
            module.fail_json(msg="internet_address or alias_name must be specified when state is"
                                 " absent, active or inactive.")

        check_rs, query_err = return_interface_information(connection_id, internet_address, alias_name)
        if len(check_rs) == 0:
            if state == "absent":
                # we are trying to remove a non-existing interface
                only_query = True
        else:
            interface_status = check_rs[0]["INTERFACE_STATUS"]
            if interface_status == state.upper():
                # This means that the interface status is already what we want, skip the cl execution
                only_query = True
    else:
        module.fail_json(msg="Value for option state is not valid.")

    if extra_params is not None:
        cl_command = cl_command + extra_params

    is_changed = False
    if only_query:
        cl_command = ""
        out = None
        err = None
        rc = IBMi_COMMAND_RC_SUCCESS
    else:
        rc, out, err = ibmi_module.itoolkit_run_command(cl_command)
        if (rc == IBMi_COMMAND_RC_SUCCESS) and (state in ["present", "absent"]):
            is_changed = True

    if sec_to_wait > 0:
        time.sleep(sec_to_wait)

    rs, query_err = return_interface_information(connection_id, internet_address, alias_name)

    if query_err is not None:
        rc = IBMi_COMMAND_RC_ERROR
        err = query_err

    if joblog or (rc != IBMi_COMMAND_RC_SUCCESS):
        job_log = ibmi_module.itoolkit_get_job_log(startd)
    else:
        job_log = []

    endd = datetime.datetime.now()
    delta = endd - startd

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            job_log=job_log,
            changed=is_changed,
            stderr=err,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            stdout=out,
            cl_command=cl_command,
        )
        module.fail_json(msg='Non zero return code.', **result_failed)
    else:
        result_success = dict(
            changed=is_changed,
            stdout=out,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            interface_info=rs,
            cl_command=cl_command,
            job_log=job_log,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
