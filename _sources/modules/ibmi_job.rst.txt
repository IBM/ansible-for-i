
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_job.py

.. _ibmi_job_module:


ibmi_job -- Returns job information according to inputs.
========================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_job`` module returns information associated with one or more jobs.





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
  The job log of the job executing the task will be returned even rc is zero if it is set to true.


  | **required**: false
  | **type**: bool


     
name
  The qualified job name.

  If this parameter is specified, the other parameters will be ignored.


  | **required**: False
  | **type**: str


     
status
  The job status filter.


  | **required**: false
  | **type**: str
  | **default**: \*ALL
  | **choices**: \*ALL, \*ACTIVE, \*JOBQ, \*OUTQ


     
submitter
  The type of submitted jobs to return.


  | **required**: false
  | **type**: str
  | **default**: \*ALL
  | **choices**: \*ALL, \*JOB, \*USER, \*WRKSTN


     
subsystem
  The job subsystem filter. A valid subsystem name can be specified. Valid values are ``*ALL`` or subsystem name.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
type
  The job type filter.


  | **required**: false
  | **type**: str
  | **default**: \*ALL
  | **choices**: \*ALL, \*BATCH, \*INTERACT


     
user
  The user profile name to use as the job user filtering criteria.

  Valid values are user profile name, ``*USER`` or ``*ALL``.


  | **required**: false
  | **type**: str
  | **default**: \*ALL




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Get status of a list of jobs
     ibmi_job:
       user: "WANGYUN"
       type: "*BATCH"

   - name: List job information
     ibmi_job:
       name: "556235/WANGYUN/TEST"




Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)



See Also
--------

.. seealso::

   - :ref:`ibmi_submit_job_module`



Return Values
-------------


   
                              
       start
        | The task execution start time
      
        | **returned**: When job has been submitted and task has waited for the job status for some time
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: When job has been submitted and task has waited for the job status for some time
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: When job has been submitted and task has waited for the job status for some time
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The task standard output
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The task standard error
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
      
                              
       stderr_lines
        | The task standard error split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       job_log
        | The job log of the job executes the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       job_info
        | The information of the job(s)
      
        | **returned**: When rc is zero
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"CCSID": "0", "COMPLETION_STATUS": "ABNORMAL", "JOB_ACCOUNTING_CODE": "*SYS", "JOB_ACTIVE_TIME": "", "JOB_DATE": "", "JOB_DESCRIPTION": "", "JOB_DESCRIPTION_LIBRARY": "", "JOB_END_REASON": "", "JOB_END_SEVERITY": "10", "JOB_END_TIME": "2020-02-14-00.36.35", "JOB_ENTERED_SYSTEM_TIME": "2020-02-14-00.36.35", "JOB_INFORMATION": "YES", "JOB_NAME": "514647/WANGYUN/QPRTJOB", "JOB_QUEUE_LIBRARY": "", "JOB_QUEUE_NAME": "", "JOB_QUEUE_PRIORITY": "0", "JOB_QUEUE_STATUS": "", "JOB_SCHEDULED_TIME": "", "JOB_STATUS": "OUTQ", "JOB_SUBSYSTEM": "", "JOB_TYPE": "BCH", "JOB_TYPE_ENHANCED": "ALTERNATE_SPOOL_USER", "SUBMITTER_JOB_NAME": "", "SUBMITTER_MESSAGE_QUEUE": "", "SUBMITTER_MESSAGE_QUEUE_LIBRARY": ""}, {"CCSID": "65535", "COMPLETION_STATUS": "ABNORMAL", "JOB_ACCOUNTING_CODE": "*SYS", "JOB_ACTIVE_TIME": "2020-03-23-22.07.18", "JOB_DATE": "", "JOB_DESCRIPTION": "QDFTJOBD", "JOB_DESCRIPTION_LIBRARY": "QGPL", "JOB_END_REASON": "JOB ENDED DUE TO A DEVICE ERROR", "JOB_END_SEVERITY": "30", "JOB_END_TIME": "2020-03-24-11.06.44", "JOB_ENTERED_SYSTEM_TIME": "2020-03-23-22.07.18", "JOB_INFORMATION": "YES", "JOB_NAME": "547343/WANGYUN/QPADEV0001", "JOB_QUEUE_LIBRARY": "", "JOB_QUEUE_NAME": "", "JOB_QUEUE_PRIORITY": "0", "JOB_QUEUE_STATUS": "", "JOB_SCHEDULED_TIME": "", "JOB_STATUS": "OUTQ", "JOB_SUBSYSTEM": "", "JOB_TYPE": "INT", "JOB_TYPE_ENHANCED": "INTERACTIVE_GROUP", "SUBMITTER_JOB_NAME": "", "SUBMITTER_MESSAGE_QUEUE": "", "SUBMITTER_MESSAGE_QUEUE_LIBRARY": ""}]
            
      
        
