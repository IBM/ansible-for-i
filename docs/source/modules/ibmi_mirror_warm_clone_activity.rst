
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_mirror_warm_clone_activity.pyy

.. _ibmi_mirror_warm_clone_activity_module:


ibmi_mirror_warm_clone_activity -- Performs suspend and resume activity for warm clone.
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_mirror_warm_clone_activity`` module performs the suspend and resume activity for a warm clone to reach a quiesce point before the clone and resume from that point after clone.
- The setup source node must reach a quiesce point before tracking changes can begin.
- If a quiesce point cannot be reached within the specified timeout, then the setup process will not proceed.





Parameters
----------


     
operation
  Specifies the activity to be performed for a warm clone.


  | **required**: True
  | **type**: str
  | **choices**: suspend, resume


     
suspend_timeout
  Specifies the the number of seconds timeout value to allow for the suspend operation to complete.


  | **required**: false
  | **type**: int
  | **default**: 300




Examples
--------

.. code-block:: yaml+jinja

   
   - name: suspend the system for a warm clone to do a clone
     ibmi_mirror_warm_clone_activity:
       operation: suspend






See Also
--------

.. seealso::

   - :ref:`ibmi_mirror_setup_source_module`



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
      
        
