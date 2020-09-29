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
module: ibmi_fix_repo
short_description: Manipulate the PTF database via sqlite3
version_added: '2.8.0'
description:
     - The C(ibmi_fix_repo) module manipulate the PTF database via sqlite3.
     - Required dependencies are C(SQLite3 >= 3.26) and python module C(requests).
     - Install them using C(yum install libsqlite3) and C(pip3 install requests)
options:
  action:
    description:
      - The action the C(ibmi_fix_repo) module takes towards the PTF database.
      - C(add), C(update), C(find), C(delete) or C(clear).
    type: str
    required: yes
  type:
    description:
      - The type of the target, C(single_ptf), C(ptf_group) or C(download_status).
    type: str
  checksum:
    description:
      - Specified if check the ptf/group image files as well when checking database
    type: bool
    default: False
  database:
    description:
      - Specified database file name, e.g. '/tmp/testdb.sqlite3'
    type: str
    default: '/tmp/testdb.sqlite3'
  parameters:
    description:
      - The binding parameters for the action executed by the task.
    type: list
    elements: dict

author:
- Xu Meng(@dmabupt)
'''

EXAMPLES = r'''
- name: add some group records
  ibmi_fix_repo:
    database: '/tmp/testdb.sqlite3'
    action: 'add'
    type: 'ptf_group'
    checksum: true
    parameters:
      - {'order_id':'2020579181', 'file_path':'/QIBM/UserData/OS/Service/ECS/PTF/2020579181'}
- name: query some PTFs records
  ibmi_fix_repo:
    database: "/tmp/testdb.sqlite3"
    action: "find"
    type: 'ptf_group'
    parameters:
      - {'ptf_group_number':'SF99738', 'ptf_group_level':'10'}
- name: delete some PTFs records
  ibmi_fix_repo:
    database: "/tmp/testdb.sqlite3"
    action: "delete"
    type: 'ptf_group'
    parameters:
      - {'ptf_group_number':'SF99738', 'ptf_group_level':'10'}
- name: run sql to drop the table
  ibmi_fix_repo:
    database: "/tmp/testdb.sqlite3"
    action: "clear"
    type: 'ptf_group'
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
    returned: when action is 'update', 'add' or 'delete'
    type: str
    sample: 1
rows:
    description: The result of the found PTFs.
    returned: when action is 'find'
    type: list
    elements: dict
    sample: [
        {
            "add_time": "2020-08-17 00:26:01",
            "checksum": "d02367d07c5ef43a5722a1ad2c36034409aad2fe",
            "description": "SF99738 740 Group Security",
            "download_time": "2020-08-17 00:26:01",
            "file_name": "S6582V01.BIN",
            "file_path": "/QIBM/UserData/OS/Service/ECS/PTF/2020579181",
            "id": 1,
            "order_id": "2020579181",
            "product": null,
            "ptf_group_level": 10,
            "ptf_group_number": "SF99738",
            "ptf_group_status": null,
            "ptf_list": [
                "SI69187",
                "SI69189",
                "SI69886",
                "SI70103",
                "SI70725",
                "SI70734",
                "SI70767",
                "SI70819",
                "SI70961",
                "SI71097",
                "SI71746",
                "SI72577",
                "SI72646",
                "SI73284",
                "SI73415",
                "SI73430",
                "SI73482"
            ],
            "release": "R740",
            "release_date": "07/07/2020"
        }
    ]
sql:
    description: The formated sql statement executed by the task.
    returned: always
    type: str
    sample: "SELECT * FROM ptf_group_image_info WHERE ptf_group_number=:ptf_group_number AND ptf_group_level=:ptf_group_level"
parameters:
    description: The input binding parameters for the sql statement executed by the task.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "ptf_group_level": "10",
            "ptf_group_number": "SF99738"
        }
    ]
