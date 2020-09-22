
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_end_subsystem.py

.. _ibmi_end_subsystem_module:


ibmi_end_subsystem -- End an active subsystem.
==============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_end_subsystem`` module ends an active subsystem.





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


     
controlled_end_delay_time
  Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation. If this amount of time is exceeded and the end operation is not complete, any jobs still being processed in the subsystem are ended immediately. If the value is greater than 99999, ``*NOLIMIT`` will be used in ENDSBS command DELAY parameter.


  | **required**: false
  | **type**: int
  | **default**: 100000


     
end_subsystem_option
  Specifies the options to take when ending the active subsystems.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['\*DFT']
  | **choices**: \*DFT, \*NOJOBLOG, \*CHGPTY, \*CHGTSL


     
how_to_end
  Specifies whether jobs in the subsystem are ended in a controlled manner or immediately.


  | **required**: false
  | **type**: str
  | **default**: \*CNTRLD
  | **choices**: \*IMMED, \*CNTRLD


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
parameters
  The parameters that ENDSBS command will take. Other than the options above, all other parameters need to be specified here. The default values of parameters for ENDSBS will be taken if not specified.


  | **required**: false
  | **type**: str


     
subsystem
  The name of the subsystem description.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: End the subsystem QBATCH with another user.
     ibmi_end_subsystem:
       subsystem: QBATCH
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: End a subsystem with options.
     ibmi_end_subsystem:
       subsystem: QBATCH
       how_to_end: '*IMMED'




Notes
-----

.. note::
   This module is NOT ALLOWED to end ALL subsystems, use the ``ibmi_cl_command`` module instead.

   This module is non-blocking, the ending subsystem may still be in progress, use ``ibmi_display_subsystem`` module to check the status.



See Also
--------

.. seealso::

   - :ref:`ibmi_display_subsystem, ibmi_start_subsystem_module`



Return Values
-------------


   
                              
       stdout
        | The standard output of the end subsystem command.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF0943: Ending of subsystem QBATCH in progress.

            
      
      
                              
       stderr
        | The standard error the end subsystem command.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF1054: No subsystem MYJOB active.

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF0943: Ending of subsystem QBATCH in progress."]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: always
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
            
      
        
