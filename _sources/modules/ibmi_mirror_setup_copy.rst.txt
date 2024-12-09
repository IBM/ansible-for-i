
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_mirror_setup_copy.py

.. _ibmi_mirror_setup_copy_module:


ibmi_mirror_setup_copy -- Configures the Db2 Mirror on the target node.
=======================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_mirror\_setup\_copy` module configures the Db2 Mirror on the target node after the clone.





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


     
ip_address
  The setup copy system IP address.


  | **required**: True
  | **type**: str


     
rdma_subnet_mask
  Sets the subnet mask if the RDMA links subnet is different than the system IP address. If set to :literal:`\*SAME`\ , will retrieve the subnet mask from the system IP address.


  | **required**: false
  | **type**: str
  | **default**: \*SAME




Examples
--------

.. code-block:: yaml+jinja

   
   - name: config the db2 mirror on the copy node
     ibm.power_ibmi.ibmi_mirror_setup_copy:
       ip_address: 192.168.100.2
       rdma_subnet_mask: 255.255.252.0






See Also
--------

.. seealso::

   - :ref:`ibmi_mirror_setup_source_module`


  

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
      
        
