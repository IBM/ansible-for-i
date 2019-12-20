#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) International Business Machines Corp. 2019
# All Rights Reserved
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'IBMi'}

DOCUMENTATION = r'''
---
module: ibmi_sql_query
short_description: Executes a SQL DQL(Data Query Language) statement on a remote IBMi node.
version_added: 1.0
description:
     - The C(ibmi_sql_query) module takes the SQL DQL(Data Query Language) statement as argument.
     - The given SQL DQL(Data Query Language) statement will be executed on all selected nodes.
     - Only run one statement at a time.
options:
  sql:
    description:
      - The C(ibmi_sql_query) module takes a IBM i SQL DQL(Data Query Language) statement to run.
    type: str
    required: yes 
  check_row_count:
    description:
      - If set to C(true), check if the actual row count returned from the query statement is matched with the expected row count
    type: bool
    default: false
  expected_row_count:
    description:
      - The expected row count
    type: int
    required: if expected_row_count set to C(true)
notes:
    - Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
see also:
- module: ibmi_sql_execute
author:
    - Le Chang (changle@cn.ibm.com)
'''

EXAMPLES = r'''
- name: Query the data of table Persons
  sql: 'select * from Persons'
'''

RETURN = r'''
start:
    description: The sql statement execution start time
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The sql statement execution end time
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The sql statement execution delta time
    returned: always
    type: str
    sample: '0:00:00.307534'
row:
    description: The sql query statement result
    returned: when rc as 0(success)
    type: json array(more than one rows) or json object(only one row)
    sample: [
        {
            "ADDRESS": "Ring Building",
            "CITY": "Beijing",
            "FIRSTNAME": "Chang",
            "ID_P": "919665",
            "LASTNAME": "Le"
        },
        {
            "ADDRESS": "Ring Building",
            "CITY": "Shanhai",
            "FIRSTNAME": "Zhang",
            "ID_P": "919689",
            "LASTNAME": "Li"
        }
    ]
stdout:
    description: The sql statement standard output
    returned: When rc as non-zero(failure)
    type: str
    sample: ''
stderr:
    description: The sql statement standard error
    returned: When rc as non-zero(failure)
    type: str
    sample: ''
sql:
    description: The sql statement executed by the task
    returned: always
    type: str
    sample: 'select * from Persons'
rc:
    description: The sql statement return code (0 means success)
    returned: always
    type: int
    sample: 0
rc_msg:
    description: Meaning of the return code 
    returned: always
    type: str
    sample: 'Generic failure'
stdout_lines:
    description: The sql statement standard output split in lines
    returned: When rc as non-zero(failure)
    type: list
    sample: ['']
stderr_lines:
    description: The sql statement standard error split in lines
    returned: When rc as non-zero(failure)
    type: list
    sample: ['']
'''

import datetime

from itoolkit import *
from itoolkit.db2.idb2call import *
import ibm_db_dbi as dbi

from ansible.module_utils.basic import AnsibleModule

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


def itoolkit_run_sql(sql):
    conn = dbi.connect()
    itransport = iDB2Call(conn)
    itool = iToolKit()

    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFetch('fetch'))
    itool.add(iSqlFree('free'))

    itool.call(itransport)

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


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql=dict(type='str', required=True),
            check_row_count=dict(type='bool', default=False),
            expected_row_count=dict(type='int', default=-1),
        ),
        supports_check_mode=True,
    )

    sql = module.params['sql']
    check_row_count = module.params['check_row_count']
    expected_row_count = module.params['expected_row_count']
    if check_row_count and expected_row_count <= 0:
        module.fail_json(
            sql=sql,
            rc=IBMi_COMMAND_RC_INVALID_EXPECTED_ROW_COUNT,
            msg='Invalid expected_row_count',
            rc_msg='When check_row_count is true, expected_row_count(default as -1) must be an integer not less than 0',
            check_row_count=check_row_count,
            expected_row_count=expected_row_count,
        )

    startd = datetime.datetime.now()

    rc, out, err = itoolkit_run_sql(sql)

    endd = datetime.datetime.now()
    delta = endd - startd

    rc_msg = interpret_return_code(rc)

    if rc != IBMi_COMMAND_RC_SUCCESS:
        result_failed = dict(
            sql=sql,
            stdout=out,
            stderr=err,
            rc=rc,
            rc_msg=rc_msg,
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            heck_row_count=check_row_count,
            expected_row_count=expected_row_count,
            # changed=True,
        )
        module.fail_json(msg='non-zero return code', **result_failed)
    else:
        actual_row_count = -999
        if isinstance(out, dict):
            actual_row_count = 1
        elif isinstance(out, list):
            actual_row_count = len(out)

        if check_row_count and expected_row_count != actual_row_count:
            result_check_row_fail = dict(
                sql=sql,
                row=out,
                rc=IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT,
                rc_msg="Unexpected row count returned",
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                check_row_count=check_row_count,
                expected_row_count=expected_row_count,
                actual_row_count=actual_row_count,
                # changed=True,
            )
            module.exit_json(**result_check_row_fail)
        else:
            result_success = dict(
                sql=sql,
                row=out,
                rc=rc,
                rc_msg=rc_msg,
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                check_row_count=check_row_count,
                expected_row_count=expected_row_count,
                actual_row_count=actual_row_count,
                # changed=True,
            )
            module.exit_json(**result_success)


if __name__ == '__main__':
    main()
