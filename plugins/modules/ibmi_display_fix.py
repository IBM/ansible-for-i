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
module: ibmi_display_fix
short_description: Displays the PTF(Program Temporary Fix) information and also get the requisite information for the PTF
version_added: 2.8
description:
  - The C(ibmi_display_fix) module displays the information of the PTF and also get the requisite PTFs and their type.
options:
  product:
    description:
      - Specifies the product ID for the PTF.
    type: str
    required: yes
  ptf:
    description:
      - Specifies which PTF is shown for the specified product.
    type: str
    required: yes
  release:
    description:
      - Specifies the release level of the PTF in one of the following formats,
        VxRyMz, for example, V7R2M0 is version 7, release 2, modification 0,
        vvrrmm, this format must be used if the version or release of the product is greater than 9.
        For example, 110300 is version 11, release 3, modification 0.
    type: str
    required: yes
  joblog:
    description:
      - If set to C(true), output the avaiable job log even the rc is 0(success).
    type: bool
    default: False
seealso:
- module: ibmi_fix

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Get PTF information
  ibmi_display_fix:
    product: '5770SS1'
    ptf: 'SI70439'
    release: 'V7R4M0'
'''

RETURN = r'''
requisite_ptf:
    description: The requisite PTFs and their type.
    returned: always
    type: dict
    sample: {
        "SI70030": "*PREREQ",
        "SI71080": "*COREQ",
        "SI71135": "*COREQ",
        "SI71137": "*COREQ",
        "SI71138": "*PREREQ",
        "SI71139": "*PREREQ"
    }
stdout:
    description: The command standard output.
    returned: always
    type: str
    sample: 'CPC2102: Library TESTLIB created'
stderr:
    description: The command standard error.
    returned: always
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
stdout_lines:
    description: The command standard output split in lines
    returned: always
    type: list
    sample: [
        "CPC2102: Library TESTLIB created."
    ]
stderr_lines:
    description: The command standard error split in lines.
    returned: always
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    sample: [{
            "FROM_INSTRUCTION": "318F",
            "FROM_LIBRARY": "QSYS",
            "FROM_MODULE": "",
            "FROM_PROCEDURE": "",
            "FROM_PROGRAM": "QWTCHGJB",
            "FROM_USER": "CHANGLE",
            "MESSAGE_FILE": "QCPFMSG",
            "MESSAGE_ID": "CPD0912",
            "MESSAGE_LIBRARY": "QSYS",
            "MESSAGE_SECOND_LEVEL_TEXT": "Cause . . . . . :   This message is used by application programs as a general escape message.",
            "MESSAGE_SUBTYPE": "",
            "MESSAGE_TEXT": "Printer device PRT01 not found.",
            "MESSAGE_TIMESTAMP": "2020-05-20-21.41.40.845897",
            "MESSAGE_TYPE": "DIAGNOSTIC",
            "ORDINAL_POSITION": "5",
            "SEVERITY": "20",
            "TO_INSTRUCTION": "9369",
            "TO_LIBRARY": "QSYS",
            "TO_MODULE": "QSQSRVR",
            "TO_PROCEDURE": "QSQSRVR",
            "TO_PROGRAM": "QSQSRVR"
        }]
ptf_info:
    description: the ptf information
    returned: always
    type: list
    sample: [
        {
            "PTF_ACTION_PENDING": "NO",
            "PTF_ACTION_REQUIRED": "NONE",
            "PTF_COVER_LETTER": "YES",
            "PTF_CREATION_TIMESTAMP": "2020-05-14-22.08.22.000000",
            "PTF_IDENTIFIER": "SI73329",
            "PTF_IPL_ACTION": "NONE",
            "PTF_IPL_REQUIRED": "IMMEDIATE",
            "PTF_IS_RELEASED": "NO",
            "PTF_LOADED_STATUS": "APPLIED",
            "PTF_MAXIMUM_LEVEL": "00",
            "PTF_MINIMUM_LEVEL": "00",
            "PTF_ON_ORDER": "NO",
            "PTF_PRODUCT_DESCRIPTION": "IBM i",
            "PTF_PRODUCT_ID": "5770SS1",
            "PTF_PRODUCT_LOAD": "5050",
            "PTF_PRODUCT_OPTION": "*BASE",
            "PTF_PRODUCT_RELEASE_LEVEL": "V7R4M0",
            "PTF_RELEASE_LEVEL": "V7R4M0",
            "PTF_SAVE_FILE": "YES",
            "PTF_STATUS_TIMESTAMP": "2020-05-14-22.39.06.000000",
            "PTF_SUPERSEDED_BY_PTF": "",
            "PTF_TECHNOLOGY_REFRESH_PTF": "NO",
            "PTF_TEMPORARY_APPLY_TIMESTAMP": "2020-05-14-22.39.06.000000"
        }
    ]
'''

import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util

__ibmi_module_version__ = "1.0.0-beta1"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            product=dict(type='str', required=True),
            ptf=dict(type='str', required=True),
            release=dict(type='str', required=True),
            joblog=dict(type='bool', default=False),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    product = module.params['product'].strip().upper()
    ptf = module.params['ptf'].strip().upper()
    release = module.params['release'].strip().upper()
    joblog = module.params['joblog']

    if len(product) > 7:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of product exceeds 7 characters")
    if len(ptf) > 7:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of ptf exceeds 7 characters")
    if not (len(release) == 6):
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID, msg="Value of release is not a correct format(VxRyMz or vvrrmm")

    command = 'QSYS/DSPPTF LICPGM({0}) SELECT({1}) RLS({2})'.format(product, ptf, release)
    args = ['system', command]
    rc, out, err = module.run_command(args, use_unsafe_shell=False)

    result = dict(
        command=command,
        rc=rc,
        stdout=out,
        stderr=err,
        ptf_info=[],
        requisite_ptf={},
        job_log=[],
    )

    if rc:
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    requisite_info = []
    formatted_requisite_info = []
    requisite_dict = {}
    ptf_info = out.splitlines()
    for line in ptf_info:
        if product in line:
            formatted_requisite_info = line.split('        ')
            while '' in formatted_requisite_info:
                formatted_requisite_info.remove('')
            requisite_info.extend(formatted_requisite_info)

    formatted_requisite_info = []  # resuse formatted_requisite_info
    for item in requisite_info:
        if ' ' + product + ' ' in item:
            formatted_requisite_info.append(item.strip())

    requisite_info = []  # resuse formatted_requisite_info
    for item in formatted_requisite_info:
        if ptf not in item:
            requisite_info.extend(item.split(product))

    formatted_requisite_info = []  # resuse formatted_requisite_info
    for item in requisite_info:
        formatted_requisite_info.append(item.strip())

    for i in range(0, len(requisite_info), 2):
        requisite_dict[formatted_requisite_info[i]] = formatted_requisite_info[i + 1]
    result.update({'requisite_ptf': requisite_dict})

    sql = "SELECT * FROM QSYS2.PTF_INFO WHERE PTF_PRODUCT_ID = '{0}' and PTF_IDENTIFIER = '{1}' and PTF_PRODUCT_RELEASE_LEVEL = '{2}'".format(
        product, ptf, release)
    rc, out, err, job_log = ibmi_util.itoolkit_run_sql_once(sql)

    result.update({'rc': rc})
    result.update({'stderr': err})
    result.update({'command': sql})
    result.update({'job_log': job_log})

    if rc:
        message = 'non-zero return code:{rc}'.format(rc=rc)
        module.fail_json(msg=message, **result)

    result.update({'ptf_info': out})

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
