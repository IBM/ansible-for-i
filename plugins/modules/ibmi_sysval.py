#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# Author, Xu Meng <mengxumx@cn.ibm.com>


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: ibmi_sysval
short_description: Displays the specified system value
version_added: '2.8.0'
description:
  - The C(ibmi_sysval) module displays the information of the specified system value.
  - Type of requisite values meaning refer to https://www.ibm.com/support/knowledgecenter/en/ssw_ibm_i_74/apis/qwcrsval.htm
  - If the returned system valus is a list, set C(check) to C(equal_as_list) to compare it with the C(expect) value.
options:
  sysvalue:
    description:
      - Specifies the input system values. The detail explanations of the elements in the dict are as follows
      - C(name) is the name of the system value. (required)
      - C(expect) is the expected returned value. (optional)
      - C(check) is the comparison method, including C(equal) and C(equal_as_list). The default value is C(equal) (optional)
    type: list
    elements: dict
    required: yes
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

author:
- Xu Meng(@dmabupt)
'''

EXAMPLES = r'''
- name: Get System Value information
  ibmi_sysval:
    sysvalue:
      - {'name':'qmaxsgnacn', 'expect':'3'}
      - {'name':'qccsid'}
    become_user: 'USER1'
    become_user_password: 'yourpassword'

- name: Compare the returned system valus as list
  ibmi_sysval:
    sysvalue:
      - {'name':'QATNPGM', 'expect':'QEZMAIN   QSYS'}
      - {'name':'QATNPGM', 'expect':'QSYS  QEZMAIN'}
      - {'name':'QATNPGM', 'expect':'QEZMAIN  QSYS', 'check':'equal_as_list'}
      - {'name':'QATNPGM', 'expect':'QSYS QEZMAIN', 'check':'equal_as_list'}
'''

RETURN = r'''
rc:
    description: The command return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
message:
    description: The command execution result.
    returned: when rc is not 0
    type: str
    sample: 'CPF2111:Library TESTLIB already exists'
job_log:
    description: The IBM i job log of the task executed.
    returned: always
    type: list
    elements: dict
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
system_values:
    description: the system value information
    returned: always
    type: list
    elements: dict
    sample: [{
                "compliant": true,
                "expect": "3",
                "name": "QMAXSGNACN",
                "type": "4A",
                "value": "3"
            },
            {
                "compliant": true,
                "name": "QCCSID",
                "type": "10i0",
                "value": "65535"
            }]
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import sys

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

__ibmi_module_version__ = "1.1.2"


