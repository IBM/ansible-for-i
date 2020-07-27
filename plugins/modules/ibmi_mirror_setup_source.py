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
version_added: '2.8'
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
      - The name of the partition designated as the secondary node. It must be same as the current system name.
    type: str
    required: yes
  secondary_node:
    description:
      - The name of the partition designated as the secondary node.
    type: str
    required: yes
  primary_hostname:
    description:
      - String that contains the host and domain name or the IP address of the partition designated as the primary node. IP address is prefered.
    type: str
    required: yes
  secondary_hostname:
    description:
      - String that contains the host and domain name or the IP address of the partition designated as the secondary node. IP address is prefered.
    type: str
    required: yes
  default_inclusion_state:
    description:
      - The default inclusion state setting will be used when no applicable rules for an object are found in the Replication Criteria List (RCL).
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
      - When set to True, this module will excute the terminate mirror without checking the replication state.
    type: bool
    default: False

seealso:
- module: ibmi_mirror_setup_copy

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: config db2 mirror on source node
  ibmi_mirror_setup_source:
    termination_level: RECLONE
    primary_node: NODEA
    secondary_node: NODEB
    primary_hostname: NODEA.COM
    secondary_hostname: NODEB.COM
    default_inclusion_state: INCLUDE
    time_server: TIME.COM
    clone_type: WARM
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
    from itoolkit import iCmd
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

CLOUDINIT_METADATA_DIR = '/QOpenSys/pkgs/lib/cloudinit/cloud/seed/config_drive/openstack/latest'

__ibmi_module_version__ = "9.9.9"


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


def mrdb_set_cluster_config_state(state):
    conn = dbi.connect()
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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return rc


def mrdb_set_mirror_config_state(state):
    conn = dbi.connect()
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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return rc


def mrdb_set_nrg_config_state(state):
    conn = dbi.connect()
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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return rc


