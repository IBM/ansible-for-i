
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_submit_job.py

.. _ibmi_submit_job_module:


ibmi_submit_job -- Submit a job on IBM i system. This module functions like SBMJOB.
===================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_submit_job`` module submits a job on IBM i system.
- It waits until the submitted job turns into expected status that is specified.





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


     
check_interval
  The time interval between current and next checks of the expected status of the submitted job. This option will be ignored if ``*NONE`` is specified for option status.


  | **required**: False
  | **type**: str
  | **default**: 1m


     
cmd
  A command that runs in the batch job.


  | **required**: True
  | **type**: str


     
parameters
  The parameters that SBMJOB will take. Other than CMD, all other parameters need to be specified here. The default values of parameters for SBMJOB will be taken if not specified.


  | **required**: False
  | **type**: str


     
status
  The expect status list. The module will wait for the job to be turned into one of the expected status specified. If one of the expect status specified matches the status of submitted job, it will return. If ``*NONE`` is specified, the module will not wait for anything and return right after the job is submitted. The valid options are ``*NONE``, ``*ACTIVE``, ``*COMPLETE``, ``*JOBQ``, ``*OUTQ``.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['\*NONE']


     
time_out
  The max time that the module waits for the submitted job is turned into expected status. It returns if the status of the submitted job is not turned into the expected status within the time_out time. This option will be ignored if ``*NONE`` is specified for option status.


  | **required**: False
  | **type**: str
  | **default**: 1m




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Submit a batch job and run CALL QGPL/PGM1
     ibmi_submit_job:
       cmd: 'CALL QGPL/PGM1'
       parameters: 'JOB(TEST)'
       check_interval: '30s'
       time_out: '80s'
       status: ['*OUTQ', '*COMPLETE']




Notes
-----

.. note::
   Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)



See Also
--------

.. seealso::

   - :ref:`ibmi_job_module`



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

            
      
      
                              
       sbmjob_cmd
        | The SBMJOB CL command that has been used.
      
        | **returned**: always
        | **type**: str
        | **sample**: SBMJOB CMD(CRTLIB LIB(TESTLIB))

            
      
      
                              
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
            
      
        