sysval_array = [
    {'type': '100A', 'key': ['QSSLPCL']},
    {'type': '152A', 'key': ['QALWOBJRST', 'QSYSLIBL']},
    {'type': '160A', 'key': ['QAUDLVL', 'QSETJOBATR']},
    {'type': '200A', 'key': ['QSCANFS', 'QSCANFSCTL']},
    {'type': '252A', 'key': ['QUSRLIBL']},
    {'type': '1280A', 'key': ['QSSLCSL']},
    {'type': '52A', 'key': ['QAUDCTL']},
    {'type': '316A', 'key': ['QBOOKPATH']},
    {'type': '500A', 'key': ['QALWUSRDMN']},
    {'type': '752A', 'key': ['QPWDRULES']},
    {'type': '80A', 'key': ['QACGLVL']},
    {'type': '992A', 'key': ['QAUDLVL2']},
    {'type': '10i0', 'key': ['QACTJOB', 'QADLACTJ', 'QADLSPLA', 'QADLTOTJ',
                             'QAUDFRCLVL', 'QAUTOVRT', 'QBASACTLVL', 'QBASPOOL', 'QCCSID', 'QENDJOBLMT',
                             'QHSTLOGSIZ', 'QIGCFNTSIZ', 'QJOBMSGQMX', 'QJOBMSGQSZ',
                             'QJOBMSGQTL', 'QJOBSPLA', 'QLEAPADJ', 'QMAXACTLVL',
                             'QMAXJOB', 'QMAXSPLF', 'QMCHPOOL', 'QPRBHLDITV',
                             'QPWDEXPWRN', 'QPWDLVL', 'QPWDMAXLEN', 'QPWDMINLEN',
                             'QPWRDWNLMT', 'QSTGLOWLMT', 'QSVRAUTITV', 'QTOTJOB']},
    {'type': '4A', 'key': ['QABNORMSW', 'QALWJOBITP', 'QAUTOCFG', 'QAUTORMT',
                           'QAUTOSPRPT', 'QCENTURY', 'QCURSYM', 'QDATSEP', 'QDBRCVYWT', 'QDECFMT',
                           'QDSPSGNINF', 'QDYNPTYADJ', 'QDYNPTYSCD', 'QFRCCVNRST', 'QIGC',
                           'QIPLSTS', 'QIPLTYPE', 'QLIBLCKLVL', 'QLMTDEVSSN', 'QLMTSECOFR',
                           'QMAXSGNACN', 'QMLTTHDACN', 'QPFRADJ',
                           'QPRCMLTTSK', 'QPWDLMTAJC', 'QPWDLMTREP', 'QPWDPOSDIF',
                           'QPWDRQDDGT', 'QPWDRQDDIF', 'QPWRRSTIPL', 'QRETSVRSEC',
                           'QRMTIPL', 'QRMTSRVATR', 'QSAVACCPTH', 'QSCPFCONS', 'QSHRMEMCTL',
                           'QSTRPRTWTR', 'QTHDRSCADJ', 'QTIMSEP', 'QVFYOBJRST']},
    {'type': '12A', 'key': ['QASTLVL', 'QAUDENDACN', 'QCHRIDCTL', 'QCMNARB', 'QCONSOLE',
                            'QCRTAUT', 'QCRTOBJAUD', 'QDBFSTCCOL', 'QDEVNAMING', 'QDSCJOBITV',
                            'QINACTITV', 'QJOBMSGQFL', 'QKBDBUF', 'QLOGOUTPUT', 'QPASTHRSVR',
                            'QPRTDEV', 'QPRTKEYFMT', 'QPWDCHGBLK',
                            'QPWDLMTCHR', 'QQRYDEGREE', 'QQRYTIMLMT', 'QRCLSPLSTG',
                            'QSFWERRLOG', 'QSPCENV', 'QSPLFACN', 'QSRVDMP', 'QSSLCSLCTL',
                            'QSTGLOWACN', 'QSTSMSG', 'QTIMZON', 'QTSEPOOL', 'QUSEADPAUT']},
    {'type': '16A', 'key': ['QIPLDATTIM']},
    {'type': '4A', 'key': ['QCNTRYID', 'QHOUR', 'QMINUTE',
                           'QMONTH', 'QSECOND', 'QSECURITY', 'QYEAR']},
    {'type': '20A', 'key': ['QATNPGM', 'QCFGMSGQ', 'QCHRID', 'QCMNRCYLMT',
                            'QCTLSBSD', 'QDATETIME', 'QDEVRCYACN', 'QIGCCDEFNT',
                            'QINACTMSGQ', 'QPRBFTR', 'QPWDVLDPGM', 'QRMTSIGN',
                            'QSRTSEQ', 'QSTRUPPGM', 'QTHDRSCAFN', 'QUPSDLYTIM', 'QUPSMSGQ']},
    {'type': '2076A', 'key': ['QLOCALE']},
    {'type': '4A', 'key': ['QDATFMT', 'QDAY', 'QKBDTYPE', 'QLANGID']},
    {'type': '32A', 'key': ['QPRTTXT', 'QTIMADJ']},
    {'type': '4A', 'key': ['QDAYOFWEEK', 'QMODEL', 'QPRCFEAT']},
    {'type': '8A', 'key': ['QUTCOFFSET']},
    {'type': '8A', 'key': ['QMAXSIGN', 'QPWDEXPITV']},
    {'type': '8A', 'key': ['QDATE']},
    {'type': '8A', 'key': ['QSRLNBR']},
    {'type': '12A', 'key': ['QTIME']},
]


