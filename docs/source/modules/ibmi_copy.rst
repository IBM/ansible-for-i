..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/IBM/ansible-for-i/tree/ansible_collection_beta/plugins/modules/ibmi_copy.py

.. _ibmi_copy_module:

ibmi_copy -- Copy a save file from local to a remote IBMi node
==============================================================


.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ibmi_copy copies a save file from local to a remote IBMi node.
- ibmi_copy will not restore save file on IBMi node.
- For non-IBMi native targets, use the copy module instead.



Parameters
----------


     
backup
  If set force true and save file already exists on remote, rename the exists remote save file so you can get the original file back.

  The backup save file name will be the original file name+number[1:9]. For example, the origial file name is obja, then rename the original file to obja1. If obja1 already exists, then rename the original file to obja2... util obja9, then report error.

  Only works when force is True.


  | **required**: false
  | **type**: bool


     
force
  Influence whether the remote save file must always be replaced.

  If ``yes``, the remote save file will be replaced.

  If ``no``, the save file will only be transferred if the destination does not exist.


  | **required**: false
  | **type**: bool


     
lib_name
  Remote library where the save file should be copied to.


  | **required**: True
  | **type**: str


     
src
  Local path to a save file to copy to the remote server.

  This can be absolute or relative.


  | **required**: True
  | **type**: str



Examples
--------

.. code-block:: yaml+jinja

   
   - name: Copy test.file on local to a remote IBMi.
     ibmi_copy:
       src: '/backup/test.file'
       lib_name: 'testlib'
       force: true
       backup: true



Notes
-----

.. note::
   ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3(or python2) under [defaults] section


See Also
--------

.. seealso::

   - :ref:`copy_module`


Return Values
-------------


   
                              
       src
        | Local absolute path to a save file to copy to the remote server.
      
        | **returned**: always
        | **type**: str
        | **sample**: /backup/test.file

            
      
      
                              
       stderr
        | The copy standard error
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF5813: File TEST in library TESTLIB already exists.", "CPF7302: File TEST not created in library TESTLIB."]
            
      
      
                              
       stdout
        | The copy standard output
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       "File TEST in library TESTLIB already exists."
            
      
      
                              
       dest
        | Remote absolute path where the file is copied to.
      
        | **returned**: always
        | **type**: str
        | **sample**: /QSYS.LIB/TESTLIB.LIB/TEST.FILE

            
      
      
                              
       delta
        | The copy execution delta time when file is renewed.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       msg
        | The fetch execution message.
      
        | **returned**: always
        | **type**: str
        | **sample**: File is successfully copied.

            
      
        
