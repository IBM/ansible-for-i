..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_lib_restore.py


ibmi_lib_restore -- Restore one library on a remote IBMi node
=============================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_lib_restore module restore an save file on a remote IBMi nodes

The restored library and save file are on the remote host.

Only support *SAVF as the save file's format by now.






Parameters
----------

  saved_lib (True, str, None)
    The library need to be restored.


  savefile_name (True, str, None)
    The save file name.


  asp_group (optional, str, )
    Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

    The ASP group name is the name of the primary ASP device within the ASP group.


  parameters (optional, str,  )
    The parameters that RSTLIB command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for RSTLIB will be taken if not specified.


  format (optional, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  joblog (optional, bool, False)
    If set to ``true``, append JOBLOG to stderr/stderr_lines.


  savefile_lib (True, str, None)
    The save file library.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Restore savedlib libary from archive.savf in archlib libary
      ibmi_lib_restore:
        saved_lib: 'savedlib'
        savefile_name: 'archive'
        savefile_lib: 'archlib'



Return Values
-------------

  saved_lib (always, str, savedlib)
    The library need to be restored.


  savefile_name (always, str, c1)
    The save file name.


  end (always, str, 2019-12-02 11:07:54.064969)
    The restore execution end time


  stdout (always, str, CPC3703: 2 objects restored from test to test.)
    The restore standard output


  format (always, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  stderr_lines (always, list, ['CPF3806: Objects from save file archive in archlib not restored.', 'CPF3780: Specified file for library test not found.'])
    The restore standard error split in lines


  start (always, str, 2019-12-02 11:07:53.757435)
    The restore execution start time


  delta (always, str, 0:00:00.307534)
    The restore execution delta time


  command (always, str, RSTLIB SAVLIB(TESTLIB) DEV(*SAVF) SAVF(TEST/ARCHLIB) )
    The last excuted command.


  savefile_lib (always, str, c1lib)
    The save file library.


  stderr (always, str, CPF3806: Objects from save file archive in archlib not restored.\n)
    The restore standard error


  rc (always, int, 255)
    The restore action return code (0 means success, non-zero means failure)


  stdout_lines (always, list, ['CPC3703: 2 objects restored from test to test.'])
    The restore standard output split in lines





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

