#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Zhang Yan <bjyanz@cn.ibm.com>
# Author, Xu Meng <mengxumx@cn.ibm.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}
DOCUMENTATION = r'''
---
module: ibmi_fix_group_check
short_description: Retrieve the latest PTF group information from PSP server.
version_added: '1.1.0'
description:
     - The C(ibmi_fix_group_check) module retrieve latest PTF group information from PSP(Preventive Service Planning) server.
     - Refer to https://www.ibm.com/support/pages/node/667567 for more details of PSP.
     - ALL PTF groups or specific PTF groups are supported.
     - A PTF group returns a list of PTFs that the group consists of, while a cumulative PTF returns a package ID.
     - The PTF group information is derived from the top level XML web page https://public.dhe.ibm.com/services/us/igsc/PSP/xmldoc.xml with a corresponding
       XML file at https://public.dhe.ibm.com/services/us/igsc/PSP/ for each PTF group (or text file for a cumulative).
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
  timeout:
    description:
      - Timeout in seconds for URL request.
    type: int
    default: 60
    required: false

notes:
   - Ansible hosts file need to specify ansible_python_interpreter=/QOpenSys/pkgs/bin/python3.
   - If the module is delegated to an IBM i server and SSL certificate verification is enabled, package C(ca-certificates-mozilla) is required.

author:
    - Zhang Yan (@bjyanz)
    - Xu Meng (@dmabupt)
'''

EXAMPLES = r'''
- name: Check specific PTF groups
  ibm.power_ibmi.ibmi_fix_group_check:
    groups:
      - "SF12345"

- name: Check the PTF groups without certificate verification
  ibm.power_ibmi.ibmi_fix_group_check:
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
            "description": "SF99738 - 740 Group Security",
            "package_id": null,
            "ptf_group_level": 70,
            "ptf_group_number": "SF99738",
            "ptf_list": [
                "SJ02177",
                ...,
                "SI70103"
            ],
            "release": "R740",
            "release_date": "10/01/2024",
            "url": "https://public.dhe.ibm.com/services/us/igsc/PSP/SF99738.xml"
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible.module_utils import urls
import datetime
import xml.etree.ElementTree as ET
import re


__ibmi_module_version__ = "3.4.0"

PSP_URL = "https://public.dhe.ibm.com/services/us/igsc/PSP/xmldoc.xml"
PTF_URL_TEMPLATE = "https://public.dhe.ibm.com/services/us/igsc/PSP/{}.xml"
PTF_TXT_URL_TEMPLATE = "https://public.dhe.ibm.com/services/us/igsc/PSP/{}.txt"
HTTP_AGENT = "ansible/ibm.power_ibmi"


def get_group_info_from_xml(groups, validate_certs, timeout):
    response = ''
    try:
        response = urls.open_url(PSP_URL, validate_certs=validate_certs, timeout=timeout, http_agent=HTTP_AGENT)
    except Exception as e:
        return [dict(
            url=PSP_URL,
            error=str(e),
        )]
    r = response.read().decode("utf-8")
    root = ET.fromstring(r)
    group_list = []
    groups = list(set([x.upper() for x in groups]))
    list_all = '*ALL' in groups
    found_groups = set()
    for psp in root.findall('psp'):
        group_number = psp.find('number').text
        if group_number is None:
            continue
        if list_all or group_number in groups:
            ptf_list, package_id, url = get_ptf_list_from_xml_or_txt(group_number, validate_certs, timeout)
            if ptf_list is not None:
                group_info = dict(
                    ptf_group_number=group_number,
                    ptf_group_level=int(psp.find('level').text) if psp.find('level') is not None else None,
                    release=psp.find('release').text if psp.find('release') is not None else None,
                    release_date=psp.find('date').text if psp.find('date') is not None else None,
                    description=psp.find('title').text if psp.find('title') is not None else None,
                    url=url,
                    ptf_list=ptf_list,
                    package_id=package_id,
                )
                group_list.append(group_info)
                found_groups.add(group_number)
    # Add missing groups with URLs
    missing_groups = set(groups) - found_groups
    for group in missing_groups:
        ptf_list, package_id, url = get_ptf_list_from_xml_or_txt(group, validate_certs, timeout)
        if ptf_list is not None:
            group_list.append(dict(
                ptf_group_number=group,
                description="Not available in XML",
                ptf_group_level=None,
                release="Not available in XML",
                release_date="Not available in XML",
                ptf_list=ptf_list,
                url=url,
                package_id=package_id,
            ))
    return group_list


def get_ptf_list_from_xml_or_txt(group_number, validate_certs, timeout):
    ptf_list = []
    package_id = None
    ptf_url = PTF_URL_TEMPLATE.format(group_number)
    # Try fetching the XML file
    try:
        response = urls.open_url(ptf_url, validate_certs=validate_certs, timeout=timeout, http_agent=HTTP_AGENT)
        r = response.read().decode("utf-8")
        root = ET.fromstring(r)
        for ptf in root.findall('ptf'):
            ptf_id = ptf.find('number')
            product = ptf.find('licpgm')
            apar = ptf.find('apar')
            date = ptf.find('date')
            ptf_list.append(dict(ptf_id=ptf_id.text, product=product.text, apar=apar.text, date=date.text))
        return ptf_list, package_id, ptf_url
    except Exception as e:
        # If XML file is not found, try fetching the TXT file
        ptf_url = PTF_TXT_URL_TEMPLATE.format(group_number)
        try:
            response = urls.open_url(ptf_url, validate_certs=validate_certs, timeout=timeout, http_agent=HTTP_AGENT)
            r = response.read().decode("utf-8")
            match = re.search(r'PACKAGE ID:\s*(C\d+)', r)
            if match:
                package_id = match.group(1)
            return ptf_list, package_id, ptf_url
        except Exception as e:
            # If TXT file is not found or there's an error, return None
            return None, package_id, ptf_url


def main():
    module = AnsibleModule(
        argument_spec=dict(
            groups=dict(type='list', elements='str', default=['*ALL']),
            validate_certs=dict(type='bool', default=True),
            timeout=dict(type='int', default=60)
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
    timeout = module.params['timeout']

    startd = datetime.datetime.now()
    psp_groups = get_group_info_from_xml(groups_num, validate_certs, timeout)
    result.update({'group_info': psp_groups})
    result.update({'count': len(psp_groups)})

    endd = datetime.datetime.now()
    delta = endd - startd
    result.update({'start': str(startd)})
    result.update({'end': str(endd)})
    result.update({'elapsed_time': str(delta)})
    result.update({'validate_certs': validate_certs})
    result.update({'timeout': timeout})
    result.update({'http_agent': HTTP_AGENT})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
