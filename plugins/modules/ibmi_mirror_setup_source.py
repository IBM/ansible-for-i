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
module: ibmi_mirror_setup_source
short_description: Configures the Db2 Mirror on the source node
version_added: '1.2.0'
description:
  - The C(ibmi_mirror_setup_source) module configures the Db2 Mirror on the source node and
    sets the configuration state to initializing.
options:
  termination_level:
    description:
      - The TERMINATE_MIRROR procedure ends all replication between the primary and secondary nodes
        and resets the replication state of both nodes to NOT MIRRORED.
        A clone operation is required to restart replication.
        When termination_level is RECLONE, all Db2 Mirror configuration information is retained.
        When termination_level is DESTROY, all Db2 Mirror configuration information is deleted.
    type: str
    choices: ['RECLONE', 'DESTROY']
    default: 'RECLONE'
  primary_node:
    description:
      - The name of the partition designated as the secondary node.
        It must be same as the current system name.
    type: str
    required: yes
  secondary_node:
    description:
      - The name of the partition designated as the secondary node.
    type: str
    required: yes
  primary_hostname:
    description:
      - String that contains the host and domain name or IP address of the partition designated as the primary node.
        IP address is preferred.
    type: str
    required: yes
  secondary_hostname:
    description:
      - String that contains the host and domain name or IP address of the partition designated as the secondary node.
        IP address is preferred.
    type: str
    required: yes
  default_inclusion_state:
    description:
      - The default inclusion state setting will be used
        when no applicable rules for an object are found in the Replication Criteria List (RCL).
    type: str
    choices: ['EXCLUDE', 'INCLUDE']
    default: 'EXCLUDE'
  time_server:
    description:
      - String that identifies the DNS name of the NTP server to be added to the configuration.
        A time server must be used to keep the clocks of the nodes synchronized.
    type: str
    required: yes
  clone_type:
    description:
      - Indicates the clone is warm clone or cold clone
        A cold clone requires the setup source node to be shut down during the cloning portion of the setup process.
        A warm clone allows the setup source node to remain active during the entire Db2 Mirror setup and configuration process.
    type: str
    choices: ['COLD', 'WARM']
    default: 'COLD'
  terminate_confirmed:
    description:
      - A bool value to indicate the terminate mirror action is confirmed.
      - When set to False, only the replication state as NOT_MIRRORED is allowed to run this module.
      - When set to True, this module will execute the terminate mirror without checking the replication state.
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
- module: ibmi_mirror_setup_copy

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: config db2 mirror on source node
  ibm.power_ibmi.ibmi_mirror_setup_source:
    termination_level: RECLONE
    primary_node: NODEA
    secondary_node: NODEB
    primary_hostname: 10.0.0.1
    secondary_hostname: 10.0.0.2
    default_inclusion_state: INCLUDE
    time_server: TIME.COM
    clone_type: WARM
'''

RETURN = r'''
msg:
    description: The message that describes the error or success
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
from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_module as imodule
import sys
import os

HAS_ITOOLKIT = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSrvPgm
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

CLOUDINIT_METADATA_DIR = '/QOpenSys/pkgs/lib/cloudinit/cloud/seed/config_drive/openstack/latest'

__ibmi_module_version__ = "2.0.1"


def get_mirror_state_text(state):
    if state == MRDB_NOT_MIRRORED:
        return "Not mirrored"
    elif state == MRDB_REPLICATE_STATE:
        return "Replicating"
    elif state == MRDB_TRACK_STATE:
        return "Tracking"
    elif state == MRDB_BLOCKED_STATE:
        return "Blocked"
    else:
        return "Unknown"


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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi),
                        sys._getframe().f_code.co_name)
    return state


def mrdb_set_cluster_config_state(imodule, state):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbSetClusterCfgState').addParm(
            iData('state', '2i0', str(state), {'io': 'in'})).addParm(
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
    rc = ERROR
    if ('success' in qmrdbapi) and (int(result['result']) == 0):
        rc = SUCCESS
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi),
                        sys._getframe().f_code.co_name)
    return rc


