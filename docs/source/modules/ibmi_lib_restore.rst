..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_lib_restore.py

.. _ibmi_lib_restore_module:

ibmi_lib_restore -- Restore one library on a remote IBMi node
=============================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ibmi_lib_restore module restore an save file on a remote IBMi nodes
- The restored library and save file are on the remote host.
- Only support *SAVF as the save file's format by now.



Parameters
----------


     
asp_group
  Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

  The ASP group name is the name of the primary ASP device within the ASP group.


  | **required**: false
  | **type**: str
  | **default**: *SYSBAS


     
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


     
parameters
  The parameters that RSTLIB command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for RSTLIB will be taken if not specified.


  | **required**: false
  | **type**: str
  | **default**:  


     
saved_lib
  The library need to be restored.


  | **required**: True
  | **type**: str


     
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

   
   - name: Restore savedlib libary from archive.savf in archlib libary
     ibmi_lib_restore:
       saved_lib: 'savedlib'
       savefile_name: 'archive'
       savefile_lib: 'archlib'



Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Return Values
-------------


   
                              
       saved_lib
        | The library need to be restored.
      
        | **returned**: always
        | **type**: str
        | **sample**: savedlib

            
      
      
                              
       savefile_name
        | The save file name.
      
        | **returned**: always
        | **type**: str
        | **sample**: c1

            
      
      
                              
       end
        | The restore execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'User Profile = TESTER', 'FROM_MODULE': 'QSQSRVR', 'FROM_PROGRAM': 'QSQSRVR', 'MESSAGE_TIMESTAMP': '2020-05-25-12.59.59.966873', 'FROM_USER': 'TESTER', 'TO_INSTRUCTION': '8873', 'MESSAGE_SECOND_LEVEL_TEXT': '', 'MESSAGE_TYPE': 'COMPLETION', 'MESSAGE_ID': '', 'MESSAGE_LIBRARY': '', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '0', 'FROM_PROCEDURE': 'QSQSRVR', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '8873', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '8', 'MESSAGE_FILE': '', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       stdout
        | The restore standard output
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC3703: 2 objects restored from test to test.

            
      
      
                              
       format
        | The save file's format. Only support *SAVF by now.
      
        | **returned**: always
        | **type**: str
        | **sample**: *SAVF

            
      
      
                              
       stderr_lines
        | The restore standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF3806: Objects from save file archive in archlib not restored.", "CPF3780: Specified file for library test not found."]
            
      
      
                              
       start
        | The restore execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       delta
        | The restore execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       command
        | The last excuted command.
      
        | **returned**: always
        | **type**: str
        | **sample**: RSTLIB SAVLIB(TESTLIB) DEV(*SAVF) SAVF(TEST/ARCHLIB) 

            
      
      
                              
       savefile_lib
        | The save file library.
      
        | **returned**: always
        | **type**: str
        | **sample**: c1lib

            
      
      
                              
       stderr
        | The restore standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF3806: Objects from save file archive in archlib not restored.\n

            
      
      
                              
       rc
        | The restore action return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The restore standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC3703: 2 objects restored from test to test."]
            
      
        
