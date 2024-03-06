
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_user_compliance_check.py

.. _ibmi_user_compliance_check_module:


ibmi_user_compliance_check -- Check if the value of a field of user profile is expected
=======================================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The \ :literal:`ibmi\_user\_compliance\_check`\  module can do the user profile compliance check.
- Check if the value of a field of user profile is matched with the value of customer input.
- User can input multi value for the multi-value fields. It includes field
- SPECIAL\_AUTHORITIES, USER\_ACTION\_AUDIT\_LEVEL, USER\_OPTIONS, SUPPLEMENTAL\_GROUP\_LIST, LOCALE\_JOB\_ATTRIBUTES.
- If some fields value do not match the user's expected value, the list of users will be returned





Parameters
----------


     
become_user
  The name of the user profile that the IBM i task will run under.

  Use this option to set a user with desired privileges to run the task.


  | **required**: false
  | **type**: str


     
become_user_password
  Use this option to set the password of the user specified in \ :literal:`become\_user`\ .


  | **required**: false
  | **type**: str


     
fields
  Specifies a set of fields which are checked.

  Customer need to input field name and expected value

  Following fields are all we support now

  SIGN\_ON\_ATTEMPTS\_NOT\_VALID

  STATUS

  NO\_PASSWORD\_INDICATOR

  PASSWORD\_LEVEL\_0\_1

  PASSWORD\_LEVEL\_2\_3

  PASSWORD\_EXPIRATION\_INTERVAL

  DAYS\_UNTIL\_PASSWORD\_EXPIRES

  SET\_PASSWORD\_TO\_EXPIRE

  USER\_CLASS\_NAME

  SPECIAL\_AUTHORITIES

  GROUP\_PROFILE\_NAME

  SUPPLEMENTAL\_GROUP\_COUNT

  SUPPLEMENTAL\_GROUP\_LIST

  OWNER

  GROUP\_AUTHORITY

  ASSISTANCE\_LEVEL

  CURRENT\_LIBRARY\_NAME

  INITIAL\_MENU\_NAME

  INITIAL\_MENU\_LIBRARY\_NAME

  INITIAL\_PROGRAM\_NAME

  INITIAL\_PROGRAM\_LIBRARY\_NAME

  LIMIT\_CAPABILITIES

  TEXT\_DESCRIPTION

  DISPLAY\_SIGNON\_INFORMATION

  LIMIT\_DEVICE\_SESSIONS

  KEYBOARD\_BUFFERING

  MAXIMUM\_ALLOWED\_STORAGE

  STORAGE\_USED

  HIGHEST\_SCHEDULING\_PRIORITY

  JOB\_DESCRIPTION\_NAME

  JOB\_DESCRIPTION\_LIBRARY\_NAME

  ACCOUNTING\_CODE

  MESSAGE\_QUEUE\_NAME

  MESSAGE\_QUEUE\_LIBRARY\_NAME

  MESSAGE\_QUEUE\_DELIVERY\_METHOD

  MESSAGE\_QUEUE\_SEVERITY

  OUTPUT\_QUEUE\_NAME

  OUTPUT\_QUEUE\_LIBRARY\_NAME

  PRINT\_DEVICE

  SPECIAL\_ENVIRONMENT

  ATTENTION\_KEY\_HANDLING\_PROGRAM\_NAME

  ATTENTION\_KEY\_HANDLING\_PROGRAM\_LIBRARY\_NAME

  LANGUAGE\_ID

  COUNTRY\_OR\_REGION\_ID

  CHARACTER\_CODE\_SET\_ID

  USER\_OPTIONS

  SORT\_SEQUENCE\_TABLE\_NAME

  SORT\_SEQUENCE\_TABLE\_LIBRARY\_NAME

  OBJECT\_AUDITING\_VALUE

  USER\_ACTION\_AUDIT\_LEVEL

  GROUP\_AUTHORITY\_TYPE

  USER\_ID\_NUMBER

  GROUP\_ID\_NUMBER

  LOCALE\_JOB\_ATTRIBUTES

  GROUP\_MEMBER\_INDICATOR

  DIGITAL\_CERTIFICATE\_INDICATOR

  CHARACTER\_IDENTIFIER\_CONTROL

  LOCAL\_PASSWORD\_MANAGEMENT

  BLOCK\_PASSWORD\_CHANGE

  USER\_ENTITLEMENT\_REQUIRED

  USER\_EXPIRATION\_INTERVAL

  USER\_EXPIRATION\_ACTION

  HOME\_DIRECTORY

  LOCALE\_PATH\_NAME

  USER\_DEFAULT\_PASSWORD

  USER\_OWNER

  USER\_CREATOR

  SIZE

  DAYS\_USED\_COUNT

  AUTHORITY\_COLLECTION\_ACTIVE

  AUTHORITY\_COLLECTION\_REPOSITORY\_EXISTS

  PASE\_SHELL\_PATH


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
     ibm.power_ibmi.ibmi_user_compliance_check:
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
            
      
        
