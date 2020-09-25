
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_cl_command.py

.. _ibmi_cl_command_module:


ibmi_cl_command -- Executes a CL(Control language) command
==========================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_cl_command`` module takes the CL command followed by a list of space-delimited arguments.
- For PASE(Portable Application Solutions Environment for i) or QSHELL(Unix/Linux-liked) commands, like 'ls', 'chmod', use the ``command`` module instead.





Parameters
----------


     
asp_group
  Specifies the name of the ASP(Auxiliary Storage Pool) group to set for the current thread.

  The ASP group name is the name of the primary ASP device within the ASP group.

  Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL, DSPHDWRSC.


  | **required**: false
  | **type**: str
  | **default**: \*SYSBAS


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
cmd
  The CL command to run.


  | **required**: True
  | **type**: str


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).

  Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL, DSPHDWRSC.


  | **required**: false
  | **type**: bool




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Create a library by using CL command CRTLIB
     ibmi_cl_command:
       cmd: 'CRTLIB LIB(TESTLIB)'
       become_user: 'USER1'
       become_user_password: 'yourpassword'




Notes
-----

.. note::
   CL command with OUTPUT parameter like DSPLIBL, DSPHDWRSC does not have job log and does not support become user.

   CL command can also be run by ``command`` module with simple stdout/stderr, put 'system' as the as first args in ``command`` module.

   The ``ibmi_cl_command`` module can only run one CL command at a time.



See Also
--------

.. seealso::

   - :ref:`command_module`



Return Values
-------------


   
                              
       joblog
        | Print job log or not when using itoolkit to run the CL command.
      
        | **returned**: always
        | **type**: bool
      
      
                              
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
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       cmd
        | The CL command executed.
      
        | **returned**: always
        | **type**: str
        | **sample**: CRTLIB LIB(TESTLIB)

            
      
      
                              
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

                       ["CPC2102: Library TESTLIB created."]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
