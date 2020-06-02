..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_tcp_interface.py


ibmi_tcp_interface -- Add, change, remove or query a tcp/ip interface.
======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_tcp_interface`` module add, change, remove, start, end or query a tcp/ip interface.

This module provides the similar function of ADDTCPIFC, CHGTCPIFC, RMVTCPIFC, STRTCPIFC, ENDTCPIFC.

In addition, the module provides query function for a specific internet address basing on internet address

or alias_name.






Parameters
----------

  line_description (False, str, None)
    the name of the line description associated with the new interface.

    The line description must exist before the TCP/IP interface can be added.


  type_of_service (False, str, None)
    The type of service specifies how the internet hosts and routers should make trade-offs

    between throughput, delay, reliability, and cost.


  preferred_interface (False, list, None)
    A list of preferred IPv4 interfaces that are to be used with the IPv4 interface being added for proxy

    Address Resolution Protocol (ARP) agent selection.


  text_description (False, str, None)
    Specifies text that briefly describes the interface.


  associated_local_interface (False, str, None)
    Use this parameter to associate the IPv4 interface being added with an existing local IPv4 TCP/IP interface.


  sec_to_wait (optional, int, 0)
    The number of seconds that the module waits after executing the task

    before returning the information of the internet address.

    Some tasks such as start and end the interface will need to wait some seconds

    before it can return the final status.

    If default zero is used, the returned information could be the intermediate status of

    starting or ending the interface.


  max_transmission_unit (False, str, None)
    Specifies the maximum size (in bytes) of IP datagrams that can be transmitted through this interface.


  subnet_mask (False, str, None)
    Defines the subnet mask

    which is a bit mask that defines the part of the network where this IPv4 interface attaches.


  state (optional, str, present)
    The state of the interface.

    present means to add, change or query the internet interface.

    When the internet address does not exist on the IBM i system, present option will create the interface.

    When the internet address exists on the IBM i system, and only internet_address or alias_name is specified,

    present option will query the specific interface.

    When the internet address exists on the IBM i system, and internet_address option is used together

    with other options, present option will change the specific interface.

    absent mean to remove the internet interface. Either internet_address or alias_name can be used.

    If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.

    active means to start the internet interface. Either internet_address or alias_name can be used.

    If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.

    inactive means to end the internet interface. Either internet_address or alias_name can be used.

    If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.


  auto_start (False, str, None)
    Specifies whether the interface is automatically started

    when the TCP/IP stack is activated by the Start TCP/IP (STRTCP) command.


  extra_params (False, str, None)
    The extra parameters that the user wants to pass into this module.

    These are the additional CL parameters that the user wants to pass to execute the CL commands.


  internet_address (False, str, None)
    The internet address that will be added, changed, removed or queried.

    The internet address may be an IPv4 or IPv6 address.

    An interface is associated with a line description.


  alias_name (False, str, None)
    A name that can be used in place of the internet address.

    This alias_name can be used to change, remove, start, end and query a internet interface.


  vlan_id (False, str, None)
    The virtual LAN identifier of the associated line.

    This identifies the virtual LAN to which this interface belongs according to IEEE standard 802.1Q.

    This parameter is only valid for interfaces defined for Ethernet adapters that support the 802.1Q standard.

    This must be used together with line_description.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Examples
--------

.. code-block:: yaml+jinja

    
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



Return Values
-------------

  stderr_lines (When task has been executed., list, ['CPF2111:Library TESTLIB already exists.'])
    The task standard error split in lines


  end (When task has been executed., str, 2019-12-02 11:07:54.064969)
    The task execution end time


  stderr (When rc as non-zero(failure), str, CPF2111:Library TESTLIB already exists)
    The task standard error


  stdout (When task has been executed., str, CPC2102: Library TESTLIB created)
    The task standard output


  cl_command (When task has been executed., str, CHGTCPIFC INTNETADR('9.5.168.12') SUBNETMASK('255.255.0.0') ALIASNAME(alias2))
    The CL command executed.


  rc (When task has been executed., int, 255)
    The task return code (0 means success, non-zero means failure)


  start (When task has been executed., str, 2019-12-02 11:07:53.757435)
    The task execution start time


  interface_info (When rc is zero., list, [{'CONNECTION_TYPE': 'IPV4', 'LINE_DESCRIPTION': 'LINDES', 'MAXIMUM_TRANSMISSION_UNIT': 'LIND', 'VIRTUAL_LAN_ID': 'NONE', 'NETWORK_ADDRESS': '9.5.0.0', 'SUBNET_MASK': '255.255.0.0', 'INTERFACE_LINE_TYPE': 'VETH', 'AUTOSTART': 'YES', 'LAST_CHANGE_TIMESTAMP': '2020-04-25T11:57:26', 'SERVICE_TYPE': 'NORMAL', 'INTERNET_ADDRESS': '9.5.155.12', 'CONFIGURED_MAXIMUM_TRANSMISSION_UNIT': '1024', 'ALIAS_NAME': 'ALIAS2', 'INTERFACE_STATUS': 'INACTIVE'}])
    The interface information. If state is absent, empty list is returned.


  delta (When task has been executed., str, 0:00:00.307534)
    The task execution delta time


  stdout_lines (When task has been executed., list, ['CPC2102: Library TESTLIB created.'])
    The task standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Wang Yun (@airwangyun)