def mrdb_set_mirror_config_state(imodule, state):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbSetCfgState').addParm(
            iData('state', '2i0', str(state), {'io': 'in'})).addParm(
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
    rc = ERROR
    if ('success' in qmrdbapi) and (int(result['result']) == 0):
        rc = SUCCESS
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi),
                        sys._getframe().f_code.co_name)
    return rc


def mrdb_set_nrg_config_state(imodule, state):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbSetNrgCfgState').addParm(
            iData('state', '2i0', str(state), {'io': 'in'})).addParm(
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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi),
                        sys._getframe().f_code.co_name)
    return rc


def mrdb_start_warm_clone(imodule):
    conn = imodule.get_connection()
    itransport = DatabaseTransport(conn)
    itool = iToolKit()
    itool.add(
        iSrvPgm('qmrdbapi', 'QMRDBAPI', 'QmrdbStartWarmClone').addParm(
            iData('asp', '2i0', '0', {'io': 'in'})).addParm(
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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi),
                        sys._getframe().f_code.co_name)
    return rc


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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi),
                        sys._getframe().f_code.co_name)
    return rc


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


def check_required_product(imodule):
    required_product_list = [
        dict(product_id='*OPSYS',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0003",
             ),
        dict(product_id='*OPSYS',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0012",
             ),
        dict(product_id='*OPSYS',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0030",
             ),
        dict(product_id='*OPSYS',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0033",
             ),
        dict(product_id='*OPSYS',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0041",
             ),
        dict(product_id='*OPSYS',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0048",
             ),
        dict(product_id='5770JV1',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0000",
             ),
        dict(product_id='5770JV1',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0016",
             ),
        dict(product_id='5770JV1',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0017",
             ),
        dict(product_id='5733SC1',
             release_level='*ONLY',
             load_id="*CODE",
             product_option="0000",
             ),
        dict(product_id='5733SC1',
             release_level='*ONLY',
             load_id="*CODE",
             product_option="0001",
             ),
        dict(product_id='5770DBM',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0000",
             ),
        dict(product_id='5770DBM',
             release_level='*CUR',
             load_id="*CODE",
             product_option="0001",
             ),
    ]
    not_installed_product_list = []
    for item in required_product_list:
        rc, product_info, out = get_product_info(
            imodule, item['product_id'], item['release_level'], item['product_option'], item['load_id'])
        if (rc == 0) and (product_info['Load_Error_Indicator'] == '*NONE') and (product_info['Symbolic_Load_State'] == '*INSTALLED'):
            continue
        not_installed_product_list.append(item)
    return not_installed_product_list


