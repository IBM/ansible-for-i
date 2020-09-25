
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_at.py

.. _ibmi_at_module:


ibmi_at -- Schedule a batch job
===============================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_at`` module schedule a batch job.





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


     
cmd
  Specifies the command that runs in the submitted job.


  | **required**: True
  | **type**: str


     
frequency
  Specifies how often the job is submitted.


  | **required**: True
  | **type**: str
  | **choices**: \*ONCE, \*WEEKLY, \*MONTHLY


     
job_name
  Specifies the name of the job schedule entry.


  | **required**: True
  | **type**: str


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
parameters
  The parameters that ADDJOBSCDE command will take. Other than options above, all other parameters need to be specified here.

  The default values of parameters for ADDJOBSCDE will be taken if not specified.


  | **required**: false
  | **type**: str


     
scddate
  Specifies the date on which the job is submitted.


  | **required**: false
  | **type**: str
  | **default**: \*CURRENT


     
scdday
  Specifies the day of the week on which the job is submitted.

  The valid value are ``*NONE``, ``*ALL``, ``*MON``, ``*TUE``, ``*WED``, ``*THU``, ``*FRI``, ``*SAT``, ``*SUN``.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: \*NONE


     
schtime
  Specifies the time on the scheduled date at which the job is submitted.


  | **required**: false
  | **type**: str
  | **default**: \*CURRENT


     
text
  Specifies text that briefly describes the job schedule entry.


  | **required**: false
  | **type**: str
  | **default**: \*BLANK




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Add a job schedule entry test with become user.
     ibmi_at:
       job_name: 'test'
       cmd: 'QSYS/WRKSRVAGT TYPE(*UAK)'
       frequency: '*WEEKLY'
       scddate: '*CURRENT'
       text: 'Test job schedule'
       become_user: 'USER1'
       become_user_password: 'yourpassword'









Return Values
-------------


   
                              
       command
        | The execution command.
      
        | **returned**: always
        | **type**: str
        | **sample**: QSYS/ADDJOBSCDE JOB(RUNCOM) CMD(QBLDSYSR/CHGSYSSEC OPTION(\*CHGPW)) FRQ(\*WEEKLY) SCDDATE(\*CURRENT) SCDDAY(\*NONE) SCDTIME(\*CURRENT) TEXT(\*BLANK) 

            
      
      
                              
       msg
        | The execution message.
      
        | **returned**: always
        | **type**: str
        | **sample**: Either scddate or scdday need to be \*NONE.

            
      
      
                              
       delta
        | The execution delta time.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPC1238: Job schedule entry TEST number 000074 added.

            
      
      
                              
       stderr
        | The standard error.
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n

            
      
      
                              
       rc
        | The action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC1238: Job schedule entry TEST number 000074 added."]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
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

                       [{"FROM_INSTRUCTION": "8873", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "QSQSRVR", "FROM_PROCEDURE": "QSQSRVR", "FROM_PROGRAM": "QSQSRVR", "FROM_USER": "TESTER", "MESSAGE_FILE": "", "MESSAGE_ID": "", "MESSAGE_LIBRARY": "", "MESSAGE_SECOND_LEVEL_TEXT": "", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "User Profile = TESTER", "MESSAGE_TIMESTAMP": "2020-05-25-12.40.00.690270", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": "8", "SEVERITY": "0", "TO_INSTRUCTION": "8873", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
