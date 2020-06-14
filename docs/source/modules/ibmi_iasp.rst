..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_iasp.py

.. _ibmi_iasp_module:

ibmi_iasp -- Control IASP on target IBMi node
=============================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Control IASP on target IBMi node
- For non-IBMi targets, no need



Parameters
----------


     
asp_type
  The asp_type of new create iasp


  | **required**: false
  | **type**: str
  | **default**: *PRIMARY
  | **choices**: *PRIMARY, *SECONDARY, *UDFS


     
disks
  The list of the unconfigure disks


  | **required**: false
  | **type**: list
  | **elements**: str


     
extra_parameters
  extra parameter is appended at the end of create operation


  | **required**: false
  | **type**: str
  | **default**:  


     
joblog
  If set to ``true``, append JOBLOG to stderr/stderr_lines.


  | **required**: false
  | **type**: bool


     
name
  The name of the iasp


  | **required**: True
  | **type**: str


     
operation
  ``create``/``delete``/``add_disks`` are idempotent actions that will not run commands unless necessary.

  ``view`` will return the iasp state

  **At least one of operation are required.**


  | **required**: True
  | **type**: str
  | **choices**: create, add_disks, delete, display


     
primary_asp
  The primary_asp of new create iasp


  | **required**: false
  | **type**: str


     
synchronous
  synchronous execute the iasp command


  | **required**: false
  | **type**: bool
  | **default**: True



Examples
--------

.. code-block:: yaml+jinja

   
   - name: start host server service
     ibmi_iasp:
       name: 'IASP1'
       operation: 'create'
       disks: ['DMP002', 'DMP019']






Return Values
-------------


   
                              
       stderr_lines
        | The command standard error split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Generic failure"]
            
      
      
                              
       end
        | The command execution end time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       stdout
        | The command standard output
      
        | **returned**: always
        | **type**: str
        | **sample**: CPCB719: Configure Device ASP *DELETE request completed.

            
      
      
                              
       asp_info
        | the asp_info of the identify iasp
      
        | **returned**: always
        | **type**: str
        | **sample**: [{'ASP_STATE': 'VARIED OFF', 'UNPROTECTED_CAPACITY_AVAILABLE': '0', 'BALANCE_DATA_MOVED': '0', 'RESOURCE_NAME': 'IASP1', 'MAIN_STORAGE_DUMP_SPACE': '0', 'TRACE_STATUS': '', 'PROTECTED_CAPACITY_AVAILABLE': '0', 'END_IMMEDIATE': '', 'TRACE_TIMESTAMP': '', 'BALANCE_TIMESTAMP': '', 'STORAGE_THRESHOLD_PERCENTAGE': '90', 'ERROR_LOG_SPACE': '0', 'MULTIPLE_CONNECTION_DISK_UNITS': 'YES', 'COMPRESSED_DISK_UNITS': 'NONE', 'TOTAL_CAPACITY_AVAILABLE': '0', 'ASP_TYPE': 'PRIMARY', 'TRACE_DURATION': '0', 'CHANGES_WRITTEN_TO_DISK': 'YES', 'MACHINE_LOG_SPACE': '0', 'SYSTEM_STORAGE': '2', 'OVERFLOW_RECOVERY_RESULT': '', 'PROTECTED_CAPACITY': '0', 'PRIMARY_ASP_RESOURCE_NAME': '', 'DEVICE_DESCRIPTION_NAME': '', 'TOTAL_CAPACITY': '0', 'MICROCODE_SPACE': '0', 'DISK_UNITS_PRESENT': 'ALL', 'BALANCE_TYPE': '', 'ASP_NUMBER': '144', 'MACHINE_TRACE_SPACE': '0', 'BALANCE_STATUS': '', 'BALANCE_DATA_REMAINING': '0', 'NUMBER_OF_DISK_UNITS': '1', 'COMPRESSION_RECOVERY_POLICY': 'OVERFLOW IMMEDIATE', 'OVERFLOW_STORAGE': '0', 'UNPROTECTED_CAPACITY': '0', 'RDB_NAME': 'IASP1'}]

            
      
      
                              
       cmd
        | The command executed by the task
      
        | **returned**: always
        | **type**: str
        | **sample**: CFGDEVASP ASPDEV(YFTEST) ACTION(*DELETE) CONFIRM(*NO)

            
      
      
                              
       start
        | The command execution start time
      
        | **returned**: always
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       delta
        | The command execution delta time
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stderr
        | The command standard error
      
        | **returned**: always
        | **type**: str
        | **sample**: Generic failure

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The command standard output split in lines
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPCB719: Configure Device ASP *DELETE request completed."]
            
      
      
                              
       rc_msg
        | Meaning of the return code
      
        | **returned**: always
        | **type**: str
        | **sample**: Generic failure

            
      
        
