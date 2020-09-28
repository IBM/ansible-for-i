from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import os
import json
import datetime
import tempfile
import logging
import logging.config
import zipfile
import binascii
import socket

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlQuery
    from itoolkit import iCmd
    from itoolkit import iCmd5250
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

from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import db2i_tools

# Constants
IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT = 258
IBMi_COMMAND_RC_INVALID_EXPECTED_ROW_COUNT = 259
IBMi_PARAM_NOT_VALID = 260
IBMi_NO_ROW_FOUND_ERROR = 261
IBMi_SUBSYSTEM_NOT_ACTIVE = 262
IBMi_END_ALL_SUBSYSTEM_NOT_ALLOWED = 263
IBMi_PTF_NOT_FOUND = 264

IBMi_SQL_RC_ERROR = 301

IBMi_PACKAGES_NOT_FOUND = 998
IBMi_DB_CONNECTION_ERROR = 997
IBMi_COMMAND_RC_UNEXPECTED = 999

SYSBAS = '*SYSBAS'

IBMi_DEFAULT_CONFIG_DIR = '/etc/ansible'
IBMi_ANSIBLE_CONFIG_FILE = 'ibmi_ansible.cfg'
IBMi_DEFAULT_LOG_DIR = '/var/log'
IBMi_DEFAULT_LOG_FILE = 'ibmi_ansible_modules.log'
IBMi_DEFAULT_LOG_LEVEL_STR = 'INFO'
IBMi_DEFAULT_MAX_LOG_SIZE = 5 * 1024 * 1024


def fmtTo10(str):
    return str.ljust(10) if len(str) <= 10 else str[0:10]


def get_host_and_ip():
    hostname = 'UNKNOWN_HOST'
    ip = 'UNKNOWN_IP'
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except Exception:
        pass
    return hostname, ip


def log_debug(s, module_name="ibmi_util"):
    hostname = 'UNKNOWN_HOST'
    ip = 'UNKNOWN_IP'
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
    except Exception:
        pass
    try:
        get_logger("ibmi_util").debug("%s(%s) - %s: %s", hostname, ip, module_name, s)
    except Exception:
        pass


def log_info(s, module_name="ibmi_util"):
    hostname, ip = get_host_and_ip()
    try:
        get_logger("ibmi_util").info("%s(%s) - %s: %s", hostname, ip, module_name, s)
    except Exception:
        pass


def log_error(s, module_name="ibmi_util"):
    hostname, ip = get_host_and_ip()
    try:
        get_logger("ibmi_util").error("%s(%s) - %s: %s", hostname, ip, module_name, s)
    except Exception:
        pass


def log_warning(s, module_name="ibmi_util"):
    hostname, ip = get_host_and_ip()
    try:
        get_logger("ibmi_util").warning("%s(%s) - %s: %s", hostname, ip, module_name, s)
    except Exception:
        pass


def log_critical(s, module_name="ibmi_util"):
    hostname, ip = get_host_and_ip()
    try:
        get_logger("ibmi_util").critical("%s(%s) - %s: %s", hostname, ip, module_name, s)
    except Exception:
        pass


def get_logger(module_name, log_level=logging.INFO):
    ibmi_logging, no_log = setup_logging(log_level)
    if no_log:
        return
    return ibmi_logging.getLogger(module_name)


def ensure_dir(path, mode=0o0755):
    ensured = set()
    dirs_created = set()
    path = os.path.abspath(path)
    if path not in ensured and not os.path.exists(path):
        ensured.add(path)
        d, f = os.path.split(path)
        ensure_dir(d, mode)
        os.mkdir(path, mode)
        dirs_created.add(path)


def archive_log(log_path, log_file, max_log_size):
    log_file_path = os.path.join(log_path, log_file)
    if os.path.exists(log_file_path):
        log_size = os.path.getsize(log_file_path)
        if log_size > max_log_size:
            zip_log_file = log_file + '_' + str(datetime.datetime.now()).replace(' ', '_').replace(':', '.')
            zip_log_file_path = os.path.join(log_path, zip_log_file)
            os.rename(log_file_path, zip_log_file_path)
            z = zipfile.ZipFile(zip_log_file_path + '.zip', 'w', zipfile.ZIP_DEFLATED)
            z.write(zip_log_file_path)
            z.close()
            os.remove(zip_log_file_path)


def setup_logging(detault_log_level=logging.INFO):
    """Default logging configuration in /etc/ansible/ibmi_ansible.cfg"""
    """
    {
        "log_config":
        {
            "log_level": "INFO",
            "log_dir": "/var/log",
            "log_file": "ibmi_ansible_modules.log",
            "no_log": false,
            "max_log_size_mb": 5
        }
    }
    """
    default_log_config_path = IBMi_DEFAULT_CONFIG_DIR
    log_path = IBMi_DEFAULT_LOG_DIR
    try:
        ensure_dir(log_path, mode=0o0777)
    except Exception:
        log_path = tempfile.gettempdir()

    log_file = IBMi_DEFAULT_LOG_FILE
    log_file_path = os.path.join(log_path, log_file)
    log_level_str = IBMi_DEFAULT_LOG_LEVEL_STR
    no_log = False
    max_log_size = IBMi_DEFAULT_MAX_LOG_SIZE
    """Setup logging configuration"""
    try:
        log_config_path = os.getenv('HOME', default_log_config_path)
        log_config_file_path = os.path.join(log_config_path, IBMi_ANSIBLE_CONFIG_FILE)
        # Try again to read from default log config path
        if not os.path.exists(log_config_file_path):
            log_config_file_path = os.path.join(default_log_config_path, IBMi_ANSIBLE_CONFIG_FILE)
        with open(log_config_file_path, 'r') as load_f:
            log_dict = json.load(load_f)
        no_log = log_dict['log_config']['no_log']
        log_path = log_dict['log_config']['log_dir']
        log_file = log_dict['log_config']['log_file']
        log_level_str = log_dict['log_config']['log_level']
        max_log_size = log_dict['log_config']['max_log_size_mb']
        max_log_size = max_log_size * 1024 * 1024
        ensure_dir(log_path, mode=0o0777)
        log_file_path = os.path.join(log_path, log_file)
    except Exception:
        pass

    log_level = logging.getLevelName(log_level_str)
    archive_log(log_path, log_file, max_log_size)
    logging.basicConfig(filename=log_file_path, filemode="a", level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        os.chmod(log_file_path, 0o0777)
    except Exception:
        pass

    return logging, no_log
