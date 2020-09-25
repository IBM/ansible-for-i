
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_reply_message.py

.. _ibmi_reply_message_module:


ibmi_reply_message -- Send a reply message to the sender of an inquiry message
==============================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Send a reply message to the sender of an inquiry message.
- For non-IBM i targets, use the :ref:`service <service_module>` module instead.





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


     
ccsid
  Coded character set ID, Vaild value are "1-65535", ``*HEX``, ``*JOB``.


  | **required**: false
  | **type**: str
  | **default**: \*JOB


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool


     
message_key
  Message key.


  | **required**: True
  | **type**: str


     
message_lib
  Message lib.


  | **required**: false
  | **type**: str
  | **default**: \*LIB


     
message_queue
  Message queue.


  | **required**: True
  | **type**: str


     
reject_default_reply
  Reject default reply.


  | **required**: false
  | **type**: str
  | **default**: \*NOALWRJT
  | **choices**: \*NOALWRJT, \*ALWRJT


     
remove_message
  Remove message.


  | **required**: false
  | **type**: str
  | **default**: \*YES
  | **choices**: \*YES, \*NO


     
reply
  Reply.


  | **required**: false
  | **type**: str
  | **default**: \*DFT




Examples
--------

.. code-block:: yaml+jinja

   
   - name: start host server service
     ibmi_reply_message:
       message_key: 1990
       message_queue: QSECOFR
       message_lib: QUSRSYS
       reply: OK
       joblog: True









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
        | **sample**: +++ success STRHOSTSVR SERVER(\*ALL)

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       cmd
        | The command executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: STRHOSTSVR SERVER(\*ALL)

            
      
      
                              
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

                       ["+++ success STRHOSTSVR SERVER(*ALL)"]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
        
