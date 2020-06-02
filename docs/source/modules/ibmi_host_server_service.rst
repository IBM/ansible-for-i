..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_host_server_service.py


ibmi_host_server_service -- Manage host server on a remote IBMi node
====================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Manage and query IBMi host server service.

For non-IBMi targets, use the :ref:`service <service_module>` module instead.






Parameters
----------

  extra_parameters (optional, str,  )
    extra parameter is appended at the end of host server service command


  state (True, str, None)
    ``started``/``stopped`` are idempotent actions that will not run commands unless necessary.

    ``restarted`` will always bounce the service.

    **At least one of state and enabled are required.**


  name_list (True, list, None)
    The name of the host server service. The valid value are "*ALL", "*CENTRAL", "*DATABASE", "*DTAQ", "*FILE", "*NETPRT", "*RMTCMD", "*SIGNON", "*SVRMAP".


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
      ibmi_host_server_service:
        name_list: ['*CENTRAL', '*DATABASE']
        state: 'started'
        joblog: True



Return Values
-------------

  stderr_lines (always, list, ['CPF2111:Library TESTLIB already exists.'])
    The command standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The command execution end time


  stdout (always, str, +++ success STRHOSTSVR SERVER(*ALL))
    The command standard output


  cmd (always, str, STRHOSTSVR SERVER(*ALL))
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


  stdout_lines (always, list, ['+++ success STRHOSTSVR SERVER(*ALL)'])
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

