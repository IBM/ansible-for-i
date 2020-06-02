..
.. SPDX-License-Identifier: Apache-2.0
..

:github_url: https://github.com/LiJunBJZhu/i_collection_core/tree/master/plugins/modules/ibmi_object_authority.py


ibmi_object_authority -- Grant, Revoke or Display Object Authority
==================================================================

.. contents::
   :local:
   :depth: 1


Synopsis
--------

The ``ibmi_object_authority`` module can do the named object(s) authority management(grant, revoke and display).






Parameters
----------

  asp_device (optional, str, *)
    Specifies the auxiliary storage pool (ASP) device name where the library that contains the object (OBJ parameter) is located.

    The ASP group name is the name of the primary ASP device within the ASP group.

    Valid for all the operations, but operations display will igonre this option.


  ref_object_type (optional, str, *OBJTYPE)
    Specify the reference object type of the object for which specific authorities are to be granted, revoked or displayed to the specified users.

    Supported reference object type refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm

    Valid only for operation grant_ref


  ref_object_library (optional, str, *LIBL)
    Specify the name of the library to be searched.

    Valid only for operation grant_ref


  object_type (True, str, None)
    Specify the object type of the object for which specific authorities are to be granted, revoked or displayed to the specified users.

    Supported object type refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm

    Valid for all the operations


  authority (optional, list, [u'*CHANGE'])
    Specifies the authority to be granted or revoked to the users specified for the Users (USER) parameter.

    Valid only for operations grant and revoke


  object_library (optional, str, *LIBL)
    Specify the name of the library to be searched.

    Valid for all the operations

    When operation is display, special value as '*LIBL', '*CURLIB', '*ALL', '*ALLUSR', '*USRLIBL', '*ALLAVL', '*ALLUSRAVL' are not supported.

    The special values and value '' will be treate as search all the ASP scope under the current thread.


  ref_object_name (optional, str, )
    Specify the name of the reference object for which specific authority is to be granted, revoked or displayed to one or more users.

    Valid only for operation grant_ref, you must specify a value other than ''


  object_name (True, str, None)
    Specify the name of the object for which specific authority is to be granted, revoked or displayed to one or more users.

    Valid for all the operations


  replace_authority (optional, bool, False)
    Specifies whether the authorities replace the user's current authorities.

    Valid only for operations grant


  user (optional, list, [u''])
    Specifies one or more users to whom authority for the named object is to be granted or revoked.

    Valid only for operations grant and revoke


  authorization_list (optional, str, )
    Specifies the authorization list that is to grant or revok on the object, only vaild for operation grant_autl or revoke_autl

    Valid only for operations grant_autl and revoke_autl, you must specify a value other than ''


  operation (True, str, None)
    The authority operation.

    Valid for all the operations

    Operation grant is to grant user(s) authority(s) to object(s)

    Operation revoke is to revoke user(s) authority(s) from object(s)

    Operation display is to display object(s)'s authority information

    Operation grant_autl is to grant a authorization list(the authorization list object contains the list of authority) to object(s)

    Operation revoke_autl is to revoke authorization list from object(s)

    Operation grant_ref is to grant the reference object to be queried to obtain authorization information

    for more information about reference object, refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm


  ref_asp_device (optional, str, *)
    Specifies the auxiliary storage pool (ASP) device name where the library that contains the reference object is located.

    The ASP group name is the name of the primary ASP device within the ASP group.

    Valid only for operation grant_ref


  asp_group (optional, str, )
    Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.

    The ASP group name is the name of the primary ASP device within the ASP group.

    The different for asp_group and (ref_)asp_device are,

    the asp_group make the current ansible thread run under the asp_group.

    the (ref_)asp_device is the search scope for the object.

    If you want to searh the (ref_)object in an ASP, the asp_group must be set and varied on,

    (ref)asp_device can be set as '*' for searching in the ASP and also the system ASP or asp_group name to just search in this ASP.

    Valid for all the operations





