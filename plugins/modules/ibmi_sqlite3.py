#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Xu Meng <mengxumx@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_sqlite3
short_description: Executes a SQL statement via sqlite3
version_added: '2.8.0'
description:
     - The C(ibmi_sqlite3) module takes the SQL statement as argument.
options:
  sql:
    description:
      - The C(ibmi_sqlite3) module takes a IBM i SQL statement to run.
    type: str
    required: yes
  database:
    description:
      - Specified database file name, e.g. '/tmp/testdb.sqlite3'
    type: str
    default: '/tmp/testdb.sqlite3'
    required: false
  parameters:
    description:
      - The binding parameters for the sql statement executed by the task.
    type: list
    elements: dict
    required: false

author:
- Xu Meng(@dmabupt)
'''

EXAMPLES = r'''
- name: Create table PTFINFO
  ibmi_sqlite3:
    database: "/tmp/testdb.sqlite3"
    sql: "CREATE TABLE PTFINFO (ID CHAR(10) PRIMARY KEY NOT NULL, PRODUCT CHAR(10) NOT NULL, VRM CHAR(10) NOT NULL, CHECKSUM CHAR(256))"

- name: Insert some records to table PTFINFO
  ibmi_sqlite3:
    database: "/tmp/testdb.sqlite3"
    sql: "INSERT INTO PTFINFO (ID, PRODUCT, VRM, CHECKSUM) VALUES (:ID, :PRODUCT, :VRM, :CHECKSUM)"
    parameters: [
      {
        "ID": "SI12345",
        "PRODUCT": "5770UME",
        "SAVF": "QSI12345",
        "CHKSUM": "f234cvfsd5345"
      },
      {
        "ID": "SI67890",
        "PRODUCT": "5770DG1",
        "SAVF": "QSI67890",
        "CHKSUM": "f2eqwe345345"
      }
    ]

- name: Find a record to table PTFINFO
  ibmi_sqlite3:
    database: "/tmp/testdb.sqlite3"
    sql: "SELECT ID FROM PTFINFO WHERE ID = :ID"
    parameters: {"ID": "SI69379"}

- name: Update a record in table PTFINFO
  ibmi_sqlite3:
    database: "/tmp/testdb.sqlite3"
    sql: "UPDATE PTFINFO SET CHECKSUM=:CHECKSUM WHERE ID=:ID"
    parameters: {"ID": "SI69379", "CHECKSUM": "abc123"}

- name: Delete a record in table PTFINFO
  ibmi_sqlite3:
    database: "/tmp/testdb.sqlite3"
    sql: "DELETE FROM PTFINFO WHERE ID=:ID"
    parameters: {"ID": "SI69379"}

- name: Delete table PTFINFO
  ibmi_sqlite3:
    database: "/tmp/testdb.sqlite3"
    sql: "DROP TABLE IF EXISTS PTFINFO"
'''

RETURN = r'''
start:
    description: The sql statement execution start time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:53.757435'
end:
    description: The sql statement execution end time.
    returned: always
    type: str
    sample: '2019-12-02 11:07:54.064969'
delta:
    description: The sql statement execution delta time.
    returned: always
    type: str
    sample: '0:00:00.307534'
row_changed:
    description: The updated row number after add/update/delete operations.
    returned: always
    type: str
    sample: 1
rows:
    description: The sql query statement result.
    returned: always
    type: list
    sample: [
      [
        "SI69375",
        "5770UME",
        "QSI69375",
        "f2342345345"
      ],
      [
        "SI69379",
        "5770DG1",
        "V7R3M0",
        "f2eqwe345345"
      ]
    ]
sql:
    description: The input sql statement executed by the task.
    returned: always
    type: str
    sample: "INSERT INTO PTFINFO (ID, PRODUCT, VRM, CHECKSUM) VALUES (:ID, :PRODUCT, :VRM, :CHECKSUM)"
parameters:
    description: The input binding parameters for the sql statement executed by the task.
    returned: always
    type: list
    sample: [
        {
            "ID": "SI69375",
            "PRODUCT": "5770UME",
            "SAVF": "QSI69375",
            "CHKSUM": "f2342345345"
        },
        {
            "ID": "SI69379",
            "PRODUCT": "5770DG1",
            "SAVF": "QSI69379",
            "CHKSUM": "f2eqwe345345"
        }
    ]
'''

from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible.module_utils.basic import AnsibleModule
import sqlite3
import datetime

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sql=dict(type='str', required=True),
            database=dict(type='str', default='/tmp/testdb.sqlite3'),
            parameters=dict(type='list', elements='dict')
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    sql = module.params['sql'].strip()
    database = module.params['database'].strip()
    parameters = module.params['parameters']

    result = dict(
        sql=sql,
        database=database,
        sqlite3Version=sqlite3.version,
        sqlite3Runtime=sqlite3.sqlite_version,
    )

    if parameters is not None:
        result['parameters'] = parameters

    startd = datetime.datetime.now()
    try:
        conn = sqlite3.connect(database)
    except sqlite3.Error as e:
        module.fail_json(msg=e.args[0], **result)
    if (conn is not None):
        c = conn.cursor()
        try:
            # multiple input parameters provided.
            if isinstance(parameters, list):
                if len(parameters) > 1:           # for better performance
                    c.executemany(sql, parameters)
                elif len(parameters) == 1:        # cannot execute SELECT statements in executemany()
                    c.execute(sql, parameters[0])
            else:                               # no input parameters provided.
                c.execute(sql)
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0], **result)
        else:
            result['row_changed'] = c.rowcount
            rows = c.fetchall()
            if len(rows) > 0:
                result['rows'] = rows
            conn.commit()
        finally:
            conn.close()

    endd = datetime.datetime.now()
    delta = endd - startd

    result['start'] = str(startd)
    result['end'] = str(endd)
    result['delta'] = str(delta)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
