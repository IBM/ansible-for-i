#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Zhang Yan <bjyanz@cn.ibm.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_download_fix_status
short_description: Checking whether the fix downloading complete
version_added: '1.2.0'
description:
     - The C(ibmi_download_fix_status) module check the downloading fix's status.
options:
  order_list:
    description:
      - The  order list of download ptf group
    type: list
    elements: str
    required: yes
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
    - Only support English language ibm i system, language ID 2924.
    - See SNDPTFORD command for more information.

author:
    - Zhang Yan (@bjyanz)
'''

EXAMPLES = r'''
- name: Check the fix order status
  ibm.power_ibmi.ibmi_download_fix_status:
    order_list:
      - '2029604329'
      - '2020579181'

- name: Check the fix order status with become user
  ibm.power_ibmi.ibmi_download_fix_status:
    order_list:
      - '2029604329'
      - '2020579181'
    become_user: 'USER1'
    become_user_password: 'yourpassword'
'''

RETURN = r'''
status:
    description: The fix downloading status.
    returned: always
    type: list
    sample: [
        {
            'order_id': '2029604329',
            'download_status': 'DOWNLOADED',
            'file_path': '/QIBM/UserData/OS/Service/ECS/PTF/2029604329',
            'complete_time': '2020-11-01 00:59:58'
        },
        {
            'order_id': '2020579181',
            'download_status': 'UNKNOWN',
            'file_path': 'UNKNOWN',
            'complete_time': 'UNKNOWN'
        }
    ]
rc:
    description: The SQL command action return code. 0 means success.
    returned: always
    type: int
    sample: 0
'''


import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
__ibmi_module_version__ = "2.0.1"

HAS_ITOOLKIT = True


def main():
    module = AnsibleModule(
        argument_spec=dict(
            order_list=dict(type='list', elements='str', required=True),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    order_list = module.params['order_list']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    result = dict(
        status=[],
        rc=0,
        stdout='',
        stderr=''
    )
    error = ''
    status = []
    complete_time = ''
    file_path = ''
    download_status = ''
    sql_query_message_info = "SELECT MESSAGE_TIMESTAMP, MESSAGE_SECOND_LEVEL_TEXT FROM QSYS2.MESSAGE_QUEUE_INFO" \
        " WHERE MESSAGE_QUEUE_LIBRARY='QSYS' AND MESSAGE_QUEUE_NAME='QSERVICE' AND MESSAGE_ID='CPZ8C15' AND" \
        " MESSAGE_TYPE='COMPLETION' AND MESSAGE_SECOND_LEVEL_TEXT LIKE '%{order_id}%'"

    try:
        ibmi_module = imodule.IBMiModule(become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = f'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    try:
        for order_id in order_list:
            download_status = 'UNKNOWN'
            complete_time = 'UNKNOWN'
            file_path = 'UNKNOWN'
            # query the messages of this order in QSERVICE
            rc, out, error = ibmi_module.itoolkit_run_sql(sql_query_message_info.format(order_id=order_id))
            if rc != 0:
                result.update({'status': status, 'rc': rc, 'stdout': '', 'stderr': error})
                module.exit_json(**result)

            if isinstance(out, list) and len(out) > 0:
                for item in out:
                    # extract the file path. e.g. /QIBM/UserData/OS/Service/ECS/PTF/1234567890
                    re_list = re.findall(r"/[0-9a-zA-Z]+", item['MESSAGE_SECOND_LEVEL_TEXT'])
                    for id_temp in re_list:
                        if id_temp[1:] == order_id:
                            # message exists. set the download_status to 'DOWNLOADED'
                            download_status = 'DOWNLOADED'
                            complete_time = out[0]['MESSAGE_TIMESTAMP'].strip()[:-7]
                            file_path = ''.join(re_list)

            status.append({'order_id': order_id, 'download_status': download_status, 'complete_time': complete_time, 'file_path': file_path})

        result.update({'status': status, 'rc': rc, 'stdout': '', 'stderr': error})
        module.exit_json(**result)

    except Exception as e_db_connect:
        module.fail_json(msg=e_db_connect.args[0])


if __name__ == '__main__':
    main()
