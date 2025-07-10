
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_subsystem.py

.. _ibmi_subsystem_module:


ibmi_subsystem -- Manage a subsystem with various operations.
=============================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_subsystem` module allows managing a subsystem with operations for start, end, restart, and display.
- The :literal:`start` operation starts an inactive subsystem.
- The :literal:`end` operation ends an active subsystem.
- The :literal:`restart` operation restarts a subsystem.
- The :literal:`display` operation displays all currently active subsystems or currently active jobs in a subsystem. In some ways it has equivalent results of WRKSBS if subsystem is :literal:`\*ALL`\ , otherwise, it has equivalent results of WRKSBSJOB.
- Idempotency applies to relevant operations, e.g., a start operation on an already active subystem or an end operation on an inactive subsystem performs no action and returns success.





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


     
controlled_end_delay_time
  Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation. If this amount of time is exceeded and the end operation is not complete, any jobs still being processed in the subsystem are ended immediately. If the value is greater than 99999, :literal:`\*NOLIMIT` will be used in ENDSBS command DELAY parameter.

  This option is only applicable to the end and restart operations.


  | **required**: false
  | **type**: int
  | **default**: 100000


     
end_subsystem_option
  Specifies the options to take when ending the active subsystems.

  This option is only applicable to the end and restart operations.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['\*DFT']
  | **choices**: \*DFT, \*NOJOBLOG, \*CHGPTY, \*CHGTSL


     
how_to_end
  Specifies whether jobs in the subsystem are ended in a controlled manner or immediately.

  This option is only applicable to the end and restart operations.


  | **required**: false
  | **type**: str
  | **default**: \*CNTRLD
  | **choices**: \*IMMED, \*CNTRLD


     
joblog
  If set to :literal:`true`\ , output the available job log even when the rc is 0 (success).


  | **required**: false
  | **type**: bool


     
library
  Specify the library where the subsystem description is located.

  This option is only applicable to the start and restart operations.


  | **required**: false
  | **type**: str
  | **default**: \*LIBL


     
operation
  The subsystem management operations include

  Start a subsystem.

  End a subsystem.

  Restart a subsystem.

  Display a subsystem.


  | **required**: True
  | **type**: str
  | **choices**: start, end, restart, display


     
parameters
  The parameters that ENDSBS command will take. Other than the options above, all other parameters need to be specified here. The default values of parameters for ENDSBS will be taken if not specified.

  This option is only applicable to the end and restart operations.


  | **required**: false
  | **type**: str


     
subsystem
  The name of the subsystem description.

  May use '\*ALL' for the display operation.


  | **required**: True
  | **type**: str


     
user
  Specifies the name of the user whose jobs are displayed, :literal:`\*ALL` for all users. If subsystem is :literal:`\*ALL`\ , this option is ignored.

  This option is only applicable to the display operation.


  | **required**: false
  | **type**: str
  | **default**: \*ALL




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Start the subsystem QBATCH.
     ibm.power_ibmi.ibmi_subsystem:
       operation: start
       subsystem: QBATCH

   - name: Start a user defined subsystem, which the subsystem description is MYSBS, located at library MYLIB.
     ibm.power_ibmi.ibmi_subsystem:
       operation: start
       subsystem: MYSBS
       library: MYLIB
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: End the subsystem QBATCH with another user.
     ibm.power_ibmi.ibmi_subsystem:
       operation: end
       subsystem: QBATCH
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: End the QBATCH subsystem with options.
     ibm.power_ibmi.ibmi_subsystem:
       operation: end
       subsystem: QBATCH
       how_to_end: '*IMMED'

   - name: Restart the subsystem QBATCH.
     ibm.power_ibmi.ibmi_subsystem:
       operation: restart
       subsystem: QBATCH

   - name: Display all the active subsystems in this system.
     ibm.power_ibmi.ibmi_subsystem:
       operation: display
       subsystem: '*ALL'

   - name: Display all the active jobs of subsystem QINTER.
     ibm.power_ibmi.ibmi_subsystem:
       operation: display
       subsystem: QINTER

   - name: Display With One User's Job of subsystem QBATCH.
     ibm.power_ibmi.ibmi_subsystem:
       operation: display
       subsystem: QBATCH
       user: 'JONES'




Notes
-----

.. note::
   This end or restart operation is NOT ALLOWED to end ALL subsystems (\*ALL); use the :literal:`ibmi\_cl\_command` module for this instead.

   This module is non-blocking for the start and end operations, so the subsystem may still be in transition after module completion, and the :literal:`ibmi\_display\_subsystem` module should be used to check the subsystem status.

   Note that the restart operation blocks to wait for the subsystem to end, while it is non-blocking for resuming/starting the subsystem. The controlled\_end\_delay\_time parameter should be used with restart to limit the wait time for subsystem end.

   Due to the non-atomic and asynchronous nature of various operations that change the subsystem state, an error may occur with this type of operation if the subsystem is currently in a transition state from active to inactive or vice-versa.



See Also
--------

.. seealso::

   - :ref:`ibmi_cl_command_module`


  

Return Values
-------------


   
                              
       stdout
        | The standard output of the subsystem command.
      
        | **returned**: always except for a display operation that has a zero rc (success).
        | **type**: str
        | **sample**: CPF0943: Ending of subsystem QBATCH in progress.

            
      
      
                              
       stderr
        | The standard error the subsystem command.
      
        | **returned**: always except for a display operation that has a zero rc (success).
        | **type**: str
        | **sample**: CPF1054: No subsystem MYJOB active.

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: always except for a display operation that has a zero rc (success).
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF0943: Ending of subsystem QBATCH in progress."]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: always except for a display operation that has a zero rc (success).
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF1054: No subsystem MYJOB active."]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       subsystems
        | The list of the currently active subsystems.
      
        | **returned**: Only for a display operation when the rc is zero (success) and all subsystems, C(*ALL), are specified.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["                                      Work with Subsystems                                       5/25/20 19:55:04        Page 0001", "                          Subsystem        Active                          Total         -----------Subsystem Pools-----------------", "      Subsystem             Number          Jobs        Status          Storage (M)       1   2   3   4   5   6   7   8   9  10", "      QBATCH                018647              0       ACTIVE                     .00    2", "      QCMN                  018651              7       ACTIVE                     .00    2", "      QCTL                  018621              1       ACTIVE                     .00    2", "      QHTTPSVR              018742              8       ACTIVE                     .00    2", "      QINTER                018642              0       ACTIVE                     .00    2   3", "      QSERVER               018631             16       ACTIVE                     .00    2", "      QSPL                  018652              0       ACTIVE                     .00    2   4", "      QSYSWRK               018622            111       ACTIVE                     .00    2", "      QUSRWRK               018633             27       ACTIVE                     .00    2", "                          * * * * *  E N D  O F  L I S T I N G  * * * * *"]
            
      
      
                              
       active_jobs
        | The result set
      
        | **returned**: Only for a display operation when the rc is zero (success) and subsystem is not C(*ALL).
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"AUTHORIZATION_NAME": "QPGMR", "CPU_TIME": "17", "ELAPSED_ASYNC_DISK_IO_COUNT": "0", "ELAPSED_CPU_PERCENTAGE": "0.0", "ELAPSED_CPU_TIME": "0", "ELAPSED_INTERACTION_COUNT": "0", "ELAPSED_PAGE_FAULT_COUNT": "0", "ELAPSED_SYNC_DISK_IO_COUNT": "0", "ELAPSED_TIME": "0.000", "ELAPSED_TOTAL_DISK_IO_COUNT": "0", "ELAPSED_TOTAL_RESPONSE_TIME": "0", "FUNCTION": "QEZSCNEP", "FUNCTION_TYPE": "PGM", "INTERNAL_JOB_ID": "002700010041F300A432B3A44FFD7001", "JOB_END_REASON": "", "JOB_NAME": "022042/QPGMR/QSYSSCD", "JOB_STATUS": "EVTW", "JOB_TYPE": "BCH", "MEMORY_POOL": "BASE", "ORDINAL_POSITION": "2", "RUN_PRIORITY": "10", "SERVER_TYPE": "", "SUBSYSTEM": "QCTL", "SUBSYSTEM_LIBRARY_NAME": "QSYS", "TEMPORARY_STORAGE": "6", "THREAD_COUNT": "1", "TOTAL_DISK_IO_COUNT": "587"}]
            
      
        
