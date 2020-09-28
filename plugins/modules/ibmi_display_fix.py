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
short_description: Displays the PTF(Program Temporary Fix) information and also get the requisite PTFs information of the PTF
version_added: '2.8.0'
description:
  - The C(ibmi_display_fix) module displays the information of the PTF and also get the requisite PTFs.
  - Type of requisite values meaning refer to https://www.ibm.com/support/knowledgecenter/ssw_ibm_i_74/apis/qpzrtvfx.htm#HDRPTFLLH2
options:
  product:
    description:
      - Specifies the product ID for the PTF.
      - Value C('*ONLY') means the product ID is not known, but only one PTF exists on the system by this PTF ID.
    type: str
    default: '*ONLY'
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
      - This field is ignored if C(*ONLY) is specified in the product ID field.
    type: str
    default: '*ALL'
  joblog:
    description:
      - If set to C(true), output the avaiable job log even the rc is 0(success).
    type: bool
    default: False
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
- name: Get PTF information
  ibmi_display_fix:
    product: '5770SS1'
    ptf: 'SI70439'
    release: 'V7R4M0'
'''

RETURN = r'''
requisite_ptf_info:
    description: The requisite PTFs infomation.
    returned: always, empty list if there is no requisite ptf
    type: list
    sample: [
        {
            "RELEASE_OF_REQUISITE": "V7R4M0",
            "REQUISITE_IS_CONDITIONAL": "0",
            "REQUISITE_IS_REQUIRED": "1",
            "REQUISITE_LOAD_ID": "5050",
            "REQUISITE_MAX_LEVLE": "00",
            "REQUISITE_MIN_LEVLE": "00",
            "REQUISITE_OPTION": "0000",
            "REQUISITE_PRODUCT_ID": "5770SS1",
            "REQUISITE_PTF_ID": "SI69832",
            "TYPE_OF_REQUISITE": "1"
        },
        {
            "RELEASE_OF_REQUISITE": "V7R4M0",
            "REQUISITE_IS_CONDITIONAL": "0",
            "REQUISITE_IS_REQUIRED": "1",
            "REQUISITE_LOAD_ID": "5050",
            "REQUISITE_MAX_LEVLE": "00",
            "REQUISITE_MIN_LEVLE": "00",
            "REQUISITE_OPTION": "0000",
            "REQUISITE_PRODUCT_ID": "5770SS1",
            "REQUISITE_PTF_ID": "SI69837",
            "TYPE_OF_REQUISITE": "2"
        },
        {
            "RELEASE_OF_REQUISITE": "V7R4M0",
            "REQUISITE_IS_CONDITIONAL": "0",
            "REQUISITE_IS_REQUIRED": "1",
            "REQUISITE_LOAD_ID": "5050",
            "REQUISITE_MAX_LEVLE": "00",
            "REQUISITE_MIN_LEVLE": "00",
            "REQUISITE_OPTION": "0000",
            "REQUISITE_PRODUCT_ID": "5770SS1",
            "REQUISITE_PTF_ID": "SI69616",
            "TYPE_OF_REQUISITE": "2"
        },
        {
            "RELEASE_OF_REQUISITE": "V7R4M0",
            "REQUISITE_IS_CONDITIONAL": "0",
            "REQUISITE_IS_REQUIRED": "1",
            "REQUISITE_LOAD_ID": "5050",
            "REQUISITE_MAX_LEVLE": "00",
            "REQUISITE_MIN_LEVLE": "00",
            "REQUISITE_OPTION": "0000",
            "REQUISITE_PRODUCT_ID": "5770SS1",
            "REQUISITE_PTF_ID": "SI69618",
            "TYPE_OF_REQUISITE": "2"
        },
        {
            "RELEASE_OF_REQUISITE": "V7R4M0",
            "REQUISITE_IS_CONDITIONAL": "0",
            "REQUISITE_IS_REQUIRED": "1",
            "REQUISITE_LOAD_ID": "5050",
            "REQUISITE_MAX_LEVLE": "00",
            "REQUISITE_MIN_LEVLE": "00",
            "REQUISITE_OPTION": "0000",
            "REQUISITE_PRODUCT_ID": "5770SS1",
            "REQUISITE_PTF_ID": "SI69619",
            "TYPE_OF_REQUISITE": "2"
        },
        {
            "RELEASE_OF_REQUISITE": "V7R4M0",
            "REQUISITE_IS_CONDITIONAL": "0",
            "REQUISITE_IS_REQUIRED": "1",
            "REQUISITE_LOAD_ID": "5050",
            "REQUISITE_MAX_LEVLE": "00",
            "REQUISITE_MIN_LEVLE": "00",
            "REQUISITE_OPTION": "0000",
            "REQUISITE_PRODUCT_ID": "5770SS1",
            "REQUISITE_PTF_ID": "SI69416",
            "TYPE_OF_REQUISITE": "2"
        }
    ]
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
stderr:
    description: The command standard error.
    returned: always, empty string if not error occurred
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
stderr_lines:
    description: The command standard error split in lines.
    returned: always, empty list if not error occurred
    type: list
    sample: [
        "CPF2111:Library TESTLIB already exists."
    ]
