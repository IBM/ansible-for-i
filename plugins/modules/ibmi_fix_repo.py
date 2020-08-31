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

HAS_REQUESTS = True

try:
    import requests
except ImportError:
    HAS_REQUESTS = False


__ibmi_module_version__ = "9.9.9"

single_ptf_table = 'single_ptf_info'
ptf_group_image_table = 'ptf_group_image_info'
ptf_group_detail_ptf_list_table = 'ptf_group_detail_ptf_list_info'
download_status_table = 'download_status'
group_web_page = 'https://www.ibm.com/support/pages/node/6211843'


single_ptf_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'product': 'CHAR(10)',
    'ptf_id': 'CHAR(10)',
    'release': 'CHAR(10)',
    'order_id': 'VARCHAR(50)',
    'file_name': 'CHAR(10)',
    'file_path': 'TEXT',
    'checksum': 'TEXT',
    'description': 'TEXT',
    'ptf_status': 'CHAR(10)',
    'download_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}

ptf_group_image_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'product': 'CHAR(10)',
    'ptf_group_number': 'CHAR(10)',
    'ptf_group_level': 'INTEGER DEFAULT 0',
    'ptf_group_status': 'CHAR(20)',
    'order_id': 'VARCHAR(50)',
    'release': 'CHAR(10)',
    'file_name': 'CHAR(10)',
    'file_path': 'TEXT',
    'checksum': 'TEXT',
    'release_date': 'TIMESTAMP',
    'description': 'TEXT',
    'download_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}


ptf_group_detail_ptf_list_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'ptf_group_id': 'INTEGER',
    'ptf_number': 'CHAR(10)',
    'ptf_status': 'CHAR(10)',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}


download_status_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'download_status': 'CHAR(20)',
    'order_id': 'CHAR(10)',
    'job_name': 'CHAR(30)',
    'file_path': 'TEXT',
    'description': 'TEXT',
    'download_start_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'download_end_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}


def getpath(dir_path):
    if dir_path.endswith('.FILE'):
        return dir_path
    if not os.path.isdir(dir_path):
        return 'FileNotFound'
    group_files = dict()
    with os.scandir(dir_path) as dirs:
        for entry in dirs:
            if entry.name.endswith('.TXT'):
                group_files['txt'] = os.path.join(dir_path, entry.name)
                group_files['txt_name'] = entry.name
            elif entry.name.endswith('.BIN'):
                group_files['image'] = os.path.join(dir_path, entry.name)
                group_files['image_name'] = entry.name
    return group_files


# file_path: /QIBM/UserData/OS/Service/ECS/PTF/2021109109/S6582.TXT
def get_group_name_from_txt(file_path):
    patten_ptf = r'[A-Z]{2}\d{5}'
    patten_group = r'(?P<group>[A-Z]{2}\d{5})\s+Level\s+(?P<level>\d+)'

    group_name = ''
    group_level = -1
    ptf_list = []

    with open(file_path, 'r') as f:
        lines = filter(None, (line.strip() for line in f))
        idx_in_group = -1

        for idx, val in enumerate(lines):
            ptf_line = re.search(patten_group, val)
            if ptf_line:
                idx_in_group = idx
                group_name = ptf_line.group('group')
                group_level = ptf_line.group('level')
            if idx == idx_in_group + 1:
                idx_in_group += 1
                ptf_line = re.search(patten_ptf, val)
                if ptf_line:
                    ptf_list.append(ptf_line.group())
                else:
                    idx_in_group = -1

    group_item = dict(
        group=group_name,
        level=group_level,
        ptf_list=ptf_list
    )
    return group_item


# url: https://www.ibm.com/support/pages/node/6211843
# group: 'SF99738'
def get_group_info_from_web(url, group):
    pattern_link = r'>(?P<rel>[A-Z]\d{3})<.+(?P<url>https?:\/\/\S+)".+>(?P<grp>[A-Z]{2}\d{5}): (?P<dsc>.+)</a>.+>(?P<lvl>\d+)<.+>.+(?P<d>\d{2}\/\d{2}\/\d{4})<'
    lines = requests.get(url).text.splitlines()
    for line in lines:
        ptf_line = re.search(pattern_link, line)
        if ptf_line:
            if group == ptf_line.group('grp'):
                group_item = dict(
                    group=ptf_line.group('grp'),
                    level=ptf_line.group('lvl'),
                    release=ptf_line.group('rel'),
                    date=ptf_line.group('d'),
                    url=ptf_line.group('url'),
                    description=ptf_line.group('dsc'),
                    # ptf_list=get_ptf_list_from_web(ptf_line.group('url'))
                )
                return group_item


