
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_save_product_to_savf.py

.. _ibmi_save_product_to_savf_module:


ibmi_save_product_to_savf -- Save the the licensed program(product) to a save file
==================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- the ``ibmi_save_product_to_savf`` module saves the product to a save file.





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


     
check_signature
  Specifies if the digital signatures of objects being saved with the licensed program are to be checked.


  | **required**: false
  | **type**: str
  | **default**: \*SIGNED
  | **choices**: \*SIGNED, \*ALL, \*NONE


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
language
  Specifies which national language version (NLV) is used for the save operation.

  It's the IBM-supplied language feature codes, like German is 2924, English is 2924.

  This parameter is ignored when object_type ``*PGM`` is specified.


  | **required**: false
  | **type**: str
  | **default**: \*PRIMARY


     
object_type
  Specifies the type of licensed program objects being saved.


  | **required**: false
  | **type**: str
  | **default**: \*ALL
  | **choices**: \*ALL, \*PGM, \*LNG


     
option
  Specifies the optional parts of the licensed program given in the Product prompt (LICPGM parameter) that are saved.


  | **required**: false
  | **type**: str
  | **default**: \*BASE


     
parameters
  The parameters that SAVLICPGM command will take. Other than options above, all other parameters need to be specified here.

  The default values of parameters for SAVLICPGM will be taken if not specified.

  Parameter CLEAR in SAVLICPGM command should not be specified here, ``CLEAR(*ALL``) already used.


  | **required**: false
  | **type**: str
  | **default**:  


     
product
  Specifies the seven-character identifier of the licensed program that is saved.


  | **required**: True
  | **type**: str


     
release
  Specifies which version, release, and modification level of the licensed program is saved.


  | **required**: false
  | **type**: str
  | **default**: \*ONLY


     
savf_library
  Specify the name of the library where the save file is located, if it is not existed, will create it.


  | **required**: True
  | **type**: str


     
savf_name
  Specify the name of the save file, if it is not existed, will create it.


  | **required**: True
  | **type**: str


     
target_release
  Specifies the release level of the operating system on which you intend to restore and use the product.


  | **required**: false
  | **type**: str
  | **default**: \*CURRENT




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Saving Program using Defaults.
     ibmi_save_product_to_savf:
       product: 5770WDS
       savf_name: MYFILE
       savf_library: MYLIB

   - name: Saving Program 5733D10 option 11.
     ibmi_save_product_to_savf:
       product: 5733D10
       option: 11
       savf_name: MYFILE
       savf_library: MYLIB
       become_user: 'USER1'
       become_user_password: 'yourpassword'






See Also
--------

.. seealso::

   - :ref:`ibmi_uninstall_product, ibmi_install_product_from_savf_module`



Return Values
-------------


   
                              
       stdout
        | The standard output.
      
        | **returned**: When rc as 0(success)
        | **type**: str
        | **sample**: +++ success SAVLICPGM LICPGM(5733D10) DEV(\*SAVF) OPTION(\*BASE) RSTOBJ(\*ALL)

            
      
      
                              
       stderr
        | The standard error.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: str
        | **sample**: CPF9801: Object QNOTE in library L10010125P not found

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The standard output split in lines.
      
        | **returned**: When rc as 0(success)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["+++ success SAVLICPGM LICPGM(5733D10) DEV(*SAVF) OPTION(*BASE) RSTOBJ(*ALL)"]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: When rc as non-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF9801: Object QNOTE in library L10010125P not found"]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
