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
module: ibmi_fix_repo_lv1
short_description: Manipulate the PTF database via sqlite3
version_added: '1.1.0'
description:
     - The C(ibmi_fix_repo_lv1) module manipulate the PTF database via sqlite3.
     - Required dependency is C(SQLite3 >= 3.26).
     - Install it using C(yum install libsqlite3)
options:
  action:
    description:
      - The action the C(ibmi_fix_repo_lv1) module takes towards the PTF database.
      - C(refresh), C(list), C(find) or C(clear).
    type: str
    required: yes
  image_root:
    description:
      - The image_root of the image files.
    type: str
  additional_sql:
    description:
      - The additional sql appended to the query for action 'find'.
    type: str
  checksum:
    description:
      - Specified if check the image file's integrity when action is 'find' or 'list'
    type: bool
    default: False
  database:
    description:
      - Specified database file name, e.g. '/tmp/testdb.sqlite3'
    type: str
    default: '/etc/ibmi_ansible/fix_management/repo_lv1.sqlite3'
  parameters:
    description:
      - The query parameters for the 'find' action executed by the task.
    type: list
    elements: dict
  fields:
    description:
      - The expected output column names of the query result for the 'find' action.
    type: list
    elements: str

author:
- Xu Meng(@dmabupt)
'''

EXAMPLES = r'''
- name: scan the PTF images root and refresh the database records
  ibmi_fix_repo_lv1:
    action: 'refresh'
    image_root: '/home/you/PTF'
- name: query some PTF records
  ibm.power_ibmi.ibmi_fix_repo_lv1:
    action: "find"
    checksum: true
    additional_sql: 'WHERE image_type IS NOT "single_ptf" ORDER BY ordered_ptf_count'
    fields:
      - 'image_type'
      - 'image_path'
      - 'ordered_ptf_count'
    parameters:
      - {'group':'SF99738', 'level':'10'}
      - {"group": "SF99876"}
      - {"ptf": "SI77631"}
      - {"shipped_ptf": "SI50077"}
- name: list all PTF records from database
  ibmi_fix_repo_lv1:
    action: 'list'
    additional_sql: 'WHERE image_type IS NOT "cum" ORDER BY download_date DESC'
- name: clear the PTF database
  ibm.power_ibmi.ibmi_fix_repo_lv1:
    action: "clear"
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
    description: The updated row number after refresh operations.
    returned: when action is 'refresh'
    type: str
    sample: 1
success_list:
    description: The result of the found PTFs.
    returned: when action is 'find' or 'list'
    type: list
    elements: dict
    sample: [
        {
            "query_item": {
                "shipped_ptf": "SI50077"
            },
            "query_result": [
                {
                    "image_files": [
                        {
                            "expected_chksum": "672d1e85aa70a79c705bbe7fffd50aad9698428f83c5fae0f2e16f508df8cba8",
                            "file": "SI77271B_1.bin",
                            "file_chksum": "672d1e85aa70a79c705bbe7fffd50aad9698428f83c5fae0f2e16f508df8cba8",
                            "integrity": true
                        }
                    ],
                    "image_path": "/home/pengzy/PTF/singleptf/SI77271SI77631",
                    "image_type": "single_ptf",
                    "ordered_ptf_count": 2
                }
            ]
        }
    ]
sql:
    description: The formatted sql statement executed by the task.
    returned: always
    type: str
    sample: "SELECT image_type,image_path,ordered_ptf_count,image_files,ordered_ptf,shipped_ptf FROM ptf_repo_lv1_info"
