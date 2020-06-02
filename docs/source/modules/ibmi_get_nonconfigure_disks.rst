..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_get_nonconfigure_disks.py


ibmi_get_nonconfigure_disks -- Get all nonconfigure disks on target IBMi node
=============================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

Get all nonconfigure disks on target IBMi node

For non-IBMi targets, no need






Parameters
----------

  joblog (optional, bool, False)
    If set to ``true``, append JOBLOG to stderr/stderr_lines.









Examples
--------

.. code-block:: yaml+jinja

    
    - name: get all nonconfigure disks
      ibmi_get_nonconfigure_disks:
        joblog: True



Return Values
-------------

  start (always, str, 2019-12-02 11:07:53.757435)
    The command execution start time


  end (always, str, 2019-12-02 11:07:54.064969)
    The command execution end time


  delta (always, str, 0:00:00.307534)
    The command execution delta time


  disks (always, str, DMP002 DMP019 DMP005 DMP014 DMP031 DMP012 )
    all un-configure disks


  rc (always, int, 0)
    The command return code (0 means success, non-zero means failure)


  rc_msg (always, str, Success to get all un-configure disks.)
    Meaning of the return code





Status
------




- This module is not guaranteed to have a backwards compatible interface. *[preview]*


- This module is maintained by community.



Authors
~~~~~~~

- Jin Yi Fan(@jinyifan)

