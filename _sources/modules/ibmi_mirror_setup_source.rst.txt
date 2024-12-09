
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_mirror_setup_source.py

.. _ibmi_mirror_setup_source_module:


ibmi_mirror_setup_source -- Configures the Db2 Mirror on the source node
========================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_mirror\_setup\_source` module configures the Db2 Mirror on the source node and sets the configuration state to initializing.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in :literal:`become\_user`.


  | **required**: false
  | **type**: str


     
clone_type
  Indicates the clone is warm clone or cold clone A cold clone requires the setup source node to be shut down during the cloning portion of the setup process. A warm clone allows the setup source node to remain active during the entire Db2 Mirror setup and configuration process.


  | **required**: false
  | **type**: str
  | **default**: COLD
  | **choices**: COLD, WARM


     
default_inclusion_state
  The default inclusion state setting will be used when no applicable rules for an object are found in the Replication Criteria List (RCL).


  | **required**: false
  | **type**: str
  | **default**: EXCLUDE
  | **choices**: EXCLUDE, INCLUDE


     
primary_hostname
  String that contains the host and domain name or IP address of the partition designated as the primary node. IP address is preferred.


  | **required**: True
  | **type**: str


     
primary_node
  The name of the partition designated as the secondary node. It must be same as the current system name.


  | **required**: True
  | **type**: str


     
secondary_hostname
  String that contains the host and domain name or IP address of the partition designated as the secondary node. IP address is preferred.


  | **required**: True
  | **type**: str


     
secondary_node
  The name of the partition designated as the secondary node.


  | **required**: True
  | **type**: str


     
terminate_confirmed
  A bool value to indicate the terminate mirror action is confirmed.

  When set to False, only the replication state as NOT\_MIRRORED is allowed to run this module.

  When set to True, this module will execute the terminate mirror without checking the replication state.


  | **required**: false
  | **type**: bool


     
termination_level
  The TERMINATE\_MIRROR procedure ends all replication between the primary and secondary nodes and resets the replication state of both nodes to NOT MIRRORED. A clone operation is required to restart replication. When termination\_level is RECLONE, all Db2 Mirror configuration information is retained. When termination\_level is DESTROY, all Db2 Mirror configuration information is deleted.


  | **required**: false
  | **type**: str
  | **default**: RECLONE
  | **choices**: RECLONE, DESTROY


     
time_server
  String that identifies the DNS name of the NTP server to be added to the configuration. A time server must be used to keep the clocks of the nodes synchronized.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: config db2 mirror on source node
     ibm.power_ibmi.ibmi_mirror_setup_source:
       termination_level: RECLONE
       primary_node: NODEA
       secondary_node: NODEB
       primary_hostname: 10.0.0.1
       secondary_hostname: 10.0.0.2
       default_inclusion_state: INCLUDE
       time_server: TIME.COM
       clone_type: WARM






See Also
--------

.. seealso::

   - :ref:`ibmi_mirror_setup_copy_module`


  

Return Values
-------------


   
                              
       msg
        | The message that describes the error or success
      
        | **returned**: always
        | **type**: str
        | **sample**: Error occurred when retrieving the mirror state

            
      
      
                              
       job_log
        | the job\_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'FROM_INSTRUCTION': '318F', 'FROM_LIBRARY': 'QSYS', 'FROM_MODULE': '', 'FROM_PROCEDURE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'FROM_USER': 'CHANGLE', 'MESSAGE_FILE': 'QCPFMSG', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_SUBTYPE': '', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'ORDINAL_POSITION': '5', 'SEVERITY': '20', 'TO_INSTRUCTION': '9369', 'TO_LIBRARY': 'QSYS', 'TO_MODULE': 'QSQSRVR', 'TO_PROCEDURE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR'}]

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
        
