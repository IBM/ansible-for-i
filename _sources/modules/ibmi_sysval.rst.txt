
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_sysval.py

.. _ibmi_sysval_module:


ibmi_sysval -- Displays the specified system value
==================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The \ :literal:`ibmi\_sysval`\  module displays the information of the specified system value.
- Type of requisite values meaning refer to https://www.ibm.com/support/knowledgecenter/en/ssw\_ibm\_i\_74/apis/qwcrsval.htm
- If the returned system valus is a list, set \ :literal:`check`\  to \ :literal:`equal\_as\_list`\  to compare it with the \ :literal:`expect`\  value.





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


     
joblog
  If set to \ :literal:`true`\ , output the available job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
sysvalue
  Specifies the input system values. The detail explanations of the elements in the dict are as follows

  \ :literal:`name`\  is the name of the system value. (required)

  \ :literal:`expect`\  is the expected returned value. If it is a number, the system value will be converted to a number brfore comparison. (optional)

  \ :literal:`check`\  is the comparison method, including \ :literal:`equal`\ , \ :literal:`range`\  and \ :literal:`equal\_as\_list`\ . The default value is \ :literal:`equal`\ . (optional)


  | **required**: True
  | **type**: list
  | **elements**: dict




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Get System Value information
     ibm.power_ibmi.ibmi_sysval:
       sysvalue:
         - {'name':'qmaxsgnacn', 'expect':3}
         - {'name':'qmaxsgnacn', 'expect':'000003'}
         - {'name':'qccsid'}
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: Compare the returned system values as list
     ibm.power_ibmi.ibmi_sysval:
       sysvalue:
         - {'name':'QATNPGM', 'expect':'QEZMAIN   QSYS'}
         - {'name':'QATNPGM', 'expect':'QSYS  QEZMAIN'}
         - {'name':'QATNPGM', 'expect':'QEZMAIN  QSYS', 'check':'equal_as_list'}
         - {'name':'QATNPGM', 'expect':'QSYS QEZMAIN', 'check':'equal_as_list'}

   - name: Check if the returned system values are in a range
     ibm.power_ibmi.ibmi_sysval:
       sysvalue:
         - {'name':'qmaxsgnacn', 'expect':'[1,8)', 'check':'range'}
         - {'name':'qccsid', 'expect':'[0,65535]', 'check':'range'}








  

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
            
      
      
                              
       sysval
        | the system value information
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"compliant": true, "expect": "3", "name": "QMAXSGNACN", "type": "4A", "value": "3"}, {"compliant": true, "name": "QCCSID", "type": "10i0", "value": "65535"}]
            
      
      
                              
       fail_list
        | the failed parameters
      
        | **returned**: when there are failed parameters
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"compliant": false, "expect": "3", "name": "QMAXSGNACN", "type": "4A", "value": "1"}]
            
      
        
