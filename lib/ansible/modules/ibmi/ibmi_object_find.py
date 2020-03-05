#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) International Business Machines Corp. 2020
# All Rights Reserved
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
version_added: 1.0
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
    default: "*SYSBAS"
    choices: ["*SYSBAS"]
    required: false
    type: str
  use_regex:
    description:
      - Controls whether regex can be used for object_name option.
        The target IBM i system needs to have the International Components for Unicode (ICU) option installed.
        It takes time to return result if this option is turned on.
    default: false
    type: bool
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
'''

HAS_ITOOLKIT = True
HAS_IBM_DB = True

import datetime
import re

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.ibmi import db2i_tools

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT = 258
IBMi_COMMAND_RC_INVALID_EXPECTED_ROW_COUNT = 259


def interpret_return_code(rc):
    if rc == IBMi_COMMAND_RC_SUCCESS:
        return 'Success'
    elif rc == IBMi_COMMAND_RC_ERROR:
        return 'Generic failure'
    elif rc == IBMi_COMMAND_RC_UNEXPECTED:
        return 'Unexpected error'
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG:
        return "iToolKit result dict does not have key 'joblog'"
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR:
        return "iToolKit result dict does not have key 'error'"
    else:
        return "Unknown error"


# def ibm_dbi_sql_query(sql):
#
#     out = []
#     # Attempt To Establish A Connection To The Database Specified
#     connection_id = None
#     try:
#         connection_id = dbi.connect()
#     except Exception:
#         pass
#
#     if connection_id is None:
#         print("\nERROR: Unable to connect to the database.")
#         err = "ERROR: Unable to connect to the database."
#         return out, err
#     else:
#         print("Done!\n")
#
#     if connection_id is not None:
#         cursor_id = connection_id.cursor()
#
#     try:
#         result_set = cursor_id.execute(sql)
#     except Exception:
#         pass
#
#     if result_set is False:
#         print("\nERROR: Unable to execute the SQL statement specified.\n")
#         connection_id.close()
#         err = "ERROR: Unable to execute the SQL statement specified."
#         return out, err
#     else:
#         print("Done!\n")
#
#     try:
#         result_set = cursor_id.fetchall()
#     except Exception:
#         pass
#
#     if result_set is None:
#         print("\nERROR: Unable to obtain the results desired.\n")
#         connection_id.close()
#         err = "ERROR: Unable to obtain the results desired."
#         return out, err
#     else:
#         print("Done!\n")
#
#     # for result in result_set:
#     #     result_map = {"OBJNAME": result[0], "OBJTYPE": result[1], "OBJOWNER": result[2], "OBJCREATED": result[3]}
#     #     out.append(result_map)
#     out = result_set
#
#     if connection_id is not None:
#         print("Disconnecting from the database ... ")
#         try:
#             return_code = connection_id.close()
#         except Exception:
#             return_code = False
#             pass
#
#         if return_code is False:
#             print("\nERROR: Unable to disconnect from the database.")
#             err = "ERROR: Unable to disconnect from the database."
#             return out, err
#
#         else:
#             print("Done!\n")
#
#     err = None
#     return out, err


def itoolkit_run_sql(sql, asp):
    conn = dbi.connect()
    db_itransport = DatabaseTransport(conn)
    itool = iToolKit()

    # if asp is not None:
    #    xml_itransport = XmlServiceTransport()
    #    sql_setaspgrp = "SETASPGRP " + asp
    #    itool.add(iCmd('setaspgrp', sql_setaspgrp))

    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFetch('fetch'))
    itool.add(iSqlFree('free'))

    itool.call(db_itransport)

    command_output = itool.dict_out('fetch')

    rc = IBMi_COMMAND_RC_UNEXPECTED
    out = ''
    err = ''
    if 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    else:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['row']

    return rc, out, err


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
            iasp_name=dict(type='str', default='*SYSBAS', choices=['*SYSBAS']),
            use_regex=dict(default=False, type='bool'),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    input_age = module.params['age']
    input_age_stamp = module.params['age_stamp']
    input_object_type = module.params['object_type_list']
    input_iasp_name = module.params['iasp_name']
    input_size = module.params['size']
    input_lib = module.params['lib_name']
    input_obj_name = module.params['object_name']
    input_use_regex = module.params['use_regex']

    startd = datetime.datetime.now()

    connection_id = None
    try:
        connection_id = dbi.connect()
    except Exception as e_db_connect:
        module.fail_json(msg="Exception when connecting to IBM i Db2. " + str(e_db_connect))

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

    # generate iasp where stmt
    if input_iasp_name == "*SYSBAS":
        sql_where_stmt_iasp = " AND IASP_NUMBER = 0 "
    else:
        # try to find the IASP number basing on the iasp name
        sql_where_stmt_iasp = " AND A.IASP_NUMBER = (SELECT ASP_NUMBER FROM QSYS2.ASP_INFO " \
                              " WHERE UPPER(DEVICE_DESCRIPTION_NAME) = '" + input_iasp_name.upper() + "') "

    if input_use_regex:
        obj_stats_expression = " SELECT OBJNAME, OBJTYPE, OBJOWNER, OBJDEFINER, OBJCREATED," \
                               " TEXT, OBJLIB, IASP_NUMBER, LAST_USED_TIMESTAMP, LAST_RESET_TIMESTAMP," \
                               " BIGINT(OBJSIZE) AS OBJSIZE, OBJATTRIBUTE " \
                               " FROM TABLE (QSYS2.OBJECT_STATISTICS('" + input_lib + "','" + \
                               input_object_type + "','*ALL')) X "
        sql_where_stmt_regex = " AND REGEXP_LIKE(A.OBJNAME, '" + input_obj_name + "') "
    else:
        obj_stats_expression = " SELECT OBJNAME, OBJTYPE, OBJOWNER, OBJDEFINER, OBJCREATED," \
                               " TEXT, OBJLIB, IASP_NUMBER, LAST_USED_TIMESTAMP, LAST_RESET_TIMESTAMP," \
                               " BIGINT(OBJSIZE) AS OBJSIZE, OBJATTRIBUTE " \
                               " FROM TABLE (QSYS2.OBJECT_STATISTICS('" + input_lib + "','" + \
                               input_object_type + "','" + input_obj_name + "')) X "
        sql_where_stmt_regex = ""

    sql = "select * from (" + obj_stats_expression + ") A WHERE 1 = 1 " + \
          sql_where_stmt_age + \
          sql_where_stmt_size + \
          sql_where_stmt_iasp + \
          sql_where_stmt_regex

    # rc, out, err = itoolkit_run_sql(sql, input_iasp_name)
    out_result_set, err = db2i_tools.ibm_dbi_sql_query(connection_id, sql)

    if err is not None:
        err = handle_db_exception(err)

    if connection_id is not None:
        try:
            connection_id.close()
        except Exception as e_disconnect:
            err = "ERROR: Unable to disconnect from the database. " + str(e_disconnect)

    endd = datetime.datetime.now()
    delta = endd - startd

    if err is not None:
        rc = IBMi_COMMAND_RC_ERROR
        rc_msg = interpret_return_code(rc)
        result_failed = dict(
            sql=sql,
            # size=input_size,
            # age=input_age,
            # age_stamp=input_age_stamp,
            stderr=err,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            # changed=True,
        )
        module.fail_json(msg='non-zero return code: ' + rc_msg, **result_failed)
    else:
        out = []
        for result in out_result_set:
            result_map = {"OBJNAME": result[0], "OBJTYPE": result[1],
                          "OBJOWNER": result[2], "OBJDEFINER": result[3],
                          "OBJCREATED": result[4], "TEXT": result[5],
                          "OBJLIB": result[6], "IASP_NUMBER": result[7],
                          "LAST_USED_TIMESTAMP": result[8], "LAST_RESET_TIMESTAMP": result[9],
                          "OBJSIZE": result[10], "OBJATTRIBUTE": result[11]
                          }
            out.append(result_map)

        rc = IBMi_COMMAND_RC_SUCCESS
        result_success = dict(
            sql=sql,
            object_list=out,
            rc=rc,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            # changed=True,
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
