..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_job.py


ibmi_job -- Returns job information according to inputs.
========================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_job`` module returns information associated with one or more jobs.






Parameters
----------

  status (optional, str, *ALL)
    The job status filter.


  subsystem (optional, str, *ALL)
    The job subsystem filter. A valid subsystem name can be specified. Valid values are "*ALL" or subsystem name.


  name (False, str, None)
    The qualified job name.

    If this parameter is specified, the other parameters will be ignored.


  submitter (optional, str, *ALL)
    The type of submitted jobs to return.


  type (optional, str, *ALL)
    The job type filter.


  user (optional, str, *USER)
    The user profile name to use as the job user filtering criteria.

    Valid values are user profile name, "*USER" or "*ALL".





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`ibmi_submit_job_module`
      The official documentation on the **ibmi_submit_job** module.


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



Return Values
-------------

  stderr_lines (When rc as non-zero(failure), list, ['CPF2111:Library TESTLIB already exists.'])
    The task standard error split in lines


  end (When job has been submitted and task has waited for the job status for some time, str, 2019-12-02 11:07:54.064969)
    The task execution end time


  stdout (When rc as non-zero(failure), str, CPC2102: Library TESTLIB created)
    The task standard output


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)


  job_info (When rc is zero, list, [{'JOB_STATUS': 'OUTQ', 'JOB_QUEUE_NAME': '', 'JOB_DESCRIPTION_LIBRARY': '', 'JOB_TYPE': 'BCH', 'JOB_ACCOUNTING_CODE': '*SYS', 'SUBMITTER_JOB_NAME': '', 'JOB_END_TIME': '2020-02-14-00.36.35', 'JOB_ENTERED_SYSTEM_TIME': '2020-02-14-00.36.35', 'JOB_DESCRIPTION': '', 'JOB_INFORMATION': 'YES', 'JOB_NAME': '514647/WANGYUN/QPRTJOB', 'JOB_TYPE_ENHANCED': 'ALTERNATE_SPOOL_USER', 'COMPLETION_STATUS': 'ABNORMAL', 'JOB_DATE': '', 'JOB_ACTIVE_TIME': '', 'JOB_QUEUE_LIBRARY': '', 'JOB_QUEUE_STATUS': '', 'SUBMITTER_MESSAGE_QUEUE': '', 'JOB_SUBSYSTEM': '', 'SUBMITTER_MESSAGE_QUEUE_LIBRARY': '', 'JOB_SCHEDULED_TIME': '', 'CCSID': '0', 'JOB_END_REASON': '', 'JOB_QUEUE_PRIORITY': '0', 'JOB_END_SEVERITY': '10'}, {'JOB_STATUS': 'OUTQ', 'JOB_QUEUE_NAME': '', 'JOB_DESCRIPTION_LIBRARY': 'QGPL', 'JOB_TYPE': 'INT', 'JOB_ACCOUNTING_CODE': '*SYS', 'SUBMITTER_JOB_NAME': '', 'JOB_END_TIME': '2020-03-24-11.06.44', 'JOB_ENTERED_SYSTEM_TIME': '2020-03-23-22.07.18', 'JOB_DESCRIPTION': 'QDFTJOBD', 'JOB_INFORMATION': 'YES', 'JOB_NAME': '547343/WANGYUN/QPADEV0001', 'JOB_TYPE_ENHANCED': 'INTERACTIVE_GROUP', 'COMPLETION_STATUS': 'ABNORMAL', 'JOB_DATE': '', 'JOB_ACTIVE_TIME': '2020-03-23-22.07.18', 'JOB_QUEUE_LIBRARY': '', 'JOB_QUEUE_STATUS': '', 'SUBMITTER_MESSAGE_QUEUE': '', 'JOB_SUBSYSTEM': '', 'SUBMITTER_MESSAGE_QUEUE_LIBRARY': '', 'JOB_SCHEDULED_TIME': '', 'CCSID': '65535', 'JOB_END_REASON': 'JOB ENDED DUE TO A DEVICE ERROR', 'JOB_QUEUE_PRIORITY': '0', 'JOB_END_SEVERITY': '30'}])
    The information of the job(s)


  start (When job has been submitted and task has waited for the job status for some time, str, 2019-12-02 11:07:53.757435)
    The task execution start time


  stderr (When rc as non-zero(failure), str, CPF2111:Library TESTLIB already exists)
    The task standard error


  delta (When job has been submitted and task has waited for the job status for some time, str, 0:00:00.307534)
    The task execution delta time


  stdout_lines (When rc as non-zero(failure), list, ['CPC2102: Library TESTLIB created.'])
    The task standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Wang Yun (@airwangyun)

