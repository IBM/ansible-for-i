#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Wang Yun <cdlwangy@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_object_find
short_description: Find specific IBM i object(s).
version_added: '2.8.0'
description:
     - Return a list of IBM i objects based on specific criteria. Multiple criteria are AND'd together.
options:
  age:
    description:
      - Select objects whose age is equal to or greater than the specified time.
        Use a negative age to find objects equal to or less than the specified time.
        You can choose seconds, minutes, hours, days, or weeks by specifying the first letter of any of those \n
        words (e.g., "1w").
    default: null
    required: false
    type: str
  age_stamp:
    description:
      - Choose the object statistic against which we compare age. Default is ctime which is the object creation time.
    required: false
    default: "ctime"
    choices: ["ctime"]
    type: str
  object_type_list:
    description:
      - One or more system object types separated by either a blank or a comma.
    default: "*ALL"
    required: false
    type: str
  lib_name:
    description:
      - The name of the library that returned objects locate in
    default: "*ALLUSR"
    required: false
    type: str
  object_name:
    description:
      - The name of the object that will be returned. Whether regex can be used for object_name is controlled by
        C(use_regex) option
    default: '*ALL'
    type: str
  size:
    description:
      - Select objects whose size is equal to or greater than the specified size.
        Use a negative size to find objects equal to or less than the specified size.
        Unqualified values are in bytes but b, k, m, g, and t can be appended to specify bytes,
        kilobytes, megabytes, gigabytes, and terabytes, respectively.
    default: null
    required: false
    type: str
  iasp_name:
    description:
      - The auxiliary storage pool (ASP) where storage is allocated for the object.
      - The default value is C(*SYSBAS).
      - If an IASP name is specified, objects in this ASP group will be returned, including both SYSBAS and IASP.
    default: "*SYSBAS"
    type: str
  use_regex:
    description:
      - Controls whether regex can be used for object_name option.
        The target IBM i system needs to have the International Components for Unicode (ICU) option installed.
        It takes time to return result if this option is turned on.
    default: false
    type: bool
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
notes:
    - Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
seealso:
    - module: find
author:
    - Wang Yun(@airwangyun)
'''

EXAMPLES = r'''
- name:  Find all journals and journal receivers in library WYTEST.
  ibmi_object_find:
    object_name: '*ALL'
    object_type_list: '*JRN *JRNRCV'
    lib_name: 'WYTEST'
    age: '1w'
    age_stamp: 'ctime'

- name:  Find all the object names that contains 'ABC' with regex.
  ibmi_object_find:
    object_name: 'ABC+'
    object_type_list: '*ALL'
    lib_name: '*ALL'
    use_regex: true

- name: find library WYTEST in sysbas
  ibmi_object_find:
    lib_name: 'QSYS'
    iasp_name: '*SYSBAS'
    object_name: 'WYTEST'
    object_type_list: "*LIB"

- name: find object OBJABC in asp group WYTEST2
  ibmi_object_find:
    lib_name: '*ALL'
    iasp_name: 'WYTEST2'
    object_type_list: "*FILE"
    object_name: 'OBJABC'
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
start:
    description: The task execution start time
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The task execution end time
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The task execution delta time
    returned: always
    type: str
    sample: '0:00:00.307534'
object_list:
    description: The object list returned
    returned: when rc as 0(success)
    type: list
    sample: [
        {
            "OBJLIB": "TESTLIB",
            "OBJNAME": "TESTOBJ1",
            "OBJCREATED": "2019-02-18T10:48:41",
            "OBJDEFINER": "USERADMIN",
            "OBJTYPE": "*FILE",
            "OBJOWNER": "WY",
            "TEXT": "TEST",
            "IASP_NUMBER": 0,
            "LAST_RESET_TIMESTAMP": null,
            "LAST_USED_TIMESTAMP": null,
            "OBJSIZE": 131072,
            "OBJATTRIBUTE": "SAVF"
        },
        {
            "OBJLIB": "TESTLIB",
            "OBJNAME": "RING1",
            "OBJCREATED": "2019-02-18T10:48:41",
            "OBJDEFINER": "USERAPP",
            "OBJTYPE": "*FILE",
            "OBJOWNER": "WY",
            "TEXT": "test",
            "IASP_NUMBER": 0,
            "LAST_RESET_TIMESTAMP": null,
            "LAST_USED_TIMESTAMP": null,
            "OBJSIZE": 131072,
            "OBJATTRIBUTE": "SAVF"
        }
    ]
