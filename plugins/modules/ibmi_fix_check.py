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
module: ibmi_fix_check
short_description: Retrieve the latest PTF group information from PSP server.
version_added: '1.1.0'
description:
     - The C(ibmi_fix_check) module retrieve latest PTF group information from PSP(Preventive Service Planning) server.
     - Refer to https://www.ibm.com/support/pages/node/667567 for more details of PSP.
     - ALL PTF groups or specific PTF groups are supported.
options:
  groups:
    description:
      - The list of the PTF groups number.
    type: list
    elements: str
    required: false
  ptfs:
    description:
      - The list of the PTF number.
    type: list
    elements: str
    required: false
  expanded_requisites:
    description:
      - Deep search all its required PTFs.
    type: bool
    default: False
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
  ibm.power_ibmi.ibmi_fix_check:
    groups:
      - "SF12345"

- name: Check the PTF groups without certificate verification
  ibm.power_ibmi.ibmi_fix_check:
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
ptf_info:
    description: PTF information.
    type: list
    returned: When rc is zero.
    sample: [
        {
            "ptf_id": "SI71691",
            "req_list": [
                {
                    "ptf_id": "SI70931",
                    "req_type": "PRE"
                }
            ]
        }
    ]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible.module_utils import urls
import datetime
import time
import re


__ibmi_module_version__ = "2.0.1"

PSP_URL = "https://www.ibm.com/support/pages/sites/default/files/inline-files/xmldoc.xml"
ALL_GROUP_PAGE = "https://www.ibm.com/support/pages/ibm-i-group-ptfs-level"
HTTP_AGENT = "ansible/ibm.power_ibmi"


# url: https://www.ibm.com/support/pages/ibm-i-group-ptfs-level
# group: 'SF99738'
def get_group_info_from_web(groups, certs, timeout):
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
        response = urls.open_url(ALL_GROUP_PAGE, validate_certs=certs, timeout=timeout, http_agent=HTTP_AGENT)
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
                        ptf_line.group('url'), certs, timeout),
                ))
    return group_list


# url: https://www.ibm.com/support/pages/uid/nas4SF99738
def get_ptf_list_from_web(url, certs, timeout):
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
        response = urls.open_url(url, validate_certs=certs, timeout=timeout, http_agent=HTTP_AGENT)
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
            return get_cum_ptf_list_from_web(cum_pack_id.group('packid'), certs, timeout)
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
def get_cum_ptf_list_from_web(pack_id, certs, timeout):
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
        response = urls.open_url(url, validate_certs=certs, timeout=timeout, http_agent=HTTP_AGENT)
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


def get_ptf_info_from_web(ptfs, expanded_requisites, certs, timeout):
    # rel_pattern = r'<td>Release\.+.+>(?P<rel>V\dR\dM\d)<\/td>'
    # product_pattern = r'<td>Licensed Program\.+.+>(?P<rel>\d{4}\w{3})<\/td>'
    ptf_list = []
    ptfs = list(set([x.upper() for x in ptfs]))
    for ptf in ptfs:
        if re.match(r'(SI|MF)\d{5}', ptf):
            req_list = get_ptf_req_from_web(ptf, [], expanded_requisites, certs, timeout)
            ptf_list.append(dict(
                ptf_id=ptf,
                req_list=req_list
            ))
    return ptf_list


# url: https://www.ibm.com/support/pages/ptf/SI71691
# ptfs: 'SI71691'
def get_ptf_req_from_web(ptf, reqs, expanded_requisites, certs, timeout):
    pattern_link = re.compile(r'<tt>(?P<req>(CO|PRE|DIST)).+?(?P<prod>\d{4}\w{3}).+?(?P<ptf>(SI|MF)\d{5}).+?</tt><br>')
    response = ''
    url = 'https://www.ibm.com/support/pages/ptf/' + ptf
    time.sleep(1)
    try:
        response = urls.open_url(url, validate_certs=certs, timeout=timeout, http_agent=HTTP_AGENT)
    except Exception as e:
        return [dict(url=url, error=str(e))]
    r = response.read().decode("utf-8")
    lines = r.splitlines()
    for line in lines:
        for ptf_line in re.finditer(pattern_link, line):
            duplicated = False
            ptf_id = ptf_line.group('ptf')
            for req in reqs:
                if req.get('ptf_id') == ptf_id:
                    duplicated = True
                    break
            if not duplicated:
                reqs.append(dict(
                    ptf_id=ptf_id,
                    req_type=ptf_line.group('req')
                ))
                if expanded_requisites is True:
                    reqs = get_ptf_req_from_web(ptf_id, reqs, expanded_requisites, certs, timeout)
    return reqs


def main():
    module = AnsibleModule(
        argument_spec=dict(
            groups=dict(type='list', elements='str'),
            ptfs=dict(type='list', elements='str'),
            expanded_requisites=dict(type='bool', default=False),
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
        ptf_info=[],
        stderr=''
    )
    group_list = module.params['groups']
    ptf_list = module.params['ptfs']
    expanded_requisites = module.params['expanded_requisites']
    certs = module.params['validate_certs']
    timeout = module.params['timeout']

    startd = datetime.datetime.now()
    if group_list and len(group_list) > 0:
        psp_groups = get_group_info_from_web(group_list, certs, timeout)
        result.update({'group_info': psp_groups})
        result.update({'count': len(psp_groups)})
    if ptf_list and len(ptf_list) > 0:
        psp_ptfs = get_ptf_info_from_web(ptf_list, expanded_requisites, certs, timeout)
        result.update({'ptf_info': psp_ptfs})

    endd = datetime.datetime.now()
    delta = endd - startd
    result.update({'start': str(startd)})
    result.update({'end': str(endd)})
    result.update({'elapsed_time': str(delta)})
    result.update({'expanded_requisites': expanded_requisites})
    result.update({'certs': certs})
    result.update({'timeout': timeout})
    result.update({'http_agent': HTTP_AGENT})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
