
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_tcp_server_service.py

.. _ibmi_tcp_server_service_module:


ibmi_tcp_server_service -- Manage tcp server
============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage and query IBMi tcp server service.
- For non-IBMi targets, use the \ :ref:`ansible.builtin.service <ansible_collections.ansible.builtin.service_module>`\  module instead.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in \ :literal:`become\_user`\ .


  | **required**: false
  | **type**: str


     
extra_parameters
  Extra parameter is appended at the end of tcp server service command.


  | **required**: false
  | **type**: str
  | **default**:  


     
joblog
  If set to \ :literal:`true`\ , append JOBLOG to stderr/stderr\_lines.


  | **required**: false
  | **type**: bool


     
name_list
  The name of the tcp server service. The valid value are \ :literal:`\*ALL`\ , \ :literal:`\*AUTOSTART`\ , \ :literal:`\*BOOTP`\ , \ :literal:`\*DBG`\ , \ :literal:`\*DDM`\ , \ :literal:`\*DHCP`\ , \ :literal:`\*DIRSRV`\ , \ :literal:`\*DLFM`\ , \ :literal:`\*DNS`\ , \ :literal:`\*DOMINO`\ , \ :literal:`\*EDRSQL`\ , \ :literal:`\*FTP`\ , \ :literal:`\*HTTP`\ , \ :literal:`\*HOD`\ , \ :literal:`\*IAS`\ , \ :literal:`\*INETD`\ , \ :literal:`\*LPD`\ , \ :literal:`\*MGTC`\ , \ :literal:`\*NETSVR`\ , \ :literal:`\*NSLD`\ , \ :literal:`\*NTP`\ , \ :literal:`\*ODPA`\ , \ :literal:`\*OMPROUTED`\ , \ :literal:`\*ONDMD`\ , \ :literal:`\*POP`\ , \ :literal:`\*QOS`\ , \ :literal:`\*REXEC`\ , \ :literal:`\*ROUTED`\ , \ :literal:`\*SLP`\ , \ :literal:`\*SMTP`\ , \ :literal:`\*SNMP`\ , \ :literal:`\*SRVSPTPRX`\ , \ :literal:`\*SSHD`\ , \ :literal:`\*TCM`\ , \ :literal:`\*TELNET`\ , \ :literal:`\*TFTP`\ , \ :literal:`\*VPN`\ , \ :literal:`\*WEBFACING`\ .


  | **required**: True
  | **type**: list
  | **elements**: str


     
state
  \ :literal:`started`\ /\ :literal:`stopped`\  are idempotent actions that will not run commands unless necessary.


  | **required**: True
  | **type**: str
  | **choices**: started, stopped




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Start http server with tcp server service
     ibm.power_ibmi.ibmi_tcp_server_service:
       name_list: ['*HTTP']
       state: 'started'
       joblog: True

   - name: Stop ssh server
     ibm.power_ibmi.ibmi_tcp_server_service:
       name_list: ['*SSH']
       state: 'stopped'
       joblog: True

   - name: Restart ssh server (in the same playbook as stopping ssh server)
     ibm.power_ibmi.ibmi_tcp_server_service:
       name_list: ['*SSH']
       state: 'started'
       joblog: True






See Also
--------

.. seealso::

   - :ref:`service_module`


  

Return Values
-------------


   
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       start
        | The command execution start time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The command execution end time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The command execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The command standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       cmd
        | The command executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: CRTLIB LIB(TESTLIB)

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The command standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
        
