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
module: ibmi_fix_group_check
short_description: Retrieve the latest PTF group information from PSP server.
version_added: '2.8.0'
description:
     - The C(ibmi_fix_group_check) module retrieve latest PTF group information from PSP(Preventive Service Planning) server.
     - Refer to https://www.ibm.com/support/pages/node/667567 for more details of PSP.
     - ALL PTF groups or specific PTF groups are supported.
options:
  groups:
    description:
      - The list of the PTF groups number.
    type: list
    elements: str
    default: ['*ALL']
    required: false
  validate_certs:
    description:
      - If set to C(False), the SSL certificate verification will be disabled. It's recommended for test scenario.
      - It's recommended to enable the SSL certificate verification for security concern.
    type: bool
    default: True
    required: false

notes:
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3.
   - If the module is delegated to an IBM i server and SSL certificate verification is enabled, package C(ca-certificates-mozilla) is required.

author:
    - Zhang Yan (@bjyanz)
'''

EXAMPLES = r'''
- name: Check specific PTF groups
  ibmi_fix_group_check:
    groups:
      - "SF12345"

- name: Check the PTF groups without certificate verification
  ibmi_fix_group_check:
    groups:
      - "SF12345"
    validate_certs: False
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
    sample: 0
count:
    description: The number of PTF groups which has been retrieved
    type: int
    returned: always.
    sample: 1
group_info:
    description: PTF group information.
    type: list
    returned: When rc is zero.
    sample: [
        {
            "PTF_GROUP_NUMBER": "SF99115",
            "RELEASE": "R610",
            "TITLE": "610 IBM HTTP Server for i",
            "PTF_GROUP_LEVEL": "46",
            "RELEASE_DATE": "09/28/2015"
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
import ansible.module_utils.urls as urls
from xml.dom.minidom import parseString

__ibmi_module_version__ = "1.0.2"

PSP_URL = "https://www.ibm.com/support/pages/sites/default/files/inline-files/xmldoc.xml"


def get_psp_group_info(validate_certs):
    response = urls.open_url(PSP_URL, validate_certs=validate_certs)
    data = response.read().decode("utf-8")

    dom = parseString(data)
    groups_dict = dict()
    groups = dom.getElementsByTagName('psp')
    for group in groups:
        release = group.getElementsByTagName("release")[0].childNodes[0].data
        number = group.getElementsByTagName("number")[0].childNodes[0].data.upper()
        title = group.getElementsByTagName("title")[0].childNodes[0].data
        level = group.getElementsByTagName("level")[0].childNodes[0].data
        date = group.getElementsByTagName("date")[0].childNodes[0].data

        group_info = {
            'PTF_GROUP_NUMBER': number,
            'RELEASE': release,
            'TITLE': title,
            'PTF_GROUP_LEVEL': level,
            'RELEASE_DATE': date
        }
        groups_dict.update({number: group_info})
    return groups_dict


def main():
    module = AnsibleModule(
        argument_spec=dict(
            groups=dict(type='list', elements='str', default=['*ALL']),
            validate_certs=dict(type='bool', default=True)
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    result = dict(
        rc=0,
        count=0,
        group_info=[],
        stderr=''
    )
    groups_num = module.params['groups']
    validate_certs = module.params['validate_certs']

    psp_groups = get_psp_group_info(validate_certs)

    if groups_num[0] == '*ALL':
        # check all the PTF groups
        result.update({'group_info': list(psp_groups.values())})
        result.update({'count': len(psp_groups)})
    else:
        # check specific PTF groups
        count = 0
        wrong_groups = []
        groups = []
        for number in groups_num:
            number = number.upper()
            if psp_groups.get(number):
                # PTF group exists
                group = psp_groups[number]
                groups.append(group)
                count = count + 1
            else:
                # PTF group does not exist
                wrong_groups.append(number)
        result.update({'group_info': groups})
        result.update({'count': count})
        if len(wrong_groups) > 0:
            result.update({'stderr': 'PTF group ' + ",".join(wrong_groups) + ' does not exit'})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
