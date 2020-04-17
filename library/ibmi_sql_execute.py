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
module: ibmi_sql_execute
short_description: Executes a SQL non-DQL(Data Query Language) statement on a remote IBMi node
version_added: 1.0
description:
     - The C(ibmi_sql_execute) module takes the SQL non-DQL(Data Query Language) statement as argument.
     - The given SQL non-DQL(Data Query Language) statement will be executed on all selected nodes.
     - Only run one statement at a time.
options:
  sql:
    description:
      - The C(ibmi_sql_execute) module takes a IBM i SQL non-DQL(Data Query Language) statement to run.
    type: str
    required: yes
notes:
    - Hosts file needs to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3(or python2)
seealso:
- module: IBMi_sql_query

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Insert one record to table Persons
  ibmi_sql_execute:
    sql: "INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
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
stdout:
    description: The sql statement standard output
    returned: always
    type: str
    sample: "+++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
stderr:
    description: The sql statement standard error
    returned: always
    type: str
    sample: ''
sql:
    description: The sql statement executed by the task
    returned: always
    type: str
    sample: "INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"
rc:
    description: The sql statement return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 0
stdout_lines:
    description: The sql statement standard output split in lines
    returned: When rc as non-zero(failure)
    type: list
    sample: ["+++ success INSERT INTO Persons VALUES('919665', 'Le', 'Chang', 'Ring Building', 'Beijing')"]
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


def itoolkit_sql_callproc(sql):
    conn = dbi.connect()
    # itransport = iDB2Call(conn)
    itransport = DatabaseTransport(conn)
    itool = iToolKit(iparm=1)

    itool.add(iSqlQuery('query', sql, {'error': 'on'}))
    itool.add(iSqlFree('free'))

    itool.call(itransport)

    command_output = itool.dict_out('query')

    rc = IBMi_COMMAND_RC_UNEXPECTED
    out = ''
    err = ''
    if 'success' in command_output:
        rc = IBMi_COMMAND_RC_SUCCESS
        out = command_output['success']
    elif 'error' in command_output:
        command_error = command_output['error']
        if 'joblog' in command_error:
            rc = IBMi_COMMAND_RC_ERROR
            err = command_error['joblog']
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
            err = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    else:
        # should not be here, must xmlservice has internal error
        rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
        err = "iToolKit result dict does not have key 'error', the output is %s" % command_output

    return rc, out, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql=dict(type='str', required=True),
        ),
        supports_check_mode=True,
    )

    if HAS_ITOOLKIT is False:
        module.fail_json(msg="itoolkit package is required")

    if HAS_IBM_DB is False:
        module.fail_json(msg="ibm_db package is required")

    sql = module.params['sql']

    startd = datetime.datetime.now()

    rc, out, err = itoolkit_sql_callproc(sql)

    endd = datetime.datetime.now()
    delta = endd - startd

    rc_msg = interpret_return_code(rc)

    result = dict(
        sql=sql,
        stdout=out,
        stderr=err,
        rc=rc,
        start=str(startd),
        end=str(endd),
        delta=str(delta),
        # changed=True,
    )

    if rc != IBMi_COMMAND_RC_SUCCESS:
        message = 'non-zero return code:{rc},{rc_msg}'.format(rc=rc, rc_msg=rc_msg)
        module.fail_json(msg=message, **result)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
