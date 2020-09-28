#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Zhou Yu <zhouyubj@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_user_compliance_check
short_description: Check if the value of a field of user profile is expected
version_added: '2.8.0'
description:
  - The C(ibmi_user_compliance_check) module can do the user profile compliance check.
  - Check if the value of a field of user profile is matched with the value of customer input.
  - User can input multi value for the multi-value fields. It includes field
  - SPECIAL_AUTHORITIES, USER_ACTION_AUDIT_LEVEL, USER_OPTIONS, SUPPLEMENTAL_GROUP_LIST, LOCALE_JOB_ATTRIBUTES.
  - If some fields value do not match the user's expected value, the list of users will be returned
options:
  users:
    description:
      - Specifies a list of user names.
    type: list
    elements: str
    required: yes
  fields:
    description:
      - Specifies a set of fields which are checked.
      - Customer need to input field name and expected value
      - Following fields are all we support now
      - 'SIGN_ON_ATTEMPTS_NOT_VALID'
      - 'STATUS'
      - 'NO_PASSWORD_INDICATOR'
      - 'PASSWORD_LEVEL_0_1'
      - 'PASSWORD_LEVEL_2_3'
      - 'PASSWORD_EXPIRATION_INTERVAL'
      - 'DAYS_UNTIL_PASSWORD_EXPIRES'
      - 'SET_PASSWORD_TO_EXPIRE'
      - 'USER_CLASS_NAME'
      - 'SPECIAL_AUTHORITIES'
      - 'GROUP_PROFILE_NAME'
      - 'SUPPLEMENTAL_GROUP_COUNT'
      - 'SUPPLEMENTAL_GROUP_LIST'
      - 'OWNER'
      - 'GROUP_AUTHORITY'
      - 'ASSISTANCE_LEVEL'
      - 'CURRENT_LIBRARY_NAME'
      - 'INITIAL_MENU_NAME'
      - 'INITIAL_MENU_LIBRARY_NAME'
      - 'INITIAL_PROGRAM_NAME'
      - 'INITIAL_PROGRAM_LIBRARY_NAME'
      - 'LIMIT_CAPABILITIES'
      - 'TEXT_DESCRIPTION'
      - 'DISPLAY_SIGNON_INFORMATION'
      - 'LIMIT_DEVICE_SESSIONS'
      - 'KEYBOARD_BUFFERING'
      - 'MAXIMUM_ALLOWED_STORAGE'
      - 'STORAGE_USED'
      - 'HIGHEST_SCHEDULING_PRIORITY'
      - 'JOB_DESCRIPTION_NAME'
      - 'JOB_DESCRIPTION_LIBRARY_NAME'
      - 'ACCOUNTING_CODE'
      - 'MESSAGE_QUEUE_NAME'
      - 'MESSAGE_QUEUE_LIBRARY_NAME'
      - 'MESSAGE_QUEUE_DELIVERY_METHOD'
      - 'MESSAGE_QUEUE_SEVERITY'
      - 'OUTPUT_QUEUE_NAME'
      - 'OUTPUT_QUEUE_LIBRARY_NAME'
      - 'PRINT_DEVICE'
      - 'SPECIAL_ENVIRONMENT'
      - 'ATTENTION_KEY_HANDLING_PROGRAM_NAME'
      - 'ATTENTION_KEY_HANDLING_PROGRAM_LIBRARY_NAME'
      - 'LANGUAGE_ID'
      - 'COUNTRY_OR_REGION_ID'
      - 'CHARACTER_CODE_SET_ID'
      - 'USER_OPTIONS'
      - 'SORT_SEQUENCE_TABLE_NAME'
      - 'SORT_SEQUENCE_TABLE_LIBRARY_NAME'
      - 'OBJECT_AUDITING_VALUE'
      - 'USER_ACTION_AUDIT_LEVEL'
      - 'GROUP_AUTHORITY_TYPE'
      - 'USER_ID_NUMBER'
      - 'GROUP_ID_NUMBER'
      - 'LOCALE_JOB_ATTRIBUTES'
      - 'GROUP_MEMBER_INDICATOR'
      - 'DIGITAL_CERTIFICATE_INDICATOR'
      - 'CHARACTER_IDENTIFIER_CONTROL'
      - 'LOCAL_PASSWORD_MANAGEMENT'
      - 'BLOCK_PASSWORD_CHANGE'
      - 'USER_ENTITLEMENT_REQUIRED'
      - 'USER_EXPIRATION_INTERVAL'
      - 'USER_EXPIRATION_ACTION'
      - 'HOME_DIRECTORY'
      - 'LOCALE_PATH_NAME'
      - 'USER_DEFAULT_PASSWORD'
      - 'USER_OWNER'
      - 'USER_CREATOR'
      - 'SIZE'
      - 'DAYS_USED_COUNT'
      - 'AUTHORITY_COLLECTION_ACTIVE'
      - 'AUTHORITY_COLLECTION_REPOSITORY_EXISTS'
      - 'PASE_SHELL_PATH'
    type: list
    elements: dict
    required: yes
  joblog:
    description:
      - The job log of the job executing the task will be returned even rc is zero if it is set to true.
    type: bool
    default: false
  become_user:
    description:
      - The name of the user profile that the IBM i task will run under.
      - Use this option to set a user with desired privileges to run the task.
    type: str
  become_user_password:
    description:
      - Use this option to set the password of the user specified in C(become_user).
    type: str