# url: https://www.ibm.com/support/pages/uid/nas4SF99738
def get_ptf_list_from_web(url):
    pattern_link = r'(?P<url>https?:\/\/\S+)".+>(?P<ptf>[A-Z]{2}\d{5})<.+(?P<date>\d{2}\/\d{2}\/\d{2}).+(?P<product>\d{4}\w{3})'
    lines = requests.get(url).text.splitlines()
    ptf_list = []
    for line in lines:
        ptf_line = re.search(pattern_link, line)
        if ptf_line:
            ptf_list.append(dict(
                ptf=ptf_line.group('ptf'),
                product=ptf_line.group('product'),
                date=ptf_line.group('date'),
                url=ptf_line.group('url'),
            ))
    return ptf_list


def check_file(module, parameters, _type):
    if _type == 'ptf_group':
        group_list = []
        for parameter in parameters:
            if not parameter.get('file_path'):
                module.fail_json(msg='Required parameter [file_path] is missing in ' + str(parameter))
            group_item = dict()
            file_path = None
            for key, val in parameter.items():
                if key == 'order_id':
                    group_item['order_id'] = val
                elif key == 'file_path':
                    group_item['file_path'] = val
                    file_path = getpath(val)
                    if isinstance(file_path, dict):
                        group_item['file_name'] = file_path.get('image_name')
                        group_item['checksum'] = module.digest_from_file(file_path.get('image'), 'sha1')
            if group_item.get('checksum'):
                group_info_from_txt = get_group_name_from_txt(file_path.get('txt'))
                group_info_from_web = get_group_info_from_web(group_web_page, group_info_from_txt.get('group'))
                # below info are from the txt file
                group_item['ptf_group_number'] = group_info_from_txt.get('group')
                group_item['ptf_group_level'] = int(group_info_from_txt.get('level'))
                group_item['ptf_list'] = group_info_from_txt.get('ptf_list')
                # below info are from the web site
                group_item['release'] = group_info_from_web.get('release')
                group_item['release_date'] = group_info_from_web.get('date')
                group_item['description'] = group_info_from_web.get('description')
                group_item['url'] = group_info_from_web.get('url')
                group_list.append(group_item)
        return group_list

    elif _type == 'single_ptf':
        ptf_list = []
        for parameter in parameters:
            ptf_item = dict()
            for key, val in parameter.items():
                if key == 'ptf_id':
                    ptf_item.ptf_id = val
                elif key == 'file_path':
                    ptf_item.checksum = module.digest_from_file(val, 'sha1')
            ptf_list.append(ptf_item)
        return ptf_list


def get_constraints(_type):
    if _type == 'ptf_group':
        return 'ptf_group_number, ptf_group_level'
    elif _type == 'ptf_list':
        return 'ptf_group_id, ptf_number'
    elif _type == 'single_ptf':
        return 'ptf_id'
    elif _type == 'download_status':
        return 'order_id, file_path'


def select_table_dict(_type):
    constraints = get_constraints(_type)
    if _type == 'ptf_group':
        return ptf_group_image_table, ptf_group_image_dict, 'CONSTRAINT group_idx UNIQUE (' + constraints + ')'
    elif _type == 'ptf_list':
        return ptf_group_detail_ptf_list_table, ptf_group_detail_ptf_list_dict, 'CONSTRAINT ptf_list_idx UNIQUE (' + constraints + ')'
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
        for key, desc in table_dict.items():
            if param_key == key:
                names += key + ', '
                values += ':' + key + ', '
                if key not in constraints_list:
                    upserts += key + '=excluded.' + key + ', '
                continue
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
    for param_key in parameter.keys():
        if param_key in table_dict.keys():
            unique_keys.append(param_key)
    for unique_key in unique_keys:
        where += unique_key + '=:' + unique_key + ' AND '
    if where.endswith(' AND '):
        where = where[:-5]
        return 'SELECT * FROM {table} WHERE {where}'.format(table=table, where=where)
    else:
        return 'SELECT * FROM {table}'.format(table=table)


def init_ptf_list_table(module, database):
    conn = None
    sql = ''
    try:
        conn = sqlite3.connect(database)
        # if the database file not exist, it will be created automatically.
        if (conn is not None):
            c = conn.cursor()
            # create the table first if needed.
            sql = build_sql_init('ptf_list')
            c.execute(sql)
    except sqlite3.Error as e:
        module.fail_json(msg=e.args[0] + ' SQL:' + sql)
    finally:
        conn.commit()
        conn.close()


