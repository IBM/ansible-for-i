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

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit import iCmd
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


def itoolkit_init(db_name=SYSBAS):
    conn = None
    if not HAS_ITOOLKIT:
        raise ImportError("itoolkit package is required.")
    if not HAS_IBM_DB:
        raise ImportError("ibm_db package is required.")
    try:
        if db_name != SYSBAS:
            conn = dbi.connect(database='{db_pattern}'.format(db_pattern=db_name))
        else:
            conn = dbi.connect()
        job_name_info = db2i_tools.get_current_job_name(conn)
        log_info("Job of the connection to execute the task: {0}".format(job_name_info),
                 "Connection Initialization")
    except Exception as e_db_connect:
        itoolkti_close_connection(conn)
        raise Exception("Exception when connecting to IBM i Db2. {0}. "
                        "Check if the database {1} existed or varied on".format(str(e_db_connect), db_name))
    return conn


def itoolkit_run_sql_once(sql, db_name=SYSBAS, hex_convert_columns=None):
    conn = None
    out_list = []
    job_log = []
    error = ''
    rc = 999
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out_list, error = itoolkit_run_sql(conn, sql, hex_convert_columns)
        job_log = db2i_tools.get_job_log(conn, '*', startd)
        return rc, out_list, error, job_log
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_list, str(e_import), job_log
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_list, str(e_db_connect), job_log
    finally:
        itoolkti_close_connection(conn)


def itoolkit_get_job_log(conn, time):
    out = db2i_tools.get_job_log(conn, '*', str(time))
    return out


def itoolkit_run_sql(conn, sql, hex_convert_columns=None):
    return db_get_result_list(conn, sql, hex_convert_columns)


def itoolkit_run_sql_old(conn, sql):
    out_list = []
    try:
        itransport = DatabaseTransport(conn)
        itool = iToolKit()
        # itool.add(iSqlQuery('query', sql, {'error': 'on'}))
        itool.add(iSqlQuery('query', sql))
        itool.add(iSqlFetch('fetch'))
        itool.add(iSqlFree('free'))
        itool.call(itransport)
        command_output = itool.dict_out('fetch')
        command_error = ''
        error = ''
        out = ''
        if 'error' in command_output:
            command_error = command_output['error']
            if 'joblog' in command_error:
                rc = IBMi_COMMAND_RC_ERROR
                error = command_error['joblog']
            else:
                rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
                error = "iToolKit result dict does not have key 'joblog', the output is {0}".format(str(command_output))
                # only for English enviroment
                if "Row not found" in error:
                    # treat as success but also indicate the Row not found message in stderr
                    rc = IBMi_COMMAND_RC_SUCCESS
                elif "xmlhint" in error:
                    xmlhint = command_output['xmlhint']
                    if len(xmlhint) < 100:
                        # most of the time, the xmlhint error is 'Row not found' by different language, check the string length < 100
                        rc = IBMi_COMMAND_RC_SUCCESS
        else:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = command_output['row']
            if isinstance(out, dict):
                out_list.append(out)
            elif isinstance(out, list):
                out_list = out
    except Exception as e_db_connect:
        raise Exception(str(e_db_connect))
    return rc, out_list, error


def itoolkti_close_connection(conn):
    if conn is not None:
        try:
            conn.close()
        except Exception as e_disconnect:
            raise Exception("ERROR: Unable to disconnect from the database. {0}".format(str(e_disconnect)))
        finally:
            conn = None


def itoolkit_run_command_once(command, db_name=SYSBAS):
    conn = None
    out = ''
    error = ''
    job_log = []
    rc = 999
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out, error = itoolkit_run_command(conn, command)
        job_log = db2i_tools.get_job_log(conn, '*', startd)
        return rc, out, error, job_log
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out, str(e_import), job_log
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out, str(e_db_connect), job_log
    finally:
        itoolkti_close_connection(conn)


def itoolkit_run_command(conn, command):
    try:
        itool = iToolKit()
        itransport = DatabaseTransport(conn)
        itool.add(iCmd('command', command))
        itool.call(itransport)
        command_output = itool.dict_out('command')

        out = ''
        err = ''

        if 'success' in command_output:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = str(command_output)
        else:
            rc = IBMi_COMMAND_RC_ERROR
            err = str(command_output)
    except Exception as e_disconnect:
        raise Exception(str(e_disconnect))
    return rc, out, err


def itoolkit_sql_callproc(conn, sql):
    try:
        itransport = DatabaseTransport(conn)
        itool = iToolKit(iparm=1)
        itool.add(iSqlQuery('query', sql))
        itool.add(iSqlFree('free'))
        itool.call(itransport)
        command_output = itool.dict_out('query')

        out = ''
        err = ''

        if 'success' in command_output:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = str(command_output)
        else:
            rc = IBMi_COMMAND_RC_ERROR
            err = str(command_output)
    except Exception as e_db_connect:
        raise Exception(str(e_db_connect))
    return rc, out, err


def itoolkit_sql_callproc_once(sql, db_name=SYSBAS):
    conn = None
    out_list = []
    job_log = []
    rc = 999
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out_list, error = itoolkit_sql_callproc(conn, sql)
        job_log = db2i_tools.get_job_log(conn, '*', startd)
        return rc, out_list, error, job_log
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_list, str(e_import), job_log
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_list, str(e_db_connect), job_log
    finally:
        itoolkti_close_connection(conn)


def db_get_fields_from_cursor(cursor):
    results = {}
    column = 0
    for d in cursor.description:
        # wy: d[0] is the name of the column, d[1] is the type of the column.
        cur_result_val = [column, d[1]]
        results[d[0]] = cur_result_val
        column = column + 1
    return results