job_log:
    description: The IBM i job log of the task executed.
    returned: always, empty list if there is joblog as False and rc as success
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
    returned: always, empty list if the ptf information can not be retrieved
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
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

__ibmi_module_version__ = "1.1.2"


def get_ptf_info(imodule, ptf_id, product_id, release_level):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    system_release_info, err = imodule.get_ibmi_release()
    ibmi_util.log_debug("get_ibmi_release() return release_info: " + str(system_release_info), sys._getframe().f_code.co_name)
    ibmi_util.log_debug("get_ibmi_release() return err: " + str(err), sys._getframe().f_code.co_name)
    # Example output for system_release_info: {'version': 7, 'release': 2, 'version_release': 7.2}
    # Note, version_release is float but not string
    if system_release_info['version_release'] == 7.2:
        itool.add(
            iPgm('qpzrtvfx', 'QPZRTVFX')
            .addParm(
                iDS('PTFR0300_t', {'len': 'rhrlen'})
                .addData(iData('rhrRet', '10i0', ''))
                .addData(iData('rhrAvl', '10i0', ''))
                .addData(iData('rhrOftAddIn', '10i0', ''))
                .addData(iData('rhrPid', '7A', ''))
                .addData(iData('rhrPtfId', '7A', ''))
                .addData(iData('rhrRlsLvl', '6A', ''))
                .addData(iData('rhrPrdOpt', '4A', ''))
                .addData(iData('rhrLodId', '4A', ''))
                .addData(iData('rhrLdSts', '1A', ''))
                .addData(iData('rhrCvrLtrSts', '1A', ''))
                .addData(iData('rhrOnOrdSts', '1A', ''))
                .addData(iData('rhrSavfSts', '1A', ''))
                .addData(iData('rhrFilNam', '10A', ''))
                .addData(iData('rhrFilLibNam', '10A', ''))
                .addData(iData('rhrPtfTyp', '1A', ''))
                .addData(iData('rhrIplAct', '1A', ''))
                .addData(iData('rhrActPnd', '1A', ''))
                .addData(iData('rhrActReq', '1A', ''))
                .addData(iData('rhrPtfRls', '1A', ''))
                .addData(iData('rhrTgtRls', '6A', ''))
                .addData(iData('rhrSpsPtf', '7A', ''))
                .addData(iData('rhrIplSid', '1A', ''))
                .addData(iData('rhrMinLvl', '2A', ''))
                .addData(iData('rhrMaxLvl', '2A', ''))
                .addData(iData('rhrFmtInfAvl', '1A', ''))
                .addData(iData('rhrStsDtaTim', '13A', ''))
                .addData(iData('rhrLicGrp', '7A', ''))
                .addData(iData('rhrSpsByPtf', '7A', ''))
                .addData(iData('rhrSvrIplSrc', '1A', ''))
                .addData(iData('rhrSvrIplRad', '1A', ''))
                .addData(iData('rhrCrtDtaTim', '13A', ''))
                .addData(iData('rhrTecRfsPtf', '1A', ''))
                # .addData(iData('rhrTmpApyDtaTim', '13A', '')) # V7R2M0 does not has this field
                .addData(iData('rhrOftPreReqRec', '10i0', ''))
                .addData(iData('rhrNbrPreReq', '10i0', '', {'enddo': 'mycnt'}))
                .addData(iData('rhrLenPreReq', '10i0', ''))
                .addData(iDS('rhrReqs', {'dim': '999', 'dou': 'mycnt'})
                         .addData(iData('REQUISITE_PRODUCT_ID', '7A', ''))
                         .addData(iData('REQUISITE_PTF_ID', '7A', ''))
                         .addData(iData('RELEASE_OF_REQUISITE', '6A', ''))
                         .addData(iData('REQUISITE_MIN_LEVLE', '2A', ''))
                         .addData(iData('REQUISITE_MAX_LEVLE', '2A', ''))
                         .addData(iData('TYPE_OF_REQUISITE', '1A', ''))
                         .addData(iData('REQUISITE_IS_CONDITIONAL', '1A', ''))
                         .addData(iData('REQUISITE_IS_REQUIRED', '1A', ''))
                         .addData(iData('REQUISITE_OPTION', '4A', ''))
                         .addData(iData('REQUISITE_LOAD_ID', '4A', ''))
                         )
            )
            .addParm(iData('rcvlen', '10i0', '', {'setlen': 'rhrlen'}))
            .addParm(
                iDS('Qpz_Rtv_PTF_Info_t')
                .addData(iData('PTF_ID', '7A', ptf_id))
                .addData(iData('PID', '7A', product_id))
                .addData(iData('Rls_Lvl', '6A', release_level))
                .addData(iData('CCSID', '10i0', ''))
                .addData(iData('Close_Files', '1A', ''))
                .addData(iData('Reserved', '25A', ''))
            )
            .addParm(iData('fmtnam', '8A', 'PTFR0300'))
            .addParm(
                iDS('ERRC0100_t', {'len': 'errlen'})
                .addData(iData('errRet', '10i0', ''))
                .addData(iData('errAvl', '10i0', ''))
                .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                .addData(iData('errRsv', '1A', ''))
            )
        )
    else:
        itool.add(
            iPgm('qpzrtvfx', 'QPZRTVFX')
            .addParm(
                iDS('PTFR0300_t', {'len': 'rhrlen'})
                .addData(iData('rhrRet', '10i0', ''))
                .addData(iData('rhrAvl', '10i0', ''))
                .addData(iData('rhrOftAddIn', '10i0', ''))
                .addData(iData('rhrPid', '7A', ''))
                .addData(iData('rhrPtfId', '7A', ''))
                .addData(iData('rhrRlsLvl', '6A', ''))
                .addData(iData('rhrPrdOpt', '4A', ''))
                .addData(iData('rhrLodId', '4A', ''))
                .addData(iData('rhrLdSts', '1A', ''))
                .addData(iData('rhrCvrLtrSts', '1A', ''))
                .addData(iData('rhrOnOrdSts', '1A', ''))
                .addData(iData('rhrSavfSts', '1A', ''))
                .addData(iData('rhrFilNam', '10A', ''))
                .addData(iData('rhrFilLibNam', '10A', ''))
                .addData(iData('rhrPtfTyp', '1A', ''))
                .addData(iData('rhrIplAct', '1A', ''))
                .addData(iData('rhrActPnd', '1A', ''))
                .addData(iData('rhrActReq', '1A', ''))
                .addData(iData('rhrPtfRls', '1A', ''))
                .addData(iData('rhrTgtRls', '6A', ''))
                .addData(iData('rhrSpsPtf', '7A', ''))
                .addData(iData('rhrIplSid', '1A', ''))
                .addData(iData('rhrMinLvl', '2A', ''))
                .addData(iData('rhrMaxLvl', '2A', ''))
                .addData(iData('rhrFmtInfAvl', '1A', ''))
                .addData(iData('rhrStsDtaTim', '13A', ''))
                .addData(iData('rhrLicGrp', '7A', ''))
                .addData(iData('rhrSpsByPtf', '7A', ''))
                .addData(iData('rhrSvrIplSrc', '1A', ''))
                .addData(iData('rhrSvrIplRad', '1A', ''))
                .addData(iData('rhrCrtDtaTim', '13A', ''))
                .addData(iData('rhrTecRfsPtf', '1A', ''))
                .addData(iData('rhrTmpApyDtaTim', '13A', ''))
                .addData(iData('rhrOftPreReqRec', '10i0', ''))
                .addData(iData('rhrNbrPreReq', '10i0', '', {'enddo': 'mycnt'}))
                .addData(iData('rhrLenPreReq', '10i0', ''))
                .addData(iDS('rhrReqs', {'dim': '999', 'dou': 'mycnt'})
                         .addData(iData('REQUISITE_PRODUCT_ID', '7A', ''))
                         .addData(iData('REQUISITE_PTF_ID', '7A', ''))
                         .addData(iData('RELEASE_OF_REQUISITE', '6A', ''))
                         .addData(iData('REQUISITE_MIN_LEVLE', '2A', ''))
                         .addData(iData('REQUISITE_MAX_LEVLE', '2A', ''))
                         .addData(iData('TYPE_OF_REQUISITE', '1A', ''))
                         .addData(iData('REQUISITE_IS_CONDITIONAL', '1A', ''))
                         .addData(iData('REQUISITE_IS_REQUIRED', '1A', ''))
                         .addData(iData('REQUISITE_OPTION', '4A', ''))
                         .addData(iData('REQUISITE_LOAD_ID', '4A', ''))
                         )
            )
            .addParm(iData('rcvlen', '10i0', '', {'setlen': 'rhrlen'}))
            .addParm(
                iDS('Qpz_Rtv_PTF_Info_t')
                .addData(iData('PTF_ID', '7A', ptf_id))
                .addData(iData('PID', '7A', product_id))
                .addData(iData('Rls_Lvl', '6A', release_level))
                .addData(iData('CCSID', '10i0', ''))
                .addData(iData('Close_Files', '1A', ''))
                .addData(iData('Reserved', '25A', ''))
            )
            .addParm(iData('fmtnam', '8A', 'PTFR0300'))
            .addParm(
                iDS('ERRC0100_t', {'len': 'errlen'})
                .addData(iData('errRet', '10i0', ''))
                .addData(iData('errAvl', '10i0', ''))
                .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                .addData(iData('errRsv', '1A', ''))
            )
        )
    itool.call(itransport)
    qpzrtvfx = itool.dict_out('qpzrtvfx')
    ibmi_util.log_debug(str(qpzrtvfx), sys._getframe().f_code.co_name)
    res_list = []
    if 'success' in qpzrtvfx:
        ptfr0300_t = qpzrtvfx['PTFR0300_t']
        ibmi_util.log_debug(str(ptfr0300_t), sys._getframe().f_code.co_name)
        if int(ptfr0300_t['rhrNbrPreReq']) > 0:
            res = ptfr0300_t['rhrReqs']
            if isinstance(res, dict):
                res_list.append(res)
            elif isinstance(res, list):
                res_list = res
            ibmi_util.log_debug(str(res_list), sys._getframe().f_code.co_name)
        return 0, res_list, qpzrtvfx['success']
    else:
        return -1, res_list, qpzrtvfx['error']


