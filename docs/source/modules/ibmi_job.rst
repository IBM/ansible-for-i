..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_job.py

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


     
name
  The qualified job name.

  If this parameter is specified, the other parameters will be ignored.


  | **required**: False
  | **type**: str


     
status
  The job status filter.


  | **required**: false
  | **type**: str
  | **default**: *ALL
  | **choices**: *ALL, *ACTIVE, *JOBQ, *OUTQ


     
submitter
  The type of submitted jobs to return.


  | **required**: false
  | **type**: str
  | **default**: *ALL
  | **choices**: *ALL, *JOB, *USER, *WRKSTN


     
subsystem
  The job subsystem filter. A valid subsystem name can be specified. Valid values are "*ALL" or subsystem name.


  | **required**: false
  | **type**: str
  | **default**: *ALL


     
type
  The job type filter.


  | **required**: false
  | **type**: str
  | **default**: *ALL
  | **choices**: *ALL, *BATCH, *INTERACT


     
user
  The user profile name to use as the job user filtering criteria.

  Valid values are user profile name, "*USER" or "*ALL".


  | **required**: false
  | **type**: str
  | **default**: *USER



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


   
                              
       stderr_lines
        | The task standard error split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: When job has been submitted and task has waited for the job status for some time
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       stdout
        | The task standard output
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       job_info
        | The information of the job(s)
      
        | **returned**: When rc is zero
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"CCSID": "0", "COMPLETION_STATUS": "ABNORMAL", "JOB_ACCOUNTING_CODE": "*SYS", "JOB_ACTIVE_TIME": "", "JOB_DATE": "", "JOB_DESCRIPTION": "", "JOB_DESCRIPTION_LIBRARY": "", "JOB_END_REASON": "", "JOB_END_SEVERITY": "10", "JOB_END_TIME": "2020-02-14-00.36.35", "JOB_ENTERED_SYSTEM_TIME": "2020-02-14-00.36.35", "JOB_INFORMATION": "YES", "JOB_NAME": "514647/WANGYUN/QPRTJOB", "JOB_QUEUE_LIBRARY": "", "JOB_QUEUE_NAME": "", "JOB_QUEUE_PRIORITY": "0", "JOB_QUEUE_STATUS": "", "JOB_SCHEDULED_TIME": "", "JOB_STATUS": "OUTQ", "JOB_SUBSYSTEM": "", "JOB_TYPE": "BCH", "JOB_TYPE_ENHANCED": "ALTERNATE_SPOOL_USER", "SUBMITTER_JOB_NAME": "", "SUBMITTER_MESSAGE_QUEUE": "", "SUBMITTER_MESSAGE_QUEUE_LIBRARY": ""}, {"CCSID": "65535", "COMPLETION_STATUS": "ABNORMAL", "JOB_ACCOUNTING_CODE": "*SYS", "JOB_ACTIVE_TIME": "2020-03-23-22.07.18", "JOB_DATE": "", "JOB_DESCRIPTION": "QDFTJOBD", "JOB_DESCRIPTION_LIBRARY": "QGPL", "JOB_END_REASON": "JOB ENDED DUE TO A DEVICE ERROR", "JOB_END_SEVERITY": "30", "JOB_END_TIME": "2020-03-24-11.06.44", "JOB_ENTERED_SYSTEM_TIME": "2020-03-23-22.07.18", "JOB_INFORMATION": "YES", "JOB_NAME": "547343/WANGYUN/QPADEV0001", "JOB_QUEUE_LIBRARY": "", "JOB_QUEUE_NAME": "", "JOB_QUEUE_PRIORITY": "0", "JOB_QUEUE_STATUS": "", "JOB_SCHEDULED_TIME": "", "JOB_STATUS": "OUTQ", "JOB_SUBSYSTEM": "", "JOB_TYPE": "INT", "JOB_TYPE_ENHANCED": "INTERACTIVE_GROUP", "SUBMITTER_JOB_NAME": "", "SUBMITTER_MESSAGE_QUEUE": "", "SUBMITTER_MESSAGE_QUEUE_LIBRARY": ""}]
            
      
      
                              
       start
        | The task execution start time
      
        | **returned**: When job has been submitted and task has waited for the job status for some time
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       stderr
        | The task standard error
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: When job has been submitted and task has waited for the job status for some time
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
        
