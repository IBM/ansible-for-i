..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_message.py


ibmi_message -- Search or reply message on a remote IBMi node
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Search or reply message on a remote IBMi node

For non-IBMi targets, no need






Parameters
----------

  message_queue (optional, list, None)
    the queue of the message


  message_lib (True, str, None)
    the library name which contains message queue


  message_text (optional, str, None)
    the message text of the message


  operation (True, str, None)
    the operation of the messgae


  message_type (True, str, None)
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


  message_id (optional, list, None)
    the id of the message







See Also
--------

.. seealso::

   :ref:`service_module`
      The official documentation on the **service** module.


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



Return Values
-------------

  stderr_lines (always, list, ['Generic failure.'])
    The command standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The command execution end time


  stdout (always, str, Success)
    The command standard output


  sql (always, str, SELECT MESSAGE_QUEUE_LIBRARY, MESSAGE_QUEUE_NAME, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, MESSAGE_TEXT, SEVERITY, MESSAGE_TIMESTAMP, MESSAGE_KEY, ASSOCIATED_MESSAGE_KEY, FROM_USER, FROM_JOB, FROM_PROGRAM, MESSAGE_FILE_LIBRARY, MESSAGE_FILE_NAME, MESSAGE_SECOND_LEVEL_TEXT FROM QSYS2.MESSAGE_QUEUE_INFO WHERE MESSAGE_QUEUE_LIBRARY = 'QUSRSYS' AND MESSAGE_QUEUE_NAME = 'CHANGLE' OR MESSAGE_QUEUE_NAME = 'QHQB' AND MESSAGE_ID = 'CPF1241' OR MESSAGE_ID = 'CPF1240' AND MESSAGE_TYPE = 'INFORMATIONAL')
    The sql executed by the task


  rc (always, int, 255)
    The command return code (0 means success, non-zero means failure)


  message_info (always, str, [{'MESSAGE_KEY': '00003B70', 'ASSOCIATED_MESSAGE_KEY': '', 'MESSAGE_TEXT': 'CPI1131 Job 013659/CHANGLE/QPADEV0002 disconnected by user QSYS.', 'MESSAGE_QUEUE_NAME': 'QSYSOPR', 'FROM_PROGRAM': 'QWTMMDSC', 'MESSAGE_QUEUE_LIBRARY': 'QSYS', 'FROM_USER': 'QSYS', 'MESSAGE_TIMESTAMP': '2020-04-24-09.44.35.568129', 'MESSAGE_SECOND_LEVEL_TEXT': '&N Cause . . . . . :   User QSYS performed the Disconnect Job (DSCJOB) command for the job.', 'MESSAGE_TYPE': 'INFORMATIONAL', 'MESSAGE_ID': 'CPI1131', 'SEVERITY': '0', 'MESSAGE_FILE_LIBRARY': 'QSYS', 'MESSAGE_SUBTYPE': '', 'FROM_JOB': '013447/QSYS/QINTER', 'MESSAGE_FILE_NAME': 'QCPFMSG'}])
    the message_info


  start (always, str, 2019-12-02 11:07:53.757435)
    The command execution start time


  stderr (always, str, Generic failure)
    The command standard error


  delta (always, str, 0:00:00.307534)
    The command execution delta time


  stdout_lines (always, list, ['Success'])
    The command standard output split in lines


  rc_msg (always, str, Generic failure)
    Meaning of the return code





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Jin Yi Fan(@jinyifan)

