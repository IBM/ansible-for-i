
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_copy.py

.. _ibmi_copy_module:


ibmi_copy -- Copy a save file from local to a remote IBM i node
===============================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_copy`` copies a save file from local to a remote IBM i node.
- ``ibmi_copy`` will not restore save file on IBM i node.
- For non-IBMi native targets, use the copy module instead.





Parameters
----------


     
backup
  If set force ``true`` and save file already exists on remote, rename the exists remote save file so you can get the original file back.

  The backup save file name will be the original file name+number[1:9]. For example, the origial file name is obja, then rename the original file to obja1. If obja1 already exists, then rename the original file to obja2... util obja9, then report error.

  Only works when force is ``True``.


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

   
   - name: Copy test.file on local to a remote IBM i.
     ibmi_copy:
       src: '/backup/test.file'
       lib_name: 'testlib'
       force: True
       backup: True




Notes
-----

.. note::
   ansible.cfg needs to specify interpreter_python=/QOpenSys/pkgs/bin/python3 under[defaults] section



See Also
--------

.. seealso::

   - :ref:`copy_module`



Return Values
-------------


   
                              
       delta
        | The copy execution delta time when file is renewed.
      
        | **returned**: always
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The copy standard output.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       "File TEST in library TESTLIB already exists."
            
      
      
                              
       stderr
        | The copy standard error.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF5813: File TEST in library TESTLIB already exists.", "CPF7302: File TEST not created in library TESTLIB."]
            
      
      
                              
       src
        | Local absolute path to a save file to copy to the remote server.
      
        | **returned**: always
        | **type**: str
        | **sample**: /backup/test.file

            
      
      
                              
       msg
        | The fetch execution message.
      
        | **returned**: always
        | **type**: str
        | **sample**: File is successfully copied.

            
      
      
                              
       dest
        | Remote absolute path where the file is copied to.
      
        | **returned**: always
        | **type**: str
        | **sample**: /QSYS.LIB/TESTLIB.LIB/TEST.FILE

            
      
      
                              
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

                       [{"FROM_INSTRUCTION": "149", "FROM_LIBRARY": "QSHELL", "FROM_MODULE": "QZSHRUNC", "FROM_PROCEDURE": "main", "FROM_PROGRAM": "QZSHRUNC", "FROM_USER": "TESTER", "MESSAGE_FILE": "QZSHMSGF", "MESSAGE_ID": "QSH0005", "MESSAGE_LIBRARY": "QSHELL", "MESSAGE_SECOND_LEVEL_TEXT": "", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Command ended normally with exit status 0.", "MESSAGE_TIMESTAMP": "2020-05-25-13.06.35.019371", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": "12", "SEVERITY": "0", "TO_INSTRUCTION": "5829", "TO_LIBRARY": "QXMLSERV", "TO_MODULE": "PLUGILE", "TO_PROCEDURE": "ILECMDEXC", "TO_PROGRAM": "XMLSTOREDP"}]
            
      
        
