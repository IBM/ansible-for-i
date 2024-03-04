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
module: ibmi_fix_compare
short_description: Verify whether the PTFs are installed.
version_added: '1.2.0'
description:
     - The C(ibmi_fix_compare) module compare the PTF list to target system to see whether the PTF is applied.
options:
  ptfs:
    description:
      - The list of the PTF number.
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
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3

author:
    - Zhang Yan (@bjyanz)
'''

EXAMPLES = r'''

- name: Check the PTFs' status
  ibm.power_ibmi.ibmi_fix_compare:
    ptfs:
      - 'SI12345'
      - 'SI67890'
'''

RETURN = r'''
stderr:
    description: The task standard error
    returned: always
    type: str
    sample: 'PTF groups SF12345 does not exist'
rc:
    description: The task return code (0 means success, non-zero means failure)
    type: int
    returned: always
    sample: 1
verified:
    description: The number of PTFs which has been retrieved
    type: int
    returned: always.
    sample: 1
unexpected:
    description: The number of PTFs which are not installed
    type: int
    returned: always.
    sample: 1
ptf_info:
    description: PTF group information.
    type: list
    returned: When rc is 1.
    sample: [
        {
            "PTF_IDENTIFIER": "SI12345",
            "PTF_STATUS": "Not installed",
        },
        {
            "PTF_ACTION_PENDING": "NO",
            "PTF_ACTION_REQUIRED": "NONE",
            "PTF_CREATION_TIMESTAMP": "2015-02-18T16:58:46",
            "PTF_IDENTIFIER": "SI12345",
            "PTF_IPL_ACTION": "NONE",
            "PTF_IPL_REQUIRED": "IMMEDIATE",
            "PTF_PRODUCT_ID": "57XXXXX",
            "PTF_SAVE_FILE": "YES",
            "PTF_STATUS": "NOT LOADED",
            "PTF_STATUS_TIMESTAMP": null
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule

__ibmi_module_version__ = "2.0.1"


def get_ptf_info(db_connection, ptf_list):
    str_ptf_list = "','".join(ptf_list)
    str_ptf_list = str_ptf_list.upper()
    sql = "SELECT PTF_PRODUCT_ID, PTF_IDENTIFIER, PTF_LOADED_STATUS, PTF_SAVE_FILE, PTF_IPL_ACTION," \
          " PTF_ACTION_PENDING, PTF_ACTION_REQUIRED, PTF_IPL_REQUIRED," \
          " PTF_STATUS_TIMESTAMP, PTF_CREATION_TIMESTAMP" \
          " FROM QSYS2.PTF_INFO WHERE UPPER(PTF_IDENTIFIER) IN ('" + str_ptf_list + "')"
    out_result_set, err = db2i_tools.ibm_dbi_sql_query(db_connection, sql)
    out = {}
    if (out_result_set is not None):
        for result in out_result_set:
            result_map = {
                "PTF_PRODUCT_ID": result[0],
                "PTF_IDENTIFIER": result[1],
                "PTF_LOADED_STATUS": result[2],
                "PTF_SAVE_FILE": result[3],
                "PTF_IPL_ACTION": result[4],
                "PTF_ACTION_PENDING": result[5],
                "PTF_ACTION_REQUIRED": result[6],
                "PTF_IPL_REQUIRED": result[7],
                "PTF_STATUS_TIMESTAMP": result[8],
                "PTF_CREATION_TIMESTAMP": result[9]
            }
            # key - PTF_PRODUCT_ID ; value - ptf information
            out.update({result[1]: result_map})
    return out, err


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ptfs=dict(type='list', elements='str', required=True),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True)
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    ptf_list = module.params['ptfs']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = f'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    db_conn = ibmi_module.get_connection()

    ptf_info = []
    err = ''
    if ptf_list is not None:
        ptf_map, query_err = get_ptf_info(db_conn, ptf_list)
        if query_err is not None:
            # failed to get PTF info
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            err = query_err
        else:
            # get PTF info succeed
            for ptf_num in ptf_list:
                if ptf_map.get(ptf_num):
                    ptf = ptf_map[ptf_num]
                    if ptf['PTF_LOADED_STATUS'] != 'APPLIED' and ptf['PTF_LOADED_STATUS'] != 'PERMANENTLY APPLIED' and ptf['PTF_LOADED_STATUS'] != 'SUPERSEDED':
                        # ptf status is not expected
                        ptf_info.append({
                            'PTF_IDENTIFIER': ptf_num,
                            'PTF_STATUS': ptf['PTF_LOADED_STATUS'],
                            'PTF_PRODUCT_ID': ptf['PTF_PRODUCT_ID'],
                            'PTF_SAVE_FILE': ptf['PTF_SAVE_FILE'],
                            'PTF_IPL_ACTION': ptf['PTF_IPL_ACTION'],
                            'PTF_ACTION_PENDING': ptf['PTF_ACTION_PENDING'],
                            'PTF_ACTION_REQUIRED': ptf['PTF_ACTION_REQUIRED'],
                            'PTF_IPL_REQUIRED': ptf['PTF_IPL_REQUIRED'],
                            'PTF_STATUS_TIMESTAMP': ptf['PTF_STATUS_TIMESTAMP'],
                            'PTF_CREATION_TIMESTAMP': ptf['PTF_CREATION_TIMESTAMP']
                        })
                else:
                    # ptf does not exist
                    ptf_info.append({'PTF_IDENTIFIER': ptf_num, 'PTF_STATUS': 'Not installed'})
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
    else:
        rc = ibmi_util.IBMi_COMMAND_RC_ERROR
        module.fail_json(msg="PTF list contains no PTF.")

    if rc == ibmi_util.IBMi_COMMAND_RC_ERROR:
        result_failed = dict(
            rc=rc,
            stderr=err
        )
        module.fail_json(msg='255 return code', **result_failed)
    else:
        result_success = dict(
            rc=rc,
            verified=len(ptf_list),
            unexpected=len(ptf_info),
            ptf_info=ptf_info,
            stderr=err
        )
        module.exit_json(**result_success)


if __name__ == '__main__':
    main()
