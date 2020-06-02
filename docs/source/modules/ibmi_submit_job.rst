..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_submit_job.py


ibmi_submit_job -- Submit a job on IBM i system. This module functions like SBMJOB.
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_submit_job`` module submits a job on IBM i system.

It waits until the submitted job turns into expected status that is specified.






Parameters
----------

  status (optional, list, [u'*NONE'])
    The expect status list. The module will wait for the job to be turned into one of the expected status specified. If one of the expect status specified matches the status of submitted job, it will return. If *NONE is specified, the module will not wait for anything and return right after the job is submitted. The valid options are "*NONE", "*ACTIVE", "*COMPLETE", "*JOBQ", "*OUTQ".


  time_out (False, str, 1m)
    The max time that the module waits for the submitted job is turned into expected status. It returns if the status of the submitted job is not turned into the expected status within the time_out time. This option will be ignored if *NONE is specified for option status.


  cmd (True, str, None)
    A command that runs in the batch job.


  check_interval (False, str, 1m)
    The time interval between current and next checks of the expected status of the submitted job. This option will be ignored if *NONE is specified for option status.


  parameters (False, str, )
    The parameters that SBMJOB will take. Other than CMD, all other parameters need to be specified here. The default values of parameters for SBMJOB will be taken if not specified.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`ibmi_job_module`
      The official documentation on the **ibmi_job** module.


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



Return Values
-------------

  stderr_lines (When rc as non-zero(failure), list, ['CPF2111:Library TESTLIB already exists.'])
    The task standard error split in lines


  end (When job has been submitted and task has waited for the job status for some time, str, 2019-12-02 11:07:54.064969)
    The task execution end time


  stdout (When rc as non-zero(failure), str, CPC2102: Library TESTLIB created)
    The task standard output


  delta (When job has been submitted and task has waited for the job status for some time, str, 0:00:00.307534)
    The task execution delta time


  start (When job has been submitted and task has waited for the job status for some time, str, 2019-12-02 11:07:53.757435)
    The task execution start time


  stderr (When rc as non-zero(failure), str, CPF2111:Library TESTLIB already exists)
    The task standard error


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)


  stdout_lines (When rc as non-zero(failure), list, ['CPC2102: Library TESTLIB created.'])
    The task standard output split in lines


  sbmjob_cmd (always, str, SBMJOB CMD(CRTLIB LIB(TESTLIB)))
    The SBMJOB CL command that has been used.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Wang Yun (@airwangyun)