author:
- Zhou Yu (@zhouyu)
'''

EXAMPLES = r'''
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

'''


RETURN = r'''
stderr:
    description: The standard error
    returned: when rc as no-zero(failure)
    type: str
    sample: ''
stderr_lines:
    description: The command standard error split in lines.
    returned: always
    type: list
    sample: ''
sql1:
    description: The sql statement executed by the task.
    returned: always
    type: str
    sample: 'select * from Persons'
sql2:
    description: The sql statement executed by the task.
    returned: always
    type: str
    sample: 'select * from Persons'
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
result_set:
    description: The result set of user information includes all fields specified by user.
    returned: When rc as 0(success) and the value of field of user who is specified by users parameter does not match the user's expected value
    type: list
    sample: [
        {
            "AUTHORIZATION_NAME": "ZHOUYU",
            "NO_PASSWORD_INDICATOR": "NO",
            "SPECIAL_AUTHORITIES": "*JOBCTL    *SAVSYS    ",
            "STATUS": "*DISABLED"
        }
    ]
job_log:
    description: The IBM i job log of the task executed.
    type: list
    sample: [{"FROM_INSTRUCTION": "8964",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "QSQSRVR",
            "FROM_PROCEDURE": "QSQSRVR",
            "FROM_PROGRAM": "QSQSRVR",
            "FROM_USER": "ZHOUYU1",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPF9898",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "&N Cause . . . . . :   This message is used by application programs as a general escape message.",
            "MESSAGE_SUBTYPE": null,
            "MESSAGE_TEXT": "SERVER MODE CONNECTING JOB IS 236764/QSECOFR/QP0ZSPWP.",
            "MESSAGE_TIMESTAMP": "2020-08-21T18:19:37.135231",
            "MESSAGE_TYPE": "COMPLETION",
            "ORDINAL_POSITION": 9,
            "SEVERITY": 40,
            "TO_INSTRUCTION": "8964",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"}]
    returned: always
'''

import datetime

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"

parmname_array = [
    'SIGN_ON_ATTEMPTS_NOT_VALID',
    'STATUS',
    'NO_PASSWORD_INDICATOR',
    'PASSWORD_LEVEL_0_1',
    'PASSWORD_LEVEL_2_3',
    'PASSWORD_EXPIRATION_INTERVAL',
    'DAYS_UNTIL_PASSWORD_EXPIRES',
    'SET_PASSWORD_TO_EXPIRE',
    'USER_CLASS_NAME',
    'SPECIAL_AUTHORITIES',
    'GROUP_PROFILE_NAME',
    'SUPPLEMENTAL_GROUP_COUNT',
    'SUPPLEMENTAL_GROUP_LIST',
    'OWNER',
    'GROUP_AUTHORITY',
    'ASSISTANCE_LEVEL',
    'CURRENT_LIBRARY_NAME',
    'INITIAL_MENU_NAME',
    'INITIAL_MENU_LIBRARY_NAME',
    'INITIAL_PROGRAM_NAME',
    'INITIAL_PROGRAM_LIBRARY_NAME',
    'LIMIT_CAPABILITIES',
    'TEXT_DESCRIPTION',
    'DISPLAY_SIGNON_INFORMATION',
    'LIMIT_DEVICE_SESSIONS',
    'KEYBOARD_BUFFERING',
    'MAXIMUM_ALLOWED_STORAGE',
    'STORAGE_USED',
    'HIGHEST_SCHEDULING_PRIORITY',
    'JOB_DESCRIPTION_NAME',
    'JOB_DESCRIPTION_LIBRARY_NAME',
    'ACCOUNTING_CODE',
    'MESSAGE_QUEUE_NAME',
    'MESSAGE_QUEUE_LIBRARY_NAME',
    'MESSAGE_QUEUE_DELIVERY_METHOD',
    'MESSAGE_QUEUE_SEVERITY',
    'OUTPUT_QUEUE_NAME',
    'OUTPUT_QUEUE_LIBRARY_NAME',
    'PRINT_DEVICE',
    'SPECIAL_ENVIRONMENT',
    'ATTENTION_KEY_HANDLING_PROGRAM_NAME',
    'ATTENTION_KEY_HANDLING_PROGRAM_LIBRARY_NAME',
    'LANGUAGE_ID',
    'COUNTRY_OR_REGION_ID',
    'CHARACTER_CODE_SET_ID',
    'USER_OPTIONS',
    'SORT_SEQUENCE_TABLE_NAME',
    'SORT_SEQUENCE_TABLE_LIBRARY_NAME',
    'OBJECT_AUDITING_VALUE',
    'USER_ACTION_AUDIT_LEVEL',
    'GROUP_AUTHORITY_TYPE',
    'USER_ID_NUMBER',
    'GROUP_ID_NUMBER',
    'LOCALE_JOB_ATTRIBUTES',
    'GROUP_MEMBER_INDICATOR',
    'DIGITAL_CERTIFICATE_INDICATOR',
    'CHARACTER_IDENTIFIER_CONTROL',
    'LOCAL_PASSWORD_MANAGEMENT',
    'BLOCK_PASSWORD_CHANGE',
    'USER_ENTITLEMENT_REQUIRED',
    'USER_EXPIRATION_INTERVAL',
    'USER_EXPIRATION_ACTION',
    'HOME_DIRECTORY',
    'LOCALE_PATH_NAME',
    'USER_DEFAULT_PASSWORD',
    'USER_OWNER',
    'USER_CREATOR',
    'SIZE',
    'DAYS_USED_COUNT',
    'AUTHORITY_COLLECTION_ACTIVE',
    'AUTHORITY_COLLECTION_REPOSITORY_EXISTS',
    'PASE_SHELL_PATH',
]


def is_number(str):
    try:
        if str == 'NaN':
            return False
        float(str)
        return True
    except ValueError:
        return False


def build_sql(fields, users):

    # sql1_part1 is built for adding seclet column
    sql1_part1 = "SELECT AUTHORIZATION_NAME"
    # sql1_part2 is built for condition part
    sql1_part2 = " FROM QSYS2.USER_INFO WHERE ("

    need_sql2 = False

    counter1 = 1
    counter2 = 1
    for field in fields:
        sql1_part1 = sql1_part1 + ", " + field['name'].upper()
        if (field['name'].upper() == 'SPECIAL_AUTHORITIES' or
                field['name'].upper() == 'USER_ACTION_AUDIT_LEVEL' or
                field['name'].upper() == 'USER_OPTIONS' or
                field['name'].upper() == 'SUPPLEMENTAL_GROUP_LIST' or
                field['name'].upper() == 'LOCALE_JOB_ATTRIBUTES' or
                field['name'].upper() == 'HOME_DIRECTORY'):
            need_sql2 = True
            counter2 += 1
        else:
            if (counter1 == 1):
                if (field['expect'][0].strip() == ''):
                    sql1_part2 = sql1_part2 + field['name'].upper() + " is not null"
                else:
                    if (field['name'].upper() == 'SUPPLEMENTAL_GROUP_COUNT' or
                            field['name'].upper() == 'AUTHORITY_COLLECTION_ACTIVE' or
                            field['name'].upper() == 'AUTHORITY_COLLECTION_REPOSITORY_EXISTS'):
                        sql1_part2 = sql1_part2 + field['name'].upper() + " <> '" + field['expect'][0].upper() + "'"
                    else:
                        sql1_part2 = sql1_part2 + "(" + field['name'].upper() + " <> '" + field['expect'][0].upper() +\
                            "' OR " + field['name'].upper() + " is null)"
            else:
                if (field['expect'][0].strip() == ''):
                    sql1_part2 = sql1_part2 + " OR " + field['name'].upper() + " is not null"
                else:
                    if (field['name'].upper() == 'SUPPLEMENTAL_GROUP_COUNT' or
                            field['name'].upper() == 'AUTHORITY_COLLECTION_ACTIVE' or
                            field['name'].upper() == 'AUTHORITY_COLLECTION_REPOSITORY_EXISTS'):
                        sql1_part2 = sql1_part2 + " OR " + field['name'].upper() + " <> '" + field['expect'][0].upper() + "'"
                    else:
                        sql1_part2 = sql1_part2 + " OR " + "(" + field['name'].upper() + " <> '" + field['expect'][0].upper() + \
                            "' OR " + field['name'].upper() + " is null)"
            counter1 += 1

    sql1 = ""
    sql2 = ""
    # build sql1 for fetching the no matched record
    if counter1 > 1:
        sql1 = sql1_part1 + sql1_part2 + ")"
        counter1 = 1
        sql1 = sql1 + " AND AUTHORIZATION_NAME IN("
        for user in users:
            if (counter1 == 1):
                sql1 = sql1 + "'" + user.upper() + "'"
            else:
                sql1 = sql1 + ", '" + user.upper() + "'"
            counter1 += 1
        sql1 = sql1 + ")"

    # build sql2 for fetching the value of multi-value field
    if need_sql2 and counter2 > 1:
        sql2 = sql1_part1 + " FROM QSYS2.USER_INFO WHERE AUTHORIZATION_NAME IN("
        counter2 = 1
        for user in users:
            if (counter2 == 1):
                sql2 = sql2 + "'" + user.upper() + "'"
            else:
                sql2 = sql2 + ", '" + user.upper() + "'"
            counter2 += 1
        sql2 = sql2 + ")"

    return sql1, sql2


def main():
    module = AnsibleModule(
        argument_spec=dict(
            users=dict(type='list', elements='str', required=True),
            fields=dict(type='list', elements='dict', required=True),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    # get input value
    users = module.params['users']
    fields = module.params['fields']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']
    # initialize variables
    check_special_authorities = False
    check_user_action_audit_level = False
    check_user_option = False
    check_supplemental_group_list = False
    check_locale_job_attributes = False
    check_home_directory = False
    out1 = []
    out2 = []
    # check input value
    for field in fields:
        if field.get('name') is None:
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                             msg="There is no element 'name' in the dictionary 'field'.")
        if field.get('expect') is None:
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                             msg="There is no element 'expect' in the dictionary 'field'.")
        if not isinstance(field['name'], str):
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                             msg="The type of element 'name' of dictionary 'field' must be string.")
        if isinstance(field['expect'], list):
            for expect_value in field['expect']:
                if not isinstance(expect_value, str):
                    module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                                     msg="The type of element 'expect' of dictionary 'field' must be a list comprised by string.")
        else:
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                             msg="The type of element 'expect' of dictionary 'field' must be a list comprised by string.")
        if (field['name'].upper() not in parmname_array):
            module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                             msg="Input attribute name is not available")
        if field['name'].upper() == 'SPECIAL_AUTHORITIES':
            check_special_authorities = True
            special_authorities_expect = list(filter(None, field['expect']))
        elif field['name'].upper() == 'USER_ACTION_AUDIT_LEVEL':
            check_user_action_audit_level = True
            user_action_audit_level_expect = list(filter(None, field['expect']))
        elif field['name'].upper() == 'USER_OPTIONS':
            check_user_option = True
            user_option_expect = list(filter(None, field['expect']))
        elif field['name'].upper() == 'SUPPLEMENTAL_GROUP_LIST':
            check_supplemental_group_list = True
            supplemental_group_list_expect = list(filter(None, field['expect']))
        elif field['name'].upper() == 'LOCALE_JOB_ATTRIBUTES':
            check_locale_job_attributes = True
            locale_job_attributes_expect = list(filter(None, field['expect']))
        elif field['name'].upper() == 'HOME_DIRECTORY':
            check_home_directory = True
            home_directory_expect = list(filter(None, field['expect']))
        elif (field['name'].upper() == 'SIGN_ON_ATTEMPTS_NOT_VALID' or
                field['name'].upper() == 'PASSWORD_EXPIRATION_INTERVAL' or
                field['name'].upper() == 'DAYS_UNTIL_PASSWORD_EXPIRES' or
                field['name'].upper() == 'SUPPLEMENTAL_GROUP_COUNT' or
                field['name'].upper() == 'MAXIMUM_ALLOWED_STORAGE' or
                field['name'].upper() == 'STORAGE_USED' or
                field['name'].upper() == 'MESSAGE_QUEUE_SEVERITY' or
                field['name'].upper() == 'USER_ID_NUMBER' or
                field['name'].upper() == 'GROUP_ID_NUMBER' or
                field['name'].upper() == 'USER_EXPIRATION_INTERVAL' or
                field['name'].upper() == 'DAYS_USED_COUNT' or
                field['name'].upper() == 'SIZE'):
            if len(field['expect']) > 1:
                module.fail_json(rc=256, msg="Field {p_name} should be only one value".format(p_name=field['name'].upper()))
            if field['expect'][0].strip() != '' and not is_number(field['expect'][0]):
                module.fail_json(rc=256, msg="Field {p_name} should be numerical".format(p_name=field['name'].upper()))

    try:
        ibmi_module = imodule.IBMiModule(become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    # Check to see if the user exists
    User_not_existed = []
    for user in users:
        chkobj_cmd = 'QSYS/CHKOBJ OBJ(QSYS/{p_user}) OBJTYPE(*USRPRF)'.format(p_user=user)
        ibmi_util.log_info("Command to run: " + chkobj_cmd, module._name)
        rc, out, err, job_log = ibmi_module.itoolkit_run_command_once(chkobj_cmd)
        if rc != 0:
            User_not_existed.append(user)

    sql1, sql2 = build_sql(fields, users)
    if sql1 != "":
        startd = datetime.datetime.now()
        rc, out1, err = ibmi_module.itoolkit_run_sql(sql1)
        if joblog or (rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS):
            job_log = ibmi_module.itoolkit_get_job_log(startd)
        else:
            job_log = []

        if rc:
            result_failed = dict(
                stderr=err,
                sql1=sql1,
                sql2=sql2,
                rc=rc,
                job_log=job_log,
            )
            message = 'non-zero return code:{rc}'.format(rc=rc)
            module.fail_json(msg=message, **result_failed)

    if sql2 != "":
        # fetch records of all users information specified by user
        startd = datetime.datetime.now()
        rc, out2, err = ibmi_module.itoolkit_run_sql(sql2)
        if joblog or (rc != ibmi_util.IBMi_COMMAND_RC_SUCCESS):
            job_log = ibmi_module.itoolkit_get_job_log(startd)
        else:
            job_log = []

        if rc:
            result_failed = dict(
                stderr=err,
                sql1=sql1,
                sql2=sql2,
                rc=rc,
                job_log=job_log,
            )
            message = 'non-zero return code:{rc}'.format(rc=rc)
            module.fail_json(msg=message, **result_failed)

        if out2:
            real_out2 = []
            for item in out2:
                # compare the column SPECIAL_AUTHORITIES
                if check_special_authorities:
                    special_authorities_list = item['SPECIAL_AUTHORITIES'].split()
                    not_expected_value = False
                    if (len(special_authorities_list) == len(special_authorities_expect)):
                        for special_authorities_value in special_authorities_list:
                            if special_authorities_value not in special_authorities_expect:
                                not_expected_value = True
                                break
                    else:
                        not_expected_value = True

                    if not_expected_value:
                        real_out2.append(item)
                        continue

                # compare the column USER_ACTION_AUDIT_LEVEL
                if check_user_action_audit_level:
                    user_action_audit_level_list = item['USER_ACTION_AUDIT_LEVEL'].split()
                    not_expected_value = False
                    if (len(user_action_audit_level_list) == len(user_action_audit_level_expect)):
                        for user_action_audit_level_value in user_action_audit_level_list:
                            if user_action_audit_level_value not in user_action_audit_level_expect:
                                not_expected_value = True
                                break
                    else:
                        not_expected_value = True

                    if not_expected_value:
                        real_out2.append(item)
                        continue

                # compare the column USER_OPTIONS
                if check_user_option:
                    user_option_list = item['USER_OPTIONS'].split()
                    not_expected_value = False
                    if (len(user_option_list) == len(user_option_expect)):
                        for user_option_value in user_option_list:
                            if user_option_value not in user_option_expect:
                                not_expected_value = True
                                break
                    else:
                        not_expected_value = True

                    if not_expected_value:
                        real_out2.append(item)
                        continue

                # compare the column SUPPLEMENTAL_GROUP_LIST
                if check_supplemental_group_list:
                    supplemental_group_list = item['SUPPLEMENTAL_GROUP_LIST'].split()
                    not_expected_value = False
                    if (len(supplemental_group_list) == len(supplemental_group_list_expect)):
                        for supplemeental_group_value in supplemental_group_list:
                            if supplemeental_group_value not in supplemental_group_list_expect:
                                not_expected_value = True
                                break
                    else:
                        not_expected_value = True

                    if not_expected_value:
                        real_out2.append(item)
                        continue

                # compare the column LOCALE_JOB_ATTRIBUTES
                if check_locale_job_attributes:
                    locale_job_attributes_list = item['LOCALE_JOB_ATTRIBUTES'].split()
                    not_expected_value = False
                    if (len(locale_job_attributes_list) == len(locale_job_attributes_expect)):
                        for locale_job_attributes_value in locale_job_attributes_list:
                            if locale_job_attributes_value not in locale_job_attributes_expect:
                                not_expected_value = True
                                break
                    else:
                        not_expected_value = True

                    if not_expected_value:
                        real_out2.append(item)
                        continue

                if check_home_directory:
                    home_directory = item['HOME_DIRECTORY']
                    if len(home_directory_expect) == 0:
                        if home_directory.strip() != '':
                            real_out2.append(item)
                            continue
                    else:
                        if home_directory_expect[0].upper() != home_directory.upper():
                            real_out2.append(item)
                            continue
            if out1:
                out1_name_list = []
                for item in out1:
                    out1_name_list.append(item['AUTHORIZATION_NAME'].upper())
                out = out1
                for item in real_out2:
                    if item['AUTHORIZATION_NAME'].upper() not in out1_name_list:
                        out.append(item)
            else:
                out = real_out2
        else:
            out = out1
    else:
        out = out1

    if len(User_not_existed) == 0:
        result_success = dict(
            result_set=out,
            sql1=sql1,
            sql2=sql2,
            rc=rc,
            job_log=job_log,
        )
    else:
        result_success = dict(
            result_set=out,
            user_not_existed=User_not_existed,
            sql1=sql1,
            sql2=sql2,
            rc=rc,
            job_log=job_log,
        )
    module.exit_json(**result_success)


if __name__ == '__main__':
    main()
