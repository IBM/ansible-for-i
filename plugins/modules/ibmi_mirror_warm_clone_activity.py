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
version_added: '1.2.0'
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
- module: ibmi_mirror_setup_source

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: suspend the system for a warm clone to do a clone
  ibm.power_ibmi.ibmi_mirror_warm_clone_activity:
    operation: suspend
'''

RETURN = r'''
msg:
    description: The message that describes the error or success
    returned: always
    type: str
    sample: 'Error occurred when retrieving the mirror state'
rc:
    description: The return code (0 means success, non-zero means failure)
    returned: always
    type: int
    sample: 0
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import sys

HAS_ITOOLKIT = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSrvPgm
    from itoolkit import iData
    from itoolkit import iDS
    from itoolkit.transport import DatabaseTransport as BaseDatabaseTransport

    class DatabaseTransport(BaseDatabaseTransport):
        def _close(self):
            """Don't close connection, we'll manage it ourselves"""
            pass

except ImportError:
    HAS_ITOOLKIT = False


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

__ibmi_module_version__ = "2.0.1"


def mrdb_retrieve_mirror_state(imodule):
    conn = imodule.get_connection()
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


def mrdb_retrieve_config_state(imodule):
    conn = imodule.get_connection()
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


def mrdb_start_engine(imodule):
    conn = imodule.get_connection()
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
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    operation = module.params['operation']
    suspend_timeout = module.params['suspend_timeout']
    become_user = module.params['become_user']
    become_user_password = module.params['become_user_password']

    if not HAS_ITOOLKIT:
        module.fail_json(rc=999, msg="itoolkit package is required.")

    try:
        ibmi_module = imodule.IBMiModule(
            become_user_name=become_user, become_user_password=become_user_password)
    except Exception as inst:
        message = f'Exception occurred: {inst}'
        module.fail_json(rc=999, msg=message)

    # check special authority *IOSYSCFG
    # get current user's special authority
    command = 'RTVUSRPRF'
    if become_user:
        command = command + f' USRPRF({become_user})'
    rc, out, err, job_log = ibmi_module.itoolkit_run_rtv_command_once(
        command, {'SPCAUT': 'char'})
    if rc:
        module.fail_json(
            rc=rc, msg=f"Error occurred when call RTVUSRPRF to special authority: {str(err)}")
    special_authority = out['SPCAUT']
    ibmi_util.log_info(f"Special authority is {special_authority}", module._name)

    if '*IOSYSCFG' not in special_authority:
        module.fail_json(
            rc=rc, msg="Special authority *IOSYSCFG is needed")

    state = mrdb_retrieve_mirror_state(ibmi_module)
    if state == ERROR:
        module.fail_json(
            rc=state, msg="Error occurred when retrieving the system mirror state")

    config_state = mrdb_retrieve_config_state(ibmi_module)
    if config_state == ERROR:
        module.fail_json(
            rc=state, msg="Error occurred when retrieving the system Db2 Mirror configuration state")
    elif config_state != MrdbConfigInitializing:
        module.fail_json(
            rc=state, msg=f"Invalid Db2 Mirror configuration state: {state}")

    if operation == 'resume':
        # resume must run under tracking state
        if state != MRDB_TRACK_STATE:
            module.fail_json(
                rc=state, msg=f"Invalid system mirror state: {state} for suspend activity")
        result = mrdb_start_engine(ibmi_module)
        if result == ERROR:
            module.fail_json(
                rc=result, msg="Error occurred when starting mirror engine")

        command = "db2mtool action=_resume"
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_debug(f"Run command={command}, rc={rc}, stdout={out}, stderr={err}", module._name)
        if 'Resume for ASP *SYSBAS was successful' not in out:
            module.fail_json(rc=rc, msg=f"Error occurred when performing warm clone resume activity, stdout={out}, stderr={err}")
    else:
        # suspend must run under not mirrored state
        if state != MRDB_NOT_MIRRORED:
            module.fail_json(
                rc=state, msg=f"Invalid system mirror state: {state} for suspend activity")
        command = f"db2mtool action=_suspend timeout={suspend_timeout}"
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_debug(f"Run command={command}, rc={rc}, stdout={out}, stderr={err}", module._name)
        if 'Suspend for ASP *SYSBAS was successful' not in out:
            module.fail_json(
                rc=rc, msg=f"Error occurred when when performing warm clone suspend activity, stdout={out}, stderr={err}")

    module.exit_json(
        rc=SUCCESS, msg=f"Success to perform warm clone activity {operation}.")


if __name__ == '__main__':
    main()
