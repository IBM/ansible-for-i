#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Chang Le <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_object_authority
short_description: Grant, revoke or display object authority
version_added: '2.8.0'
description:
  - The C(ibmi_object_authority) module can do the named object(s) authority management(grant, revoke and display).
options:
  operation:
    description:
      - The authority operation.
      - Valid for all the operations.
      - Operation grant is to grant user(s) authority(s) to object(s).
      - Operation revoke is to revoke user(s) authority(s) from object(s).
      - Operation display is to display object(s)'s authority information.
      - Operation grant_autl is to grant a authorization list(the authorization list object contains the list of authority) to object(s).
      - Operation revoke_autl is to revoke authorization list from object(s).
      - Operation grant_ref is to grant the reference object to be queried to obtain authorization information.
      - For more information about reference object, refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm
    choices: ['grant', 'revoke', 'display', 'grant_autl', 'revoke_autl', 'grant_ref']
    type: str
    required: yes
  object_name:
    description:
      - Specify the name of the object for which specific authority is to be granted, revoked or displayed to one or more users.
      - Valid for all the operations.
    type: str
    required: yes
  object_library:
    description:
      - Specify the name of the library to be searched.
      - Valid for all the operations.
      - When operation is display, special value as C(*LIBL), C(*CURLIB), C(*ALL), C(*ALLUSR), C(*USRLIBL), C(*ALLAVL), C(*ALLUSRAVL) are not supported.
    type: str
    default: '*LIBL'
  object_type:
    description:
      - Specify the object type of the object for which specific authorities are to be granted, revoked or displayed to the specified users.
      - Supported object type refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm
      - Valid for all the operations.
    type: str
    required: yes
    choices: ['*ALL', '*ALRTBL', '*BNDDIR', '*CFGL', '*CHTFMT', '*CLD', '*CLS',
        '*CMD', '*CNNL', '*COSD', '*CRG', '*CRQD', '*CSI', '*CSPMAP',
        '*CSPTBL', '*CTLD', '*DEVD', '*DTAARA', '*DTADCT', '*DTAQ', '*EDTD',
        '*FCT', '*FILE', '*FNTRSC', '*FNTTBL', '*FORMDF', '*FTR', '*GSS',
        '*IGCDCT', '*IGCSRT', '*IGCTBL', '*IMGCLG', '*IPXD', '*JOBD', '*JOBQ',
        '*JOBSCD', '*JRN', '*JRNRCV', '*LIB', '*LIND', '*LOCALE', '*M36',
        '*M36CFG', '*MEDDFN', '*MENU', '*MGTCOL', '*MODD', '*MODULE',
        '*MSGF', '*MSGQ', '*NODGRP', '*NODL', '*NTBD', '*NWID', '*NWSCFG',
        '*NWSD', '*OUTQ', '*OVL', '*PAGDFN', '*PAGSEG', '*PDFMAP', '*PDG',
        '*PGM', '*PNLGRP', '*PRDAVL', '*PRDDFN', '*PRDLOD', '*PSFCFG',
        '*QMFORM', '*QMQRY', '*QRYDFN', '*RCT', '*S36', '*SBSD',
        '*SCHIDX', '*SPADCT', '*SQLPKG', '*SQLUDT', '*SQLXSR', '*SRVPGM',
        '*SSND', '*SVRSTG', '*TBL', '*TIMZON', '*USRIDX', '*USRPRF',
        '*USRQ', '*USRSPC', '*VLDL', '*WSCST']
  asp_device:
    description:
      - Specifies the auxiliary storage pool (ASP) device name where the library that contains the object (OBJ parameter) is located.
      - The ASP group name is the name of the primary ASP device within the ASP group.
      - Valid for all the operations, but operations display will igonre this option.
    type: str
    default: '*'
  user:
    description:
      - Specifies one or more users to whom authority for the named object is to be granted or revoked.
      - Valid only for operations grant and revoke.
    type: list
    elements: str
    default: ['']
  authority:
    description:
      - Specifies the authority to be granted or revoked to the users specified for the Users (USER) parameter.
      - Valid only for operations grant and revoke.
    type: list
    elements: str
    default: ['*CHANGE']
    choices: ['*CHANGE', '*ALL', '*USE', '*EXCLUDE', '*AUTL',
        '*OBJALTER', '*OBJEXIST', '*OBJMGT', '*OBJOPR', '*OBJREF', '*ADD', '*DLT', '*READ', '*UPD', '*EXECUTE']
  replace_authority:
    description:
      - Specifies whether the authorities replace the user's current authorities.
      - Valid only for operations grant.
    type: bool
    default: false
  authorization_list:
    description:
      - Specifies the authorization list that is to grant or revok on the object, only vaild for operation grant_autl or revoke_autl.
      - Valid only for operations grant_autl and revoke_autl, you must specify a value other than C('').
    type: str
    default: ''
  ref_object_name:
    description:
      - Specify the name of the reference object for which specific authority is to be granted, revoked or displayed to one or more users.
      - Valid only for operation grant_ref, you must specify a value other than C('').
    type: str
    default: ''
  ref_object_library:
    description:
      - Specify the name of the library to be searched.
      - Valid only for operation grant_ref.
    type: str
    default: '*LIBL'
  ref_object_type:
    description:
      - Specify the reference object type of the object for which specific authorities are to be granted, revoked or displayed to the specified users.
      - Supported reference object type refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/cl/grtobjaut.htm
      - Valid only for operation grant_ref.
    type: str
    default: '*OBJTYPE'
    choices: ['*OBJTYPE', '*ALRTBL', '*AUTL', '*BNDDIR', '*CFGL', '*CHTFMT', '*CLD', '*CLS',
        '*CMD', '*CNNL', '*COSD', '*CRG', '*CRQD', '*CSI', '*CSPMAP',
        '*CSPTBL', '*CTLD', '*DEVD', '*DTAARA', '*DTADCT', '*DTAQ', '*EDTD',
        '*FCT', '*FILE', '*FNTRSC', '*FNTTBL', '*FORMDF', '*FTR', '*GSS',
        '*IGCDCT', '*IGCSRT', '*IGCTBL', '*IMGCLG', '*IPXD', '*JOBD', '*JOBQ',
        '*JOBSCD', '*JRN', '*JRNRCV', '*LIB', '*LIND', '*LOCALE', '*M36',
        '*M36CFG', '*MEDDFN', '*MENU', '*MGTCOL', '*MODD', '*MODULE',
        '*MSGF', '*MSGQ', '*NODGRP', '*NODL', '*NTBD', '*NWID', '*NWSCFG',
        '*NWSD', '*OUTQ', '*OVL', '*PAGDFN', '*PAGSEG', '*PDFMAP', '*PDG',
        '*PGM', '*PNLGRP', '*PRDDFN', '*PRDLOD', '*PSFCFG',
        '*QMFORM', '*QMQRY', '*QRYDFN', '*RCT', '*S36', '*SBSD',
        '*SCHIDX', '*SPADCT', '*SQLPKG', '*SQLUDT', '*SQLXSR', '*SRVPGM',
        '*SSND', '*SVRSTG', '*TBL', '*TIMZON', '*USRIDX', '*USRPRF',
        '*USRQ', '*USRSPC', '*VLDL', '*WSCST']
  ref_asp_device:
    description:
      - Specifies the auxiliary storage pool (ASP) device name where the library that contains the reference object is located.
      - The ASP group name is the name of the primary ASP device within the ASP group.
      - Valid only for operation grant_ref
    type: str
    default: '*'
  asp_group:
    description:
      - Specifies the name of the auxiliary storage pool (ASP) group to set for the current thread.
        The ASP group name is the name of the primary ASP device within the ASP group.
        The different for asp_group and asp_device or ref_asp_device are,
        the asp_group make the current ansible thread run under the asp_group.
        the asp_device or ref_asp_device is the search scope for the object.
        If you want to searh the object or ref_object in an ASP, the asp_group must be set and varied on,
        asp_device or ref_asp_device can be set as C(*) for searching in the ASP and also the system ASP or asp_group name to just search in this ASP.
      - Valid for all the operations
    type: str
    default: '*SYSBAS'
  joblog:
    description:
      - If set to C(true), output the avaiable job log even the rc is 0(success).
    type: bool
    default: False
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str