def chk_system_value(current, expect, check='equal'):
    if check == 'equal':
        if current == expect:
            return True
        return False
    elif check == 'equal_as_list':
        if [i for i in current.split() if i not in expect.split()] == []:
            return True
        return False
    return True


def get_system_value(imodule, sysvaluename, expect=None, check='equal'):
    sysvalue = dict()
    sysvalue['name'] = sysvaluename.strip().upper()
    for value in sysval_array:
        for key in value['key']:
            if (sysvalue['name'] == key):
                sysvalue['type'] = value['type']
                if expect is not None:
                    sysvalue['expect'] = expect
                    if not check:
                        check = 'equal'
                    sysvalue['check'] = check
                break

    if sysvalue.get('type') is None:
        return -1, sysvalue, 'Unknown System Value Name'

    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iPgm('qwcrsval', 'QWCRSVAL', {'lib': 'QSYS'})
        .addParm(
            iDS('QWCRSVAL_t', {'len': 'qwcrslen', 'io': 'out'})
            # Number of system values returned
            .addData(iData('count', '10i0', ''))
            # Offset to system value information table
            .addData(iData('offset', '10i0', ''))
            .addData(iData('sysvalue', '10A', ''))           # System value
            # Type of data(C--character / B--binary / blank--not available.)
            .addData(iData('dataType', '1A', ''))
            # Information status(blank--The information was available.)
            .addData(iData('infoStatus', '1A', ''))
            .addData(iData('length', '10i0', ''))            # Length of data
            # Returned system value data
            .addData(iData('data', sysvalue['type'], ''))
        )
        .addParm(iData('rcvlen', '10i0', '', {'setlen': 'qwcrslen'}))
        .addParm(iData('count', '10i0', '1'))
        .addParm(iData('valueName', '10A', sysvalue['name']))
        .addParm(
            iDS('ERRC0100_t', {'len': 'errlen'})
            .addData(iData('bytesProvided', '10i0', '', {'setlen': 'errlen'}))
            .addData(iData('bytesAvailable', '10i0', ''))
            .addData(iData('messageID', '7A', ''))
            .addData(iData('reserved', '1A', ''))
        )
    )
    itool.call(itransport)

    qwcrsval = itool.dict_out('qwcrsval')
    ibmi_util.log_debug(str(qwcrsval), sys._getframe().f_code.co_name)

    if 'success' in qwcrsval:
        qwcrsval_t = qwcrsval['QWCRSVAL_t']
        ibmi_util.log_debug(str(qwcrsval_t), sys._getframe().f_code.co_name)
        if int(qwcrsval_t['count']) > 0:
            sysvalue['value'] = qwcrsval_t['data']
            if 'expect' in sysvalue:
                sysvalue['compliant'] = chk_system_value(
                    sysvalue['value'], sysvalue['expect'], check)
            ibmi_util.log_debug(str(sysvalue), sys._getframe().f_code.co_name)
        return 0, sysvalue, qwcrsval['success']
    return -1, sysvalue, qwcrsval['error']


def main():
    module = AnsibleModule(
        argument_spec=dict(
            sysvalue=dict(type='list', elements='dict', required=True),
            joblog=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )

    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    sysvalue = module.params['sysvalue']
    joblog = module.params['joblog']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if len(sysvalue) == 0:
        module.fail_json(rc=ibmi_util.IBMi_PARAM_NOT_VALID,
                         msg="Not found input system value name")

    result = dict(
        sysval=[],
        rc=0,
        message=''
    )
    rc = 0

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        module.fail_json(rc=999, msg='Exception occurred: {0}'.format(str(inst)))

    for value in sysvalue:
        rc, sysval, message = get_system_value(
            ibmi_module, value.get('name'), value.get('expect'), value.get('check'))
        result['sysval'].append(sysval)

    if rc:
        result.update({'rc': rc})
        result.update({'stderr': message})
        message = 'non-zero return code when get system value:{rc}'.format(
            rc=rc)
        module.fail_json(msg=message, **result)

    if not joblog:
        empty_list = []
        result.update({'job_log': empty_list})
    else:
        result.update({'job_log': message})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
