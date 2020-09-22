
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_start_subsystem.py

.. _ibmi_start_subsystem_module:


ibmi_start_subsystem -- Start an inactive subsystem
===================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- the ``ibmi_start_subsystem`` module start an inactive subsystem.





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


     
library
  Specify the library where the subsystem description is located.


  | **required**: false
  | **type**: str
  | **default**: \*LIBL


     
subsystem
  The name of the subsystem description.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Start the subsystem QBATCH.
     ibmi_start_subsystem:
       subsystem: QBATCH

   - name: Start a user defined subsystem, which the subsystem description is MYSBS, located at library MYLIB.
     ibmi_start_subsystem:
       subsystem: MYSBS
       library: MYLIB
       become_user: 'USER1'
       become_user_password: 'yourpassword'






See Also
--------

.. seealso::

   - :ref:`ibmi_end_subsystem_module`



Return Values
-------------


   
                              
       stdout
        | The standard output of the start subsystem command.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF0902: Subsystem QBATCH in library QSYS being started.

            
      
      
                              
       stderr
        | The standard error the start subsystem command.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF1010: Subsystem name QBATCH active.

            
      
      
                              
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

                       ["CPF0902: Subsystem QINTER in library QSYS being started."]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF1080: Library MYLIB not found."]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