def mrdb_start_warm_clone():
    conn = dbi.connect()
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
    ibmi_util.log_debug("qmrdbapi output: " + str(qmrdbapi), sys._getframe().f_code.co_name)
    return rc


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

    if not HAS_ITOOLKIT:
        module.fail_json(rc=999, msg="itoolkit package is required.")
    if not HAS_IBM_DB:
        module.fail_json(rc=999, msg="ibm_db package is required.")

    # get system name
    rc, out, err = ibmi_util.rtvneta()
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when call RTVNETA to get system name: {0}".format(str(err)))
    sys_name = out['SYSNAME']
    ibmi_util.log_info("System name is {0}".format(sys_name), module._name)

    # get local RDBDIRE entry
    rc, out, err, job_log = ibmi_util.itoolkit_run_sql_once(
        "SELECT RDB_NAME FROM QSYS2.ASP_INFO WHERE ASP_NUMBER=1")
    if rc or (len(out) != 1):
        module.fail_json(
            rc=rc, msg="Error occurred when get local RDB name", job_log=job_log)
    rdb_name = out[0]['RDB_NAME']
    ibmi_util.log_info("Local RDB name is {0}".format(rdb_name), module._name)
    # Activation Engine will change the local RDBDIRE name when it matchs system name during openstack deployment,
    # which will cause the Db2 Mirror RCL error due to not same RDBDIRE entry between the pair nodes.
    if rdb_name.strip().upper() == sys_name.strip().upper():
        module.fail_json(
            msg="System name:{0} is same as *LOCAL RDBDIRE name:{1}, which is not allowed in Db2 Mirror configuration.".format(sys_name, rdb_name))

    rc, out, err, job_log = ibmi_util.itoolkit_run_sql_once(
        "SELECT * FROM QSYS2.NRG_INFO")
    if rc or (len(out) != 5):
        module.fail_json(
            rc=rc, msg="NRGs are not configured", job_log=job_log)

    if not terminate_confirmed:
        terminate_msg = "Specify terminate_confirmed as True to force the setup process. CAUTION: it will terminate the mirror."
        state = mrdb_retrieve_mirror_state()
        if state == ERROR:
            module.fail_json(
                rc=state, msg="Error occurred when retrieving the system mirror state. {0}".format(terminate_msg))
        elif state != MRDB_NOT_MIRRORED:
            module.fail_json(
                rc=state, msg="Invalid system mirror state: {0}. {1}".format(get_mirror_state_text(state), terminate_msg))

    rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(
        "CALL QSYS2.TERMINATE_MIRROR('{0}')".format(termination_level))
    if rc and 'ENGINE DATA DOES NOT EXIST' not in str(job_log):
        module.fail_json(
            rc=rc, msg="Error occurred when terminate mirror", job_log=job_log)

    rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(
        "CALL QSYS2.SETUP_MIRROR(\
        PRIMARY_NODE => '{p_node}',\
        SECONDARY_NODE => '{s_node}', \
        PRIMARY_HOSTNAME => '{p_host}', \
        SECONDARY_HOSTNAME => '{s_host}')".format(
            p_node=primary_node,
            s_node=secondary_node,
            p_host=primary_hostname,
            s_host=secondary_hostname))
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when setup mirror", job_log=job_log)

    rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(
        "CALL QSYS2.SET_DEFAULT_INCLUSION_STATE('RESET')")
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when reset default inclusion state", job_log=job_log)
    rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(
        "CALL QSYS2.SET_DEFAULT_INCLUSION_STATE('{0}')".format(default_inclusion_state))
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when set default inclusion state", job_log=job_log)

    rc, out, err = module.run_command(['system', 'QSYS/ENDTCPSVR SERVER(*NTP)'], use_unsafe_shell=False)
    ibmi_util.log_info("ENDTCPSVR *NTP: stdout: " + str(out) + ". stderr: " + str(err), module._name)

    rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(
        "CALL QSYS2.ADD_TIME_SERVER(TIME_SERVER=>'{0}',PREFERRED_INDICATOR=>'YES')".format(time_server))
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when add time server", job_log=job_log)

    rc, out, err = module.run_command(['system', 'QSYS/STRTCPSVR SERVER(*NTP)'], use_unsafe_shell=False)
    ibmi_util.log_info("STRTCPSVR *NTP: stdout: " + str(out) + ". stderr: " + str(err), module._name)
    rc, out, err = module.run_command(['system', 'QSYS/CHGTCPSVR SVRSPCVAL(*NTP) AUTOSTART(*YES)'], use_unsafe_shell=False)
    ibmi_util.log_info("CHGTCPSVR *NTP: stdout: " + str(out) + ". stderr: " + str(err), module._name)

    rc, out, err, job_log = ibmi_util.itoolkit_sql_callproc_once(
        "CALL QSYS2.SET_MIRROR_CLUSTER()")
    if rc:
        module.fail_json(
            rc=rc, msg="Error occurred when set mirror cluster", job_log=job_log)

    result = mrdb_set_nrg_config_state(MrdbConfigComplete)
    if result == ERROR:
        module.fail_json(
            rc=result, msg="Error occurred when setting the nrg configuration state")

    result = mrdb_set_cluster_config_state(MrdbConfigNotReady)
    if result == ERROR:
        module.fail_json(
            rc=result, msg="Error occurred when setting the cluster configuration state")

    result = mrdb_set_mirror_config_state(MrdbConfigInitializing)
    if result == ERROR:
        module.fail_json(
            rc=result, msg="Error occurred when setting the mirror configuration state")

    if os.path.exists(CLOUDINIT_METADATA_DIR + "/meta_data.json"):
        os.remove(CLOUDINIT_METADATA_DIR + "/meta_data.json")

    if clone_type == 'COLD':
        clone_message = 'Power down the system to clone and then power on to make the nodes synchronized.'
    else:
        clone_message = 'Suspend the system to clone and then resume to make the nodes synchronized.'

    module.exit_json(
        rc=SUCCESS, msg="Success to confiure Db2Mirror source node." + clone_message)


if __name__ == '__main__':
    main()
