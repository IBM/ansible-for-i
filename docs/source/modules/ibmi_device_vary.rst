..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_device_vary.py


ibmi_device_vary -- vary on or off target device on a remote IBMi node
======================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

vary on or off target device on a remote IBMi node.

For non-IBMi targets, no need






Parameters
----------

  status (True, str, None)
    ``on``/``off`` are idempotent actions that will not run commands unless necessary.

    ``reset`` will always bounce the service.

    **At least one of status are required.**


  extra_parameters (optional, str,  )
    extra parameter is appended at the end of VARYCFG command


  device_list (True, list, None)
    The name of the device


  joblog (optional, bool, False)
    If set to ``true``, append JOBLOG to stderr/stderr_lines.







See Also
--------

.. seealso::

   :ref:`service_module`
      The official documentation on the **service** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: start host server service
      ibmi_device_vary:
        device_list: ['IASP1', 'IASP2']
        state: '*ON'
        joblog: True



Return Values
-------------

  stderr_lines (always, list, ['CPF2111:Library TESTLIB already exists.'])
    The command standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The command execution end time


  stdout (always, str, +++ success VRYCFG CFGOBJ(IASP1) CFGTYPE(*DEV) STATUS(*ON))
    The command standard output


  cmd (always, str, VRYCFG CFGOBJ(IASP1) CFGTYPE(*DEV) STATUS(*ON) )
    The command executed by the task


  rc (always, int, 255)
    The command return code (0 means success, non-zero means failure)


  start (always, str, 2019-12-02 11:07:53.757435)
    The command execution start time


  delta (always, str, 0:00:00.307534)
    The command execution delta time


  stderr (always, str, CPF2111:Library TESTLIB already exists)
    The command standard error


  joblog (always, bool, False)
    Append JOBLOG to stderr/stderr_lines or not.


  stdout_lines (always, list, ['+++ success VRYCFG CFGOBJ(IASP1) CFGTYPE(*DEV) STATUS(*ON)'])
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

