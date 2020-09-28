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
module: ibmi_module_config
short_description: Configures managed nodes settings
version_added: '2.8.0'
description:
  - The C(ibmi_module_config) module configures the managed nodes settings, like module log settings.
options:
  section:
    description:
      - The section to be configured.
      - When set to C(dump), the current configuration will be displayed
    type: str
    required: yes
    choices: ['log_config', 'dump']
  config_dir:
    description:
      - The configuration file directory.
      - When set to C(home), the configurations takes effect for the current user.
      - When set to C(etc), the configurations takes effect for all the users.
    type: str
    default: 'home'
    choices: ['etc', 'home']
  log_level:
    description:
      - The log level setting.
      - critical > error > warning > info > debug
      - debug, print all the log
      - info, print info,warning,error,critical
      - warning, print warning,error,critical
      - error, print error,critical
      - critical, print critical only
    type: str
    default: 'info'
    choices: ['debug', 'info', 'warning', 'error', 'critical']
  no_log:
    description:
      - If set to C(true), no module log will be written on managed nodes.
    type: bool
    default: False
  log_file:
    description:
      - The modules log file name.
    type: str
    default: 'ibmi_ansible_modules.log'
  log_dir:
    description:
      - The directory of the modules log file.
    type: str
    default: '/var/log'
  max_log_size_mb:
    description:
      - The maximum size of the modules log file, if the log file is larger that this value, an archieve(zip) will be occurred.
    type: int
    default: 5

seealso:
- module: ibmi_cl_command

author:
- Chang Le(@changlexc)
'''

EXAMPLES = r'''
- name: Config the logging as debug level
  ibmi_module_config:
    section: log_config
    config_dir: home
    log_level: debug
'''

RETURN = r'''
version:
    description: The module version string.
    returned: always
    type: str
    sample: '1.0.0'
rc:
    description: The return code (0 means success, non-zero means failure).
    returned: always
    type: int
    sample: 255
msg:
    description: The message descript the return value
    returned: always
    type: str
    sample: 'Success to confiure Ansible module settings'
settings:
    description: The content of current settings
    returned: when rc is 0 and the section is 'dump'
    type: dict
    sample: {
        "log_config": {
            "log_dir": "/var/log",
            "log_file": "ibmi_ansible_modules.log",
            "log_level": "DEBUG",
            "max_log_size_mb": 5,
            "no_log": false
        },
        "time": "2020-06-28 22:01:57.881370"
    }