stdout:
    description: The task execution standard output
    returned: When rc as non-zero(failure)
    type: str
    sample: ''
stderr:
    description: The task execution standard error
    returned: When rc as non-zero(failure)
    type: str
    sample: ''
rc:
    description: The task execution return code (0 means success)
    returned: always
    type: int
    sample: 0
stdout_lines:
    description: The task execution standard output split in lines
    returned: When rc as non-zero(failure)
    type: list
    sample: ['']
stderr_lines:
    description: The task execution standard error split in lines
    returned: When rc as non-zero(failure)
    type: list
    sample: ['']
job_log:
    description: The job log of the job executes the task.
    returned: always
    type: list
    sample: [
        {
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
        }
    ]
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
import re

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "1.1.2"

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT = 258
IBMi_COMMAND_RC_INVALID_EXPECTED_ROW_COUNT = 259


def age_where_stmt(input_age, input_age_stamp):
    m = re.match(r"^(-?\d+)([smhdw])?$", input_age.lower())
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    if m:
        age = int(m.group(1)) * seconds_per_unit.get(m.group(2), 1)
    else:
        return None

    current_time = datetime.datetime.now()
    time_delta = datetime.timedelta(seconds=abs(age))
    time_with_age = current_time - time_delta
    str_timestamp_with_age = time_with_age.strftime("%Y-%m-%d %H:%M:%S")

    age_stamp_map = {"ctime": "OBJCREATED", "utime": "LAST_USED_TIMESTAMP", "rtime": "LAST_RESET_TIMESTAMP"}
    age_stamp_in_sql = age_stamp_map.get(input_age_stamp)
    if age_stamp_in_sql is None:
        return None

    if age >= 0:
        sql_where_stmt_age = " AND " + age_stamp_in_sql + " <= '" + str_timestamp_with_age + "'"
    else:
        sql_where_stmt_age = " AND " + age_stamp_in_sql + " > '" + str_timestamp_with_age + "'"
    return sql_where_stmt_age


def size_where_stmt(input_size):
    if input_size is None:
        return None
    else:
        # convert size to bytes:
        m = re.match(r"^(-?\d+)([bkmgt])?$", input_size.lower())
        bytes_per_unit = {"b": 1, "k": 1024, "m": 1024 ** 2, "g": 1024 ** 3, "t": 1024 ** 4}
        if m:
            size = int(m.group(1)) * bytes_per_unit.get(m.group(2), 1)
        else:
            return None

        if size >= 0:
            sql_where_stmt_size = " AND OBJSIZE >= " + str(abs(size))
        else:
            sql_where_stmt_size = " AND OBJSIZE <= " + str(abs(size))

    return sql_where_stmt_size


