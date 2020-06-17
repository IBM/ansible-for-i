..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_start_subsystem.py

.. _ibmi_start_subsystem_module:

ibmi_start_subsystem -- start a subsystem
=========================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- the ``ibmi_start_subsystem`` module start a subsystem of the target ibmi node.



Parameters
----------


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
library
  Specify the library where the subsystem description is located


  | **required**: false
  | **type**: str
  | **default**: *LIBL


     
subsystem
  The name of the subsystem description


  | **required**: True
  | **type**: str



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Start the subsystem QBATCH
     ibmi_start_subsystem:
       subsystem: QBATCH

   - name: Start a user defined subsystem, which the subsystem description is MYSBS, located at library MYLIB
     ibmi_start_subsystem:
       subsystem: MYSBS
       library: MYLIB




See Also
--------

.. seealso::

   - :ref:`ibmi_end_subsystem_module`


Return Values
-------------


   
                              
       stderr_lines
        | The standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF1080: Library MYLIB not found."]
            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'FROM_MODULE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'FROM_USER': 'CHANGLE', 'TO_INSTRUCTION': '9369', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '20', 'FROM_PROCEDURE': '', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '318F', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '5', 'MESSAGE_FILE': 'QCPFMSG', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       stderr
        | The standard error the start subsystem command
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF1010: Subsystem name QBATCH active.

            
      
      
                              
       stdout
        | The standard output of the start subsystem command
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF0902: Subsystem QBATCH in library QSYS being started.

            
      
      
                              
       stdout_lines
        | The standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF0902: Subsystem QINTER in library QSYS being started."]
            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
        
