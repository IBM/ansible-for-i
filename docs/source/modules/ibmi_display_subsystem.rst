..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_display_subsystem.py


ibmi_display_subsystem -- display all currently active subsystems or currently active jobs in a subsystem
=========================================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

the ``ibmi_display_subsystem`` module all currently active subsystems or currently active jobs in a subsystem of the target ibmi node.

In some ways it has equivalent results of WRKSBS if subsystem is '*ALL', otherwise, it has equivalent results of WRKSBSJOB






Parameters
----------

  subsystem (optional, str, *ALL)
    Specifies the name of the subsystem


  user (optional, str, *ALL)
    Specifies the name of the user whose jobs are displayed('*ALL' for all user names). If subsystem is '*ALL', this option is ignored







See Also
--------

.. seealso::

   :ref:`ibmi_end_subsystem, ibmi_start_subsystem_module`
      The official documentation on the **ibmi_end_subsystem, ibmi_start_subsystem** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Display all the active subsystems in this system
      ibmi_display_subsystem:

    - name: Display all the active jobs of subsystem QINTER
      ibmi_display_subsystem:
        subsystem: QINTER

    - name: Display With One User's Job of subsystem QBATCH
      ibmi_display_subsystem:
        subsystem: QBATCH
        user: 'JONES'



Return Values
-------------

  stderr_lines (When rc as non-zero(failure), list, [''])
    The standard error split in lines


  subsystems (When rc as 0(success) and subsystem is '*ALL', list, ['QCMN', 'QCTL', 'QHTTPSVR', 'QINTER', 'QSERVER', 'QSPL', 'QSYSWRK', 'QUSRWRK'])
    The result set


  stderr (When rc as non-zero(failure), str, )
    The standard error the the display subsystem job


  stdout (When rc as non-zero(failure), str, )
    The standard output of the display subsystem job results set


  stdout_lines (When rc as non-zero(failure), list, [''])
    The standard output split in lines


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)


  active_jobs (When rc as 0(success) and subsystem is not '*ALL', list, [{'JOB_STATUS': 'EVTW', 'FUNCTION': 'QEZSCNEP', 'CPU_TIME': '17', 'ELAPSED_SYNC_DISK_IO_COUNT': '0', 'ELAPSED_TOTAL_DISK_IO_COUNT': '0', 'ELAPSED_INTERACTION_COUNT': '0', 'ELAPSED_TIME': '0.000', 'ELAPSED_CPU_TIME': '0', 'FUNCTION_TYPE': 'PGM', 'ELAPSED_ASYNC_DISK_IO_COUNT': '0', 'JOB_NAME': '022042/QPGMR/QSYSSCD', 'SUBSYSTEM_LIBRARY_NAME': 'QSYS', 'SUBSYSTEM': 'QCTL', 'AUTHORIZATION_NAME': 'QPGMR', 'MEMORY_POOL': 'BASE', 'THREAD_COUNT': '1', 'RUN_PRIORITY': '10', 'SERVER_TYPE': '', 'JOB_TYPE': 'BCH', 'ELAPSED_CPU_PERCENTAGE': '0.0', 'TEMPORARY_STORAGE': '6', 'ORDINAL_POSITION': '2', 'INTERNAL_JOB_ID': '002700010041F300A432B3A44FFD7001', 'ELAPSED_TOTAL_RESPONSE_TIME': '0', 'TOTAL_DISK_IO_COUNT': '587', 'ELAPSED_PAGE_FAULT_COUNT': '0', 'JOB_END_REASON': ''}])
    The result set





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le (@changlexc)

