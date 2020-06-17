..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_lib_save.py

.. _ibmi_lib_save_module:

ibmi_lib_save -- Save one libary on a remote IBMi node
======================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ibmi_lib_save module create an save file on a remote IBMi nodes
- The save file *is not* copied to the local host.
- Only support *SAVF as the save file's format by now.



Parameters
----------


     
asp_group
  Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

  The ASP group name is the name of the primary ASP device within the ASP group.


  | **required**: false
  | **type**: str
  | **default**: *SYSBAS


     
force_save
  If save file already exists or contains data, whether to clear data or not.


  | **required**: false
  | **type**: bool


     
format
  The save file's format. Only support *SAVF by now.


  | **required**: false
  | **type**: str
  | **default**: *SAVF
  | **choices**: *SAVF


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


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
  The release of the operating system on which you intend to restore and use the SAVF.


  | **required**: false
  | **type**: str
  | **default**: *CURRENT



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Force to save test libary to archive.savf in archlib libary
     ibmi_lib_save:
       lib_name: 'test'
       savefile_name: 'archive'
       savefile_lib: 'archlib'
       force_save: true
       target_release: 'V7R2M0'



Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Return Values
-------------


   
                              
       stderr_lines
        | The save standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF5813: File archive in library archlib already exists.", "CPF7302: File archive not created in library archlib."]
            
      
      
                              
       stdout
        | The save standard output
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC3722: 2 objects saved from library test.

            
      
      
                              
       savefile_lib
        | The save file library.
      
        | **returned**: always
        | **type**: str
        | **sample**: archlib

            
      
      
                              
       delta
        | The save execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout_lines
        | The save standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC3722: 2 objects saved from library test."]
            
      
      
                              
       savefile_name
        | The save file name.
      
        | **returned**: always
        | **type**: str
        | **sample**: archive

            
      
      
                              
       end
        | The save execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'User Profile = TESTER', 'FROM_MODULE': 'QSQSRVR', 'FROM_PROGRAM': 'QSQSRVR', 'MESSAGE_TIMESTAMP': '2020-05-25-12.54.26.489891', 'FROM_USER': 'TESTER', 'TO_INSTRUCTION': '8873', 'MESSAGE_SECOND_LEVEL_TEXT': '', 'MESSAGE_TYPE': 'COMPLETION', 'MESSAGE_ID': '', 'MESSAGE_LIBRARY': '', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '0', 'FROM_PROCEDURE': 'QSQSRVR', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '8873', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '8', 'MESSAGE_FILE': '', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       start
        | The save execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       format
        | The save file's format. Only support *SAVF by now.
      
        | **returned**: always
        | **type**: str
        | **sample**: *SAVF

            
      
      
                              
       target_release
        | The release of the operating system on which you intend to restore and use the library.
      
        | **returned**: always
        | **type**: str
        | **sample**: V7R2M0

            
      
      
                              
       force_save
        | If save file already exists or contains data, whether to clear data or not.
      
        | **returned**: always
        | **type**: bool      
        | **sample**:

              .. code-block::

                       true
            
      
      
                              
       command
        | The last excuted command.
      
        | **returned**: always
        | **type**: str
        | **sample**: SAVLIB LIB(TEST) DEV(*SAVF) SAVF(TEST/ARCHLIB) TGTRLS(V7R2M0)

            
      
      
                              
       stderr
        | The save standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n

            
      
      
                              
       rc
        | The save action return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       lib_name
        | The library need to be saved.
      
        | **returned**: always
        | **type**: str
        | **sample**: test

            
      
        
