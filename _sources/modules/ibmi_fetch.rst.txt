
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fetch.py

.. _ibmi_fetch_module:


ibmi_fetch -- Fetch objects or a library from a remote IBM i node and store on local
====================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_feth`` is used for fetching objects or a library as a SAVF from remote IBM i node and storing them locally in a file tree, organized by hostname.
- Save file that already exists at dest will be overwritten if it is different than the new one.
- For non-IBMi native targets, use the fetch module instead.





Parameters
----------


     
backup
  If delete the save file on remote IBM i or not. If set True, the save file on remote IBM i will not be deleted.


  | **required**: false
  | **type**: bool


     
dest
  A local directory to save the file into.

  For example, if the dest directory is /backup save file named /qsys.lib/objlib.lib/test1.file on host host.example.com, would be saved into /backup/host.example.com/qsys.lib/objlib.lib/test1.file. The host name is based on the inventory name. If dest='', dest will be current directory.


  | **required**: True
  | **type**: str


     
flat
  Allows you to override the default behavior of appending hostname/path/to/file to the destination.

  This can be useful if working with a single host, or if retrieving files that are uniquely named per host.

  If using multiple hosts with the same filename, the file will be overwritten for each host.


  | **required**: false
  | **type**: bool


     
force_save
  If force to use savefile_name when savefile_name.file already exists on remote IBM i.


  | **required**: false
  | **type**: bool


     
format
  The save file's format. Only support ``*SAVF`` by now.


  | **required**: false
  | **type**: str
  | **default**: \*SAVF
  | **choices**: \*SAVF


     
is_lib
  If it is a library needed to be fetched. If set True, the whole library will be fetched.


  | **required**: false
  | **type**: bool


     
lib_name
  The library contains the objects. If is_lib is ``Ture``, lib_name means the library name.


  | **required**: True
  | **type**: str


     
object_names
  The objects need to be fetched.

  One or more object names can be specified. Use space as separator.

  If object type is ``*FILE``, then fetch it directly. Only one ``*FILE`` object will fetch directly at one time.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
object_types
  The object types.

  One or more object types can be specified. Use space as separator.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
savefile_name
  The save file name can be specified.

  If not specified savefile_name, the save file name will be the first object_name.file. If is_lib is True, the save file name will be lib_name.file. For example, if fetch obja.pgm and objb.srvpgm in objlib library, the save file name will be obja. If the obja already exists in objlib, then rename the save file name to (obja+number), number range from 1 to 9(obja1, obja2...obja9).


  | **required**: false
  | **type**: str


     
target_release
  The release of the operating system on which you intend to restore and use the SAVF.


  | **required**: false
  | **type**: str
  | **default**: \*CURRENT


     
validate_checksum
  Verify that the source and destination checksums match after the files are fetched.


  | **required**: false
  | **type**: bool
  | **default**: True




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Fetch obja.pgm and objb.srvpgm in objlib libary as test1.savf(target release V7R2M0) on a remote IBM i to local. Store
           as /backup/host.example.com/qsys.lib/objlib.lib/test1.file and keep the save file on remote.
     ibmi_fetch:
       object_names: 'obj1 obj2'
       lib_name: 'objlib'
       object_types: '*PGM *SRVPGM'
       savefile_name: 'test1'
       dest: '/backup'
       backup: True
       target_release: 'V7R2M0'

   - name: Fetch objlib libary on a remote IBM i to local, store as /backup/objlib.file.
     ibmi_fetch:
       lib_name: 'objlib'
       dest: '/backup'
       flat: True




Notes
-----

.. note::
   ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under[defaults] section

   Need install 5770SS1 option 39 on remote IBM i for regex usage



See Also
--------

.. seealso::

   - :ref:`fetch_module`



Return Values
-------------


   
                              
       delta
        | The fetch execution delta time when file is renewed.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The fetch standard output.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       "File OBJA in library TESTLIB already exists. If still need save, please set force."
            
      
      
                              
       stderr
        | The fetch standard error.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF5813: File OBJA in library TESTLIB already exists.", "CPF7302: File OBJA not created in library TESTLIB."]
            
      
      
                              
       file
        | The save file path on remote IBM i.
      
        | **returned**: always
        | **type**: str
        | **sample**: /qsys.lib/test.lib/obja.file

            
      
      
                              
       msg
        | The fetch execution message.
      
        | **returned**: always
        | **type**: str
        | **sample**: File is renewed on local.

            
      
      
                              
       md5sum
        | The md5sum of the file on local.
      
        | **returned**: always
        | **type**: str
        | **sample**: ef67xhfs8638ac5d7e31fc56rfcv3760

            
      
      
                              
       dest
        | The file path on local.
      
        | **returned**: always
        | **type**: str
        | **sample**: /users/tester/test/obja.file

            
      
      
                              
       remote_md5sum
        | The md5sum of the file on remote IBM i.
      
        | **returned**: always
        | **type**: str
        | **sample**: ef67xhfs8638ac5d7e31fc56rfcv3760

            
      
      
                              
       remote_checksum
        | The checksum of the file on remote IBM i.
      
        | **returned**: always
        | **type**: str
        | **sample**: 573f3e66ee97071134c9001732ed16f6bb7e8ab4

            
      
      
                              
       checksum
        | The checksum of the file on local.
      
        | **returned**: always
        | **type**: str
        | **sample**: 573f3e66ee97071134c9001732ed16f6bb7e8ab4

            
      
      
                              
       rc
        | The action return code. 0 means success.
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "025D", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QDDCDF", "FROM_USER": "TESTER", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPC7301", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "File QUMEC created in library TEST.", "MESSAGE_TIMESTAMP": "2020-06-02-14.29.52.770625", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": "10", "SEVERITY": "0", "TO_INSTRUCTION": "5829", "TO_LIBRARY": "QXMLSERV", "TO_MODULE": "PLUGILE", "TO_PROCEDURE": "ILECMDEXC", "TO_PROGRAM": "XMLSTOREDP"}]
            
      
        
