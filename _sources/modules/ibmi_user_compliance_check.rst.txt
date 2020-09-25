
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_user_compliance_check.py

.. _ibmi_user_compliance_check_module:


ibmi_user_compliance_check -- Check if the value of a field of user profile is expected
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_user_compliance_check`` module can do the user profile compliance check.
- Check if the value of a field of user profile is matched with the value of customer input.
- User can input multi value for the multi-value fields. It includes field
- SPECIAL_AUTHORITIES, USER_ACTION_AUDIT_LEVEL, USER_OPTIONS, SUPPLEMENTAL_GROUP_LIST, LOCALE_JOB_ATTRIBUTES.
- If some fields value do not match the user's expected value, the list of users will be returned





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


     
fields
  Specifies a set of fields which are checked.

  Customer need to input field name and expected value

  Following fields are all we support now

  SIGN_ON_ATTEMPTS_NOT_VALID

  STATUS

  NO_PASSWORD_INDICATOR

  PASSWORD_LEVEL_0_1

  PASSWORD_LEVEL_2_3

  PASSWORD_EXPIRATION_INTERVAL

  DAYS_UNTIL_PASSWORD_EXPIRES

  SET_PASSWORD_TO_EXPIRE

  USER_CLASS_NAME

  SPECIAL_AUTHORITIES

  GROUP_PROFILE_NAME

  SUPPLEMENTAL_GROUP_COUNT

  SUPPLEMENTAL_GROUP_LIST

  OWNER

  GROUP_AUTHORITY

  ASSISTANCE_LEVEL

  CURRENT_LIBRARY_NAME

  INITIAL_MENU_NAME

  INITIAL_MENU_LIBRARY_NAME

  INITIAL_PROGRAM_NAME

  INITIAL_PROGRAM_LIBRARY_NAME

  LIMIT_CAPABILITIES

  TEXT_DESCRIPTION

  DISPLAY_SIGNON_INFORMATION

  LIMIT_DEVICE_SESSIONS

  KEYBOARD_BUFFERING

  MAXIMUM_ALLOWED_STORAGE

  STORAGE_USED

  HIGHEST_SCHEDULING_PRIORITY

  JOB_DESCRIPTION_NAME

  JOB_DESCRIPTION_LIBRARY_NAME

  ACCOUNTING_CODE

  MESSAGE_QUEUE_NAME

  MESSAGE_QUEUE_LIBRARY_NAME

  MESSAGE_QUEUE_DELIVERY_METHOD

  MESSAGE_QUEUE_SEVERITY

  OUTPUT_QUEUE_NAME

  OUTPUT_QUEUE_LIBRARY_NAME

  PRINT_DEVICE

  SPECIAL_ENVIRONMENT

  ATTENTION_KEY_HANDLING_PROGRAM_NAME

  ATTENTION_KEY_HANDLING_PROGRAM_LIBRARY_NAME

  LANGUAGE_ID

  COUNTRY_OR_REGION_ID

  CHARACTER_CODE_SET_ID

  USER_OPTIONS

  SORT_SEQUENCE_TABLE_NAME

  SORT_SEQUENCE_TABLE_LIBRARY_NAME

  OBJECT_AUDITING_VALUE

  USER_ACTION_AUDIT_LEVEL

  GROUP_AUTHORITY_TYPE

  USER_ID_NUMBER

  GROUP_ID_NUMBER

  LOCALE_JOB_ATTRIBUTES

  GROUP_MEMBER_INDICATOR

  DIGITAL_CERTIFICATE_INDICATOR

  CHARACTER_IDENTIFIER_CONTROL

  LOCAL_PASSWORD_MANAGEMENT

  BLOCK_PASSWORD_CHANGE

  USER_ENTITLEMENT_REQUIRED

  USER_EXPIRATION_INTERVAL

  USER_EXPIRATION_ACTION

  HOME_DIRECTORY

  LOCALE_PATH_NAME

  USER_DEFAULT_PASSWORD

  USER_OWNER

  USER_CREATOR

  SIZE

  DAYS_USED_COUNT

  AUTHORITY_COLLECTION_ACTIVE

  AUTHORITY_COLLECTION_REPOSITORY_EXISTS

  PASE_SHELL_PATH


  | **required**: True
  | **type**: list
  | **elements**: dict


     
joblog
  The job log of the job executing the task will be returned even rc is zero if it is set to true.


  | **required**: false
  | **type**: bool


     
users
  Specifies a list of user names.


  | **required**: True
  | **type**: list
  | **elements**: str




Examples
--------

.. code-block:: yaml+jinja

   
   - name: Do user profile compliance check
     ibmi_user_compliance_check:
         users:
           - 'ibmiuser1'
           - 'ibmiuser2'
           - 'ibmiuser3'
         fields:
           - {'name':'status', 'expect':['*enabled']}
           - {'name':'NO_PASSWORD_INDICATOR', 'expect':['no']}
           - {'name':'SPECIAL_AUTHORITIES', 'expect': ['*JOBCTL','*SAVSYS']}










Return Values
-------------


   
                              
       stderr
        | The standard error
      
        | **returned**: when rc as no-zero(failure)
        | **type**: str
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: always
        | **type**: list
      
      
                              
       sql1
        | The sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: select \* from Persons

            
      
      
                              
       sql2
        | The sql statement executed by the task.
      
        | **returned**: always
        | **type**: str
        | **sample**: select \* from Persons

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       result_set
        | The result set of user information includes all fields specified by user.
      
        | **returned**: When rc as 0(success) and the value of field of user who is specified by users parameter does not match the user's expected value
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"AUTHORIZATION_NAME": "ZHOUYU", "NO_PASSWORD_INDICATOR": "NO", "SPECIAL_AUTHORITIES": "*JOBCTL    *SAVSYS    ", "STATUS": "*DISABLED"}]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "8964", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "QSQSRVR", "FROM_PROCEDURE": "QSQSRVR", "FROM_PROGRAM": "QSQSRVR", "FROM_USER": "ZHOUYU1", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPF9898", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "\u0026N Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": null, "MESSAGE_TEXT": "SERVER MODE CONNECTING JOB IS 236764/QSECOFR/QP0ZSPWP.", "MESSAGE_TIMESTAMP": "2020-08-21T18:19:37.135231", "MESSAGE_TYPE": "COMPLETION", "ORDINAL_POSITION": 9, "SEVERITY": 40, "TO_INSTRUCTION": "8964", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
