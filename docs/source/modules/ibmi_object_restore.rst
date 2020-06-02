..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_object_restore.py


ibmi_object_restore -- Restore one or more objects on a remote IBMi node
========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_object_restore module restore an save file on a remote IBMi nodes

The restored objects and save file are on the remote host.

Only support *SAVF as the save file's format by now.






Parameters
----------

  savefile_name (True, str, None)
    The save file name.


  parameters (optional, str,  )
    The parameters that RSTOBJ command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for RSTOBJ will be taken if not specified.


  format (optional, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  object_lib (True, str, None)
    The library that contains the saved objects.


  object_names (optional, str, *ALL)
    The objects need to be restored. One or more object names can be specified. Use space as separator.


  savefile_lib (True, str, None)
    The save file library.


  joblog (optional, bool, False)
    If set to ``true``, append JOBLOG to stderr/stderr_lines.


  object_types (optional, str, *ALL)
    The object types. One or more object types can be specified. Use space as separator.


  asp_group (optional, str, )
    Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

    The ASP group name is the name of the primary ASP device within the ASP group.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)




Examples
--------

.. code-block:: yaml+jinja

    
    - name: Restore test1.pgm test2.srvpgm in savedlib libary from archive.savf in archlib libary
      ibmi_object_restore:
        object_names: 'test1 test2'
        object_lib: 'savedlib'
        object_types: '*PGM *SRVPGM'
        savefile_name: 'archive'
        savefile_lib: 'archlib'



Return Values
-------------

  stderr_lines (always, list, ['CPF9812: File file1 in library C1 not found.'])
    The restore standard error split in lines


  stdout (always, str, CPC3703: 2 objects restored from C1 to C1.)
    The restore standard output


  rc (always, int, 255)
    The restore action return code (0 means success, non-zero means failure)


  object_names (always, str, test1 test2)
    The objects need to be restored.


  savefile_lib (always, str, c1lib)
    The save file library.


  delta (always, str, 0:00:00.307534)
    The restore execution delta time


  stdout_lines (always, list, ['CPC3703: 2 objects restored from C1 to C1.'])
    The restore standard output split in lines


  savefile_name (always, str, c1)
    The save file name.


  end (always, str, 2019-12-02 11:07:54.064969)
    The restore execution end time


  format (always, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  start (always, str, 2019-12-02 11:07:53.757435)
    The restore execution start time


  object_lib (always, str, objectlib)
    The library that contains the saved objects.


  stderr (always, str, CPF9812: File file1 in library C1 not found..\)
    The restore standard error


  joblog (always, bool, False)
    Append JOBLOG to stderr/stderr_lines or not.


  command (always, str, RSTOBJ OBJ(OBJA) SAVLIB(TESTLIB) DEV(*SAVF) OBJTYPE(*ALL) SAVF(TEST/ARCHLIB))
    The last excuted command.


  object_types (always, str, *PGM *SRVPGM)
    The objects types.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

