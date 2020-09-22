
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_tcp_interface.py

.. _ibmi_tcp_interface_module:


ibmi_tcp_interface -- Add, change, remove or query a tcp/ip interface.
======================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_tcp_interface`` module add, change, remove, start, end or query a tcp/ip interface.
- This module provides the similar function of ADDTCPIFC, CHGTCPIFC, RMVTCPIFC, STRTCPIFC, ENDTCPIFC.
- In addition, the module provides query function for a specific internet address basing on internet address
- or alias_name.





Parameters
----------


     
alias_name
  A name that can be used in place of the internet address.

  This alias_name can be used to change, remove, start, end and query a internet interface.


  | **required**: False
  | **type**: str


     
associated_local_interface
  Use this parameter to associate the IPv4 interface being added with an existing local IPv4 TCP/IP interface.


  | **required**: False
  | **type**: str


     
auto_start
  Specifies whether the interface is automatically started

  when the TCP/IP stack is activated by the Start TCP/IP (STRTCP) command.


  | **required**: False
  | **type**: str
  | **choices**: \*YES, \*NO


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
extra_params
  The extra parameters that the user wants to pass into this module.

  These are the additional CL parameters that the user wants to pass to execute the CL commands.


  | **required**: False
  | **type**: str


     
internet_address
  The internet address that will be added, changed, removed or queried.

  The internet address may be an IPv4 or IPv6 address.

  An interface is associated with a line description.


  | **required**: False
  | **type**: str


     
joblog
  The job log of the job executing the task will be returned even rc is zero if it is set to True.


  | **required**: false
  | **type**: bool


     
line_description
  the name of the line description associated with the new interface.

  The line description must exist before the TCP/IP interface can be added.


  | **required**: False
  | **type**: str


     
max_transmission_unit
  Specifies the maximum size (in bytes) of IP datagrams that can be transmitted through this interface.


  | **required**: False
  | **type**: str


     
preferred_interface
  A list of preferred IPv4 interfaces that are to be used with the IPv4 interface being added for proxy

  Address Resolution Protocol (ARP) agent selection.


  | **required**: False
  | **type**: list
  | **elements**: str


     
sec_to_wait
  The number of seconds that the module waits after executing the task

  before returning the information of the internet address.

  Some tasks such as start and end the interface will need to wait some seconds

  before it can return the final status.

  If default zero is used, the returned information could be the intermediate status of

  starting or ending the interface.


  | **required**: false
  | **type**: int


     
state
  The state of the interface.

  present means to add, change or query the internet interface.

  When the internet address does not exist on the IBM i system, present option will create the interface.

  When the internet address exists on the IBM i system, and only internet_address or alias_name is specified, present option will query the specific interface.

  When the internet address exists on the IBM i system, and internet_address option is used together with other options, present option will change the specific interface.

  absent means to remove the internet interface. Either internet_address or alias_name can be used.

  If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.

  active means to start the internet interface. Either internet_address or alias_name can be used.

  If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.

  inactive means to end the internet interface. Either internet_address or alias_name can be used.

  If both internet_address and alias_name are used for absent option, the alias_name option will be ignored.


  | **required**: false
  | **type**: str
  | **default**: present
  | **choices**: present, absent, inactive, active


     
subnet_mask
  Defines the subnet mask

  which is a bit mask that defines the part of the network where this IPv4 interface attaches.


  | **required**: False
  | **type**: str


     
text_description
  Specifies text that briefly describes the interface.


  | **required**: False
  | **type**: str


     
type_of_service
  The type of service specifies how the internet hosts and routers should make trade-offs

  between throughput, delay, reliability, and cost.


  | **required**: False
  | **type**: str
  | **choices**: \*NORMAL, \*MINDELAY, \*MAXTHRPUT, \*MAXRLB, \*MINCOST


     
vlan_id
  The virtual LAN identifier of the associated line.

  This identifies the virtual LAN to which this interface belongs according to IEEE standard 802.1Q.

  This parameter is only valid for interfaces defined for Ethernet adapters that support the 802.1Q standard.

  This must be used together with line_description.


  | **required**: False
  | **type**: str




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




Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)






Return Values
-------------


   
                              
       start
        | The task execution start time
      
        | **returned**: When task has been executed.
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: When task has been executed.
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: When task has been executed.
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The task standard output
      
        | **returned**: When task has been executed.
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The task standard error
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: When task has been executed.
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When task has been executed.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
      
                              
       stderr_lines
        | The task standard error split in lines
      
        | **returned**: When task has been executed.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       job_log
        | The job log of the job executes the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       cl_command
        | The CL command executed.
      
        | **returned**: When task has been executed.
        | **type**: str
        | **sample**: CHGTCPIFC INTNETADR('9.5.168.12') SUBNETMASK('255.255.0.0') ALIASNAME(alias2)

            
      
      
                              
       interface_info
        | The interface information. If state is absent, empty list is returned.
      
        | **returned**: When rc is zero.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ALIAS_NAME": "ALIAS2", "AUTOSTART": "YES", "CONFIGURED_MAXIMUM_TRANSMISSION_UNIT": "1024", "CONNECTION_TYPE": "IPV4", "INTERFACE_LINE_TYPE": "VETH", "INTERFACE_STATUS": "INACTIVE", "INTERNET_ADDRESS": "9.5.155.12", "LAST_CHANGE_TIMESTAMP": "2020-04-25T11:57:26", "LINE_DESCRIPTION": "LINDES", "MAXIMUM_TRANSMISSION_UNIT": "LIND", "NETWORK_ADDRESS": "9.5.0.0", "SERVICE_TYPE": "NORMAL", "SUBNET_MASK": "255.255.0.0", "VIRTUAL_LAN_ID": "NONE"}]
            
      
        