def main():
    module = AnsibleModule(
        argument_spec=dict(
            product=dict(type='str', default='*ONLY'),
            ptf=dict(type='str', required=True),
            release=dict(type='str', default='*ALL'),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    product = module.params['product'].strip().upper()
    ptf = module.params['ptf'].strip().upper()
    release = module.params['release'].strip().upper()
    if release:
        release = release.strip().upper()
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if len(product) > 7:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                         msg="Value of product exceeds 7 characters")
    if len(ptf) > 7:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                         msg="Value of ptf exceeds 7 characters")
    if (release != '*ALL') and (not (len(release) == 6)):
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                         msg="Value of release is not a correct format(VxRyMz or vvrrmm")

    result = dict(
        rc=0,
        ptf_info=[],
        requisite_ptf_info=[],
        job_log=[],
        stderr=''
    )
    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = 'Exception occurred: {0}'.format(str(inst))
        module.fail_json(rc=999, msg=message)

    sql = "SELECT * FROM QSYS2.PTF_INFO WHERE PTF_IDENTIFIER = '{0}' ".format(ptf)
    if product != '*ONLY':
        sql = sql + "and PTF_PRODUCT_ID = '{0}' ".format(product)
    if release != '*ALL':
        sql = sql + "and PTF_PRODUCT_RELEASE_LEVEL = '{0}' ".format(release)
    ibmi_util.log_debug("SQL to run: {0}".format(sql), module._name)

    rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(sql)

    result.update({'job_log': job_log})

    if rc:
        result.update({'rc': rc})
        result.update({'stderr': err})
        message = 'non-zero return code when get PTF information:{rc}'.format(
            rc=rc)
        module.fail_json(msg=message, **result)

    result.update({'ptf_info': out})

    if len(out) > 0:
        if product == '*ONLY':
            product = out[0]['PTF_PRODUCT_ID']
        if release == '*ALL':
            release = out[0]['PTF_RELEASE_LEVEL']
        ibmi_util.log_debug("PTF release level: {0}, product id: {1}, ptf id: {2}".format(
            release, product, ptf), module._name)
        rc, pre_req_list, api_result = get_ptf_info(ibmi_module, ptf, product, release)
        ibmi_util.log_debug("Requisite PTFs info: " +
                            str(pre_req_list), module._name)
        if rc:
            result.update({'rc': rc})
            result.update({'stderr': str(api_result)})
            message = 'non-zero return code when get requisite PTFs infomation:{rc}'.format(
                rc=rc)
            module.fail_json(msg=message, **result)
        result.update({'requisite_ptf_info': pre_req_list})
    else:
        ibmi_util.log_info("No PTF information returned", module._name)
        message = 'No PTF information returned, check if the inputs are correct or if the PTF is loaded status'
        result.update({'rc': ibmi_util.IBMi_PTF_NOT_FOUND})
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})
    module.exit_json(**result)


if __name__ == '__main__':
    main()
