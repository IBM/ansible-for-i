..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_lib_save.py


ibmi_lib_save -- Save one libary on a remote IBMi node
======================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_lib_save module create an save file on a remote IBMi nodes

The save file *is not* copied to the local host.

Only support *SAVF as the save file's format by now.






Parameters
----------

  savefile_name (True, str, None)
    The save file name.


  parameters (optional, str,  )
    The parameters that SAVLIB command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for SAVLIB will be taken if not specified.


  format (optional, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  target_release (optional, str, *CURRENT)
    The release of the operating system on which you intend to restore and use the SAVF.


  force_save (optional, bool, False)
    If save file already exists or contains data, whether to clear data or not.


  savefile_lib (True, str, None)
    The save file library.


  joblog (optional, bool, False)
    If set to ``true``, append JOBLOG to stderr/stderr_lines.


  lib_name (True, str, None)
    The library need to be saved.


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

    
    - name: Force to save test libary to archive.savf in archlib libary
      ibmi_lib_save:
        lib_name: 'test'
        savefile_name: 'archive'
        savefile_lib: 'archlib'
        force_save: true
        target_release: 'V7R2M0'



Return Values
-------------

  savefile_name (always, str, archive)
    The save file name.


  stderr_lines (always, list, ['CPF5813: File archive in library archlib already exists.', 'CPF7302: File archive not created in library archlib.'])
    The save standard error split in lines


  end (always, str, 2019-12-02 11:07:54.064969)
    The save execution end time


  stdout (always, str, CPC3722: 2 objects saved from library test.)
    The save standard output


  format (always, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  target_release (always, str, V7R2M0)
    The release of the operating system on which you intend to restore and use the library.


  force_save (always, bool, True)
    If save file already exists or contains data, whether to clear data or not.


  delta (always, str, 0:00:00.307534)
    The save execution delta time


  command (always, str, SAVLIB LIB(TEST) DEV(*SAVF) SAVF(TEST/ARCHLIB) TGTRLS(V7R2M0))
    The last excuted command.


  savefile_lib (always, str, archlib)
    The save file library.


  stderr (always, str, CPF5813: File archive in library archlib already exists.\nCPF7302: File archive not created in library archlib.\n)
    The save standard error


  rc (always, int, 255)
    The save action return code (0 means success, non-zero means failure)


  stdout_lines (always, list, ['CPC3722: 2 objects saved from library test.'])
    The save standard output split in lines


  start (always, str, 2019-12-02 11:07:53.757435)
    The save execution start time


  lib_name (always, str, test)
    The library need to be saved.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

