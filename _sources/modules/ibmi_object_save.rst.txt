
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_object_save.py

.. _ibmi_object_save_module:


ibmi_object_save -- Save one or more objects
============================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_object_save`` module create an save file on a remote IBM i nodes.
- The saved objects and save file are on the remote host, and the save file is not copied to the local host.
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


     
force_save
  If save file already exists or contains data, whether to clear data or not.


  | **required**: false
  | **type**: bool


     
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
  The library contains the objects.


  | **required**: True
  | **type**: str


     
object_names
  The objects need to be saved. One or more object names can be specified. Use space as separator.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
object_types
  The object types. One or more object types can be specified. Use space as separator.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
parameters
  The parameters that SAVOBJ command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for SAVOBJ will be taken if not specified.


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


     
target_release
  The release of the operating system on which you intend to restore and use the object.


  | **required**: false
  | **type**: str
  | **default**: \*CURRENT




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Force to save test1.pgm and test2.srvpgm in objlib libary to archive.savf in archlib libary with become user.
     ibmi_object_save:
       object_names: 'test1 test2'
       object_lib: 'objlib'
       object_types: '*PGM *SRVPGM'
       savefile_name: 'archive'
       savefile_lib: 'archlib'
       force_save: True
       target_release: 'V7R2M0'
       become_user: 'USER1'
       become_user_password: 'yourpassword'









Return Values
-------------


   
                              
       start
        | The save execution start time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The save execution end time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The save execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The save standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC3722: 2 objects saved from library objlib.

            
      
      
                              
       stderr
        | The save standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n

            
      
      
                              
       object_names
        | The objects need to be saved.
      
        | **returned**: always
        | **type**: str
        | **sample**: test1 test2

            
      
      
                              
       object_lib
        | The library contains the object.
      
        | **returned**: always
        | **type**: str
        | **sample**: objlib

            
      
      
                              
       object_types
        | The object types.
      
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

            
      
      
                              
       force_save
        | If save file already exists or contains data, whether to clear data or not.
      
        | **returned**: always
        | **type**: bool      
        | **sample**:

              .. code-block::

                       true
            
      
      
                              
       target_release
        | The release of the operating system on which you intend to restore and use the object.
      
        | **returned**: always
        | **type**: str
        | **sample**: V7R1M0

            
      
      
                              
       command
        | The last excuted command.
      
        | **returned**: always
        | **type**: str
        | **sample**: SAVOBJ OBJ(\*ALL) LIB(TESTLIB) DEV(\*SAVF) OBJTYPE(\*ALL) SAVF(TEST/ARCHLIB) TGTRLS(V7R1M0)

            
      
      
                              
       joblog
        | Append JOBLOG to stderr/stderr_lines or not.
      
        | **returned**: always
        | **type**: bool
      
      
                              
       rc
        | The save action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The save standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC3722: 2 objects saved from library objlib."]
            
      
      
                              
       stderr_lines
        | The save standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF5813: File archive in library archlib already exists.", "CPF7302: File archive not created in library archlib."]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "149", "FROM_LIBRARY": "QSHELL", "FROM_MODULE": "QZSHRUNC", "FROM_PROCEDURE": "main", "FROM_PROGRAM": "QZSHRUNC", "FROM_USER": "TESTER", "MESSAGE_FILE": "QZSHMSGF", "MESSAGE_ID": "QSH0005", "MESSAGE_LIBRARY": "QSHELL", "MESSAGE_SECOND_LEVEL_TEXT": "", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Command ended normally with exit status 0.", "MESSAGE_TIMESTAMP": "2020-05-25-13.06.35.019371", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": "12", "SEVERITY": "0", "TO_INSTRUCTION": "5829", "TO_LIBRARY": "QXMLSERV", "TO_MODULE": "PLUGILE", "TO_PROCEDURE": "ILECMDEXC", "TO_PROGRAM": "XMLSTOREDP"}]
            
      
        
