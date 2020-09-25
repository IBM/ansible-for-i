
:github_url: https://github.com/IBM/ansible-for-i/tree/devel/plugins/modules/ibmi_user_and_group.py

.. _ibmi_user_and_group_module:


ibmi_user_and_group -- Create, change or display a user(or group) profile
=========================================================================



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The ``ibmi_user_and_group`` module can do the user(or group) profile management(create, change, delete and display).
- A user profile contain a user's passwords, the list of special authorities assigned to a user, and the objects the user owns.
- A group profile is a special type of user profile that provides the same authority to a group of users.
- You create group profiles in the same way that you create individual profiles.
- The system recognizes a group profile when you add the first member to it.
- At that point, the system sets information in the profile indicating that it is a group profile.





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


     
expire
  Specifies whether the password for this user is set to expired.

  If the password is set to expired, the user is required to change the password to sign on the system.

  If not specify, ``*NO`` will be used for operation create, ``*SAME`` will be used for operation change.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME
  | **choices**: \*NO, \*YES, \*SAME


     
joblog
  If set to ``true``, output the avaiable job log even the rc is 0(success).


  | **required**: false
  | **type**: bool


     
operation
  The user or group profile operation.

  Operation create to create user(group) profile.

  Operation change to change user(group) profile.

  Operation display to display user(group) profile inforamtion.

  Operation display_group_menbers to display the members of a group profile.


  | **required**: True
  | **type**: str
  | **choices**: create, change, delete, display, display_group_members


     
owner
  Specifies the user that is to be the owner of objects created by this user.

  If not specify, ``*USRPRF`` will be used for operation create, ``*SAME`` will be used for operation change.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME
  | **choices**: \*USRPRF, \*GRPPRF, \*SAME


     
parameters
  The parameters that CRTUSRPRF or CHGUSRPRF or DLTUSRPRF command will take.

  Other than options above, all other parameters need to be specified here.

  The default values of parameters for CRTUSRPRF or CHGUSRPRF or DLTUSRPRF will be taken if not specified.

  Supported parameters contain ASTLVL, CURLIB, INLPGM, INLMNU, LMTCPB, TEXT, SPCENV, DSPSGNINF, PWDEXPITV, PWDCHGBLK, LCLPWDMGT, LMTDEVSSN, KBDBUF, MAXSTGLRG, MAXSTG, PTYLMT, GRPAUT, GRPAUTTYP, SUPGRPPRF, ACGCDE, DOCPWD, MSGQ, DLVRY, SEV, PRTDEV, OUTQ, ATNPGM, SRTSEQ, LANGID, CNTRYID, CCSID, CHRIDCTL, SETJOBATR, LOCALE, USROPT, UID, GID, HOMEDIR, EIMASSOC, USREXPDATE, USREXPITV, AUT, JOBD when the operation is create or change Or OWNOBJOPT, PGPOPT, EIMASSOC when the operation is delete.

  Refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/crtusrprf.htm. and https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/dltusrprf.htm for detail.


  | **required**: false
  | **type**: str
  | **default**:  


     
password
  Specifies the password that allows the user to sign on the system.

  If not specify, operation create will use the user name as the password, operation change will not change the password.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME


     
special_authority
  Specifies the special authorities given to a user.

  If not specify, ``*USRCLS`` will be used for operation create, ``*SAME`` will be used for operation change.

  Valid only for operation create and change.


  | **required**: false
  | **type**: list
  | **elements**: str
  | **default**: ['\*SAME']
  | **choices**: \*USRCLS, \*NONE, \*SAME, \*ALLOBJ, \*AUDIT, \*JOBCTL, \*SAVSYS, \*IOSYSCFG, \*SECADM, \*SERVICE, \*SPLCTL


     
status
  Specifies the status of the user profile.

  If not specify, ``*ENABLED`` will be used for operation create, ``*SAME`` will be used for operation change.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME
  | **choices**: \*ENABLED, \*DISABLED, \*SAME


     
text
  Specifies the text that briefly describes the user or group profile.

  If not specify, 'Create by Ansible' will be used for operation create, ``*SAME`` will be used for operation change.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME


     
