..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_display_subsystem.py

.. _ibmi_display_subsystem_module:

ibmi_display_subsystem -- display all currently active subsystems or currently active jobs in a subsystem
=========================================================================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- the ``ibmi_display_subsystem`` module all currently active subsystems or currently active jobs in a subsystem of the target ibmi node.
- In some ways it has equivalent results of WRKSBS if subsystem is '*ALL', otherwise, it has equivalent results of WRKSBSJOB



Parameters
----------


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
subsystem
  Specifies the name of the subsystem


  | **required**: false
  | **type**: str
  | **default**: *ALL


     
user
  Specifies the name of the user whose jobs are displayed('*ALL' for all user names). If subsystem is '*ALL', this option is ignored


  | **required**: false
  | **type**: str
  | **default**: *ALL



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




See Also
--------

.. seealso::

   - :ref:`ibmi_end_subsystem, ibmi_start_subsystem_module`


Return Values
-------------


   
                              
       stderr_lines
        | The standard error split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [""]
            
      
      
                              
       subsystems
        | The result set
      
        | **returned**: When rc as 0(success) and subsystem is '*ALL'
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["                                      Work with Subsystems                                       5/25/20 19:55:04        Page 0001", "                          Subsystem        Active                          Total         -----------Subsystem Pools-----------------", "      Subsystem             Number          Jobs        Status          Storage (M)       1   2   3   4   5   6   7   8   9  10", "      QBATCH                018647              0       ACTIVE                     .00    2", "      QCMN                  018651              7       ACTIVE                     .00    2", "      QCTL                  018621              1       ACTIVE                     .00    2", "      QHTTPSVR              018742              8       ACTIVE                     .00    2", "      QINTER                018642              0       ACTIVE                     .00    2   3", "      QSERVER               018631             16       ACTIVE                     .00    2", "      QSPL                  018652              0       ACTIVE                     .00    2   4", "      QSYSWRK               018622            111       ACTIVE                     .00    2", "      QUSRWRK               018633             27       ACTIVE                     .00    2", "                          * * * * *  E N D  O F  L I S T I N G  * * * * *"]
            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'FROM_MODULE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'FROM_USER': 'CHANGLE', 'TO_INSTRUCTION': '9369', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '20', 'FROM_PROCEDURE': '', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '318F', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '5', 'MESSAGE_FILE': 'QCPFMSG', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       stdout
        | The standard output of the display subsystem job results set
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
      
      
                              
       stderr
        | The standard error the the display subsystem job
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       [""]
            
      
      
                              
       active_jobs
        | The result set
      
        | **returned**: When rc as 0(success) and subsystem is not '*ALL'
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"AUTHORIZATION_NAME": "QPGMR", "CPU_TIME": "17", "ELAPSED_ASYNC_DISK_IO_COUNT": "0", "ELAPSED_CPU_PERCENTAGE": "0.0", "ELAPSED_CPU_TIME": "0", "ELAPSED_INTERACTION_COUNT": "0", "ELAPSED_PAGE_FAULT_COUNT": "0", "ELAPSED_SYNC_DISK_IO_COUNT": "0", "ELAPSED_TIME": "0.000", "ELAPSED_TOTAL_DISK_IO_COUNT": "0", "ELAPSED_TOTAL_RESPONSE_TIME": "0", "FUNCTION": "QEZSCNEP", "FUNCTION_TYPE": "PGM", "INTERNAL_JOB_ID": "002700010041F300A432B3A44FFD7001", "JOB_END_REASON": "", "JOB_NAME": "022042/QPGMR/QSYSSCD", "JOB_STATUS": "EVTW", "JOB_TYPE": "BCH", "MEMORY_POOL": "BASE", "ORDINAL_POSITION": "2", "RUN_PRIORITY": "10", "SERVER_TYPE": "", "SUBSYSTEM": "QCTL", "SUBSYSTEM_LIBRARY_NAME": "QSYS", "TEMPORARY_STORAGE": "6", "THREAD_COUNT": "1", "TOTAL_DISK_IO_COUNT": "587"}]
            
      
        
