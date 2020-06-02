..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_end_subsystem.py

.. _ibmi_end_subsystem_module:

ibmi_end_subsystem -- end a subsystem
=====================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- the ``ibmi_end_subsystem`` module end a subsystem of the target ibmi node.



Parameters
----------


     
controlled_end_delay_time
  Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation

  If this amount of time is exceeded and the end operation is not complete,

  any jobs still being processed in the subsystem are ended immediately

  If the value is greater than 99999, '*NOLIMIT' will be used in ENDSBS commnad


  | **required**: false
  | **type**: int
  | **default**: 100000


     
end_subsystem_option
  Specifies the options to take when ending the active subsystems


  | **required**: false
  | **type**: list
  | **elements**: str
  | **choices**: *DFT, *NOJOBLOG, *CHGPTY, *CHGTSL


     
how_to_end
  Specifies whether jobs in the subsystem are ended in a controlled manner or immediately


  | **required**: false
  | **type**: str
  | **default**: *CNTRLD
  | **choices**: *IMMED, *CNTRLD


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
parameters
  The parameters that ENDSBS command will take

  Other than options above, all other parameters need to be specified here

  The default values of parameters for ENDSBS will be taken if not specified


  | **required**: false
  | **type**: str


     
subsystem
  The name of the subsystem description


  | **required**: True
  | **type**: str



Examples
--------

.. code-block:: yaml+jinja

   
   - name: End the subsystem QBATCH
     ibmi_end_subsystem:
       subsystem: QBATCH

   - name: End a subsystem with options
     ibmi_end_subsystem:
       subsystem: QBATCH
       how_to_end: '*IMMED'



Notes
-----

.. note::
   This module is NOT ALLOWED to end ALL subsystems, use the ``ibmi_cl_command`` module instead

   This module is non-blocking, the end subsystem may still be in progress, use ``ibmi_display_subsystem_job`` module to check the status


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

                       ["CPF1054: No subsystem MYJOB active."]
            
      
      
                              
       job_log
        | the job_log
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'TO_MODULE': 'QSQSRVR', 'TO_PROGRAM': 'QSQSRVR', 'MESSAGE_TEXT': 'Printer device PRT01 not found.', 'FROM_MODULE': '', 'FROM_PROGRAM': 'QWTCHGJB', 'MESSAGE_TIMESTAMP': '2020-05-20-21.41.40.845897', 'FROM_USER': 'CHANGLE', 'TO_INSTRUCTION': '9369', 'MESSAGE_SECOND_LEVEL_TEXT': 'Cause . . . . . :   This message is used by application programs as a general escape message.', 'MESSAGE_TYPE': 'DIAGNOSTIC', 'MESSAGE_ID': 'CPD0912', 'MESSAGE_LIBRARY': 'QSYS', 'FROM_LIBRARY': 'QSYS', 'SEVERITY': '20', 'FROM_PROCEDURE': '', 'TO_LIBRARY': 'QSYS', 'FROM_INSTRUCTION': '318F', 'MESSAGE_SUBTYPE': '', 'ORDINAL_POSITION': '5', 'MESSAGE_FILE': 'QCPFMSG', 'TO_PROCEDURE': 'QSQSRVR'}]

            
      
      
                              
       stderr
        | The standard error the end subsystem command
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF1054: No subsystem MYJOB active.

            
      
      
                              
       stdout
        | The standard output of the end subsystem command
      
        | **returned**: always
        | **type**: str
        | **sample**: CPF0943: Ending of subsystem QBATCH in progress.

            
      
      
                              
       stdout_lines
        | The standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF0943: Ending of subsystem QBATCH in progress."]
            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
        