parameters:
    description: The input query parameters for the sql statement executed by the task.
    returned: always
    type: list
    elements: dict
    sample: [
        {
            "shipped_ptf": "SI50077"
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


__ibmi_module_version__ = "2.0.1"

images = []
ptf_repo_lv1_table = 'ptf_repo_lv1_info'
ptf_repo_lv1_dict = {
    'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
    'order_id': 'CHAR(10)',
    'download_date': 'CHAR(20)',
    'image_path': 'TEXT NOT NULL UNIQUE',
    'image_type': 'CHAR(10)',
    'image_files': 'JSON',
    'cum_id': 'CHAR(10)',
    'cum_vrm': 'CHAR(10)',
    'ordered_ptf': 'JSON',
    'ordered_ptf_count': 'INTEGER',
    'shipped_ptf': 'JSON',
    'shipped_ptf_count': 'INTEGER',
    'add_time': 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP',
}
list_image_dict = [
    'order_id',
    'download_date',
    'image_type',
    'image_path',
    'image_files',
    'ordered_ptf',
    'ordered_ptf_count',
    'shipped_ptf_count',
]


def get_checksum_in_txt(sha256_file):
    if not os.path.isfile(sha256_file):
        return None

    chksum_pattern = r'^\((?P<file>\S+)\)\=\s*(?P<chksum>[a-z0-9]{64})$'
    chksum_info_all = []
    lines = []

    with open(sha256_file, 'r', encoding="utf-8") as f:
        lines += filter(None, (line.strip() for line in f))

    for idx, val in enumerate(lines):
        chksum_line = re.search(chksum_pattern, val)
        if chksum_line:
            chksum_info = dict(
                file=chksum_line.group('file'),
                expected_chksum=chksum_line.group('chksum')
            )
            chksum_info_all.append(chksum_info)

    if len(chksum_info_all) > 0:
        return chksum_info_all
    else:
        return None


def get_common_info_from_txt(lines):
    pattern_order = r'Order#:\s+(?P<order>\w{6,10})'
    pattern_date = r'Date:\s+(?P<date>\d{4}/\d{1,2}/\d{1,2})'

    pattern_ordered_ptf = r'(?P<ptf>[A-Z]{2}\d{5})\s+ORDERED\s+<<< Shipped >>>\s+(?P<product>\S{7})\s+(?P<vrm>V\d+R\d+M\d+)'
    pattern_group = r'(?P<group>[A-Z]{2}\d{5})\s+Level\s+(?P<level>\d+)'
    pattern_vrm = r'(?P<group>[A-Z]{2}\d{5}).+<<< Shipped >>>\s+SEL Lst\s+(?P<vrm>V\d+R\d+M\d+)'
    pattern_cum_vrm = r'VERSION\s+(?P<v>\d+)\s+RELEASE\s+(?P<r>\d+)\.(?P<m>\d+)'
    pattern_cumid = r'PACKAGE ID:\s+(?P<cum_id>\w+)'
    pattern_shipped_ptf = r'(?P<ptf>[A-Z]{2}\d{5}).+<<< Shipped >>>\s+(?P<product>\S{7})\s+(?P<vrm>V\d+R\d+M\d+)'
    pattern_ptf = r'[A-Z]{2}\d{5}'

    order_str = None
    date_str = None
    idx_in_group = -100
    cum_id = None
    cum_vrm = None
    ordered_group = []
    group_set = set(ordered_group)
    group_vrm = []
    ordered_ptf = []
    shipped_ptf = []

    for idx, val in enumerate(lines):
        if date_str is None:
            date_line = re.search(pattern_date, val)
            if date_line:
                date_str = date_line.group('date')
        if order_str is None:
            order_line = re.search(pattern_order, val)
            if order_line:
                order_str = order_line.group('order')
        # search group_name:
        ptf_line = re.search(pattern_group, val)
        if ptf_line:
            idx_in_group = idx
            group_level_info = dict(
                group=ptf_line.group('group'),
                level=int(ptf_line.group('level')),
                release=None,
            )
            # avoid adding duplicated group item
            if ptf_line.group('group') not in group_set:
                group_set.add(ptf_line.group('group'))
                ordered_group.append(group_level_info)
        # add children PTFs of current group
        if idx == idx_in_group + 1:
            idx_in_group += 1
            ptf_line = re.search(pattern_ptf, val)
            if ptf_line and len(ordered_group) > 0:
                # ordered_group[len(ordered_group) - 1]['shipped_ptf'].append(ptf_line.group())
                shipped_ptf.append(ptf_line.group())
        # search vrm:
        vrm_line = re.search(pattern_vrm, val)
        if vrm_line:
            group_vrm_info = dict(
                group=vrm_line.group('group'),
                vrm=vrm_line.group('vrm')
            )
            group_vrm.append(group_vrm_info)
        if cum_id is None:
            cumid_line = re.search(pattern_cumid, val)
            if cumid_line:
                cum_id = cumid_line.group('cum_id')
        if cum_vrm is None:
            cum_vrm_line = re.search(pattern_cum_vrm, val)
            if cum_vrm_line:
                cum_vrm = 'V' + cum_vrm_line.group('v') + 'R' + cum_vrm_line.group('r') + 'M' + cum_vrm_line.group('m')
        ordered_ptf_line = re.search(pattern_ordered_ptf, val)
        if ordered_ptf_line:
            ptf_info = dict(
                ptf=ordered_ptf_line.group('ptf'),
                product=ordered_ptf_line.group('product'),
                vrm=ordered_ptf_line.group('vrm'),
            )
            ordered_ptf.append(ptf_info)
        ptf_line = re.search(pattern_shipped_ptf, val)
        if ptf_line:
            shipped_ptf.append(ptf_line.group('ptf'))
    # Add VRM info to single ptf and group ptf
    for ordered_group_info in ordered_group:
        for group_vrm_info in group_vrm:
            if ordered_group_info['group'] == group_vrm_info['group']:
                ordered_group_info['release'] = group_vrm_info['vrm']
    # Add VRM info to cum package based on its group name (e.g. SF99730 for V7R3M0)
    for ordered_group_info in ordered_group:
        if ordered_group_info['release'] is None and len(ordered_group_info['group']) == 7:
            gn = ordered_group_info['group']
            ordered_group_info['release'] = 'V' + gn[4] + 'R' + gn[5] + 'M' + gn[6]
    if len(ordered_group) > 0:
        ordered_ptf = ordered_group
    return order_str, date_str, cum_id, cum_vrm, ordered_ptf, shipped_ptf


def get_group_info_from_txt(lines):
    order_str, date_str, cum_id, cum_vrm, ordered_ptf, shipped_ptf = get_common_info_from_txt(lines)
    return order_str, date_str, ordered_ptf, len(ordered_ptf), shipped_ptf, len(shipped_ptf)


def get_cum_info_from_txt(lines):
    order_str, date_str, cum_id, cum_vrm, ordered_ptf, shipped_ptf = get_common_info_from_txt(lines)
    return order_str, date_str, cum_id, cum_vrm, ordered_ptf, len(ordered_ptf), shipped_ptf, len(shipped_ptf)


def get_ptf_info_from_txt(lines):
    order_str, date_str, cum_id, cum_vrm, ordered_ptf, shipped_ptf = get_common_info_from_txt(lines)
    return order_str, date_str, ordered_ptf, len(ordered_ptf), shipped_ptf, len(shipped_ptf)


def get_info_in_lst(lst_file):
    if not os.path.isfile(lst_file):
        return None

    pattern_group = r'(?P<group>[A-Z]{2}\d{5})\s+Level\s+(?P<level>\d+)'
    image_type = 'single_ptf'
    lines = []
    order_id = ''
    download_date = ''
    cum_id = ''
    cum_vrm = ''
    ordered_ptf = []
    ordered_ptf_count = -1
    shipped_ptf = []
    shipped_ptf_count = -1

    with open(lst_file, 'r', encoding="utf-8") as f:
        lines += filter(None, (line.strip() for line in f))

    for idx, val in enumerate(lines):
        if re.match(pattern_group, val, re.IGNORECASE):
            image_type = 'group'
        elif val == 'IBM i CUMULATIVE PTF PACKAGE':
            image_type = 'cum'
            break
    if image_type == 'group':
        order_id, download_date, ordered_ptf, ordered_ptf_count, shipped_ptf, shipped_ptf_count = get_group_info_from_txt(lines)
    elif image_type == 'cum':
        order_id, download_date, cum_id, cum_vrm, ordered_ptf, ordered_ptf_count, shipped_ptf, shipped_ptf_count = get_cum_info_from_txt(lines)
    else:
        order_id, download_date, ordered_ptf, ordered_ptf_count, shipped_ptf, shipped_ptf_count = get_ptf_info_from_txt(lines)

    image_info = dict(
        order_id=order_id,
        image_type=image_type,
        download_date=download_date,
        cum_id=cum_id,
        cum_vrm=cum_vrm,
        ordered_ptf=ordered_ptf,
        ordered_ptf_count=ordered_ptf_count,
        shipped_ptf=shipped_ptf,
        shipped_ptf_count=shipped_ptf_count,
    )

    return image_info


def get_image_info(module, image_path):
    lst_patthern = r"^ilst\S+.txt$"
    img_patthern = r"^\S+_\d.bin$"

    file_list = os.listdir(image_path)
    lst_found = ftp_found = sha_found = img_found = 0

    image_dir = dict(
        image_path=image_path,
        image_files=[]
    )

    for file_name in file_list:
        full_file_path = os.path.join(image_path, file_name)
        if not os.path.isdir(full_file_path):
            if file_name == "sha256.txt":
                sha_found += 1
            if re.match(lst_patthern, file_name, re.IGNORECASE):
                lst_found += 1
                image_info = get_info_in_lst(full_file_path)
                image_dir['order_id'] = image_info['order_id']
                image_dir['image_type'] = image_info['image_type']
                image_dir['download_date'] = image_info['download_date']
                image_dir['cum_id'] = image_info['cum_id']
                image_dir['cum_vrm'] = image_info['cum_vrm']
                image_dir['ordered_ptf'] = image_info['ordered_ptf']
                image_dir['ordered_ptf_count'] = image_info['ordered_ptf_count']
                image_dir['shipped_ptf'] = image_info['shipped_ptf']
                image_dir['shipped_ptf_count'] = image_info['shipped_ptf_count']
            if re.match(img_patthern, file_name, re.IGNORECASE):
                img_found += 1
                img_file = dict(
                    file=file_name,
                )
                image_dir['image_files'].append(img_file)

    if lst_found == 1 and sha_found == 1 and img_found >= 1:
        sha256_file = os.path.join(image_path, "sha256.txt")
        chksum_info_all = get_checksum_in_txt(sha256_file)
        if not chksum_info_all:
            return None
        for chksum_info in chksum_info_all:
            for img_file in image_dir['image_files']:
                if chksum_info['file'] == img_file['file']:
                    img_file['expected_chksum'] = chksum_info['expected_chksum']

        image_dir['ordered_ptf'] = json.dumps(image_dir['ordered_ptf'])
        image_dir['shipped_ptf'] = json.dumps(image_dir['shipped_ptf'])
        image_dir['image_files'] = json.dumps(image_dir['image_files'])

        return image_dir
    else:
        return None


def scan_image_files(module, dir_path):
    if os.path.isdir(dir_path):
        image_info = get_image_info(module, dir_path)
        if image_info:
            images.append(image_info)

        file_list = os.listdir(dir_path)
        for file in file_list:
            cur_path = os.path.join(dir_path, file)
            if os.path.isdir(cur_path):
                scan_image_files(module, cur_path)


def checksum_after_find(module, success_list):
    if isinstance(success_list, list) and len(success_list) > 0:
        for row in success_list:
            image_path = image_files = None
            if row.get('query_result'):
                sublist = row.get('query_result')
                if isinstance(sublist, list) and len(sublist) > 0:
                    for row in sublist:
                        if isinstance(row, dict) and row.get('image_path') and row.get('image_files'):
                            image_path = row.get('image_path')
                            image_files = row.get('image_files')
                            if os.path.isdir(image_path) and isinstance(image_files, list):
                                for image_file in image_files:
                                    full_path = os.path.join(image_path, image_file.get('file'))
                                    if os.path.isfile(full_path) and image_file.get('expected_chksum'):
                                        image_file['file_chksum'] = module.sha256(full_path)
                                        image_file['integrity'] = image_file.get('file_chksum') == image_file.get('expected_chksum')
            elif isinstance(row, dict) and row.get('image_path') and row.get('image_files'):
                image_path = row.get('image_path')
                image_files = row.get('image_files')
                if os.path.isdir(image_path) and isinstance(image_files, list):
                    for image_file in image_files:
                        full_path = os.path.join(image_path, image_file.get('file'))
                        if os.path.isfile(full_path) and image_file.get('expected_chksum'):
                            image_file['file_chksum'] = module.sha256(full_path)
                            image_file['integrity'] = image_file.get('file_chksum') == image_file.get('expected_chksum')


def generate_query_fields(fields):
    if fields is None:
        return ','.join(list_image_dict)
    else:
        valid_fields = []
        for field in fields:
            if field in ptf_repo_lv1_dict:
                valid_fields.append(field)
        return ','.join(valid_fields)


def build_sql_init():
    fields = ''
    for k, v in ptf_repo_lv1_dict.items():
        fields += f'{k} {v}, '
    fields = fields.rstrip(', ')
    sql = f'CREATE TABLE IF NOT EXISTS {ptf_repo_lv1_table} ({fields})'
    return sql


def build_sql_list(fields):
    list_param = generate_query_fields(fields)
    return f'SELECT {list_param} FROM {ptf_repo_lv1_table}'


def remove_temp_fields(temp_ordered_ptf, temp_shipped_ptf, row):
    new_row = row.copy()
    if temp_ordered_ptf:
        new_row.pop('ordered_ptf')
    if temp_shipped_ptf:
        new_row.pop('shipped_ptf')
    return new_row


def build_sql_add(parameters):
    names = ''
    values = ''
    for param_key in parameters[0].keys():
        if param_key in ptf_repo_lv1_dict.keys():
            names += param_key + ', '
            values += ':' + param_key + ', '
    name = names.rstrip(', ')
    value = values.rstrip(', ')
    return f'INSERT OR IGNORE INTO {ptf_repo_lv1_table} ({name}) VALUES({value})'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def run_sql(module, database, fields, parameters, additional_sql, action):
    sql = ''
    success_list = []
    fail_list = []
    temp_ordered_ptf = False
    temp_shipped_ptf = False

    if additional_sql is None:
        additional_sql = ''

    if action == 'find':
        if 'ordered_ptf' not in fields:
            fields.append('ordered_ptf')
            temp_ordered_ptf = True
        if 'shipped_ptf' not in fields:
            fields.append('shipped_ptf')
            temp_shipped_ptf = True

    try:
        ibmi_util.ensure_dir(os.path.dirname(database))
    except Exception:
        module.fail_json(msg='Failed to create path ' + database)

    try:
        conn = sqlite3.connect(database)
        # if the database file not exist, it will be created automatically.
    except sqlite3.Error as e:
        module.fail_json(msg=e.args[0])

    if (conn is not None):
        c = conn.cursor()
        # create the table first if needed.
        sql = build_sql_init()
        try:
            c.execute(sql)
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0] + ' ***SQL:' + sql)

        if action == 'refresh':
            sql = 'DELETE FROM ' + ptf_repo_lv1_table
            c.execute(sql)
            sql = build_sql_add(parameters)
        elif action == 'list' or action == 'find':
            sql = build_sql_list(fields) + ' ' + additional_sql
        elif action == 'clear':
            sql = 'DROP TABLE IF EXISTS ' + ptf_repo_lv1_table
        else:
            return -2, 'Unsupported action: ' + action, -1, success_list, fail_list, sql
        try:
            if action == 'list' or action == 'find':
                c.row_factory = dict_factory
                c.execute(sql)
                rs = c.fetchall()
                if isinstance(rs, list) and len(rs) > 0:
                    for row in rs:
                        if row.get('image_files'):
                            row['image_files'] = json.loads(row.get('image_files'))
                        if row.get('ordered_ptf'):
                            row['ordered_ptf'] = json.loads(row.get('ordered_ptf'))
                        if row.get('shipped_ptf'):
                            row['shipped_ptf'] = json.loads(row.get('shipped_ptf'))
                        if action == 'list':
                            success_list.append(row)
                if action == 'find' and isinstance(parameters, list):
                    for param in parameters:
                        rs_copy = []
                        result = dict(
                            query_item=param,
                        )
                        for row in rs:
                            if param.get('shipped_ptf') and row.get('shipped_ptf') and param.get('shipped_ptf') in row.get('shipped_ptf'):
                                rs_copy.append(remove_temp_fields(temp_ordered_ptf, temp_shipped_ptf, row))
                            elif param.get('ptf'):
                                for ordered_ptf in row.get('ordered_ptf'):
                                    if ordered_ptf.get('ptf') and param.get('ptf') == ordered_ptf.get('ptf'):
                                        rs_copy.append(remove_temp_fields(temp_ordered_ptf, temp_shipped_ptf, row))
                            elif param.get('group') and param.get('level'):
                                for ordered_ptf in row.get('ordered_ptf'):
                                    if ordered_ptf.get('group') and param.get('group') == ordered_ptf.get('group'):
                                        if ordered_ptf.get('level') and param.get('level') == ordered_ptf.get('level'):
                                            rs_copy.append(remove_temp_fields(temp_ordered_ptf, temp_shipped_ptf, row))
                            elif param.get('group'):
                                for ordered_ptf in row.get('ordered_ptf'):
                                    if ordered_ptf.get('group') and param.get('group') == ordered_ptf.get('group'):
                                        rs_copy.append(remove_temp_fields(temp_ordered_ptf, temp_shipped_ptf, row))
                        result['query_result'] = rs_copy
                        success_list.append(result)
            elif isinstance(parameters, list):  # update/delete
                c.executemany(sql, parameters)
            else:  # clear/init tables (no param)
                c.execute(sql)
        except sqlite3.Error as e:
            module.fail_json(msg=e.args[0] + ' ***SQL:' + sql + ' ***Param:' + str(parameters))
        finally:
            conn.commit()
            conn.close()

        return 0, '', c.rowcount, success_list, fail_list, sql