Notes
-----

.. note::
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)


See Also
--------

.. seealso::

   :ref:`ibmi_object_find_module`
      The official documentation on the **ibmi_object_find** module.


Examples
--------

.. code-block:: yaml+jinja

    
    - name: Grant 1 user 1 authority on object
      ibmi_object_authority:
        operation: grant
        object_name: testobj
        object_library: testlib
        object_type: '*DTAARA'
        user: testuser
        authority: '*ALL'

    - name: Revoke 1 user's 2 authorities on object
      ibmi_object_authority:
        operation: 'revoke'
        object_name: 'ANSIBLE'
        object_library: 'CHANGLE'
        user:
          - 'CHANGLE'
        authority:
          - '*READ'
          - '*DLT'

    - name: Display the authority
      ibmi_object_authority:
        operation: display
        object_name: testobj
        object_library: testlib
        object_type: '*DTAARA'

    - name: Grant the reference object authority
      ibmi_object_authority:
        operation: grant_ref
        object_name: testobj
        object_library: testlib
        object_type: '*DTAARA'
        ref_object: testrefobj
        ref_object_library: testreflib
        ref_object_type: '*DTAARA'

    - name: Revoke the authority list on object
      ibmi_object_authority:
        operation: revoke_autl
        object_name: testobj
        object_library: testlib
        object_type: '*DTAARA'
        authorization_list: 'MYAUTL'

    - name: grant user 2 authority on an iasp
      ibmi_object_authority:
        operation: 'grant'
        object_name: 'iasp1'
        object_library: 'CHANGLE2'
        object_type: '*DTAARA'
        asp_group: 'IASP1'
        user:
          - 'CHANGLE'
        authority:
          - '*READ'
          - '*DLT'



Return Values
-------------

  stderr_lines (when rc as no-zero(failure), list, ['CPF2209: Library CHANGL not found'])
    The command standard error split in lines


  object_authority_list (When rc as 0(success) and operation is display, list, [{'OBJECT_TYPE': '*DTAARA', 'DATA_READ': 'YES', 'DATA_UPDATE': 'YES', 'SYSTEM_OBJECT_SCHEMA': 'CHANGLE', 'DATA_ADD': 'YES', 'DATA_DELETE': 'YES', 'OBJECT_EXISTENCE': 'NO', 'SQL_OBJECT_TYPE': '', 'AUTHORIZATION_LIST': '', 'OBJECT_AUTHORITY': '*CHANGE', 'AUTHORIZATION_NAME': '*PUBLIC', 'TEXT_DESCRIPTION': '', 'OBJECT_ALTER': 'NO', 'OBJECT_OPERATIONAL': 'YES', 'OBJECT_MANAGEMENT': 'NO', 'OBJECT_NAME': 'ANSIBLE', 'DATA_EXECUTE': 'YES', 'OBJECT_REFERENCE': 'NO', 'OWNER': 'CHANGLE', 'SYSTEM_OBJECT_NAME': 'ANSIBLE', 'OBJECT_SCHEMA': 'CHANGLE'}])
    The result set of object authority list


  stderr (when rc as no-zero(failure), str, CPF2209: Library CHANGL not found)
    The standard error


  stdout (when rc as 0(success) and the operation is not display, str, CPI2204: Authority given to 1 objects. Not given to 0 objects. Partially given to 0 objects.)
    The standard output


  stdout_lines (when rc as 0(success) and the operation is not display, list, ['CPI2204: Authority given to 1 objects. Not given to 0 objects. Partially given to 0 objects.', 'CPC2201: Object authority granted.'])
    The command standard output split in lines


  rc (always, int, 255)
    The return code (0 means success, non-zero means failure)





Status
------




- This  is not guaranteed to have a backwards compatible interface. *[preview]*


- This  is maintained by community.



Authors
~~~~~~~

- Chang Le(@changlexc)

