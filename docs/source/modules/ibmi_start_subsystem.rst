..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_start_subsystem.py


ibmi_start_subsystem -- start a subsystem
=========================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

the ``ibmi_start_subsystem`` module start a subsystem of the target ibmi node.






Parameters
----------

  subsystem (True, str, None)
    The name of the subsystem description


  library (optional, str, *LIBL)
    Specify the library where the subsystem description is located







See Also
--------

.. seealso::

   :ref:`ibmi_end_subsystem_module`
      The official documentation on the **ibmi_end_subsystem** module.


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



Return Values
-------------

  stderr_lines (always, list, ['CPF1080: Library MYLIB not found.'])
    The standard error split in lines


  stdout_lines (always, list, ['CPF0902: Subsystem QINTER in library QSYS being started.'])
    The standard output split in lines


  stdout (always, str, CPF0902: Subsystem QBATCH in library QSYS being started.)
    The standard output of the start subsystem command


  stderr (always, str, CPF1010: Subsystem name QBATCH active.)
    The standard error the start subsystem command


  rc (always, int, 255)
    The task return code (0 means success, non-zero means failure)





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le (@changlexc)

