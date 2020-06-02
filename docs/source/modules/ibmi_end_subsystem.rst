..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_end_subsystem.py


ibmi_end_subsystem -- end a subsystem
=====================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

the ``ibmi_end_subsystem`` module end a subsystem of the target ibmi node.






Parameters
----------

  subsystem (True, str, None)
    The name of the subsystem description


  controlled_end_delay_time (optional, int, 100000)
    Specifies the amount of time (in seconds) that is allowed to complete the controlled subsystem end operation

    If this amount of time is exceeded and the end operation is not complete,

    any jobs still being processed in the subsystem are ended immediately

    If the value is greater than 99999, '*NOLIMIT' will be used in ENDSBS commnad


  how_to_end (optional, str, *CNTRLD)
    Specifies whether jobs in the subsystem are ended in a controlled manner or immediately


  end_subsystem_option (optional, list, [u'*DFT'])
    Specifies the options to take when ending the active subsystems


  parameters (optional, str, )
    The parameters that ENDSBS command will take

    Other than options above, all other parameters need to be specified here

    The default values of parameters for ENDSBS will be taken if not specified





Notes
-----

.. note::
   - This module is NOT ALLOWED to end ALL subsystems, use the ``ibmi_cl_command`` module instead
   - This module is non-blocking, the end subsystem may still be in progress, use ``ibmi_display_subsystem_job`` module to check the status


See Also
--------

.. seealso::

   :ref:`ibmi_end_subsystem_module`
      The official documentation on the **ibmi_end_subsystem** module.


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



Return Values
-------------

  stderr_lines (always, list, ['CPF1054: No subsystem MYJOB active.'])
    The standard error split in lines


  stdout_lines (always, list, ['CPF0943: Ending of subsystem QBATCH in progress.'])
    The standard output split in lines


  stdout (always, str, CPF0943: Ending of subsystem QBATCH in progress.)
    The standard output of the end subsystem command


  stderr (always, str, CPF1054: No subsystem MYJOB active.)
    The standard error the end subsystem command


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le (@changlexc)

