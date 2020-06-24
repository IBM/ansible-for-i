..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_at.py

.. _ibmi_at_module:

ibmi_at -- Schedule a batch job on a remote IBMi node
=====================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ibmi_at module schedule a batch job on a remote IBMi node



Parameters
----------


     
cmd
  Specifies the command that runs in the submitted job.


  | **required**: True
  | **type**: str


     
frequency
  Specifies how often the job is submitted.


  | **required**: True
  | **type**: str
  | **choices**: *ONCE, *WEEKLY, *MONTHLY


     
job_name
  Specifies the name of the job schedule entry.


  | **required**: True
  | **type**: str


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool


     
parameters
  The parameters that ADDJOBSCDE command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for ADDJOBSCDE will be taken if not specified.


  | **required**: false
  | **type**: str


     
scddate
  Specifies the date on which the job is submitted.


  | **required**: false
  | **type**: str
  | **default**: *CURRENT


     
scdday
  Specifies the day of the week on which the job is submitted.

  The valid value are '*NONE', '*ALL', '*MON', '*TUE', '*WED', '*THU', '*FRI', '*SAT', '*SUN'.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: *NONE


     
schtime
  Specifies the time on the scheduled date at which the job is submitted.


  | **required**: false
  | **type**: str
  | **default**: *CURRENT


     
text
  Specifies text that briefly describes the job schedule entry.


  | **required**: false
  | **type**: str
  | **default**: *BLANK



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Add a job schedule entry test
     ibmi_at:
       job_name: 'test'
       cmd: 'QSYS/WRKSRVAGT TYPE(*UAK)'
       frequency: '*WEEKLY'
       scddate: '*CURRENT'
       text: 'Test job schedule'



Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Return Values
-------------


   
                              
       stderr_lines
        | The standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF5813: File archive in library archlib already exists.", "CPF7302: File archive not created in library archlib."]
            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'User Profile = TESTER', 'FROM_MODULE': 'QSQSRVR', 'FROM_PROGRAM': 'QSQSRVR', 'MESSAGE_TIMESTAMP': '2020-05-25-12.40.00.690270', 'FROM_USER': 'TESTER', 'TO_INSTRUCTION': '8873', 'MESSAGE_SECOND_LEVEL_TEXT': '', 'MESSAGE_TYPE': 'COMPLETION', 'MESSAGE_ID': '', 'MESSAGE_LIBRARY': '', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '0', 'FROM_PROCEDURE': 'QSQSRVR', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '8873', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '8', 'MESSAGE_FILE': '', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       stdout
        | The standard output
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC1238: Job schedule entry TEST number 000074 added.

            
      
      
                              
       rc
        | The action return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       command
        | The execution command
      
        | **returned**: always
        | **type**: str
        | **sample**: QSYS/ADDJOBSCDE JOB(RUNCOM) CMD(QBLDSYSR/CHGSYSSEC OPTION(*CHGPW)) FRQ(*WEEKLY) SCDDATE(*CURRENT) SCDDAY(*NONE) SCDTIME(*CURRENT) TEXT(*BLANK) 

            
      
      
                              
       stderr
        | The standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n

            
      
      
                              
       delta
        | The execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       msg
        | The execution message.
      
        | **returned**: always
        | **type**: str
        | **sample**: Either scddate or scdday need to be *NONE.

            
      
      
                              
       stdout_lines
        | The standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC1238: Job schedule entry TEST number 000074 added."]
            
      
        
