#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Chang Le <changle@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_fix_product_check
short_description: Check the software product installation status for a fix
version_added: '1.2.0'
description:
  - The C(ibmi_fix_product_check) module checks if the software product of a fix is installed.
options:
  ptfs:
    description:
      - The list of the PTF.
    type: list
    elements: dict
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
seealso:
- module: ibmi_fix

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Get PTF products installation status
  ibm.power_ibmi.ibmi_fix_product_check:
    ptfs:
      - {
        "product": "5770UME",
        "ptf_id": "SI67856",
        "release": "V1R4M0"
        }
      - {
        "product": "5733SC1",
        "ptf_id": "SI73751",
        "release": "V7R2M0"
        }
'''

RETURN = r'''
ptfs_with_product_installed:
    description: The PTF list which the product was installed.
    returned: always, empty list if error occurred or none of the product was installed.
    type: list
    sample: [{
      "product": "5770UME",
      "ptf_id": "SI67856",
      "release": "V1R4M0"
    }]
ptfs_without_product_installed:
    description: The PTF list which the product was not installed.
    returned: always, empty list if all of the products were installed.
    type: list
    sample: [{
      "product": "5733SC1",
      "ptf_id": "SI73751",
      "release": "V7R2M0"
    }]
rc:
    description: The return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
msg:
    description: The error or success message.
    returned: always
    type: str
    sample: 'Success to check software product installation status'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import sys

HAS_ITOOLKIT = True
try:
    from itoolkit import iToolKit
    from itoolkit import iPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport as BaseDatabaseTransport

    class DatabaseTransport(BaseDatabaseTransport):
        def _close(self):
            """Don't close connection, we'll manage it ourselves"""
            pass

except ImportError:
    HAS_ITOOLKIT = False

__ibmi_module_version__ = "2.0.1"


def get_product_info(imodule, product_id, release_level, product_option, load_id):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iPgm('qszrtvpr', 'QSZRTVPR')
        .addParm(
            iDS('Qsz_PRDR0100_t', {'len': 'qszlen'})
            .addData(iData('Bytes_Returned', '10i0', ''))
            .addData(iData('Bytes_Available', '10i0', ''))
            .addData(iData('Reserved_1', '10i0', ''))
            .addData(iData('Product_Id', '7A', ''))
            .addData(iData('Release_Level', '6A', ''))
            .addData(iData('Product_Option', '4A', ''))
            .addData(iData('Load_Id', '4A', ''))
            .addData(iData('Load_Type', '10A', ''))
            .addData(iData('Symbolic_Load_State', '10A', ''))
            .addData(iData('Load_Error_Indicator', '10A', ''))
            .addData(iData('Load_State', '2A', ''))
            .addData(iData('Supported_Flag', '1A', ''))
            .addData(iData('Registration_Type', '2A', ''))
            .addData(iData('Registration_Value', '14A', ''))
            .addData(iData('Reserved_2', '2A', ''))
            .addData(iData('Ofst_Addn_Info', '10i0', ''))
            .addData(iData('Prim_Lng_Lod', '4A', ''))
            .addData(iData('Min_Tgt_Rls', '6A', ''))
            .addData(iData('Min_VRM_Base_Req', '6A', ''))
            .addData(iData('Base_Opt_VRM_Reqs_Met', '1A', ''))
            .addData(iData('Level', '3A', ''))
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'qszlen'}))
        .addParm(iData('fmtnam', '8A', 'PRDR0100'))
        .addParm(
            iDS('Qsz_Product_Info_Rec_t')
            .addData(iData('Product_Id', '7A', product_id))
            .addData(iData('Release_Level', '6A', release_level))
            .addData(iData('Product_Option', '4A', product_option))
            .addData(iData('Load_Id', '10A', load_id))
        )
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('errRet', '10i0', ''))
            .addData(iData('errAvl', '10i0', ''))
            .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
            .addData(iData('errRsv', '1A', ''))
        )
    )
    itool.call(itransport)
    qszrtvpr = itool.dict_out('qszrtvpr')
    ibmi_util.log_debug(str(qszrtvpr), sys._getframe().f_code.co_name)
    if 'success' in qszrtvpr:
        prdr0100_t = qszrtvpr['Qsz_PRDR0100_t']
        ibmi_util.log_debug(str(prdr0100_t), sys._getframe().f_code.co_name)
        return 0, prdr0100_t, qszrtvpr['success']
    else:
        return -1, None, qszrtvpr['error']


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ptfs=dict(type='list', elements='dict', required=True),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True)
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    ptfs_list = module.params['ptfs']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = f'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    ptfs_with_product_installed = []
    ptfs_without_product_installed = []
    for ptf in ptfs_list:
        try:
            product_id = ptf['product']
            release_level = ptf['release']
            ptf_id = ptf['ptf_id']
        except KeyError as ke:
            message = f'KeyError: missing key {ke} in the input PTFs dict list'
            module.fail_json(rc=999, msg=message)
        ibmi_util.log_info(f'Checking PTF {ptf_id} {product_id} {release_level}', sys._getframe().f_code.co_name)
        rc, product_info, out = get_product_info(
            ibmi_module, product_id, release_level, '0000', '*CODE')
        if (rc == 0) and (product_info['Load_Error_Indicator'] == '*NONE') and (product_info['Symbolic_Load_State'] == '*INSTALLED'):
            ptfs_with_product_installed.append(ptf)
            ibmi_util.log_info(
                f'Product for PTF {ptf_id} {product_id} {release_level} was installed', sys._getframe().f_code.co_name)
        else:
            ptfs_without_product_installed.append(ptf)
            ibmi_util.log_info(
                f'Product for PTF {ptf_id} {product_id} {release_level} was not installed or error occurred', sys._getframe().f_code.co_name)

    result = dict(
        rc=0,
        ptfs_with_product_installed=ptfs_with_product_installed,
        ptfs_without_product_installed=ptfs_without_product_installed,
    )
    module.exit_json(msg='Success to check software product installation status', **result)


if __name__ == '__main__':
    main()
