..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_fetch.py


ibmi_fetch -- Fetch objects or a library from a remote IBMi node and store on local
===================================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ibmi_feth is used for fetching objects or a library as a SAVF from remote IBMi node and storing them locally in a file tree, organized by hostname.

Save file that already exists at dest will be overwritten if it is different than the new one.

For non-IBMi native targets, use the fetch module instead.






Parameters
----------

  savefile_name (optional, str, )
    The save file name can be specified.

    If not specified savefile_name, the save file name will be the first object_name.file. If is_lib is True, the save file name will be lib_name.file. For example, if fetch obja.pgm and objb.srvpgm in objlib library, the save file name will be obja. If the obja already exists in objlib, then rename the save file name to (obja+number), number range from 1 to 9(obja1, obja2...obja9).


  flat (optional, bool, False)
    Allows you to override the default behavior of appending hostname/path/to/file to the destination.

    This can be useful if working with a single host, or if retrieving files that are uniquely named per host.

    If using multiple hosts with the same filename, the file will be overwritten for each host.


  is_lib (optional, bool, False)
    If it is a library needed to be fetched. If set True, the whole library will be fetched.


  format (optional, str, *SAVF)
    The save file's format. Only support *SAVF by now.


  dest (True, str, None)
    A local directory to save the file into.

    For example, if the dest directory is /backup save file named /qsys.lib/objlib.lib/test1.file on host host.example.com, would be saved into /backup/host.example.com/qsys.lib/objlib.lib/test1.file. The host name is based on the inventory name. If dest='', dest will be current directory.


  target_release (optional, str, *CURRENT)
    The release of the operating system on which you intend to restore and use the SAVF.


  force_save (optional, bool, False)
    If force to use savefile_name when savefile_name.file already exists on remote IBM i.


  validate_checksum (optional, bool, True)
    Verify that the source and destination checksums match after the files are fetched.


  object_names (optional, str, *ALL)
    The objects need to be fetched. One or more object names can be specified. Use space as separator.

    If object type is *FILE, then fetch it directly. Only one *FILE object will fetch directly at one time.


  lib_name (True, str, None)
    The library contains the objects. If is_lib is Ture, lib_name means the library name.


  backup (optional, bool, False)
    If delete the save file on remote IBM i or not. If set True, the save file on remote IBM i will not be deleted.


  object_types (optional, str, *ALL)
    The object types. One or more object types can be specified. Use space as separator.





Notes
-----

.. note::
   - ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3(or python2) under [defaults] section
   - Need install 5770SS1 option 39 on remote IBM i for regex usage


See Also
--------

.. seealso::

   :ref:`fetch_module`
      The official documentation on the **fetch** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Fetch obja.pgm and objb.srvpgm in objlib libary as test1.savf(target release V7R2M0) on a remote IBMi to local. Store
            as /backup/host.example.com/qsys.lib/objlib.lib/test1.file and keep the save file on remote
      ibmi_fetch:
        object_names: 'obj1 obj2'
        lib_name: 'objlib'
        object_types: '*PGM *SRVPGM'
        savefile_name: 'test1'
        dest: '/backup'
        backup: true
        target_release: 'V7R2M0'
    - name: Fetch objlib libary on a remote IBMi to local, store as /backup/objlib.file.
      ibmi_fetch:
        lib_name: 'objlib'
        dest: '/backup'
        flat: true



Return Values
-------------

  file (always, str, /qsys.lib/test.lib/obja.file)
    The save file path on remote IBM i.


  remote_md5sum (always, str, ef67xhfs8638ac5d7e31fc56rfcv3760)
    The md5sum of the file on remote IBM i.


  stdout (always, list, File OBJA in library TESTLIB already exists. If still need save, please set force.)
    The fetch standard output


  dest (always, str, /users/tester/test/obja.file)
    The file path on local.


  checksum (always, str, 573f3e66ee97071134c9001732ed16f6bb7e8ab4)
    The checksum of the file on local.


  md5sum (always, str, ef67xhfs8638ac5d7e31fc56rfcv3760)
    The md5sum of the file on local.


  stderr (always, list, ['CPF5813: File OBJA in library TESTLIB already exists.', 'CPF7302: File OBJA not created in library TESTLIB.'])
    The fetch standard error


  delta (always, str, 0:00:00.307534)
    The fetch execution delta time when file is renewed.


  msg (always, str, File is renewed on local.)
    The fetch execution message.


  remote_checksum (always, bool, 573f3e66ee97071134c9001732ed16f6bb7e8ab4)
    The checksum of the file on remote IBM i.





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Peng Zeng Yu (@pengzengyufish)

