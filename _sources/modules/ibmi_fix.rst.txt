
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_fix.py

.. _ibmi_fix_module:


ibmi_fix -- Install, remove or query an individual fix or a set of fixes on to IBM i system.
============================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The :literal:`ibmi\_fix` module install fixes to target IBM i system.
- The installation file of the fixes should be in the format of save file.
- The fixes are normally known as PTFs for IBM i users.





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in :literal:`become\_user`.


  | **required**: false
  | **type**: str


     
delayed_option
  Controls whether the PTF is delayed apply or not


  | **required**: false
  | **type**: str
  | **default**: \*NO
  | **choices**: \*YES, \*NO, \*IMMDLY


     
fix_list
  PTF list that will be applied to the IBM i system.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['\*ALL']


     
fix_omit_list
  The list of PTFs that will be omitted.

  The key of the dict should be the product ID of the fix that is omitted.


  | **required**: False
  | **type**: list
  | **elements**: str


     
joblog
  The job log of the job executing the task will be returned even rc is zero if it is set to true.


  | **required**: false
  | **type**: bool


     
operation
  The operation for the fix, the options are as follows

  load\_and\_apply will load the PTF and apply the PTF

  apply\_only will only apply the PTF

  load\_only will only load the PTF by LODPTF

  remove will remove the PTF

  query will return the specific PTF status


  | **required**: false
  | **type**: str
  | **default**: load_and_apply
  | **choices**: load_and_apply, apply_only, load_only, remove, query


     
product_id
  Product identifier to which PTFs are applied.


  | **required**: false
  | **type**: str


     
save_file_lib
  The library name of the save file to be installed.


  | **required**: false
  | **type**: str
  | **default**: QGPL


     
save_file_object
  The object name of the save file to be installed.


  | **required**: false
  | **type**: str


     
temp_or_perm
  Controls whether the PTF will be permanent applied or temporary applied.


  | **required**: false
  | **type**: str
  | **default**: \*TEMP
  | **choices**: \*TEMP, \*PERM




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Remove a single PTF
     ibm.power_ibmi.ibmi_fix:
       product_id: '5770DBM'
       delayed_option: "*NO"
       temp_or_perm: "*PERM"
       operation: 'remove'
       fix_list:
         - "SI72223"
       become_user: "QSECOFR"
       become_user_password: "yourpassword"
   - name: Install a single PTF
     ibm.power_ibmi.ibmi_fix:
       product_id: '5770DBM'
       save_file_object: 'QSI72223'
       save_file_lib: 'QGPL'
       delayed_option: "*NO"
       temp_or_perm: "*TEMP"
       operation: 'load_and_apply'
       fix_list:
         - "SI72223"
       become_user: "QSECOFR"
       become_user_password: "yourpassword"
   - name: query ptf
     ibm.power_ibmi.ibmi_fix:
       operation: 'query'
       fix_list:
         - "SI72223"
         - "SI70819"




Notes
-----

.. note::
   Ansible hosts file need to specify ansible\_python\_interpreter=/QOpenSys/pkgs/bin/python3(or python2)



See Also
--------

.. seealso::

   - :ref:`ibmi_fix_imgclg_module`


  

Return Values
-------------


   
                              
       start
        | The task execution start time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 2019-12-02 11:07:53.757435

            
      
      
                              
       end
        | The task execution end time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 2019-12-02 11:07:54.064969

            
      
      
                              
       delta
        | The task execution delta time
      
        | **returned**: When rc is zero
        | **type**: str
        | **sample**: 0:00:00.307534

            
      
      
                              
       stdout
        | The task standard output
      
        | **returned**: When error occurs.
        | **type**: str
        | **sample**: CPC2102: Library TESTLIB created

            
      
      
                              
       stderr
        | The task standard error
      
        | **returned**: When error occurs.
        | **type**: str
        | **sample**: CPF2111:Library TESTLIB already exists

            
      
      
                              
       rc
        | The task return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       job_log
        | The job log of the job executes the task.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
      
                              
       stdout_lines
        | The task standard output split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2102: Library TESTLIB created."]
            
      
      
                              
       stderr_lines
        | The task standard error split in lines
      
        | **returned**: When error occurs.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2111:Library TESTLIB already exists."]
            
      
      
                              
       ptf_not_on_system_list
        | The PTF list contains the ones that are not on the system.
      
        | **returned**: When use option query.
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["MF98212"]
            
      
      
                              
       ptf_list
        | The PTF list returned by the query option.
      
        | **returned**: When use option query.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"PTF_ACTION_PENDING": "NO", "PTF_ACTION_REQUIRED": "NONE", "PTF_CREATION_TIMESTAMP": null, "PTF_IDENTIFIER": "SI70819", "PTF_IPL_ACTION": "NONE", "PTF_IPL_REQUIRED": "UNKNOWN", "PTF_LOADED_STATUS": "SUPERSEDED", "PTF_PRODUCT_ID": "5733SC1", "PTF_SAVE_FILE": "NO", "PTF_STATUS_TIMESTAMP": "2020-09-01T01:15:42", "PTF_TEMPORARY_APPLY_TIMESTAMP": null}, {"PTF_ACTION_PENDING": "NO", "PTF_ACTION_REQUIRED": "NONE", "PTF_CREATION_TIMESTAMP": null, "PTF_IDENTIFIER": "SI72223", "PTF_IPL_ACTION": "NONE", "PTF_IPL_REQUIRED": "UNKNOWN", "PTF_LOADED_STATUS": "SUPERSEDED", "PTF_PRODUCT_ID": "5770DBM", "PTF_SAVE_FILE": "NO", "PTF_STATUS_TIMESTAMP": "2020-09-01T23:01:04", "PTF_TEMPORARY_APPLY_TIMESTAMP": null}]
            
      
      
                              
       requisite_ptf_list
        | The PTF list contains the requiste PTF of the PTF being applied.
      
        | **returned**: When use option apply_only.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"ptf_id": "SI76012", "requisite": "SI76014"}, {"ptf_id": "SI76012", "requisite": "SI76013"}]
            
      
      
                              
       load_fail_dict
        | The PTF list contains the PTFs which failed to be loaded and the reason. When PTF list which should be loaded is \*ALL, the result is empty.
      
        | **returned**: When use option apply_only or load_and_apply.
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"SI73543": "OPTION_NOT_INSTALLED"}]
            
      
        
