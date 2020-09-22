
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_uninstall_product.py

.. _ibmi_uninstall_product_module:


ibmi_uninstall_product -- Delete the objects that make up the licensed program(product)
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- the ``ibmi_uninstall_product`` module deletes the objects that make up the product.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in ``become_user``.


  | **required**: false
  | **type**: str


     
joblog
  If set to ``true``, output the avaiable JOBLOG even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
language
  Specifies which national language version (NLV) objects are deleted for the licensed program specified on the LICPGM parameter.

  It's the IBM-supplied language feature codes, like German is 2924, English is 2924.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
option
  Specifies which of the parts of the licensed program specified on the Product prompt (LICPGM parameter) are deleted.


  | **required**: false
  | **type**: str
  | **default**: \*ALL


     
product
  Specifies the seven-character identifier of the licensed program that is deleted.


  | **required**: True
  | **type**: str


     
release
  Specifies which version, release, and modification level of the licensed program is deleted.


  | **required**: false
  | **type**: str
  | **default**: \*ONLY




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Deleting all Licensed Program Objects, run as USER1.
     ibmi_uninstall_product:
       product: 5770QU1
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: Deleting only the German (NLV 2929) objects for all options of the licensed program 5770QU1.
     ibmi_uninstall_product:
       product: 5770QU1
       language: 2929






See Also
--------

.. seealso::

   - :ref:`ibmi_install_product_from_savf, ibmi_save_product_to_savf_module`



Return Values
-------------


   
                              
       stdout
        | The standard output.
      
        | **returned**: always
        | **type**: str
        | **sample**: Product 5733D10 option 11 release \*ONLY language \*ALL deleted.

            
      
      
                              
       stderr
        | The standard error
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: Product 5733D10 option \*ALL release \*ONLY language \*ALL not installed

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Product 5733D10 option 11 release *ONLY language *ALL deleted."]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["Product 5733D10 option *ALL release *ONLY language *ALL not installed"]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