# returns the result list containing maps with column name as key, column value as value
def db_get_result_list(connection_id, sql, hex_convert_columns):
    try:
        if hex_convert_columns is None:
            hex_convert_columns = []
        result_list = []
        cur = connection_id.cursor()
        cur.execute(sql)
        field_map = db_get_fields_from_cursor(cur)

        for row in cur:
            row_map = dict()
            for (k, v) in field_map.items():
                col_num = v[0]
                # wy: convert the db data type to python data type
                # do not do changes to those types we cannot find a python type to convert
                col_type = v[1]
                if not row[col_num]:
                    row_map[str(k)] = ''
                elif col_type in [dbi.STRING, dbi.TEXT, dbi.XML, dbi.BINARY]:
                    try:
                        # Chang Le: convert the string which actually store a hex, like MESSAGE_KEY
                        if str(k) in hex_convert_columns:
                            row_map[str(k)] = binascii.b2a_hex(row[col_num]).decode('utf-8').upper()
                        else:
                            row_map[str(k)] = str(row[col_num])
                    except TypeError:
                        row_map[str(k)] = str(row[col_num])
                elif col_type in [dbi.NUMBER]:
                    row_map[str(k)] = int(row[col_num])
                # elif col_type in [dbi.BIGINT]:
                #     row_map[str(k)] = long(row[col_num])
                elif col_type in [dbi.FLOAT, dbi.DECIMAL]:
                    row_map[str(k)] = float(row[col_num])
                elif col_type in [dbi.DATE, dbi.TIME, dbi.DATETIME]:
                    row_map[str(k)] = str(row[col_num])
                else:
                    row_map[str(k)] = row[col_num]
            result_list.append(row_map)
        cur.close()
        rc = IBMi_COMMAND_RC_SUCCESS
        error = None
    except Exception as e_db:
        rc = IBMi_SQL_RC_ERROR
        error = str(e_db)
    return rc, result_list, error


def fmtTo10(str):
    return str.ljust(10) if len(str) <= 10 else str[0:10]


def log_debug(s, module_name="ibmi_util"):
    try:
        get_logger("ibmi_util").debug(module_name + ": " + s)
    except Exception:
        pass


def log_info(s, module_name="ibmi_util"):
    try:
        get_logger("ibmi_util").info(module_name + ": " + s)
    except Exception:
        pass


def log_error(s, module_name="ibmi_util"):
    try:
        get_logger("ibmi_util").error(module_name + ": " + s)
    except Exception:
        pass


def log_warning(s, module_name="ibmi_util"):
    try:
        get_logger("ibmi_util").warning(module_name + ": " + s)
    except Exception:
        pass


def log_critical(s, module_name="ibmi_util"):
    try:
        get_logger("ibmi_util").critical(module_name + ": " + s)
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


def rtvneta():
    conn = None
    out_dict = dict()
    try:
        conn = itoolkit_init(SYSBAS)
        itransport = DatabaseTransport(conn)
        itool = iToolKit(iparm=0, iret=0, ids=1, irow=0)
        itool.add(iCmd('rtvneta', 'RTVNETA\
            SYSNAME(?)\
            PNDSYSNAME(?)\
            LCLNETID(?)\
            LCLCPNAME(?)\
            LCLLOCNAME(?)\
            DFTMODE(?)\
            NODETYPE(?)\
            DTACPR(?N)\
            DTACPRINM(?N)\
            MAXINTSSN(?N)\
            RAR(?N)\
            NETSERVER(?)\
            ALRSTS(?)\
            ALRPRIFP(?)\
            ALRDFTFP(?)\
            ALRLOGSTS(?)\
            ALRBCKFP(?)\
            ALRRQSFP(?)\
            ALRCTLD(?)\
            ALRHLDCNT(?N)\
            ALRFTR(?)\
            ALRFTRLIB(?)\
            MSGQ(?)\
            MSGQLIB(?)\
            OUTQ(?)\
            OUTQLIB(?)\
            JOBACN(?)\
            MAXHOP(?N)\
            DDMACC(?)\
            DDMACCLIB(?)\
            PCSACC(?)\
            PCSACCLIB(?)\
            NWSDOMAIN(?)\
            ALWVRTAPPN(?)\
            ALWHPRTWR(?)\
            VRTAUTODEV(?N)\
            HPRPTHTMR(?)\
            ALWADDCLU(?)\
            MDMCNTRYID(?)\
                '))
        itool.call(itransport)
        rtvneta = itool.dict_out('rtvneta')
        if 'error' in rtvneta:
            return IBMi_COMMAND_RC_ERROR, out_dict, str(rtvneta)
        else:
            del rtvneta['success']
            return IBMi_COMMAND_RC_SUCCESS, rtvneta, ''
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_dict, str(e_import)
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_dict, str(e_db_connect)
    finally:
        itoolkti_close_connection(conn)


def rtv_command(command, args_dict):
    conn = None
    out_dict = dict()
    try:
        conn = itoolkit_init(SYSBAS)
        itransport = DatabaseTransport(conn)
        itool = iToolKit(iparm=0, iret=0, ids=1, irow=0)
        args = ' '
        for (k, v) in args_dict.items():
            parm = '(?) '
            if v == 'number':
                parm = '(?N) '
            args = args + k + parm
        itool.add(iCmd('rtv_command', command + args))
        itool.call(itransport)
        rtv_command = itool.dict_out('rtv_command')
        if 'error' in rtv_command:
            return IBMi_COMMAND_RC_ERROR, out_dict, str(rtv_command)
        else:
            del rtv_command['success']
            return IBMi_COMMAND_RC_SUCCESS, rtv_command, ''
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_dict, str(e_import)
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_dict, str(e_db_connect)
    finally:
        itoolkti_close_connection(conn)
