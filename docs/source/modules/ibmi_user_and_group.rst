..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_user_and_group.py


ibmi_user_and_group -- Create, Change or Display a user(or group) profile
=========================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_user_and_group`` module can do the user(or group) profile management(create, change, delete and display).

A user profile contain a user's passwords, the list of special authorities assigned to a user, and the objects the user owns.

A group profile is a special type of user profile that provides the same authority to a group of users.

You create group profiles in the same way that you create individual profiles.

The system recognizes a group profile when you add the first member to it.

At that point, the system sets information in the profile indicating that it is a group profile.






Parameters
----------

  status (optional, str, *SAME)
    Specifies the status of the user profile.

    If not specify, '*ENABLED' will be used for operation create, '*SAME' will be used for operation change.

    Valid only for operation create and change.


  parameters (optional, str,  )
    The parameters that CRTUSRPRF or CHGUSRPRF or DLTUSRPRF command will take.

    Other than options above, all other parameters need to be specified here.

    The default values of parameters for CRTUSRPRF or CHGUSRPRF or DLTUSRPRF will be taken if not specified.

    Supported parameters contain

    ASTLVL, CURLIB, INLPGM, INLMNU, LMTCPB, TEXT, SPCENV, DSPSGNINF, PWDEXPITV, PWDCHGBLK, LCLPWDMGT, LMTDEVSSN, KBDBUF, MAXSTGLRG, MAXSTG, PTYLMT,

    GRPAUT, GRPAUTTYP, SUPGRPPRF, ACGCDE, DOCPWD, MSGQ, DLVRY, SEV, PRTDEV, OUTQ, ATNPGM, SRTSEQ, LANGID, CNTRYID, CCSID, CHRIDCTL, SETJOBATR,

    LOCALE, USROPT, UID, GID, HOMEDIR, EIMASSOC, USREXPDATE, USREXPITV, AUT, JOBD when the operation is create or change

    Or OWNOBJOPT, PGPOPT, EIMASSOC when the operation is delete.

    refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/crtusrprf.htm.

    and https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/dltusrprf.htm for detail.


  text (optional, str, *SAME)
    Specifies the text that briefly describes the user or group profile.

    If not specify, 'Create by Ansible' will be used for operation create, '*SAME' will be used for operation change.

    Valid only for operation create and change.


  special_authority (optional, list, [u'*SAME'])
    Specifies the special authorities given to a user.

    If not specify, '*USRCLS' will be used for operation create, '*SAME' will be used for operation change.

    Valid only for operation create and change.


  expire (optional, str, *SAME)
    Specifies whether the password for this user is set to expired.

    If the password is set to expired, the user is required to change the password to sign on the system.

    If not specify, '*NO' will be used for operation create, '*SAME' will be used for operation change.

    Valid only for operation create and change.


  user (True, str, None)
    Specifies the user profile to be operated. A numeric user profile can be specified.

    If the user profile begins with a numeric, it must be prefixed with a Q.

    If you want to create, display, display group members of a group, this parameter is the group profile name.


  user_group (optional, str, *SAME)
    Specifies the user's group profile name whose authority is used if no specific authority is given for the user.

    If not specify, operation create is to create an individual user, or else, the new created user will be a member of the group.

    If not specify, operation change does nothing on the user, or else, the new changed user will be added as a member of the group.

    Valid only for operation create and change.


  owner (optional, str, *SAME)
    Specifies the user that is to be the owner of objects created by this user.

    If not specify, '*USRPRF' will be used for operation create, '*SAME' will be used for operation change.

    Valid only for operation create and change.


  operation (True, str, None)
    The user or group profile operation.

    Operation create to create user(group) profile

    Operation change to change user(group) profile

    Operation display to display user(group) profile inforamtion

    Operation display_group_menbers to display the members of a group profile


  password (optional, str, *SAME)
    Specifies the password that allows the user to sign on the system.

    If not specify, operation create will use the user name as the password, operation change will not change the password.

    Valid only for operation create and change.


  user_class (optional, str, *SAME)
    Specifies the type of user associated with this user profile, security officer, security administrator, programmer, system operator, or user.

    If not specify, '*USER' will be used for operation create, '*SAME' will be used for operation change.

    Valid only for operation create and change.





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`ibmi_cl_command_module`
      The official documentation on the **ibmi_cl_command** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: create user profile
      ibmi_user_and_group:
        operation: 'create'
        user: 'changle'

    - name: display user profile
      ibmi_user_and_group:
        operation: 'display'
        user: 'changle'

    - name: display group members
      ibmi_user_and_group:
        operation: 'display_group_members'
        user: 'group1'



Return Values
-------------

  stderr_lines (when rc as no-zero(failure), list, ['CPF2204: User profile CHANGL1 not found.'])
    The command standard error split in lines


  stderr (when rc as no-zero(failure), str, CPF22CF: User profile not allowed to be a group profile)
    The standard error


  stdout (when rc as 0(success) and the operation is not display or display_group_members, str, CPC2205: User profile CHANGLE changed.)
    The standard output


  stdout_lines (when rc as 0(success) and the operation is not display or display_group_members, list, ['CPC2205: User profile CHANGLE changed.'])
    The command standard output split in lines


  rc (always, int, 255)
    The return code (0 means success, non-zero means failure)


  result_set (When rc as 0(success) and operation is display or display_group_members, list, [{'USER_TEXT': '', 'GROUP_PROFILE_NAME': 'GROUP1', 'USER_PROFILE_NAME': 'USERG1'}, {'USER_TEXT': '', 'GROUP_PROFILE_NAME': 'GROUP1', 'USER_PROFILE_NAME': 'USER2G1'}])
    The result set of user information or group members





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le(@changlexc)

