
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_query_job_log.py

.. _ibmi_query_job_log_module:


ibmi_query_job_log -- Query the specfic job log.
================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Query the specfic job log.





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


     
job_name
  job name


  | **required**: True
  | **type**: str


     
job_number
  Job number


  | **required**: True
  | **type**: str


     
job_user
  job user


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Query the specfic job log
     ibmi_query_job_log:
       job_number: "025366"
       job_user: "QUSER"
       job_name: "QZDASOINIT"









Return Values
-------------


   
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       sql
        | the sql executed
      
        | **returned**: always
        | **type**: str
        | **sample**: SELECT ORDINAL_POSITION, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, SEVERITY, MESSAGE_TIMESTAMP, FROM_LIBRARY, FROM_PROGRAM, FROM_MODULE, FROM_PROCEDURE, FROM_INSTRUCTION, TO_LIBRARY, TO_PROGRAM, TO_MODULE, TO_PROCEDURE, TO_INSTRUCTION, FROM_USER, MESSAGE_FILE, MESSAGE_LIBRARY, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT FROM TABLE(QSYS2.JOBLOG_INFO('025366/QUSER/QZDASOINIT'))

            
      
      
                              
       start
        | The command execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The command execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The command execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stderr
        | The command standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stderr_lines
        | The command standard error split in lines
      
        | **returned**: always
        | **type**: list
      
        
