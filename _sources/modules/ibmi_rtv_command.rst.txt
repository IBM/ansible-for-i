
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_rtv_command.py

.. _ibmi_rtv_command_module:


ibmi_rtv_command -- Executes a command which is valid only within a CL program or REXX procedure
================================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_rtv_command`` module executes command which used in a CL program or REXX procedure.
- Usually, this kind of commands can not run directly from the 5250 console, like RTVJOBA, RTVNETA.





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


     
char_vars
  Specifies the name of the CL variable that receives character value. In the command's help, indicated as Character value.


  | **required**: false
  | **type**: list
  | **elements**: str


     
cmd
  The RTV command to run.


  | **required**: True
  | **type**: str


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).

  Ignored when the CL command with OUTPUT parameter, e.g. DSPLIBL, DSPHDWRSC.


  | **required**: false
  | **type**: bool


     
number_vars
  Specifies the name of the CL variable that receives digit value. In the command's help, indicated as Number.


  | **required**: false
  | **type**: list
  | **elements**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Call RTVJOBA to get job information
     ibmi_rtv_command:
       cmd: 'RTVJOBA'
       char_vars:
         - 'JOB'
         - 'USER'
       number_vars:
         - 'LOGSEV'
         - 'JOBMSGQMX'

   - name: Call RTVAUTLE to get information of the authority list
     ibmi_rtv_command:
       cmd: 'RTVAUTLE AUTL(PAYROLL) USER(TOM)'
       char_vars:
         - 'USE'
         - 'OBJOPR'
         - 'AUTLMGT'

   - name: Call RTVDTAARA to get content of a data area
     ibmi_rtv_command:
       cmd: 'RTVDTAARA DTAARA(QSYS/QAENGWTTM)'
       char_vars:
         - 'RTNVAR'




Notes
-----

.. note::
   The vars name and type for the rtv command must be correctly.

   F1 or F4 in 5250 console can help determine the vars name and type.

   Or check it with the command's url in Knowledge Center, e.g. RTVJOBA refers to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/rtvjoba.htm



See Also
--------

.. seealso::

   - :ref:`ibmi_cl_command_module`



Return Values
-------------


   
                              
       msg
        | The result message of the rtv command.
      
        | **returned**: always
        | **type**: str
        | **sample**: Error occurred when call RTVJOBA: {u'dftccsid': u'37', u'error1': u'CPF7CFD'}

            
      
      
                              
       rc
        | The command return code (0 means success, non-zero means failure).
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       output
        | The RTV command output.
      
        | **returned**: when rc as 0(success)
        | **type**: dict      
        | **sample**:

              .. code-block::

                       {"JOB": "QSQSRVR", "LOGSEV": "0", "USER": "QUSER"}
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
