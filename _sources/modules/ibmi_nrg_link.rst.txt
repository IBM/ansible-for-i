
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_nrg_link.py

.. _ibmi_nrg_link_module:


ibmi_nrg_link -- Manages NRGs(Network Redundancy Groups) links
==============================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_nrg_link`` module adds or removes a link to one or all of the Db2 Mirror Network Redundancy Groups (NRGs).





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
change_load_balance_link_count
  Indicates whether to increment the load balance link count when ``add`` a new link to the NRG or decrement the load balance link count when ``remove`` a link from the NRG.


  | **required**: false
  | **type**: bool
  | **default**: True


     
line_description
  A string that contains the local system line description associated with this link. This parameter is required when source-address is an IPv6 link-local address and is used to identify a unique local interface. It is ignored for all other addresses.


  | **required**: false
  | **type**: str


     
link_priority
  A string that contains an integer value set as the priority of the link. The range of priorities is from 1 to 16, where 1 is the highest priority. Priority values do not need to be unique.

  Required when the operation is ``add``

  Ignored when the operation is ``remove``


  | **required**: false
  | **type**: str


     
nrg_name
  A string that contains the name of the NRG where the link is to be added. If the NRG does not exist, it will be created.


  | **required**: false
  | **type**: str
  | **default**: \*MIRROR
  | **choices**: \*MIRROR, MIRROR_DATABASE, MIRROR_ENGINE, MIRROR_IFS, MIRROR_OTHER, MIRROR_RESYNC


     
operation
  NRGs link operation.


  | **required**: True
  | **type**: str
  | **choices**: add, remove


     
source_address
  A string that contains the local IP address for the link to add. Either an IPv4 or an IPv6 address can be specified.

  When the operation is ``remove``, it can also contain the following special value ``*ALL`` to remove all links for this NRG.


  | **required**: True
  | **type**: str


     
target_address
  A string that contains the remote IP address for the link to add. Either an IPv4 or an IPv6 address can be specified.

  Required when the operation is ``add``

  Ignored when the operation is ``remove``


  | **required**: false
  | **type**: str


     
virtual_lan_id
  A string that contains an integer value for the local virtual LAN identifier associated with this link. This parameter is required when source-address is an IPv6 link-local address and is used to identify a unique local interface. It is ignored for all other addresses.


  | **required**: false
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
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




Notes
-----

.. note::
   This module supports IBMi 7.4 and above release, and 5770SS1 option 48 is required.

   NRG_INFO and NRG_LINK_INFO view can be used to retrieve the NRG and NRG links information by using module ibmi_sql_query.

   More information about NRG releated services refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/db2mi/db2mservicesnrg.htm



See Also
--------

.. seealso::

   - :ref:`ibmi_sql_query_module`



Return Values
-------------


   
                              
       msg
        | The message that descript the error or success
      
        | **returned**: always
        | **type**: str
        | **sample**: Error occurred when retrieving the mirror state

            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'FROM_INSTRUCTION': '318F', 'FROM_LIBRARY': 'QSYS', 'FROM_MODULE': '', 'FROM_PROCEDURE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'FROM_USER': 'CHANGLE', 'MESSAGE_FILE': 'QCPFMSG', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_SUBTYPE': '', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'ORDINAL_POSITION': '5', 'SEVERITY': '20', 'TO_INSTRUCTION': '9369', 'TO_LIBRARY': 'QSYS', 'TO_MODULE': 'QSQSRVR', 'TO_PROCEDURE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR'}]

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
      
        