'''

from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util
from ansible.module_utils.basic import AnsibleModule
import datetime
import json
import os
import pwd

__ibmi_module_version__ = "1.1.2"


def main():
    module = AnsibleModule(
        argument_spec=dict(
            section=dict(type='str', required=True,
                         choices=['log_config', 'dump']),
            config_dir=dict(type='str', default='home',
                            choices=['etc', 'home']),
            log_level=dict(type='str', default='info', choices=[
                           'debug', 'info', 'warning', 'error', 'critical']),
            no_log=dict(type='bool', default=False),
            log_file=dict(type='str', default='ibmi_ansible_modules.log'),
            log_dir=dict(type='str', default='/var/log'),
            max_log_size_mb=dict(type='int', default=5),
        ),
        supports_check_mode=True,
    )
    # Do not log the version since there may be no log configurations
    # ibmi_util.log_info("version: " + __ibmi_module_version__, module._name)

    section = module.params['section']
    config_dir = module.params['config_dir']
    log_level = module.params['log_level']
    no_log = module.params['no_log']
    log_file = module.params['log_file']
    log_dir = module.params['log_dir']
    max_log_size_mb = module.params['max_log_size_mb']

    # When this module supports another section, update the default settings dict
    default_settings = dict(
        time='notset',
        log_config=dict(
            no_log=False,
            log_dir=ibmi_util.IBMi_DEFAULT_LOG_DIR,
            log_file=ibmi_util.IBMi_DEFAULT_LOG_FILE,
            log_level=ibmi_util.IBMi_DEFAULT_LOG_LEVEL_STR,
            max_log_size_mb=int(ibmi_util.IBMi_DEFAULT_MAX_LOG_SIZE / float(1024 * 1024)))
    )

    if section == 'dump':
        try:
            home_log_config_dir = os.getenv('HOME', '')
            home_log_config_file_path = home_log_config_dir + \
                "/" + ibmi_util.IBMi_ANSIBLE_CONFIG_FILE
            etc_log_config_dir = '/etc/ansible'
            etc_log_config_file_path = etc_log_config_dir + \
                "/" + ibmi_util.IBMi_ANSIBLE_CONFIG_FILE
            if os.path.exists(home_log_config_file_path):
                with open(home_log_config_file_path, 'r') as load_f:
                    load_dict = json.load(load_f)
                config_path = home_log_config_file_path
            elif os.path.exists(etc_log_config_file_path):
                with open(etc_log_config_file_path, 'r') as load_f:
                    load_dict = json.load(load_f)
                config_path = etc_log_config_file_path
            else:
                config_path = '*** There is no configuration file either in home or /etc/ansible directory, using default settings ***'
                load_dict = default_settings

            module.exit_json(
                rc=0,
                version=__ibmi_module_version__,
                settings=load_dict,
                msg="Success to dump IBMi Ansible module settings, config file = {0}".format(
                    config_path)
            )
        except Exception as e:
            module.fail_json(
                rc=255,
                version=__ibmi_module_version__,
                msg="Error occurred when dump IBMi Ansible module settings: {0}".format(
                    str(e))
            )

    try:
        mode = 0o0755
        ibmi_util.ensure_dir(log_dir, mode)
    except Exception as e:
        module.fail_json(
            rc=255,
            version=__ibmi_module_version__,
            msg="Error occurred when create IBMi Ansible log directory: {0}, {1}".format(
                log_dir, str(e))
        )
    if not os.access(log_dir, os.W_OK):
        module.fail_json(
            rc=255,
            version=__ibmi_module_version__,
            msg="Current user write permission denied for IBMi Ansible log directory: {0}".format(
                log_dir)
        )

    if config_dir == 'home':
        log_config_dir = os.getenv('HOME', ibmi_util.IBMi_DEFAULT_CONFIG_DIR)
    else:
        log_config_dir = ibmi_util.IBMi_DEFAULT_CONFIG_DIR
    try:
        mode = 0o0755
        ibmi_util.ensure_dir(log_config_dir, mode)
    except Exception as e:
        module.fail_json(
            rc=255,
            version=__ibmi_module_version__,
            msg="Error occurred when create IBMi Ansible configuration directory: {0}, {1}".format(
                log_config_dir, str(e))
        )

    if not os.access(log_config_dir, os.W_OK):
        module.fail_json(
            rc=255,
            version=__ibmi_module_version__,
            msg="Current user write permission denied for IBMi Ansible configuration directory: {0}".format(
                log_config_dir)
        )
    config_dict = default_settings
    config_dict['time'] = str(datetime.datetime.now())
    config_dict[section]['no_log'] = no_log
    config_dict[section]['log_dir'] = log_dir
    config_dict[section]['log_file'] = log_file
    config_dict[section]['log_level'] = log_level.upper()
    config_dict[section]['max_log_size_mb'] = max_log_size_mb

    try:
        log_config_file_path = os.path.join(
            log_config_dir, ibmi_util.IBMi_ANSIBLE_CONFIG_FILE)
        with open(log_config_file_path, 'w') as dump_f:
            json.dump(config_dict, dump_f)
            mode = 0o0644
            os.chmod(log_config_file_path, mode)
    except Exception as e:
        module.fail_json(
            rc=255,
            version=__ibmi_module_version__,
            msg="Error occurred when create IBMi Ansible configuration file: {0}, {1}".format(
                log_config_file_path, str(e))
        )

    if log_config_dir == ibmi_util.IBMi_DEFAULT_CONFIG_DIR:
        try:
            os.chown(log_config_dir, pwd.getpwnam('QSYS').pw_uid, -1)
            os.chown(log_config_file_path, pwd.getpwnam('QSYS').pw_uid, -1)
        except Exception as e:
            ibmi_util.log_info("chown to QSYS error: " + str(e), module._name)

    module.exit_json(
        rc=0,
        version=__ibmi_module_version__,
        msg="Success to configure IBMi Ansible module settings"
    )


if __name__ == '__main__':
    main()