seealso:
- module: ibmi_object_find

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
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
'''

RETURN = r'''
stdout:
    description: The standard output
    returned: when rc as 0(success) and the operation is not display
    type: str
    sample: "CPI2204: Authority given to 1 objects. Not given to 0 objects. Partially given to 0 objects."
stderr:
    description: The standard error
    returned: when rc as no-zero(failure)
    type: str
    sample: 'CPF2209: Library CHANGL not found'
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The command standard output split in lines
    returned: when rc as 0(success) and the operation is not display
    type: list
    sample: [
        "CPI2204: Authority given to 1 objects. Not given to 0 objects. Partially given to 0 objects.",
        "CPC2201: Object authority granted."
    ]
stderr_lines:
    description: The command standard error split in lines
    returned: when rc as no-zero(failure)
    type: list
    sample: [
        "CPF2209: Library CHANGL not found"
    ]
object_authority_list:
    description: The result set of object authority list
    returned: When rc as 0(success) and operation is display
    type: list
    sample: [
        {
            "AUTHORIZATION_LIST": "",
            "AUTHORIZATION_NAME": "*PUBLIC",
            "DATA_ADD": "YES",
            "DATA_DELETE": "YES",
            "DATA_EXECUTE": "YES",
            "DATA_READ": "YES",
            "DATA_UPDATE": "YES",
            "OBJECT_ALTER": "NO",
            "OBJECT_AUTHORITY": "*CHANGE",
            "OBJECT_EXISTENCE": "NO",
            "OBJECT_MANAGEMENT": "NO",
            "OBJECT_NAME": "ANSIBLE",
            "OBJECT_OPERATIONAL": "YES",
            "OBJECT_REFERENCE": "NO",
            "OBJECT_SCHEMA": "CHANGLE",
            "OBJECT_TYPE": "*DTAARA",
            "OWNER": "CHANGLE",
            "SQL_OBJECT_TYPE": "",
            "SYSTEM_OBJECT_NAME": "ANSIBLE",
            "SYSTEM_OBJECT_SCHEMA": "CHANGLE",
            "TEXT_DESCRIPTION": ""
        }
    ]
