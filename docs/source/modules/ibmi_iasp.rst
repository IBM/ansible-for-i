..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_iasp.py


ibmi_iasp -- Control IASP on target IBMi node
=============================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Control IASP on target IBMi node

For non-IBMi targets, no need






Parameters
----------

  extra_parameters (optional, str,  )
    extra parameter is appended at the end of create operation


  primary_asp (optional, str, None)
    The primary_asp of new create iasp


  name (True, str, None)
    The name of the iasp


  operation (True, str, None)
    ``create``/``delete``/``add_disks`` are idempotent actions that will not run commands unless necessary.

    ``view`` will return the iasp state

    **At least one of operation are required.**


  disks (optional, list, None)
    The list of the unconfigure disks


  synchronous (optional, bool, True)
    synchronous execute the iasp command


  asp_type (optional, str, *PRIMARY)
    The asp_type of new create iasp









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

  stderr_lines (always, list, ['Generic failure'])
    The command standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The command execution end time


  stdout (always, str, CPCB719: Configure Device ASP *DELETE request completed.)
    The command standard output


  asp_info (always, str, [{'ASP_STATE': 'VARIED OFF', 'UNPROTECTED_CAPACITY_AVAILABLE': '0', 'BALANCE_DATA_MOVED': '0', 'RESOURCE_NAME': 'IASP1', 'MAIN_STORAGE_DUMP_SPACE': '0', 'TRACE_STATUS': '', 'PROTECTED_CAPACITY_AVAILABLE': '0', 'END_IMMEDIATE': '', 'TRACE_TIMESTAMP': '', 'BALANCE_TIMESTAMP': '', 'STORAGE_THRESHOLD_PERCENTAGE': '90', 'ERROR_LOG_SPACE': '0', 'MULTIPLE_CONNECTION_DISK_UNITS': 'YES', 'COMPRESSED_DISK_UNITS': 'NONE', 'TOTAL_CAPACITY_AVAILABLE': '0', 'ASP_TYPE': 'PRIMARY', 'TRACE_DURATION': '0', 'CHANGES_WRITTEN_TO_DISK': 'YES', 'MACHINE_LOG_SPACE': '0', 'SYSTEM_STORAGE': '2', 'OVERFLOW_RECOVERY_RESULT': '', 'PROTECTED_CAPACITY': '0', 'PRIMARY_ASP_RESOURCE_NAME': '', 'DEVICE_DESCRIPTION_NAME': '', 'TOTAL_CAPACITY': '0', 'MICROCODE_SPACE': '0', 'DISK_UNITS_PRESENT': 'ALL', 'BALANCE_TYPE': '', 'ASP_NUMBER': '144', 'MACHINE_TRACE_SPACE': '0', 'BALANCE_STATUS': '', 'BALANCE_DATA_REMAINING': '0', 'NUMBER_OF_DISK_UNITS': '1', 'COMPRESSION_RECOVERY_POLICY': 'OVERFLOW IMMEDIATE', 'OVERFLOW_STORAGE': '0', 'UNPROTECTED_CAPACITY': '0', 'RDB_NAME': 'IASP1'}])
    the asp_info of the identify iasp


  cmd (always, str, CFGDEVASP ASPDEV(YFTEST) ACTION(*DELETE) CONFIRM(*NO))
    The command executed by the task


  start (always, str, 2019-12-02 11:07:53.757435)
    The command execution start time


  delta (always, str, 0:00:00.307534)
    The command execution delta time


  stderr (always, str, Generic failure)
    The command standard error


  rc (always, int, 255)
    The command return code (0 means success, non-zero means failure)


  stdout_lines (always, list, ['CPCB719: Configure Device ASP *DELETE request completed.'])
    The command standard output split in lines


  rc_msg (always, str, Generic failure)
    Meaning of the return code





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Jin Yi Fan(@jinyifan)