def main():
    module = AnsibleModule(
        argument_spec=dict(
            termination_level=dict(type='str', choices=[
                                   'RECLONE', 'DESTROY'], default='RECLONE'),
            primary_node=dict(type='str', required=True),
            secondary_node=dict(type='str', required=True),
            primary_hostname=dict(type='str', required=True),
            secondary_hostname=dict(type='str', required=True),
            default_inclusion_state=dict(
                type='str', choices=['EXCLUDE', 'INCLUDE'], default='EXCLUDE'),
            time_server=dict(type='str', required=True),
            clone_type=dict(type='str', choices=[
                            'COLD', 'WARM'], default='COLD'),
            terminate_confirmed=dict(type='bool', default=False),
            become_user=dict(type='str'),
            become_user_password=dict(type='str', no_log=True),
        ),
        supports_check_mode=True,
    )
    ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    termination_level = module.params['termination_level']
    primary_node = module.params['primary_node']
    secondary_node = module.params['secondary_node']
    primary_hostname = module.params['primary_hostname']
    secondary_hostname = module.params['secondary_hostname']
    default_inclusion_state = module.params['default_inclusion_state']
    time_server = module.params['time_server']
    clone_type = module.params['clone_type']
    terminate_confirmed = module.params['terminate_confirmed']
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

    # check system level is 7.4 or higher
    system_release_info, err = ibmi_module.get_ibmi_release()
    ibmi_util.log_debug(
        f"get_ibmi_release() return release_info={str(system_release_info)}, error={str(err)} ", sys._getframe().f_code.co_name)
    # Example output for system_release_info: {'version': 7, 'release': 2, 'version_release': 7.2}
    # Note, version_release is float but not string
    if system_release_info['version_release'] < 7.4:
        module.fail_json(
            rc=255, msg="Db2 Mirror requires IBM i 7.4 or higher")

    # check required products
    not_installed_product_list = check_required_product(ibmi_module)
    if len(not_installed_product_list) > 0:
        module.fail_json(
            rc=255, msg=f"Db2 Mirror required Products and Options are not installed: {str(not_installed_product_list)}")

    # check cloud-init
    '''
        command = "/QOpenSys/pkgs/bin/rpm -q cloud-init --queryformat '%{VERSION}'"
        rc, out, err = module.run_command(command, use_unsafe_shell=False)
        ibmi_util.log_debug("Run command={0}, rc={1}, stdout={2}, stderr={3}".format(
            command, rc, out, err), module._name)
        if rc or (('1.2' not in out) and ('1.3' not in out)):
            module.fail_json(
                rc=rc, msg="Db2 Mirror requires cloud-init 1.2 or above installed")
    '''
    # check local rdbdire name should not be same as system name
    # get system name
    rc, out, err, job_log = ibmi_module.itoolkit_run_rtv_command_once(
        'RTVNETA', {'SYSNAME': 'char'})
    if rc:
        module.fail_json(
            rc=rc, msg=f"Error occurred when call RTVNETA to get system name: {str(err)}")
    sys_name = out['SYSNAME']
    ibmi_util.log_info(f"System name is {sys_name}", module._name)

    # get local RDBDIRE entry
    rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(
        "SELECT RDB_NAME FROM QSYS2.ASP_INFO WHERE ASP_NUMBER=1")
    if rc or (len(out) != 1):
        module.fail_json(
            rc=rc, msg="Error occurred when get local RDB name", job_log=job_log)
    rdb_name = out[0]['RDB_NAME']
    ibmi_util.log_info(f"Local RDB name is {rdb_name}", module._name)
    # Activation Engine will change the local RDBDIRE name when it matches system name during openstack deployment,
    # which will cause the Db2 Mirror RCL error due to not same RDBDIRE entry between the pair nodes.
    if rdb_name.strip().upper() == sys_name.strip().upper():
        module.fail_json(
            msg=f"System name:{sys_name} is same as *LOCAL RDBDIRE name:{rdb_name}, which is not allowed in Db2 Mirror configuration.")

    # check nrg config is ready
    rc, out, err, job_log = ibmi_module.itoolkit_run_sql_once(
        "SELECT * FROM QSYS2.NRG_INFO")
    if rc or (len(out) != 5):
        module.fail_json(
            rc=rc, msg="NRGs are not configured", job_log=job_log)

    if not terminate_confirmed:
        terminate_msg = "Specify terminate_confirmed as True to force the setup process. CAUTION: it will terminate the mirror."
        state = mrdb_retrieve_mirror_state(ibmi_module)
        if state == ERROR:
            module.fail_json(
                rc=state, msg=f"Error occurred when retrieving the system mirror state. {terminate_msg}")
        elif state != MRDB_NOT_MIRRORED:
            module.fail_json(
                rc=state, msg=f"Invalid system mirror state: {get_mirror_state_text(state)}. {terminate_msg}")

    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(
        f"CALL QSYS2.TERMINATE_MIRROR('{termination_level}')")
    if rc and 'ENGINE DATA DOES NOT EXIST' not in str(job_log):
        module.fail_json(
            rc=rc, msg="Error occurred when terminate mirror", job_log=job_log)
    if termination_level == 'DESTROY':
        module.exit_json(
            rc=SUCCESS, msg="Success to terminate mirror with DESTORY Db2Mirror configuration on source node. Re-configuration NRG is required.")

    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(
        f"CALL QSYS2.SETUP_MIRROR(\
        PRIMARY_NODE => '{primary_node}',\
        SECONDARY_NODE => '{secondary_node}', \
        PRIMARY_HOSTNAME => '{primary_hostname}', \
        SECONDARY_HOSTNAME => '{secondary_hostname}')")
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when setting up mirror primary and secondary role", job_log=job_log)

    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(
        "CALL QSYS2.SET_DEFAULT_INCLUSION_STATE('RESET')")
    if rc and ("WARNING, FOUND AND REGISTERED AN EXISTING RCL OBJECT" not in str(job_log)):
        module.fail_json(
            rc=rc, msg="Error occurred when resetting default inclusion state", job_log=job_log)
    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(
        f"CALL QSYS2.SET_DEFAULT_INCLUSION_STATE('{default_inclusion_state}')")
    if rc and ("WARNING, FOUND AND REGISTERED AN EXISTING RCL OBJECT" not in str(job_log)):
        module.fail_json(
            rc=rc, msg="Error occurred when setting default inclusion state", job_log=job_log)

    rc, out, err = module.run_command(
        ['system', 'QSYS/ENDTCPSVR SERVER(*NTP)'], use_unsafe_shell=False)
    ibmi_util.log_info("ENDTCPSVR *NTP: stdout: " +
                       str(out) + ". stderr: " + str(err), module._name)

    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(
        f"CALL QSYS2.ADD_TIME_SERVER(TIME_SERVER=>'{time_server}',PREFERRED_INDICATOR=>'YES')")
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when adding time server", job_log=job_log)

    rc, out, err = module.run_command(
        ['system', 'QSYS/STRTCPSVR SERVER(*NTP)'], use_unsafe_shell=False)
    ibmi_util.log_info("STRTCPSVR *NTP: stdout: " +
                       str(out) + ". stderr: " + str(err), module._name)
    rc, out, err = module.run_command(
        ['system', 'QSYS/CHGTCPSVR SVRSPCVAL(*NTP) AUTOSTART(*YES)'], use_unsafe_shell=False)
    ibmi_util.log_info("CHGTCPSVR *NTP: stdout: " +
                       str(out) + ". stderr: " + str(err), module._name)
    rc, out, err = module.run_command(
        ['system', 'QSYS/CHGTCPSVR SVRSPCVAL(*SSHD) AUTOSTART(*YES)'], use_unsafe_shell=False)
    ibmi_util.log_info("CHGTCPSVR *SSHD: stdout: " +
                       str(out) + ". stderr: " + str(err), module._name)

    rc, out, err, job_log = ibmi_module.itoolkit_sql_callproc_once(
        "CALL QSYS2.SET_MIRROR_CLUSTER()")
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when setting mirror cluster", job_log=job_log)

    result = mrdb_set_nrg_config_state(ibmi_module, MrdbConfigComplete)
    if result == ERROR:
        module.fail_json(
            rc=result, msg="Error occurred when setting the nrg configuration state")

    result = mrdb_set_cluster_config_state(ibmi_module, MrdbConfigNotReady)
    if result == ERROR:
        module.fail_json(
            rc=result, msg="Error occurred when setting the cluster configuration state")

    result = mrdb_set_mirror_config_state(ibmi_module, MrdbConfigInitializing)
    if result == ERROR:
        module.fail_json(
            rc=result, msg="Error occurred when setting the mirror configuration state")

    if os.path.exists(CLOUDINIT_METADATA_DIR + "/meta_data.json"):
        os.remove(CLOUDINIT_METADATA_DIR + "/meta_data.json")

    if clone_type == 'COLD':
        clone_message = 'Power down the system to clone and then power on after clone to make the nodes synchronized.'
    else:
        clone_message = 'Suspend the system to clone and then resume after clone to make the nodes synchronized.'

    module.exit_json(
        rc=SUCCESS, msg="Success to configure Db2Mirror source node." + clone_message)


if __name__ == '__main__':
    main()
