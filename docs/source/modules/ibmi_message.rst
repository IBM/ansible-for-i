..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_message.py

.. _ibmi_message_module:

ibmi_message -- Search or reply message on a remote IBMi node
=============================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Search or reply message on a remote IBMi node
- For non-IBMi targets, no need



Parameters
----------


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool


     
message_id
  the id of the message


  | **required**: false
  | **type**: list
  | **elements**: str


     
message_lib
  the library name which contains message queue


  | **required**: True
  | **type**: str


     
message_queue
  the queue of the message


  | **required**: false
  | **type**: list
  | **elements**: str


     
message_text
  the message text of the message


  | **required**: false
  | **type**: str


     
message_type
  the type of the message

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
  the operation of the messgae


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

   - name: find all un-reply message with message type, message_lib and message_queue
     ibmi_message:
       operation: 'find'
       message_type: 'NO_REPLY'
       message_lib: 'QUSRSYS'
       message_queue: ['QPGMR', 'QSECOFR']




See Also
--------

.. seealso::

   - :ref:`service_module`


Return Values
-------------


   
                              
       stderr_lines
        | The command standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Generic failure."]
            
      
      
                              
       end
        | The command execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_KEY': '00000379', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'TO_INSTRUCTION': '9369', 'FROM_MODULE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'FROM_USER': 'CHANGLE', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'FROM_PROCEDURE': '', 'FROM_INSTRUCTION': '318F', 'MESSAGE_LIBRARY': 'QSYS', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '20', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'TO_LIBRARY': 'QSYS', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '5', 'MESSAGE_FILE': 'QCPFMSG', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       sql
        | The sql executed by the task
      
        | **returned**: always
        | **type**: str
        | **sample**: SELECT MESSAGE_QUEUE_LIBRARY, MESSAGE_QUEUE_NAME, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, MESSAGE_TEXT, SEVERITY, MESSAGE_TIMESTAMP, MESSAGE_KEY, ASSOCIATED_MESSAGE_KEY, FROM_USER, FROM_JOB, FROM_PROGRAM, MESSAGE_FILE_LIBRARY, MESSAGE_FILE_NAME, MESSAGE_SECOND_LEVEL_TEXT FROM QSYS2.MESSAGE_QUEUE_INFO WHERE MESSAGE_QUEUE_LIBRARY = 'QUSRSYS' AND MESSAGE_QUEUE_NAME = 'CHANGLE' OR MESSAGE_QUEUE_NAME = 'QHQB' AND MESSAGE_ID = 'CPF1241' OR MESSAGE_ID = 'CPF1240' AND MESSAGE_TYPE = 'INFORMATIONAL'

            
      
      
                              
       delta
        | The command execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       message_info
        | the message_info
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'MESSAGE_KEY': '00003B70', 'ASSOCIATED_MESSAGE_KEY': '', 'MESSAGE_TEXT': 'CPI1131 Job 013659/CHANGLE/QPADEV0002 disconnected by user QSYS.', 'MESSAGE_QUEUE_NAME': 'QSYSOPR', 'FROM_PROGRAM': 'QWTMMDSC', 'MESSAGE_QUEUE_LIBRARY': 'QSYS', 'FROM_USER': 'QSYS', 'MESSAGE_TIMESTAMP': '2020-04-24-09.44.35.568129', 'MESSAGE_SECOND_LEVEL_TEXT': '&N Cause . . . . . :   User QSYS performed the Disconnect Job (DSCJOB) command for the job.', 'MESSAGE_TYPE': 'INFORMATIONAL', 'MESSAGE_ID': 'CPI1131', 'SEVERITY': '0', 'MESSAGE_FILE_LIBRARY': 'QSYS', 'MESSAGE_SUBTYPE': '', 'FROM_JOB': '013447/QSYS/QINTER', 'MESSAGE_FILE_NAME': 'QCPFMSG'}]

            
      
      
                              
       start
        | The command execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       stderr
        | The command standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: Generic failure

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
        
