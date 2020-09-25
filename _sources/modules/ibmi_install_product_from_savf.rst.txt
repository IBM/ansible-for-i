
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_install_product_from_savf.py

.. _ibmi_install_product_from_savf_module:


ibmi_install_product_from_savf -- Install the licensed program(product) from a save file.
=========================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_install_product_from_savf`` module installs the product from a save file.





Parameters
----------


     
acceptance_cmd
  The Accept Software Agreement command records the acceptance of the software agreement for a product. It is assumed that the caller of this command has previously displayed and obtained acceptance for the terms of the agreement. This command cannot be used to accept the Licensed Internal Code or the IBM i ``*Base`` software agreements. If invalid command specificed, message CPDB6D5 with following reason will be received, 'Product cannot be installed in a batch request because the software agreement has not been previously accepted'. In general, a command or program should be implemented by QLPACAGR API, consult the product support if you don't know the command.


  | **required**: false
  | **type**: str
  | **default**:  


     
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
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
language
  Specifies which national language version (NLV) objects to be used for restoring the licensed program. It's the IBM-supplied language feature codes, like German is 2924, English is 2924.


  | **required**: false
  | **type**: str
  | **default**: \*PRIMARY


     
object_type
  Specifies the type of licensed program objects to be restored.


  | **required**: false
  | **type**: str
  | **default**: \*ALL
  | **choices**: \*ALL, \*PGM, \*LNG


     
option
  Specifies which one of the optional parts of the licensed program given in the Product prompt (LICPGM parameter) is to be restored.


  | **required**: false
  | **type**: str
  | **default**: \*BASE


     
parameters
  The parameters that RSTLICPGM command will take. Other than options above, all other parameters need to be specified here. The default values of parameters for RSTLICPGM will be taken if not specified.


  | **required**: false
  | **type**: str
  | **default**:  


     
product
  Specifies the seven-character identifier of the licensed program that is restored.


  | **required**: True
  | **type**: str


     
release
  Specifies the version, release, and modification level of the licensed program being restored.


  | **required**: false
  | **type**: str
  | **default**: \*FIRST


     
replace_release
  Specifies the version, release, and modification level of the licensed program being replaced.


  | **required**: false
  | **type**: str
  | **default**: \*ONLY


     
savf_library
  Specify the name of the library where the save file is located.


  | **required**: True
  | **type**: str


     
savf_name
  Specify the name of the save file.


  | **required**: True
  | **type**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Restoring Program with become user.
     ibmi_install_product_from_savf:
       product: 5770WDS
       savf_name: MYFILE
       savf_library: MYLIB
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: Restoring Program with acceptance command.
     ibmi_install_product_from_savf:
       product: 5733D10
       option: 11
       savf_name: MYFILE
       savf_library: MYLIB
       acceptance_cmd: "CALL PGM(QSYS/QLPACAGR) PARM('5733D10' '100001' '0011' X'00000010000000000000000000000000')"






See Also
--------

.. seealso::

   - :ref:`ibmi_uninstall_product, ibmi_save_product_to_savf_module`



Return Values
-------------


   
                              
       stdout
        | The standard output.
      
        | **returned**: When rc as 0(success)
        | **type**: str
        | **sample**: +++ success RSTLICPGM LICPGM(5733D10) DEV(\*SAVF) OPTION(\*BASE) RSTOBJ(\*ALL)

            
      
      
                              
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

                       ["+++ success RSTLICPGM LICPGM(5733D10) DEV(*SAVF) OPTION(*BASE) RSTOBJ(*ALL)"]
            
      
      
                              
       stderr_lines
        | The standard error split in lines.
      
        | **returned**: When rc as non-zero(failure).
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
            
      
        
