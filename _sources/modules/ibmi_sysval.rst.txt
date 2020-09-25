
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sysval.py

.. _ibmi_sysval_module:


ibmi_sysval -- Displays the specified system value
==================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_sysval`` module displays the information of the specified system value.
- Type of requisite values meaning refer to https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_74/apis/qwcrsval.htm
- If the returned system valus is a list, set ``check`` to ``equal_as_list`` to compare it with the ``expect`` value.





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


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
sysvalue
  Specifies the input system values. The detail explanations of the elements in the dict are as follows

  ``name`` is the name of the system value. (required)

  ``expect`` is the expected returned value. (optional)

  ``check`` is the comparison method, including ``equal`` and ``equal_as_list``. The default value is ``equal`` (optional)


  | **required**: True
  | **type**: list
  | **elements**: dict




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Get System Value information
     ibmi_sysval:
       sysvalue:
         - {'name':'qmaxsgnacn', 'expect':'3'}
         - {'name':'qccsid'}
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: Compare the returned system valus as list
     ibmi_sysval:
       sysvalue:
         - {'name':'QATNPGM', 'expect':'QEZMAIN   QSYS'}
         - {'name':'QATNPGM', 'expect':'QSYS  QEZMAIN'}
         - {'name':'QATNPGM', 'expect':'QEZMAIN  QSYS', 'check':'equal_as_list'}
         - {'name':'QATNPGM', 'expect':'QSYS QEZMAIN', 'check':'equal_as_list'}









Return Values
-------------


   
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       message
        | The command execution result.
      
        | **returned**: when rc is not 0
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       system_values
        | the system value information
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"compliant": true, "expect": "3", "name": "QMAXSGNACN", "type": "4A", "value": "3"}, {"compliant": true, "name": "QCCSID", "type": "10i0", "value": "65535"}]
            
      
        
