#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Zhou Yu <zhouyubj@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_module_authority_check
short_description: Check the authority of executing a module.
version_added: '2.8.0'
description:
  - The C(ibmi_module_authority_check) module can do the module authority check.
  - This module returns the authority of executing the module specified in the parameter
options:
  modulelist:
    description:
      - Specifies a list of module which are checked the authority.
    type: list
    elements: str
    required: yes


author:
- Zhou Yu (@zhouyu)
'''

EXAMPLES = r'''
- name: Do module authority check
  ibmi_user_compliance_check:
       modulelist:
        - 'ibmi_copy'
        - 'ibmi_display_subsystem'
        - 'ibmi_invaild_module'

'''


RETURN = r'''
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 255
authority_result:
    description: The result set of required authories of module.
    returned: always
    type: dict
    sample: {
        "ibmi_copy": [
            "*ALLOBJ"
        ],
        "ibmi_display_subsystem": [
            "*JOBCTL"
        ],
        "ibmi_invaild_module": "this module name is invaild."
    }
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util

__ibmi_module_version__ = "1.1.2"

module_authority_map = {
    'ibmi_at': ['*NONE'],
    'ibmi_cl_command': ['Depend on authority of CL command'],
    'ibmi_copy': ['*ALLOBJ'],
    'ibmi_device_vary': ['*NONE'],
    'ibmi_display_fix': ['*NONE'],
    'ibmi_display_subsystem': ['*JOBCTL'],
    'ibmi_end_subsystem': ['*JOBCTL'],
    'ibmi_ethernet_port': ['*NONE'],
    'ibmi_fetch': ['*SAVSYS'],
    'ibmi_fix': ['*ALLOBJ'],
    'ibmi_fix_imgclg': ['*ALLOBJ', '*IOSYSCFG'],
    'ibmi_get_nonconfigure_disks': ['*NONE'],
    'ibmi_host_server_service': ['NONE'],
    'ibmi_iasp': ['*IOSYSCFG', '*SERVICE'],
    'ibmi_install_product_from_savf': ['*SECADM', '*ALLOBJ'],
    'ibmi_job': ['NONE'],
    'ibmi_lib_restore': ['*SAVSYS'],
    'ibmi_lib_save': ['*SAVSYS'],
    'ibmi_message': ['NONE'],
    'ibmi_module_config': ['*NONE'],
    'ibmi_nrg_link': ['*IOSYSCFG'],
    'ibmi_object_authority': ['*ALLOBJ', '*OBJMGT'],
    'ibmi_object_find': ['*NONE'],
    'ibmi_object_restore': ['*SAVSYS'],
    'ibmi_object_save': ['*SAVSYS'],
    'ibmi_fix_repo': ['*NONE'],
    'ibmi_query_job_log': ['*NONE'],
    'ibmi_reboot': ['*JOBCTL'],
    'ibmi_reply_message': ['*NONE'],
    'ibmi_save_product_to_savf': ['*ALLOBJ'],
    'ibmi_script': ['Depend on CL/SQL commands'],
    'ibmi_script_execute': ['Depend on CL/SQL commands'],
    'ibmi_sql_execute': ['Depend on SQL procedure'],
    'ibmi_sql_query': ['Depend on SQL query statements'],
    'ibmi_start_subsystem': ['*JOBCTL'],
    'ibmi_submit_job': ['*NONE'],
    'ibmi_sync': ['*NONE'],
    'ibmi_sync_files': ['*NONE'],
    'ibmi_synchronize': ['*NONE'],
    'ibmi_synchronize_files': ['*NONE'],
    'ibmi_sysval': ['Depends on specified system values'],
    'ibmi_tcp_interface': ['*IOSYSCFG'],
    'ibmi_tcp_server_service': ['*IOSYSCFG'],
    'ibmi_uninstall_product': ['*ALLOBJ'],
    'ibmi_user_compliance_check': ['*OBJOPR', '*READ'],
}


def main():
    module = AnsibleModule(
        argument_spec=dict(
            modulelist=dict(type='list', elements='str', required=True),
        ),
        supports_check_mode=True,
    )
    # get input value
    modulelist = module.params['modulelist']

    authority_result = {}
    for module_name in modulelist:
        authority_list = module_authority_map.get(module_name)
        if authority_list is None:
            authority_result[module_name] = 'this module name is invaild.'
        else:
            authority_result[module_name] = authority_list

    result_success = dict(
        authority_result=authority_result,
        rc=0,
    )
    module.exit_json(**result_success)


if __name__ == '__main__':
    main()
