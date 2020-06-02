..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_object_save.py


ibmi_object_save -- Save one or more objects on a remote IBMi node
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_object_save module create an save file on a remote IBMi nodes

The saved objects and save file are on the remote host, and the save file *is not* copied to the local host.

Only support *SAVF as the save file's format by now.






Parameters
----------

  savefile_name (True, str, None)
    The save file name.


  parameters (optional, str,  )
    The parameters that SAVOBJ command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for SAVOBJ will be taken if not specified.


  format (optional, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  object_lib (True, str, None)
    The library contains the objects.


  target_release (optional, str, *CURRENT)
    The release of the operating system on which you intend to restore and use the object.


  force_save (optional, bool, False)
    If save file already exists or contains data, whether to clear data or not.


  object_names (optional, str, *ALL)
    The objects need to be saved. One or more object names can be specified. Use space as separator.


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

    
    - name: Force to save test1.pgm and test2.srvpgm in objlib libary to archive.savf in archlib libary
      ibmi_object_save:
        object_names: 'test1 test2'
        object_lib: 'objlib'
        object_types: '*PGM *SRVPGM'
        savefile_name: 'archive'
        savefile_lib: 'archlib'
        force_save: true
        target_release: 'V7R2M0'



Return Values
-------------

  stderr_lines (always, list, ['CPF5813: File archive in library archlib already exists.', 'CPF7302: File archive not created in library archlib.'])
    The save standard error split in lines


  stdout (always, str, CPC3722: 2 objects saved from library objlib.)
    The save standard output


  rc (always, int, 255)
    The save action return code (0 means success, non-zero means failure)


  object_names (always, str, test1 test2)
    The objects need to be saved.


  savefile_lib (always, str, c1lib)
    The save file library.


  delta (always, str, 0:00:00.307534)
    The save execution delta time


  stdout_lines (always, list, ['CPC3722: 2 objects saved from library objlib.'])
    The save standard output split in lines


  savefile_name (always, str, c1)
    The save file name.


  end (always, str, 2019-12-02 11:07:54.064969)
    The save execution end time


  start (always, str, 2019-12-02 11:07:53.757435)
    The save execution start time


  format (always, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  target_release (always, str, V7R1M0)
    The release of the operating system on which you intend to restore and use the object.


  force_save (always, bool, True)
    If save file already exists or contains data, whether to clear data or not.


  object_lib (always, str, objlib)
    The library contains the object.


  stderr (always, str, CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n)
    The save standard error


  joblog (always, bool, False)
    Append JOBLOG to stderr/stderr_lines or not.


  command (always, str, SAVOBJ OBJ(*ALL) LIB(TESTLIB) DEV(*SAVF) OBJTYPE(*ALL) SAVF(TEST/ARCHLIB) TGTRLS(V7R1M0))
    The last excuted command.


  object_types (always, str, *PGM *SRVPGM)
    The object types.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