def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(type='str', required=True),
            image_root=dict(type='str'),
            checksum=dict(type='bool', default=False),
            database=dict(type='str', default='/etc/ibmi_ansible/fix_management/repo_lv1.sqlite3'),
            additional_sql=dict(type='str'),
            parameters=dict(type='list', elements='dict'),
            fields=dict(type='list', elements='str'),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    action = module.params['action'].strip().lower()
    image_root = module.params['image_root']
    additional_sql = module.params['additional_sql']
    database = module.params['database'].strip()
    parameters = module.params['parameters']
    fields = module.params['fields']
    checksum = module.params['checksum']

    result = dict(
        action=action,
        database=database,
        image_root=image_root,
        additional_sql=additional_sql,
        checksum=checksum,
        parameters=parameters,
        fields=fields,
        sqlite3Version=sqlite3.version,
        sqlite3Runtime=sqlite3.sqlite_version,
    )

    if int(sqlite3.sqlite_version.split('.')[1]) < 9:
        module.fail_json(msg="Please upgrade your SQLite3 to version 3.9.0 or above", **result)

    row_changed = -1
    success_list = []
    fail_list = []
    invalid_params = []
    checksum_failed_params = []
    mismatched_params = []
    fail_list_after_run_sql = []
    list_to_sqlite = []
    sql = ''

    startd = datetime.datetime.now()

    if action == 'refresh':
        scan_image_files(module, image_root)
        if len(images) == 0:
            module.fail_json(msg="No valid image found in image_root", **result)
        list_to_sqlite = images
    else:
        list_to_sqlite = parameters

    if fields is None:
        fields = list_image_dict.copy()

    if checksum is True:
        if 'image_path' not in fields:
            fields.append('image_path')
        if 'image_files' not in fields:
            fields.append('image_files')

    if action in ('refresh', 'list', 'clear', 'find') or len(list_to_sqlite) > 0:
        rc, msg, row_changed, success_list, fail_list, sql = run_sql(module, database, fields, list_to_sqlite, additional_sql, action)
        if rc != 0:
            module.fail_json(msg=msg, **result)
        result['sql'] = sql
        if isinstance(row_changed, int):
            result['row_changed'] = row_changed
        if len(success_list) > 0:  # only for action = 'find'
            if checksum is True:
                checksum_after_find(module, success_list)
            result['success_list'] = success_list
        result['success_list'] = success_list
    if len(fail_list) > 0 or len(invalid_params) > 0 or len(checksum_failed_params) > 0 or len(fail_list_after_run_sql) > 0 or len(mismatched_params) > 0:
        result['fail_list'] = fail_list + invalid_params + checksum_failed_params + fail_list_after_run_sql + mismatched_params

    endd = datetime.datetime.now()
    delta = endd - startd
    result['start'] = str(startd)
    result['end'] = str(endd)
    result['delta'] = str(delta)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