def clear_ptf_list_table(module, database):
    conn = sqlite3.connect(database)
    sql = ''
    try:
        table, table_dict, constraints = select_table_dict('ptf_list')
        if (conn is not None):
            c = conn.cursor()
            sql = 'DROP TABLE IF EXISTS ' + table
            c.execute(sql)
    except sqlite3.Error as e:
        module.fail_json(msg=e.args[0] + ' SQL:' + sql)
    finally:
        conn.commit()
        conn.close()


def get_id_of_group(module, database, param):
    conn = None
    id = -1
    sql = ''
    group_name = param.get('ptf_group_number')
    group_level = param.get('ptf_group_level')
    try:
        conn = sqlite3.connect(database)
        # if the database file not exist, it will be created automatically.
        if (conn is not None):
            c = conn.cursor()
            # create the table first if needed.
            sql = build_sql_init('ptf_group')
            c.execute(sql)

            table, table_dict, constraints = select_table_dict('ptf_group')
            sql = 'SELECT id FROM {table} WHERE ptf_group_number="{ptf_group_number}" AND ptf_group_level="{ptf_group_level}"'.format(
                table=table, ptf_group_number=group_name, ptf_group_level=group_level)
            c.execute(sql)
            rs = c.fetchone()
            if rs is not None and len(rs) > 0:
                id = int(rs[0])
            else:
                id = -1
    except sqlite3.Error as e:
        module.fail_json(msg=e.args[0] + ' SQL:' + sql)
    finally:
        conn.commit()
        conn.close()
    return id


def find_ptf_list_of_group(module, database, param):
    conn = None
    sql = ''
    ptf_list = []
    id = get_id_of_group(module, database, param)
    if id >= 0:
        try:
            init_ptf_list_table(module, database)
            conn = sqlite3.connect(database)
            if (conn is not None):
                c = conn.cursor()
                table, table_dict, constraints = select_table_dict('ptf_list')
                sql = 'SELECT ptf_number FROM {table} WHERE ptf_group_id={id}'.format(table=table, id=id)
                c.execute(sql)
                rs = c.fetchall()
                if isinstance(rs, list) and len(rs) > 0:
                    for ptf in rs:
                        ptf_list.append(ptf[0])
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0] + ' SQL:' + sql)
        finally:
            conn.commit()
            conn.close()
    return ptf_list


def upsert_ptf_list_of_group(module, database, param):
    conn = None
    row_changed = -1
    id = get_id_of_group(module, database, param)
    if id >= 0:
        try:
            ptf_list = param.get('ptf_list')
            init_ptf_list_table(module, database)
            conn = sqlite3.connect(database)
            if (conn is not None):
                c = conn.cursor()
                rows = []
                for ptf in ptf_list:
                    row = dict(
                        ptf_group_id=id,
                        ptf_number=ptf,
                        ptf_status='',
                    )
                    rows.append(row)
                sql = build_sql_udpate('ptf_list', rows)
                c.executemany(sql, rows)
                row_changed = c.rowcount
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0] + ' SQL:' + sql)
        finally:
            conn.commit()
            conn.close()
    return row_changed


def delete_ptf_list_of_group(module, database, param):
    conn = None
    sql = ''
    row_changed = -1
    id = get_id_of_group(module, database, param)
    if id >= 0:
        try:
            conn = sqlite3.connect(database)
            if (conn is not None):
                c = conn.cursor()
                rows = []
                row = dict(ptf_group_id=id,)
                rows.append(row)
                sql = build_sql_delete('ptf_list', rows)
                c.execute(sql, row)
                row_changed = c.rowcount
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0] + ' SQL:' + sql)
        finally:
            conn.commit()
            conn.close()
    return row_changed


