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
    default: 10
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
from ansible.module_utils import urls
import datetime
import re


__ibmi_module_version__ = "1.9.2"

PSP_URL = "https://www.ibm.com/support/pages/sites/default/files/inline-files/xmldoc.xml"
ALL_GROUP_PAGE = "https://www.ibm.com/support/pages/ibm-i-group-ptfs-level"
HTTP_AGENT = "ansible/ibm.power_ibmi"


# url: https://www.ibm.com/support/pages/ibm-i-group-ptfs-level
# group: 'SF99738'
def get_group_info_from_web(groups, validate_certs, timeout):
    pattern_link = re.compile(
        r'>(?P<rel>R\d{3})<.+?'
        r'(?P<url>https:\/\/\S+?)\".+?>'
        r'(?P<grp>[A-Z]{2}\d{5}):.+?'
        r'(?P<dsc>\w.+?)<.+?'
        r'(?P<lvl>\d{1,5})<.+?>'
        r'(?P<d>\d{2}\/\d{2}\/\d{4})<'
    )
    response = ''
    try:
        response = urls.open_url(ALL_GROUP_PAGE, validate_certs=validate_certs, timeout=timeout, http_agent=HTTP_AGENT)
    except Exception as e:
        return [dict(
                url=ALL_GROUP_PAGE,
                error=str(e),
                )]
    r = response.read().decode("utf-8")
    lines = r.splitlines()
    group_list = []
    groups = list(set([x.upper() for x in groups]))
    list_all = False
    if '*ALL' in groups:
        list_all = True
    for line in lines:
        for ptf_line in re.finditer(pattern_link, line):
            if list_all or ptf_line.group('grp') in groups:
                group_list.append(dict(
                    ptf_group_number=ptf_line.group('grp'),
                    ptf_group_level=int(ptf_line.group('lvl')),
                    release=ptf_line.group('rel'),
                    release_date=ptf_line.group('d'),
                    url=ptf_line.group('url'),
                    description=ptf_line.group('dsc'),
                    ptf_list=get_ptf_list_from_web(
                        ptf_line.group('url'), validate_certs, timeout),
                ))
    return group_list


# url: https://www.ibm.com/support/pages/uid/nas4SF99738
def get_ptf_list_from_web(url, validate_certs, timeout):
    pattern_link = re.compile(
        r'(?P<url>https://www.ibm.com/support/pages/ptf/\S+?)\".+?'
        r'(?P<ptf>[A-Z]{2}\d{5})<.+?'
        r'(?P<date>\d{2}\/\d{2}\/\d{2}).+?'
        r'(?P<apar>[A-Z]{2}\d{5}).+?'
        r'(?P<product>\d{4}\w{3})'
    )
    pattern_packid = r'PACKAGE ID:.+?(?P<packid>[A-Z]\d{7})'
    response = ''
    try:
        response = urls.open_url(url, validate_certs=validate_certs, timeout=timeout, http_agent=HTTP_AGENT)
    except Exception as e:
        return [dict(
                url=url,
                error=str(e),
                )]
    r = response.read().decode("utf-8")
    lines = r.splitlines()
    ptf_list = []
    for line in lines:
        # if it is a cum package
        cum_pack_id = re.search(pattern_packid, line)
        if cum_pack_id:
            return get_cum_ptf_list_from_web(cum_pack_id.group('packid'), validate_certs, timeout)
        # common ptf groups
        for ptf_line in re.finditer(pattern_link, line):
            ptf_list.append(dict(
                ptf_id=ptf_line.group('ptf'),
                product=ptf_line.group('product'),
                apar=ptf_line.group('apar'),
                date=ptf_line.group('date'),
            ))
    return ptf_list


# url: https://www.ibm.com/support/pages/uid/nas4C0128730
def get_cum_ptf_list_from_web(pack_id, validate_certs, timeout):
    pattern_link = re.compile(
        r'(?P<url>https?:\/\/\S+)>'
        r'(?P<ptf>[A-Z]{2}\d{5})<.+'
        r'(?P<lvl>\d{5}).+'
        r'(?P<product>\d{4}\w{3}).+'
        r'(?P<rel>V\dR\dM\d)'
    )
    response = ''
    url = 'https://www.ibm.com/support/pages/uid/nas4' + pack_id
    try:
        response = urls.open_url(url, validate_certs=validate_certs, timeout=timeout, http_agent=HTTP_AGENT)
    except Exception as e:
        return [dict(
                url=url,
                error=str(e),
                )]
    r = response.read().decode("utf-8")
    lines = r.splitlines()
    ptf_list = []
    for line in lines:
        for ptf_line in re.finditer(pattern_link, line):
            ptf_list.append(dict(
                ptf_id=ptf_line.group('ptf'),
                product=ptf_line.group('product'),
                level_added=ptf_line.group('lvl'),
                release=ptf_line.group('rel'),
            ))
    return ptf_list


def main():
    module = AnsibleModule(
        argument_spec=dict(
            groups=dict(type='list', elements='str', default=['*ALL']),
            validate_certs=dict(type='bool', default=True),
            timeout=dict(type='int', default=10)
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
    psp_groups = get_group_info_from_web(groups_num, validate_certs, timeout)
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
