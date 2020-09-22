
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_object_restore.py

.. _ibmi_object_restore_module:


ibmi_object_restore -- Restore one or more objects
==================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_object_restore`` module restore an save file on a remote IBM i nodes
- The restored objects and save file are on the remote host.
- Only support ``*SAVF`` as the save file's format by now.





Parameters
----------


     
asp_group
  Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

  The ASP group name is the name of the primary ASP device within the ASP group.


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


     
format
  The save file's format. Only support ``*SAVF`` by now.


  | **required**: false
  | **type**: str
  | **default**: \*SAVF
  | **choices**: \*SAVF


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
object_lib
  The library that contains the saved objects.


  | **required**: True
  | **type**: str


     
object_names
  The objects need to be restored.

  One or more object names can be specified. Use space as separator.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
object_types
  The object types.

  One or more object types can be specified. Use space as separator.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
parameters
  The parameters that RSTOBJ command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for RSTOBJ will be taken if not specified.


  | **required**: false
  | **type**: str
  | **default**:  


     
savefile_lib
  The save file library.


  | **required**: True
  | **type**: str


     
savefile_name
  The save file name.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Restore test1.pgm test2.srvpgm in savedlib libary from archive.savf in archlib libary with become user.
     ibmi_object_restore:
       object_names: 'test1 test2'
       object_lib: 'savedlib'
       object_types: '*PGM *SRVPGM'
       savefile_name: 'archive'
       savefile_lib: 'archlib'
       become_user: 'USER1'
       become_user_password: 'yourpassword'









Return Values
-------------


   
                              
       start
        | The restore execution start time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The restore execution end time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The restore execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The restore standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC3703: 2 objects restored from C1 to C1.

            
      
      
                              
       stderr
        | The restore standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF9812: File file1 in library C1 not found..\

            
      
      
                              
       object_names
        | The objects need to be restored.
      
        | **returned**: always
        | **type**: str
        | **sample**: test1 test2

            
      
      
                              
       object_lib
        | The library that contains the saved objects.
      
        | **returned**: always
        | **type**: str
        | **sample**: objectlib

            
      
      
                              
       object_types
        | The objects types.
      
        | **returned**: always
        | **type**: str
        | **sample**: \*PGM \*SRVPGM

            
      
      
                              
       savefile_name
        | The save file name.
      
        | **returned**: always
        | **type**: str
        | **sample**: c1

            
      
      
                              
       savefile_lib
        | The save file library.
      
        | **returned**: always
        | **type**: str
        | **sample**: c1lib

            
      
      
                              
       format
        | The save file's format. Only support ``*SAVF`` by now.
      
        | **returned**: always
        | **type**: str
        | **sample**: \*SAVF

            
      
      
                              
       command
        | The last excuted command.
      
        | **returned**: always
        | **type**: str
        | **sample**: RSTOBJ OBJ(OBJA) SAVLIB(TESTLIB) DEV(\*SAVF) OBJTYPE(\*ALL) SAVF(TEST/ARCHLIB)

            
      
      
                              
       joblog
        | Append JOBLOG to stderr/stderr_lines or not.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       rc
        | The restore action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The restore standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC3703: 2 objects restored from C1 to C1."]
            
      
      
                              
       stderr_lines
        | The restore standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF9812: File file1 in library C1 not found."]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "8873", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "QSQSRVR", "FROM_PROCEDURE": "QSQSRVR", "FROM_PROGRAM": "QSQSRVR", "FROM_USER": "TESTER", "MESSAGE_FILE": "", "MESSAGE_ID": "", "MESSAGE_LIBRARY": "", "MESSAGE_SECOND_LEVEL_TEXT": "", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "User Profile = TESTER", "MESSAGE_TIMESTAMP": "2020-05-25-13.09.36.988652", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": "8", "SEVERITY": "0", "TO_INSTRUCTION": "8873", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