'''

from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible.module_utils.basic import AnsibleModule
import os
import sqlite3
import datetime
import re
import json


__ibmi_module_version__ = "1.1.2"

single_ptf_table = 'single_ptf_info'
ptf_group_image_table = 'ptf_group_image_info'
download_status_table = 'download_status'


single_ptf_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'ptf_id': 'CHAR(10)',
    'order_id': 'VARCHAR(50)',
    'file_path': 'TEXT',
    'file_name': 'CHAR(10)',
    'product': 'CHAR(10)',
    'release': 'CHAR(10)',
    'description': 'TEXT',
    'checksum': 'TEXT',
    'ptf_status': 'CHAR(10)',
    'download_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}


ptf_group_image_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'order_id': 'VARCHAR(50)',
    'file_path': 'TEXT',
    'ptf_group_number': 'CHAR(10)',
    'ptf_group_level': 'INTEGER DEFAULT 0',
    'release_date': 'TIMESTAMP',
    'release': 'CHAR(10)',
    'description': 'TEXT',
    'url': 'TEXT',
    'ptf_list': 'TEXT',
    'file_name': 'CHAR(10)',
    'checksum': 'TEXT',
    'ptf_group_status': 'CHAR(20)',
    'download_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}


download_status_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'download_status': 'CHAR(20)',
    'order_id': 'CHAR(10)',
    'job_name': 'CHAR(30)',
    'file_path': 'TEXT',
    'description': 'TEXT',
    'ptf_group_number': 'CHAR(10)',
    'ptf_group_level': 'INTEGER DEFAULT 0',
    'release_date': 'TIMESTAMP',
    'download_start_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'download_end_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}


required_params_enable_checksum = {
    'single_ptf': ['file_path', 'ptf_id', 'product'],
    'ptf_group': ['file_path', 'ptf_group_number', 'ptf_group_level', 'release_date'],
    'download_status': ['file_path', 'order_id'],
}


required_params_disable_checksum = {
    'single_ptf': ['ptf_id', 'product'],
    'ptf_group': ['ptf_group_number', 'ptf_group_level', 'release_date'],
    'download_status': ['order_id'],
}


def get_constraints(_type):
    return ','.join(required_params_disable_checksum.get(_type))


def json2obj(json_str):
    if isinstance(json_str, str):
        return json.loads(json_str)
    return json_str


def obj2json(obj):
    if isinstance(obj, str):
        return obj
    return json.dumps(obj, separators=(',', ':'))


def getpath(dir_path):
    if dir_path.endswith('.FILE'):
        return dir_path
    if not os.path.isdir(dir_path):
        return 'FileNotFound'
    downloaded_files = dict(
        txt='',
        images=[]
    )
    cum_txt = None
    with os.scandir(dir_path) as dirs:
        for entry in dirs:
            if entry.name.endswith('.TXT'):
                downloaded_files['txt'] = os.path.join(dir_path, entry.name)
            elif entry.name.endswith('.txt'):
                cum_txt = os.path.join(dir_path, entry.name)
            elif entry.name.endswith('.BIN') or entry.name.endswith('.bin'):
                downloaded_files['images'].append(os.path.join(dir_path, entry.name))
    if cum_txt:  # this is a cum directory
        downloaded_files['txt'] = cum_txt
    return downloaded_files


# file_path: /QIBM/UserData/OS/Service/ECS/PTF/2021109109/S6582.TXT
def get_group_name_from_txt(file_path):
    pattern_ptf = r'[A-Z]{2}\d{5}'
    pattern_group = r'(?P<group>[A-Z]{2}\d{5})\s+Level\s+(?P<level>\d+)'
    pattern_vrm = r'VERSION\s+(?P<v>\d+)\s+RELEASE\s+(?P<r>\d+)\.(?P<m>\d+)'

    group_name = None
    group_level = -1
    vrm = None
    idx_in_group = -100
    ptf_list = []
    lines = []

    with open(file_path, 'r') as f:
        lines += filter(None, (line.strip() for line in f))

    for idx, val in enumerate(lines):
        if vrm is None:
            vrm_line = re.search(pattern_vrm, val)
            if vrm_line:
                vrm = 'V' + vrm_line.group('v') + 'R' + vrm_line.group('r') + 'M' + vrm_line.group('m')
        if group_name is None:
            ptf_line = re.search(pattern_group, val)
            if ptf_line:
                idx_in_group = idx
                group_name = ptf_line.group('group')
                group_level = ptf_line.group('level')
        if idx == idx_in_group + 1:
            idx_in_group += 1
            ptf_line = re.search(pattern_ptf, val)
            if ptf_line:
                ptf_list.append(ptf_line.group())
            else:
                break

    group_item = dict(
        group=group_name,
        level=group_level,
        vrm=vrm,
        ptf_list=obj2json(ptf_list)
    )
    return group_item


# check invalid input parameters
def check_param(module, parameters, _type, checksum):
    success_list = []
    fail_list = []
    required_params = required_params_disable_checksum.get(_type)
    if checksum is True:
        required_params = required_params_enable_checksum.get(_type)
    for parameter in parameters:
        group_item = parameter.copy()
        rc = 0
        for required_param in required_params:
            if not parameter.get(required_param):
                group_item['msg'] = 'Required parameter [' + required_param + '] is missing in parameters'
                rc = -1
                group_item['rc'] = rc
                fail_list.append(group_item)
                break
        if rc < 0:
            continue
        if isinstance(group_item.get('ptf_list'), list):
            group_item['ptf_list'] = obj2json(parameter.get('ptf_list'))
        if isinstance(group_item.get('ptf_group_level'), str):
            group_item['ptf_group_level'] = int(parameter.get('ptf_group_level'))
        success_list.append(group_item)
    return success_list, fail_list


# append checksum data from files to the parameter list
def check_sum(module, parameters, _type):
    success_list = []
    fail_list = []
    if _type == 'ptf_group':
        for parameter in parameters:
            # if input parameters at least contains order_id and file_path, check the files now
            group_item = dict()
            if not parameter.get('file_path'):
                group_item['msg'] = 'Required parameter [file_path] is missing'
                group_item['rc'] = -1
                fail_list.append(group_item)
                continue
            if parameter.get('order_id'):
                group_item['order_id'] = parameter.get('order_id')
            path = parameter.get('file_path')
            group_item['file_path'] = path
            path_object = getpath(path)
            if not isinstance(path_object, dict):
                group_item['msg'] = 'Specified image path [' + path + '] is not a valid directory'
                group_item['rc'] = -2
                fail_list.append(group_item)
                continue
            image_paths = path_object.get('images')
            checksums = []
            file_names = []
            rc = 0
            for image_path in image_paths:
                checksum = module.sha1(image_path)
                file_name = os.path.basename(image_path)
                if not checksum:
                    group_item['msg'] = 'Target image file [' + image_path + '] is not readable'
                    rc = -3
                    group_item['rc'] = rc
                    fail_list.append(group_item)
                    break
                checksums.append(file_name + ':' + checksum)
                file_names.append(file_name)
            if rc < 0:
                continue
            group_item['checksum'] = obj2json(checksums)
            group_item['file_name'] = obj2json(file_names)
            if parameter.get('release_date'):
                group_item['release_date'] = parameter.get('release_date')
            if parameter.get('description'):
                group_item['description'] = parameter.get('description')
            if parameter.get('url'):
                group_item['url'] = parameter.get('url')

            group_info_from_txt = get_group_name_from_txt(path_object.get('txt'))
            group_item['ptf_group_number'] = group_info_from_txt.get('group')
            group_item['ptf_group_level'] = int(group_info_from_txt.get('level'))
            if group_item.get('ptf_group_number') == parameter.get('ptf_group_number') and \
                    group_item.get('ptf_group_level') == int(parameter.get('ptf_group_level')):
                if parameter.get('release'):
                    group_item['release'] = parameter.get('release')
                if parameter.get('ptf_list'):
                    group_item['ptf_list'] = obj2json(parameter.get('ptf_list'))
            else:
                group_item['release'] = group_info_from_txt.get('vrm')
                group_item['ptf_list'] = obj2json(group_info_from_txt.get('ptf_list'))
            success_list.append(group_item)
    elif _type == 'single_ptf':
        for parameter in parameters:
            # if input parameters are valid, check the file now
            ptf_item = parameter.copy()
            path = parameter.get('file_path')
            ptf_item['file_name'] = os.path.basename(path)
            ptf_item['checksum'] = module.sha1(path)
            if not ptf_item.get('checksum'):
                ptf_item['msg'] = 'Target image file [' + path + '] is not readable'
                ptf_item['rc'] = -3
                fail_list.append(ptf_item)
                continue
            success_list.append(ptf_item)
    return success_list, fail_list


def select_table_dict(_type):
    constraints = get_constraints(_type)
    if _type == 'ptf_group':
        return ptf_group_image_table, ptf_group_image_dict, 'CONSTRAINT group_idx UNIQUE (' + constraints + ')'
    elif _type == 'single_ptf':
        return single_ptf_table, single_ptf_dict, 'UNIQUE (' + constraints + ')'
    elif _type == 'download_status':
        return download_status_table, download_status_dict, 'CONSTRAINT download_status_idx UNIQUE (' + constraints + ')'


def build_sql_init(_type):
    table, table_dict, constraints = select_table_dict(_type)
    fields = ''
    for item in table_dict.items():
        fields += '%s %s, ' % item
    sql = 'CREATE TABLE IF NOT EXISTS {table} ({fields} {constraints})'.format(
        table=table, fields=fields, constraints=constraints)
    return sql


def build_sql_udpate(_type, parameters):
    table, table_dict, constraints = select_table_dict(_type)
    names = ''
    values = ''
    upserts = ''
    conflictions = ''
    constraints = get_constraints(_type)
    constraints_list = constraints.split(', ')
    for param_key in parameters[0].keys():
        if param_key in table_dict.keys():
            names += param_key + ', '
            values += ':' + param_key + ', '
            if param_key not in constraints_list:
                upserts += param_key + '=excluded.' + param_key + ', '
    if upserts != '':
        conflictions = 'ON CONFLICT({constraints}) DO UPDATE SET {upserts}'.format(
            constraints=constraints, upserts=upserts.rstrip(', '))
    return 'INSERT INTO {table} ({name}) VALUES({value}) {conflictions}'.format(
        table=table, name=names.rstrip(', '), value=values.rstrip(', '), conflictions=conflictions)


def build_sql_delete(_type, parameters):
    table, table_dict, constraints = select_table_dict(_type)
    unique_keys = []
    where = ''
    for param_key in parameters[0].keys():
        if param_key in table_dict.keys():
            unique_keys.append(param_key)
    for unique_key in unique_keys:
        where += unique_key + '=:' + unique_key + ' AND '
    if where.endswith(' AND '):
        where = where[:-5]
    return 'DELETE FROM {table} WHERE {where}'.format(table=table, where=where)


def build_sql_find(_type, parameter):
    table, table_dict, constraints = select_table_dict(_type)
    unique_keys = []
    where = ''
    additional_param = ''
    for param_key in parameter.keys():
        if param_key in table_dict.keys():
            unique_keys.append(param_key)
        if param_key == 'additional_param':
            additional_param = parameter.get(param_key)
    for unique_key in unique_keys:
        where += unique_key + '=:' + unique_key + ' AND '
    if where.endswith(' AND '):
        where = where[:-5]
        return 'SELECT * FROM {table} WHERE {where} {additional_param}'.format(table=table, where=where, additional_param=additional_param)
    else:
        return 'SELECT * FROM {table} {additional_param}'.format(table=table, additional_param=additional_param)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def run_sql(module, database, parameters, action, _type):
    sql = ''
    success_list = []
    fail_list = []
    table, table_dict, constraints = select_table_dict(_type)
    try:
        conn = sqlite3.connect(database)
        # if the database file not exist, it will be created automatically.
    except sqlite3.Error as e:
        module.fail_json(msg=e.args[0])

    if (conn is not None):
        c = conn.cursor()
        # create the table first if needed.
        sql = build_sql_init(_type)
        c.execute(sql)

        if action == 'add' or action == 'update':
            sql = build_sql_udpate(_type, parameters)
        elif action == 'delete':
            sql = build_sql_delete(_type, parameters)
        elif action == 'clear':
            sql = 'DROP TABLE IF EXISTS ' + table
        elif action != 'find':
            return -2, 'Unsupported action: ' + action, -1, success_list, fail_list, sql
        try:
            if isinstance(parameters, list):
                if action == 'find':  # cannot execute SELECT statements in executemany()
                    c.row_factory = dict_factory
                    for param in parameters:
                        sql = build_sql_find(_type, param)
                        c.execute(sql, param)
                        rs = c.fetchall()
                        if isinstance(rs, list):
                            if len(rs) > 0:
                                for row in rs:
                                    row['db_record'] = 'Match'
                                    if row.get('ptf_list'):
                                        row['ptf_list'] = json2obj(row.get('ptf_list'))
                                    elif row.get('ptf_group_level'):
                                        row['ptf_group_level'] = int(row.get('ptf_group_level'))
                                    if _type == 'ptf_group':
                                        if row.get('checksum'):
                                            row['checksum'] = json2obj(row.get('checksum'))
                                        if row.get('file_name'):
                                            row['file_name'] = json2obj(row.get('file_name'))
                                    success_list.append(row)
                            else:
                                fail_item = param.copy()
                                fail_item['db_record'] = 'RecordNotFound'
                                fail_list.append(fail_item)
                        else:
                            fail_item = param.copy()
                            fail_item['db_record'] = 'Unknown'
                            fail_list.append(fail_item)
                else:
                    c.executemany(sql, parameters)
            else:  # clear/init tables (no param)
                c.execute(sql)
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0] + ' ***SQL:' + sql + ' ***Param:' + str(parameters))
        finally:
            conn.commit()
            conn.close()

        return 0, '', c.rowcount, success_list, fail_list, sql


# This is only called on action insert or update
def checksum_before_upsert(_type, list_from_db, list_from_file):
    for db_item in list_from_db:
        for file_item in list_from_file:
            if (
                (_type == 'ptf_group' and db_item.get('ptf_group_number') == file_item.get('ptf_group_number') and
                 int(db_item.get('ptf_group_level')) == int(file_item.get('ptf_group_level')))
                or
                (_type == 'single_ptf' and
                 db_item.get('ptf_id') == file_item.get('ptf_id'))
            ):
                for key, val in file_item.items():
                    # if the input checksum not match with the calculated checksum,
                    # override the input with the real checksum for the db record and no error thrown.
                    if db_item.get(key) is None or db_item.get(key) != val:
                        db_item[key] = val
    return list_from_db


# This is only called on action find
def checksum_after_find(_type, list_from_db, list_from_file):
    success_list = []
    fail_list = []
    if not list_from_file or len(list_from_file) == 0:
        for db_item in list_from_db:
            db_item['db_record'] = 'FileNotFound'
            fail_list.append(db_item)
        return success_list, fail_list
    for db_item in list_from_db:
        for file_item in list_from_file:
            if _type == 'ptf_group':
                if db_item.get('ptf_group_number') == file_item.get('ptf_group_number') and \
                   int(db_item.get('ptf_group_level')) == int(file_item.get('ptf_group_level')):
                    # if the input checksum not match with the calculated checksum
                    db_item_checksum = json2obj(db_item.get('checksum'))
                    file_item_checksum = json2obj(file_item.get('checksum'))
                    if [i for i in db_item_checksum if i not in file_item_checksum] == []:
                        db_item['db_record'] = 'Match'
                        db_item['checksum'] = file_item_checksum
                        success_list.append(db_item)
                    else:
                        if file_item.get('checksum'):
                            db_item['db_record'] = 'FileNotMatch'
                        else:
                            db_item['db_record'] = 'FileNotFound'
                        db_item['checksum'] = db_item_checksum
                        fail_list.append(db_item)
                    break
            elif _type == 'single_ptf':
                new_item = db_item.copy()
                if db_item.get('ptf_id') == file_item.get('ptf_id'):
                    if new_item.get('checksum') == file_item.get('checksum'):
                        new_item['db_record'] = 'Match'
                        success_list.append(new_item)
                    else:
                        if file_item.get('checksum'):
                            new_item['db_record'] = 'FileNotMatch'
                        else:
                            new_item['db_record'] = 'FileNotFound'
                        fail_list.append(new_item)
                    break

    return success_list, fail_list


def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(type='str', required=True),
            type=dict(type='str'),
            database=dict(type='str', default='/tmp/testdb.sqlite3'),
            parameters=dict(type='list', elements='dict'),
            checksum=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    action = module.params['action'].strip().lower()
    _type = module.params['type']
    database = module.params['database'].strip()
    parameters = module.params['parameters']
    checksum = module.params['checksum']

    if action == 'delete' or _type == 'download_status':
        checksum = False

    result = dict(
        action=action,
        database=database,
        checksum=checksum,
        type=_type,
        parameters=parameters,
        sqlite3Version=sqlite3.version,
        sqlite3Runtime=sqlite3.sqlite_version,
    )

    row_changed = -1
    success_list = []
    fail_list = []
    invalid_parameters = []
    fail_list_before_run_sql = []
    fail_list_after_run_sql = []
    list_to_sqlite = []
    sql = ''

    startd = datetime.datetime.now()

    # for adding/updating records, retrieve file's checksum first when checksum == True.
    if action == 'add' or action == 'update':
        # filter out the invalid parameters without required input parameters
        valid_parameters, invalid_parameters = check_param(module, parameters, _type, checksum)
        if checksum is True:  # filter out the not existing files
            valid_parameters, fail_list_before_run_sql = check_sum(module, valid_parameters, _type)
        if len(valid_parameters) > 0:
            if action == 'add':  # all the parameter data come from the physical files.
                list_to_sqlite = valid_parameters
            elif action == 'update':  # merge the data the physical files into db records as new paramters.
                list_to_sqlite = checksum_before_upsert(_type, parameters, valid_parameters)
        else:
            result['fail_list'] = invalid_parameters + fail_list_before_run_sql
            module.exit_json(**result)
    else:
        list_to_sqlite = parameters
    if action == 'clear' or len(list_to_sqlite) > 0:
        rc, msg, row_changed, success_list, fail_list, sql = run_sql(module, database, list_to_sqlite, action, _type)
        if rc != 0:
            module.fail_json(msg=msg, **result)

        if isinstance(row_changed, int):
            result['row_changed'] = row_changed
        if len(success_list) > 0:  # only for action = 'find'
            # check physical files when the query has been done.
            # because we need the file_path parameter for checksum
            if checksum is True:
                # check_sum returns the checksums of the input list. But it does not compare it.
                # if all the image files exist, fail_list_not_existing_files is empty.
                success_list_existing_files, fail_list_not_existing_files = check_sum(module, success_list, _type)
                # checksum_after_find compares the checksums with the database records.
                # if all parameters' checksums are matched, fail_list_checksum_mismatched is empty
                # it also adds the PTF lists of groups to the result.
                success_list_checksum_matched, fail_list_checksum_mismatched = checksum_after_find(_type, success_list, success_list_existing_files)
                fail_list_after_run_sql = fail_list_not_existing_files + fail_list_checksum_mismatched
                result['success_list'] = success_list_checksum_matched
            else:
                result['success_list'] = success_list
    if len(fail_list) > 0 or len(invalid_parameters) > 0 or len(fail_list_before_run_sql) > 0 or len(fail_list_after_run_sql) > 0:
        result['fail_list'] = fail_list + invalid_parameters + fail_list_before_run_sql + fail_list_after_run_sql

    endd = datetime.datetime.now()
    delta = endd - startd
    result['sql'] = sql
    result['start'] = str(startd)
    result['end'] = str(endd)
    result['delta'] = str(delta)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