def run_ptf_list_sql(module, database, parameters, action, rows):
    if action == 'clear':
        clear_ptf_list_table(module, database)
        return []
    elif isinstance(rows, list):
        if action == 'find':
            for row in rows:
                row['ptf_list'] = find_ptf_list_of_group(module, database, row)
            return rows
        elif action == 'add' or action == 'update':
            for param in parameters:
                upsert_ptf_list_of_group(module, database, param)
        elif action == 'delete':
            for param in parameters:
                group_item = dict(
                    ptf_group_number=param.get('ptf_group_number'),
                    ptf_group_level=param.get('ptf_group_level'),
                )
                delete_ptf_list_of_group(module, database, group_item)
        return []


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
                                rs[0]['db_record'] = 'Match'
                                success_list.append(rs[0])
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
            module.fail_json(msg=e.args[0] + ' SQL:' + sql)
        finally:
            conn.commit()
            conn.close()

        if _type == 'ptf_group':
            success_list = run_ptf_list_sql(module, database, parameters, action, success_list)

        return 0, '', c.rowcount, success_list, fail_list, sql


# This is only called on action insert or update
def checksum_before_upsert(_type, list_from_db, list_from_file):
    for db_item in list_from_db:
        for file_item in list_from_file:
            if (
                (_type == 'ptf_group' and
                 db_item.get('ptf_group_number') == file_item.get('ptf_group_number') and
                 db_item.get('ptf_group_level') == file_item.get('ptf_group_level'))
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
    if not list_from_file:
        return list_from_db, []
    success_list = []
    fail_list = []
    for db_item in list_from_db:
        for file_item in list_from_file:
            if _type == 'ptf_group':
                if db_item.get('ptf_group_number') == file_item.get('ptf_group_number') and \
                   db_item.get('ptf_group_level') == file_item.get('ptf_group_level'):
                    # if the input checksum not match with the calculated checksum,
                    # mark the ptf_group_status label.
                    if db_item.get('checksum') == file_item.get('checksum'):
                        db_item['db_record'] = 'Match'
                        success_list.append(db_item)
                    else:
                        if file_item.get('checksum'):
                            db_item['db_record'] = 'FileNotMatch'
                        else:
                            db_item['db_record'] = 'FileNotFound'
                        fail_list.append(db_item)
                    break
            elif _type == 'single_ptf':
                new_item = db_item.copy()
                if db_item.get('ptf_id') == file_item.get('ptf_id'):
                    if new_item.get('checksum') == file_item.get('checksum'):
                        new_item['ptf_status'] = 'Match'
                        success_list.append(new_item)
                    else:
                        if file_item.get('checksum'):
                            new_item['ptf_status'] = 'FileNotMatch'
                        else:
                            new_item['ptf_status'] = 'FileNotFound'
                        fail_list.append(db_item)
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

    result = dict(
        action=action,
        database=database,
        checksum=checksum,
        sqlite3Version=sqlite3.version,
        sqlite3Runtime=sqlite3.sqlite_version,
    )

    row_changed = -1
    success_list = []
    fail_list = []
    list_from_file = []
    sql = ''

    startd = datetime.datetime.now()
    # for adding a new records, checking file's checksum is always needed.
    if action == 'add':
        checksum = True
    if _type == 'download_status':
        checksum = False
    # for adding/updating records, need to retrieve file's checksum before any SQL operations.
    if checksum is True and (action == 'add' or action == 'update'):
        # filter out the file not existing or matching the input param
        list_from_file = check_file(module, parameters, _type)
        if _type == 'ptf_group' and len(list_from_file) > 0:
            # update input params with list_from_file
            if action == 'add':  # all the info come from the physical files.
                parameters = list_from_file
            elif action == 'update':  # merge the info from the db records and the physical files.
                parameters = checksum_before_upsert(_type, parameters, list_from_file)
    if parameters is not None:
        result['parameters'] = parameters
    if _type is not None:
        result['type'] = _type

    rc, msg, row_changed, success_list, fail_list, sql = run_sql(module, database, parameters, action, _type)
    if rc != 0:
        module.fail_json(msg=msg, **result)

    endd = datetime.datetime.now()
    delta = endd - startd
    fail_list_from_file = []

    if row_changed >= 0:
        result['row_changed'] = row_changed
    if len(success_list) > 0:  # only for action = 'find'
        if checksum is True:
            # for action 'find', checking physical files can only be done when the DB query has been done.
            # because we need the file_path parameter for checksum
            list_from_file = check_file(module, success_list, _type)
            success_list_from_file, fail_list_from_file = checksum_after_find(_type, success_list, list_from_file)  # add the ptf_list info of group
            result['success_list'] = success_list_from_file
        else:
            result['success_list'] = success_list
    if len(fail_list) > 0 or len(fail_list_from_file) > 0:
        result['fail_list'] = fail_list + fail_list_from_file

    result['sql'] = sql
    result['start'] = str(startd)
    result['end'] = str(endd)
    result['delta'] = str(delta)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
