
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_iasp.py

.. _ibmi_iasp_module:


ibmi_iasp -- Control IASP
=========================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Control IASP.
- For IBM i V7R2, PTF SI72162 is required.
- For IBM i V7R3, PTF SI72161 is required.
- For non-IBM i targets, no need.





Parameters
----------


     
asp_type
  The asp_type of new create iasp.


  | **required**: false
  | **type**: str
  | **default**: \*PRIMARY
  | **choices**: \*PRIMARY, \*SECONDARY, \*UDFS


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
disks
  The list of the unconfigure disks.


  | **required**: false
  | **type**: list
  | **elements**: str


     
extra_parameters
  Extra parameter is appended at the end of create operation.


  | **required**: false
  | **type**: str
  | **default**:  


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool


     
name
  The name of the iasp.


  | **required**: True
  | **type**: str


     
operation
  ``create``/``delete``/``add_disks`` are idempotent actions that will not run commands unless necessary.

  ``view`` will return the iasp state

  **At least one of operation are required.**


  | **required**: True
  | **type**: str
  | **choices**: create, add_disks, delete, display


     
primary_asp
  The primary_asp of new create iasp.


  | **required**: false
  | **type**: str


     
synchronous
  Synchronous execute the iasp command.


  | **required**: false
  | **type**: bool
  | **default**: True




Examples
--------

.. code-block:: yaml+jinja

   
   - name: create an IASP
     ibmi_iasp:
       name: 'IASP1'
       operation: 'create'
       disks: ['DMP002', 'DMP019']
       become_user: 'USER1'
       become_user_password: 'yourpassword'









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
        | **sample**: CPCB719: Configure Device ASP \*DELETE request completed.

            
      
      
                              
       stderr
        | The command standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: Generic failure

            
      
      
                              
       cmd
        | The command executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: CFGDEVASP ASPDEV(YFTEST) ACTION(\*DELETE) CONFIRM(\*NO)

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       asp_info
        | The asp_info of the identify iasp.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ASP_NUMBER": "144", "ASP_STATE": "VARIED OFF", "ASP_TYPE": "PRIMARY", "BALANCE_DATA_MOVED": "0", "BALANCE_DATA_REMAINING": "0", "BALANCE_STATUS": "", "BALANCE_TIMESTAMP": "", "BALANCE_TYPE": "", "CHANGES_WRITTEN_TO_DISK": "YES", "COMPRESSED_DISK_UNITS": "NONE", "COMPRESSION_RECOVERY_POLICY": "OVERFLOW IMMEDIATE", "DEVICE_DESCRIPTION_NAME": "", "DISK_UNITS_PRESENT": "ALL", "END_IMMEDIATE": "", "ERROR_LOG_SPACE": "0", "MACHINE_LOG_SPACE": "0", "MACHINE_TRACE_SPACE": "0", "MAIN_STORAGE_DUMP_SPACE": "0", "MICROCODE_SPACE": "0", "MULTIPLE_CONNECTION_DISK_UNITS": "YES", "NUMBER_OF_DISK_UNITS": "1", "OVERFLOW_RECOVERY_RESULT": "", "OVERFLOW_STORAGE": "0", "PRIMARY_ASP_RESOURCE_NAME": "", "PROTECTED_CAPACITY": "0", "PROTECTED_CAPACITY_AVAILABLE": "0", "RDB_NAME": "IASP1", "RESOURCE_NAME": "IASP1", "STORAGE_THRESHOLD_PERCENTAGE": "90", "SYSTEM_STORAGE": "2", "TOTAL_CAPACITY": "0", "TOTAL_CAPACITY_AVAILABLE": "0", "TRACE_DURATION": "0", "TRACE_STATUS": "", "TRACE_TIMESTAMP": "", "UNPROTECTED_CAPACITY": "0", "UNPROTECTED_CAPACITY_AVAILABLE": "0"}]
            
      
      
                              
       stdout_lines
        | The command standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPCB719: Configure Device ASP *DELETE request completed."]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Generic failure"]
            
      
        
