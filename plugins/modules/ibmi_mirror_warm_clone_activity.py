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
module: ibmi_mirror_warm_clone_activity
short_description: Performs suspend and resume activity for warm clone.
version_added: '2.8'
description:
  - The C(ibmi_mirror_warm_clone_activity) module performs the suspend and resume activity for a warm clone
    to reach a quiesce point before the clone and resume from that point after clone.
  - The setup source node must reach a quiesce point before tracking changes can begin.
  - If a quiesce point cannot be reached within the specified timeout, then the setup process will not proceed.
options:
  operation:
    description:
      - Specifies the activity to be performed for a warm clone.
    type: str
    choices: ['suspend', 'resume']
    required: yes
  suspend_timeout:
    description:
      - Specifies the the number of seconds timeout value to allow for the suspend operation to complete.
    type: int
    default: 300

seealso:
- module: ibmi_mirror_setup_source

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: suspend the system for a warm clone to do a clone
  ibmi_mirror_warm_clone_activity:
    operation: suspend
'''

RETURN = r'''
msg:
    description: The message that descript the error or success
    returned: always
    type: str
    sample: 'Error occurred when retrieving the mirror state'
job_log:
    description: the job_log
    returned: always
    type: str
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
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 0
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
import os
import sys

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSrvPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport
except ImportError:
    HAS_ITOOLKIT = False

try:
    import ibm_db_dbi as dbi
except ImportError:
    HAS_IBM_DB = False

# The mirror state
MRDB_NOT_MIRRORED = 0
MRDB_REPLICATE_STATE = 1
MRDB_TRACK_STATE = 2
MRDB_BLOCKED_STATE = 3

# The configuration state
MrdbConfigNotReady = 0
MrdbConfigInitializing = 1
MrdbConfigComplete = 2

SUCCESS = 0
ERROR = -1

__ibmi_module_version__ = "9.9.9"


def mrdb_retrieve_mirror_state():
    conn = dbi.connect()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbRtvSysState_r').addParm(
            iData('rState', '2i0', '')).addParm(
                iDS('MrdbSPIResult').addData(
                    iData('result', '10i0', '')).addData(
                        iData('additionalErrorCode', '10i0', '')).addData(
                            iData('offset', '10i0', '')).addData(
                                iData('reserved', '52a', ''))))
    # xmlservice
    itool.call(itransport)
    # output
    qmrdbapi = itool.dict_out('qmrdbapi')
    result = qmrdbapi['MrdbSPIResult']
    state = ERROR
    if ('success' in qmrdbapi) and (int(result['result']) == 0):
        state = int(qmrdbapi['rState'])
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return state


def mrdb_retrieve_config_state():
    conn = dbi.connect()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbRtvCfgState').addParm(
            iData('rState', '2i0', '')).addParm(
                iDS('MrdbSPIResult').addData(
                    iData('result', '10i0', '')).addData(
                        iData('additionalErrorCode', '10i0', '')).addData(
                            iData('offset', '10i0', '')).addData(
                                iData('reserved', '52a', ''))))
    # xmlservice
    itool.call(itransport)
    # output
    qmrdbapi = itool.dict_out('qmrdbapi')
    result = qmrdbapi['MrdbSPIResult']
    state = ERROR
    if ('success' in qmrdbapi) and (int(result['result']) == 0):
        state = int(qmrdbapi['rState'])
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return state


def mrdb_start_engine():
    conn = dbi.connect()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbStartEngine').addParm(
            iDS('MrdbSPIResult').addData(
                iData('result', '10i0', '')).addData(
                    iData('additionalErrorCode', '10i0', '')).addData(
                        iData('offset', '10i0', '')).addData(
                            iData('reserved', '52a', ''))))
    itool.call(itransport)
    qmrdbapi = itool.dict_out('qmrdbapi')
    result = qmrdbapi['MrdbSPIResult']
    rc = ERROR
    if ('success' in qmrdbapi) and (int(result['result']) == 0):
        rc = SUCCESS
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return rc


def main():
    module = AnsibleModule(
        argument_spec=dict(
            operation=dict(type='str', choices=[
                           'suspend', 'resume'], required=True),
            suspend_timeout=dict(type='int', default=300),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    operation = module.params['operation']
    suspend_timeout = module.params['suspend_timeout']

    if not HAS_ITOOLKIT:
        module.fail_json(rc=999, msg="itoolkit package is required.")
    if not HAS_IBM_DB:
        module.fail_json(rc=999, msg="ibm_db package is required.")

    state = mrdb_retrieve_mirror_state()
    if state == ERROR:
        module.fail_json(
            rc=state, msg="Error occurred when retrieving the system mirror state")

    config_state = mrdb_retrieve_config_state()
    if config_state == ERROR:
        module.fail_json(
            rc=state, msg="Error occurred when retrieving the system Db2 Mirror configuration state")
    elif config_state != MrdbConfigInitializing:
        module.fail_json(
            rc=state, msg="Invalid Db2 Mirror configuration state: {0}".format(state))

    if operation == 'resume':
        # resume must run under tracking state
        if state != MRDB_TRACK_STATE:
            module.fail_json(
                rc=state, msg="Invalid system mirror state: {0} for suspend activity".format(state))
        result = mrdb_start_engine()
        if result == ERROR:
            module.fail_json(
                rc=result, msg="Error occurred when starting mirror engine")

        command = "db2mtool action=_resume"
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_debug("Run command={0}, rc={1}, stdout={2}, stderr={3}".format(command, rc, out, err), module._name)
        if 'Resume for ASP *SYSBAS was successful' not in out:
            module.fail_json(rc=rc, msg="Error occurred when performing warm clone resume activity", stdout=out, stderr=err)
    else:
        # suspend must run under not mirrored state
        if state != MRDB_NOT_MIRRORED:
            module.fail_json(
                rc=state, msg="Invalid system mirror state: {0} for suspend activity".format(state))
        command = "db2mtool action=_suspend timeout={0}".format(
            suspend_timeout)
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_debug("Run command={0}, rc={1}, stdout={2}, stderr={3}".format(command, rc, out, err), module._name)
        if 'Suspend for ASP *SYSBAS was successful' not in out:
            module.fail_json(rc=rc, msg="Error occurred when when performing warm clone suspend activity", stdout=out, stderr=err)

    module.exit_json(
        rc=SUCCESS, msg="Success to perform warm clone activity {0}.".format(operation))


if __name__ == '__main__':
    main()
