
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_message.py

.. _ibmi_message_module:


ibmi_message -- Search message
==============================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Search message.
- For non-IBM i targets, no need.





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
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool


     
message_id
  The id of the message.


  | **required**: false
  | **type**: list
  | **elements**: str


     
message_lib
  The library name which contains message queue.


  | **required**: True
  | **type**: str


     
message_queue
  The queue of the message.


  | **required**: false
  | **type**: list
  | **elements**: str


     
message_text
  The message text of the message.


  | **required**: false
  | **type**: str


     
message_type
  The type of the message.

  INFORMATIONAL, A message that conveys information about the condition of a function.

  COMPLETION, A message that conveys completion status of work.

  DIAGNOSTIC, A message about errors in the processing of a system function, in an application program, or in input data.

  ESCAPE, A message that describes a condition for which a procedure or program must end abnormally. A procedure or program can monitor for the arrival of escape messages from the program or procedure it calls or from the machine. Control does not return to the sending program after an escape message is sent.

  INQUIRY, A message that conveys information but also asks for a reply.

  REPLY, A message that is a response to a received inquiry or notify message.

  NOTIFY, A message that describes a condition for which a procedure or program requires corrective action or a reply from its calling procedure or program. A procedure or program can monitor for the arrival of notify messages from the programs or procedures it calls.

  REQUEST, A message that requests a function from the receiving procedure or program. (For example, a CL command is a request message.)

  SENDER, an inquiry or notify message that is kept by the sender.

  NO_REPLY, a message that type is "INQUIRY" and has not been replied.


  | **required**: True
  | **type**: str
  | **choices**: INFORMATIONAL, COMPLETION, DIAGNOSTIC, ESCAPE, INQUIRY, REPLY, NOTIFY, REQUEST, SENDER, NO_REPLY


     
operation
  The operation of the messgae.


  | **required**: True
  | **type**: str
  | **choices**: find




Examples
--------

.. code-block:: yaml+jinja

   
   - name: find a message with message type, message_lib, message_queue and message_id
     ibmi_message:
       operation: 'find'
       message_type: 'INFORMATIONAL'
       message_lib: 'QUSRSYS'
       message_queue: ['QPGMR', 'QSECOFR']
       message_id: ['CPF1241', 'CPF1240']

   - name: find all un-reply message with message type, message_lib and message_queue, run as another user
     ibmi_message:
       operation: 'find'
       message_type: 'NO_REPLY'
       message_lib: 'QUSRSYS'
       message_queue: ['QPGMR', 'QSECOFR']
       become_user: 'USER1'
       become_user_password: 'yourpassword'






See Also
--------

.. seealso::

   - :ref:`service_module`



Return Values
-------------


   
                              
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

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: Generic failure

            
      
      
                              
       sql
        | The sql executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: SELECT MESSAGE_QUEUE_LIBRARY, MESSAGE_QUEUE_NAME, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, MESSAGE_TEXT, SEVERITY, MESSAGE_TIMESTAMP, MESSAGE_KEY, ASSOCIATED_MESSAGE_KEY, FROM_USER, FROM_JOB, FROM_PROGRAM, MESSAGE_FILE_LIBRARY, MESSAGE_FILE_NAME, MESSAGE_SECOND_LEVEL_TEXT FROM QSYS2.MESSAGE_QUEUE_INFO WHERE MESSAGE_QUEUE_LIBRARY = 'QUSRSYS' AND MESSAGE_QUEUE_NAME = 'CHANGLE' OR MESSAGE_QUEUE_NAME = 'QHQB' AND MESSAGE_ID = 'CPF1241' OR MESSAGE_ID = 'CPF1240' AND MESSAGE_TYPE = 'INFORMATIONAL'

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       message_info
        | The message_info.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ASSOCIATED_MESSAGE_KEY": "", "FROM_JOB": "013447/QSYS/QINTER", "FROM_PROGRAM": "QWTMMDSC", "FROM_USER": "QSYS", "MESSAGE_FILE_LIBRARY": "QSYS", "MESSAGE_FILE_NAME": "QCPFMSG", "MESSAGE_ID": "CPI1131", "MESSAGE_KEY": "00003B70", "MESSAGE_QUEUE_LIBRARY": "QSYS", "MESSAGE_QUEUE_NAME": "QSYSOPR", "MESSAGE_SECOND_LEVEL_TEXT": "\u0026N Cause . . . . . :   User QSYS performed the Disconnect Job (DSCJOB) command for the job.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "CPI1131 Job 013659/CHANGLE/QPADEV0002 disconnected by user QSYS.", "MESSAGE_TIMESTAMP": "2020-04-24-09.44.35.568129", "MESSAGE_TYPE": "INFORMATIONAL", "SEVERITY": "0"}]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Generic failure."]
            
      
        
