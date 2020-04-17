#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Le Chang <changle@cn.ibm.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

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
  expected_row_count:
    description:
      - The expected row count
      - If it is equal or greater than 0, check if the actual row count returned from the query statement is matched with the expected row count
      - If it is less than 0, do not check if the actual row count returned from the query statement is matched with the expected row counit
    type: int
    default: -1
notes:
    - Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
seealso:
- module: ibmi_sql_execute
author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Query the data of table Persons
  ibmi_sql_query:
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
    type: list
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

from ansible.module_utils.basic import AnsibleModule

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    # from itoolkit.db2.idb2call import iDB2Call
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


def itoolkit_run_sql(sql):
    conn = dbi.connect()
    # itransport = iDB2Call(conn)
    itransport = DatabaseTransport(conn)
    itool = iToolKit()

    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFetch('fetch'))
    itool.add(iSqlFree('free'))

    itool.call(itransport)

    command_output = itool.dict_out('fetch')

    rc = IBMi_COMMAND_RC_UNEXPECTED
    out_list = []
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
            if 'Row not found' in err:
                rc = 0  # treat as success but also indicate the Row not found message in stderr
    else:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['row']
        if isinstance(out, dict):
            out_list.append(out)
        elif isinstance(out, list):
            out_list = out

    return rc, out_list, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql=dict(type='str', required=True),
            expected_row_count=dict(type='int', default=-1),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    sql = module.params['sql']
    check_row_count = False
    expected_row_count = module.params['expected_row_count']
    if expected_row_count >= 0:
        check_row_count = True

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
            start=str(startd),
            end=str(endd),
            delta=str(delta),
            # changed=True,
        )
        message = 'non-zero return code:{rc},{rc_msg}'.format(rc=rc, rc_msg=rc_msg)
        module.fail_json(msg=message, **result_failed)
    else:
        row_count = -999
        if isinstance(out, list):
            row_count = len(out)

        if check_row_count and expected_row_count != row_count:
            result_check_row_fail = dict(
                sql=sql,
                row=out,
                rc=IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT,
                msg="Unexpected row count returned",
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                expected_row_count=expected_row_count,
                row_count=row_count,
                # changed=True,
            )
            module.exit_json(**result_check_row_fail)
        else:
            result_success = dict(
                sql=sql,
                row=out,
                rc=rc,
                start=str(startd),
                end=str(endd),
                delta=str(delta),
                row_count=row_count,
                # changed=True,
            )
            module.exit_json(**result_success)


if __name__ == '__main__':
    main()
