
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_lib_save.py

.. _ibmi_lib_save_module:


ibmi_lib_save -- Save one libary
================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_lib_save`` module create an save file on a remote IBM i nodes.
- The save file is not copied to the local host.
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


     
lib_name
  The library need to be saved.


  | **required**: True
  | **type**: str


     
parameters
  The parameters that SAVLIB command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for SAVLIB will be taken if not specified.


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
  The release of the operating system on which you intend to restore and use the save file.


  | **required**: false
  | **type**: str
  | **default**: \*CURRENT




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Force to save test libary to archive.savf in archlib libary with become user.
     ibmi_lib_save:
       lib_name: 'test'
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
        | **sample**: CPC3722: 2 objects saved from library test.

            
      
      
                              
       stderr
        | The save standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n

            
      
      
                              
       lib_name
        | The library need to be saved.
      
        | **returned**: always
        | **type**: str
        | **sample**: test

            
      
      
                              
       savefile_name
        | The save file name.
      
        | **returned**: always
        | **type**: str
        | **sample**: archive

            
      
      
                              
       savefile_lib
        | The save file library.
      
        | **returned**: always
        | **type**: str
        | **sample**: archlib

            
      
      
                              
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
        | The release of the operating system on which you intend to restore and use the library.
      
        | **returned**: always
        | **type**: str
        | **sample**: V7R2M0

            
      
      
                              
       command
        | The last excuted command.
      
        | **returned**: always
        | **type**: str
        | **sample**: SAVLIB LIB(TEST) DEV(\*SAVF) SAVF(TEST/ARCHLIB) TGTRLS(V7R2M0)

            
      
      
                              
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

                       ["CPC3722: 2 objects saved from library test."]
            
      
      
                              
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

                       [{"FROM_INSTRUCTION": "8873", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "QSQSRVR", "FROM_PROCEDURE": "QSQSRVR", "FROM_PROGRAM": "QSQSRVR", "FROM_USER": "TESTER", "MESSAGE_FILE": "", "MESSAGE_ID": "", "MESSAGE_LIBRARY": "", "MESSAGE_SECOND_LEVEL_TEXT": "", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "User Profile = TESTER", "MESSAGE_TIMESTAMP": "2020-05-25-12.54.26.489891", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": "8", "SEVERITY": "0", "TO_INSTRUCTION": "8873", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