def handle_db_exception(db_err):
    if 'SQLSTATE=2201S SQLCODE=-20558' in str(db_err):
        err = 'ERROR: Regular expression specified is not valid. '
    elif 'SQLSTATE=42616 SQLCODE=-443' in str(db_err):
        err = 'ERROR: Input parameters are not valid. Please check the input of ' \
              'library name, object name and object type whether they are valid. '
    else:
        return db_err

    return err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            age=dict(default=None, type='str'),
            age_stamp=dict(default="ctime", choices=['ctime'], type='str'),
            object_type_list=dict(type='str', default='*ALL'),
            lib_name=dict(type='str', default='*ALLUSR'),
            object_name=dict(type='str', default='*ALL'),
            size=dict(default=None, type='str'),
            iasp_name=dict(type='str', default='*SYSBAS'),
            use_regex=dict(default=False, type='bool'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    input_age = module.params['age']
    input_age_stamp = module.params['age_stamp']
    input_object_type = module.params['object_type_list']
    input_iasp_name = module.params['iasp_name']
    input_size = module.params['size']
    input_lib = module.params['lib_name']
    input_obj_name = module.params['object_name']
    input_use_regex = module.params['use_regex']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    startd = datetime.datetime.now()

    try:
        ibmi_module = imodule.IBMiModule(
            db_name=input_iasp_name, become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    db_conn = ibmi_module.get_connection()

    # generate age where stmt
    if input_age is None:
        # age = None
        sql_where_stmt_age = ''
    else:
        sql_where_stmt_age = age_where_stmt(input_age, input_age_stamp)
        if sql_where_stmt_age is None:
            module.fail_json(msg="failed to process age: " + input_age)

    # generate size where stmt
    if input_size is None:
        sql_where_stmt_size = ''
    else:
        sql_where_stmt_size = size_where_stmt(input_size)
        if sql_where_stmt_size is None:
            module.fail_json(msg="failed to process size: " + input_size)

    # get the version and release info
    release_info, err = db2i_tools.get_ibmi_release(db_conn)

    if release_info["version_release"] < 7.4:
        lib_name_label = "(SELECT SYSTEM_SCHEMA_NAME FROM QSYS2.SYSSCHEMAS WHERE SCHEMA_NAME = OBJLONGSCHEMA)"
    else:
        lib_name_label = "OBJLIB"

    if input_use_regex:
        obj_stats_expression = " SELECT OBJNAME, OBJTYPE, OBJOWNER, OBJDEFINER, OBJCREATED," \
                               " TEXT, " + lib_name_label + " AS OBJLIB, IASP_NUMBER, LAST_USED_TIMESTAMP, " \
                               " LAST_RESET_TIMESTAMP," \
                               " BIGINT(OBJSIZE) AS OBJSIZE, OBJATTRIBUTE, OBJLONGSCHEMA " \
                               " FROM TABLE (QSYS2.OBJECT_STATISTICS('" + input_lib + "','" + \
                               input_object_type + "','*ALL')) X "
        sql_where_stmt_regex = " AND REGEXP_LIKE(A.OBJNAME, '" + input_obj_name + "') "
    else:
        obj_stats_expression = " SELECT OBJNAME, OBJTYPE, OBJOWNER, OBJDEFINER, OBJCREATED," \
                               " TEXT, " + lib_name_label + " AS OBJLIB, IASP_NUMBER, LAST_USED_TIMESTAMP, " \
                               " LAST_RESET_TIMESTAMP," \
                               " BIGINT(OBJSIZE) AS OBJSIZE, OBJATTRIBUTE, OBJLONGSCHEMA " \
                               " FROM TABLE (QSYS2.OBJECT_STATISTICS('" + input_lib + "','" + \
                               input_object_type + "','" + input_obj_name + "')) X "
        sql_where_stmt_regex = ""

    sql = "select * from (" + obj_stats_expression + ") A WHERE 1 = 1 " + \
          sql_where_stmt_age + \
          sql_where_stmt_size + \
          sql_where_stmt_regex

    rc, out_result_set, err = ibmi_module.itoolkit_run_sql(sql)

    if joblog or (rc != IBMi_COMMAND_RC_SUCCESS):
        job_log = ibmi_module.itoolkit_get_job_log(startd)
    else:
        job_log = []

    endd = datetime.datetime.now()
    delta = endd - startd

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            sql=sql,
            # size=input_size,
            # age=input_age,
            job_log=job_log,
            stderr=err,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            # changed=True,
        )
        module.fail_json(msg='Non-zero return code. ', **result_failed)
    else:
        # out = []
        # for result in out_result_set:
        #     result_map = {"OBJNAME": result[0], "OBJTYPE": result[1],
        #                   "OBJOWNER": result[2], "OBJDEFINER": result[3],
        #                   "OBJCREATED": result[4], "TEXT": result[5],
        #                   "OBJLIB": result[6], "IASP_NUMBER": result[7],
        #                   "LAST_USED_TIMESTAMP": result[8], "LAST_RESET_TIMESTAMP": result[9],
        #                   "OBJSIZE": result[10], "OBJATTRIBUTE": result[11], "OBJLONGSCHEMA": result[12]
        #                   }
        #     out.append(result_map)

        result_success = dict(
            sql=sql,
            object_list=out_result_set,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            job_log=job_log,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