job_log:
    description: The IBM i job log of the task executed.
    type: list
    sample: [{
            "FROM_INSTRUCTION": "318F",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "",
            "FROM_PROCEDURE": "",
            "FROM_PROGRAM": "QWTCHGJB",
            "FROM_USER": "CHANGLE",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPD0912",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Printer device PRT01 not found.",
            "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897",
            "MESSAGE_TYPE": "DIAGNOSTIC",
            "ORDINAL_POSITION": "5",
            "SEVERITY": "20",
            "TO_INSTRUCTION": "9369",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
        }]
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str',
                           choices=['grant', 'revoke', 'display',
                                    'grant_autl', 'revoke_autl', 'grant_ref'],
                           required=True),
            object_name=dict(type='str', required=True),
            object_library=dict(type='str', default='*LIBL'),
            object_type=dict(type='str',
                             choices=['*ALL', '*ALRTBL', '*BNDDIR', '*CFGL', '*CHTFMT', '*CLD', '*CLS',
                                      '*CMD', '*CNNL', '*COSD', '*CRG', '*CRQD', '*CSI', '*CSPMAP',
                                      '*CSPTBL', '*CTLD', '*DEVD', '*DTAARA', '*DTADCT', '*DTAQ', '*EDTD',
                                      '*FCT', '*FILE', '*FNTRSC', '*FNTTBL', '*FORMDF', '*FTR', '*GSS',
                                      '*IGCDCT', '*IGCSRT', '*IGCTBL', '*IMGCLG', '*IPXD', '*JOBD', '*JOBQ',
                                      '*JOBSCD', '*JRN', '*JRNRCV', '*LIB', '*LIND', '*LOCALE', '*M36',
                                      '*M36CFG', '*MEDDFN', '*MENU', '*MGTCOL', '*MODD', '*MODULE',
                                      '*MSGF', '*MSGQ', '*NODGRP', '*NODL', '*NTBD', '*NWID', '*NWSCFG',
                                      '*NWSD', '*OUTQ', '*OVL', '*PAGDFN', '*PAGSEG', '*PDFMAP', '*PDG',
                                      '*PGM', '*PNLGRP', '*PRDAVL', '*PRDDFN', '*PRDLOD', '*PSFCFG',
                                      '*QMFORM', '*QMQRY', '*QRYDFN', '*RCT', '*S36', '*SBSD',
                                      '*SCHIDX', '*SPADCT', '*SQLPKG', '*SQLUDT', '*SQLXSR', '*SRVPGM',
                                      '*SSND', '*SVRSTG', '*TBL', '*TIMZON', '*USRIDX', '*USRPRF',
                                      '*USRQ', '*USRSPC', '*VLDL', '*WSCST'],
                             required=True),
            asp_device=dict(type='str', default='*'),
            user=dict(type='list', default=[''], elements='str'),
            authority=dict(type='list',
                           default=['*CHANGE'],
                           choices=['*CHANGE', '*ALL', '*USE', '*EXCLUDE', '*AUTL',
                                    '*OBJALTER', '*OBJEXIST', '*OBJMGT', '*OBJOPR', '*OBJREF',
                                    '*ADD', '*DLT', '*READ', '*UPD', '*EXECUTE'],
                           elements='str'),
            replace_authority=dict(type='bool', default=False),
            authorization_list=dict(type='str', default=''),
            ref_object_name=dict(type='str', default=''),
            ref_object_library=dict(type='str', default='*LIBL'),
            ref_object_type=dict(type='str',
                                 choices=['*OBJTYPE', '*ALRTBL', '*AUTL', '*BNDDIR', '*CFGL', '*CHTFMT', '*CLD', '*CLS',
                                          '*CMD', '*CNNL', '*COSD', '*CRG', '*CRQD', '*CSI', '*CSPMAP',
                                          '*CSPTBL', '*CTLD', '*DEVD', '*DTAARA', '*DTADCT', '*DTAQ', '*EDTD',
                                          '*FCT', '*FILE', '*FNTRSC', '*FNTTBL', '*FORMDF', '*FTR', '*GSS',
                                          '*IGCDCT', '*IGCSRT', '*IGCTBL', '*IMGCLG', '*IPXD', '*JOBD', '*JOBQ',
                                          '*JOBSCD', '*JRN', '*JRNRCV', '*LIB', '*LIND', '*LOCALE', '*M36',
                                          '*M36CFG', '*MEDDFN', '*MENU', '*MGTCOL', '*MODD', '*MODULE',
                                          '*MSGF', '*MSGQ', '*NODGRP', '*NODL', '*NTBD', '*NWID', '*NWSCFG',
                                          '*NWSD', '*OUTQ', '*OVL', '*PAGDFN', '*PAGSEG', '*PDFMAP', '*PDG',
                                          '*PGM', '*PNLGRP', '*PRDDFN', '*PRDLOD', '*PSFCFG',
                                          '*QMFORM', '*QMQRY', '*QRYDFN', '*RCT', '*S36', '*SBSD',
                                          '*SCHIDX', '*SPADCT', '*SQLPKG', '*SQLUDT', '*SQLXSR', '*SRVPGM',
                                          '*SSND', '*SVRSTG', '*TBL', '*TIMZON', '*USRIDX', '*USRPRF',
                                          '*USRQ', '*USRSPC', '*VLDL', '*WSCST'],
                                 default='*OBJTYPE'),
            ref_asp_device=dict(type='str', default='*'),
            asp_group=dict(type='str', default='*SYSBAS'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        required_if=[
            ['operation', 'grant', ['object_name', 'user', 'authority']],
            ['operation', 'revoke', ['object_name', 'user', 'authority']],
            ['operation', 'display', ['object_name']],
            ['operation', 'grant_autl', ['object_name', 'authorization_list']],
            ['operation', 'revoke_autl', ['object_name', 'authorization_list']],
            ['operation', 'grant_ref', ['object_name', 'ref_object_name']]
        ],
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    operation = module.params['operation'].strip().upper()
    object_name = module.params['object_name'].strip().upper()
    if len(object_name) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of object_name exceeds 10 characters")
    object_library = module.params['object_library'].strip().upper()
    if len(object_library) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of object_library exceeds 10 characters")
    object_type = module.params['object_type'].strip().upper()
    asp_device = module.params['asp_device'].strip().upper()
    if len(asp_device) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of asp_device exceeds 10 characters")
    user = module.params['user']
    user = [item.strip().upper() for item in user]
    for item in user:
        if len(item) > 10:
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of {p_item} in option user exceeds 10 characters".format(p_item=item))
    authority = module.params['authority']
    authority = [item.strip().upper() for item in authority]
    for item in authority:
        if len(item) > 10:
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of {p_item} in option authority exceeds 10 characters".format(p_item=item))
    replace_authority = module.params['replace_authority']
    authorization_list = module.params['authorization_list'].strip().upper()
    if len(authorization_list) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of authorization_list exceeds 10 characters")
    ref_object_name = module.params['ref_object_name'].strip().upper()
    if len(ref_object_name) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of ref_object_name exceeds 10 characters")
    ref_object_library = module.params['ref_object_library'].strip().upper()
    if len(ref_object_library) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of ref_object_library exceeds 10 characters")
    ref_object_type = module.params['ref_object_type'].strip().upper()
    ref_asp_device = module.params['ref_asp_device'].strip().upper()
    if len(ref_asp_device) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of ref_asp_device exceeds 10 characters")
    asp_group = module.params['asp_group'].strip().upper()
    if len(asp_group) > 10:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of asp_group exceeds 10 characters")
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if operation == 'GRANT' or operation == 'REVOKE':
        # handle single value for user
        if isinstance(user, list) and len(user) > 1 and ('*PUBLIC' in user or '*ALL' in user):
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="*PUBLIC or *ALL must be only value for parameter user")

        # handle single value or other values for authority
        if isinstance(authority, list) and len(authority) > 1:
            single_value = ['*CHANGE', '*ALL', '*USE', '*EXCLUDE', '*AUTL']
            for item in single_value:
                if item in authority:
                    module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="{p_item} must be only value for parameter authority".format(p_item=item))

        # handle the relateionship of *PUBLIC and *AUTL
        if isinstance(authority, list) and len(authority) == 1 and authority[0] == '*AUTL' and user[0] != '*PUBLIC':
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Authority of *AUTL is allowed only with user *PUBLIC")

        # handle the REPLACE option
        replace = '*NO'
        if replace_authority:
            replace = '*YES'

        # handle parameter user
        users = ''
        for item in user:
            users = users + ' ' + item
        if users.strip() == '':
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Specify user when the operation is grant or revoke")

        # handle parameter authority
        authorities = ''
        for item in authority:
            authorities = authorities + ' ' + item

    if operation == 'GRANT_REF' and ref_object_type == '*OBJTYPE' and object_type == '*ALL':
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="ref_object_type(*OBJTYPE) and object_type(*ALL) cannot be used together")

    if operation == 'GRANT_REF' and ref_object_name == '':
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Specify ref_object_name when the operation is grant_ref")

    if (operation == 'GRANT_AUTL' or operation == 'REVOKE_AUTL') and authorization_list == '':
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Specify authorization_list when the operation is grant_autl or revoke_autl")

    if operation == 'GRANT':
        command = 'QSYS/GRTOBJAUT OBJ({p_lib}/{p_obj}) \
            OBJTYPE({p_type}) ASPDEV({p_asp}) USER({p_user}) \
            AUT({p_aut}) REPLACE({p_rep})'.format(
            p_lib=object_library,
            p_obj=object_name,
            p_type=object_type,
            p_asp=asp_device,
            p_user=users,
            p_aut=authorities,
            p_rep=replace)
    elif operation == 'REVOKE':
        command = 'QSYS/RVKOBJAUT OBJ({p_lib}/{p_obj}) \
            OBJTYPE({p_type}) ASPDEV({p_asp}) USER({p_user}) \
            AUT({p_aut})'.format(
            p_lib=object_library,
            p_obj=object_name,
            p_type=object_type,
            p_asp=asp_device,
            p_user=users,
            p_aut=authorities)
    elif operation == 'GRANT_AUTL':
        command = 'QSYS/GRTOBJAUT OBJ({p_lib}/{p_obj}) \
            OBJTYPE({p_type}) ASPDEV({p_asp}) \
            AUTL({p_autl})'.format(
            p_lib=object_library,
            p_obj=object_name,
            p_type=object_type,
            p_asp=asp_device,
            p_autl=authorization_list)
    elif operation == 'REVOKE_AUTL':
        command = 'QSYS/RVKOBJAUT OBJ({p_lib}/{p_obj}) \
            OBJTYPE({p_type}) ASPDEV({p_asp}) \
            AUTL({p_autl})'.format(
            p_lib=object_library,
            p_obj=object_name,
            p_type=object_type,
            p_asp=asp_device,
            p_autl=authorization_list)
    elif operation == 'GRANT_REF':
        command = 'QSYS/GRTOBJAUT OBJ({p_lib}/{p_obj}) \
            OBJTYPE({p_type}) ASPDEV({p_asp}) \
            REFOBJ({p_ref_lib}/{p_ref_obj}) REFOBJTYPE({p_ref_type}) \
            REFASPDEV({p_ref_asp})'.format(
            p_lib=object_library,
            p_obj=object_name,
            p_type=object_type,
            p_asp=asp_device,
            p_ref_lib=ref_object_library,
            p_ref_obj=ref_object_name,
            p_ref_type=ref_object_type,
            p_ref_asp=ref_asp_device)
    else:
        command = "SELECT * FROM QSYS2.OBJECT_PRIVILEGES WHERE SYSTEM_OBJECT_NAME = '{p_obj}'".format(
            p_obj=object_name)
        if (object_library != '') and (not object_library.startswith('*')):
            command = command + ' ' + "AND SYSTEM_OBJECT_SCHEMA = '{p_lib}'".format(p_lib=object_library)
        if object_type != '*ALL':
            command = command + ' ' + "AND OBJECT_TYPE = '{p_type}'".format(p_type=object_type)

    try:
        ibmi_module = imodule.IBMiModule(
            db_name=asp_group, become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    if asp_group or operation == 'DISPLAY':
        if operation != 'DISPLAY':
            command = ' '.join(command.split())  # keep only one space between adjacent strings
            rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)
        else:
            command = ' '.join(command.split())  # keep only one space between adjacent strings
            rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(command)
    else:
        rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(command)

    if operation == 'DISPLAY':
        if rc:
            result_failed = dict(
                stdout=out,
                stderr=err,
                command=command,
                job_log=job_log,
                rc=rc,
            )
            message = 'non-zero return code:{rc}'.format(rc=rc)
            module.fail_json(msg=message, **result_failed)
        else:
            result_success = dict(
                object_authority_list=out,
                command=command,
                job_log=job_log,
                rc=rc,
            )
            if not joblog:
                empty_list = []
                result_success.update({'job_log': empty_list})
            module.exit_json(**result_success)
    else:
        if rc:
            result_failed = dict(
                command=command,
                stderr=err,
                job_log=job_log,
                rc=rc,
            )
            message = 'non-zero return code:{rc}'.format(rc=rc)
            module.fail_json(msg=message, **result_failed)
        else:
            result_success = dict(
                command=command,
                stdout=out,
                rc=rc,
                job_log=job_log,
                changed=True,
            )
            if not joblog:
                empty_list = []
                result_success.update({'job_log': empty_list})
            module.exit_json(**result_success)


if __name__ == '__main__':
    main()