user
  Specifies the user profile to be operated. A numeric user profile can be specified.

  If the user profile begins with a numeric, it must be prefixed with a Q.

  If you want to create, display, display group members of a group, this parameter is the group profile name.


  | **required**: True
  | **type**: str


     
user_class
  Specifies the type of user associated with this user profile, security officer, security administrator, programmer, system operator, or user.

  If not specify, ``*USER`` will be used for operation create, ``*SAME`` will be used for operation change.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME
  | **choices**: \*USER, \*SYSOPR, \*PGMR, \*SECADM, \*SECOFR, \*SAME


     
user_group
  Specifies the user's group profile name whose authority is used if no specific authority is given for the user.

  If not specify, operation create is to create an individual user, or else, the new created user will be a member of the group.

  If not specify, operation change does nothing on the user, or else, the new changed user will be added as a member of the group.

  Valid only for operation create and change.


  | **required**: false
  | **type**: str
  | **default**: \*SAME




Examples
--------

.. code-block:: yaml+jinja

   
   - name: create user profile
     ibmi_user_and_group:
       operation: 'create'
       user: 'changle'

   - name: create user profile with become user
     ibmi_user_and_group:
       operation: 'create'
       user: 'changle'
       become_user: 'USER1'
       become_user_password: 'yourpassword'

   - name: display user profile
     ibmi_user_and_group:
       operation: 'display'
       user: 'changle'

   - name: display group members
     ibmi_user_and_group:
       operation: 'display_group_members'
       user: 'group1'






See Also
--------

.. seealso::

   - :ref:`ibmi_cl_command_module`



Return Values
-------------


   
                              
       stdout
        | The standard output.
      
        | **returned**: when rc as 0(success) and the operation is not display or display_group_members
        | **type**: str
        | **sample**: CPC2205: User profile CHANGLE changed.

            
      
      
                              
       stderr
        | The standard error
      
        | **returned**: when rc as no-zero(failure)
        | **type**: str
        | **sample**: CPF22CF: User profile not allowed to be a group profile

            
      
      
                              
       rc
        | The return code (0 means success, non-zero means failure)
      
        | **returned**: always
        | **type**: int
        | **sample**: 255

            
      
      
                              
       stdout_lines
        | The command standard output split in lines.
      
        | **returned**: when rc as 0(success) and the operation is not display or display_group_members
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPC2205: User profile CHANGLE changed."]
            
      
      
                              
       stderr_lines
        | The command standard error split in lines.
      
        | **returned**: when rc as no-zero(failure)
        | **type**: list      
        | **sample**:

              .. code-block::

                       ["CPF2204: User profile CHANGL1 not found."]
            
      
      
                              
       result_set
        | The result set of user information or group members.
      
        | **returned**: When rc as 0(success) and operation is display or display_group_members
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"GROUP_PROFILE_NAME": "GROUP1", "USER_PROFILE_NAME": "USERG1", "USER_TEXT": ""}, {"GROUP_PROFILE_NAME": "GROUP1", "USER_PROFILE_NAME": "USER2G1", "USER_TEXT": ""}]
            
      
      
                              
       job_log
        | The IBM i job log of the task executed.
      
        | **returned**: always
        | **type**: list      
        | **sample**:

              .. code-block::

                       [{"FROM_INSTRUCTION": "318F", "FROM_LIBRARY": "QSYS", "FROM_MODULE": "", "FROM_PROCEDURE": "", "FROM_PROGRAM": "QWTCHGJB", "FROM_USER": "CHANGLE", "MESSAGE_FILE": "QCPFMSG", "MESSAGE_ID": "CPD0912", "MESSAGE_LIBRARY": "QSYS", "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.", "MESSAGE_SUBTYPE": "", "MESSAGE_TEXT": "Printer device PRT01 not found.", "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897", "MESSAGE_TYPE": "DIAGNOSTIC", "ORDINAL_POSITION": "5", "SEVERITY": "20", "TO_INSTRUCTION": "9369", "TO_LIBRARY": "QSYS", "TO_MODULE": "QSQSRVR", "TO_PROCEDURE": "QSQSRVR", "TO_PROGRAM": "QSQSRVR"}]
            
      
        
