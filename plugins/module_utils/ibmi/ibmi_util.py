from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import glob
import os
import re
import datetime
import decimal
import tempfile
import logging
import logging.config

HAS_ITOOLKIT = True
HAS_IBM_DB = True

try:
    from itoolkit import iToolKit
    from itoolkit import iSqlFree
    from itoolkit import iSqlFetch
    from itoolkit import iSqlQuery
    from itoolkit import iCmd
    from itoolkit import iCmd5250
    from itoolkit.transport import DatabaseTransport
    from itoolkit.transport import DirectTransport
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

IBMi_SQL_RC_ERROR = 301

IBMi_PACKAGES_NOT_FOUND = 998
IBMi_DB_CONNECTION_ERROR = 997
IBMi_COMMAND_RC_UNEXPECTED = 999

SYSBAS = '*SYSBAS'


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
    except Exception as e_db_connect:
        itoolkti_close_connection(conn)
        raise Exception("Exception when connecting to IBM i Db2. {0}. Check if the database {1} existed or varied on".format(str(e_db_connect), db_name))
    return conn


def itoolkit_run_sql_once(sql, db_name=SYSBAS):
    conn = None
    out_list = []
    job_log = []
    error = ''
    rc = 999
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out_list, error = itoolkit_run_sql(conn, sql)
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


def itoolkit_run_sql(conn, sql):
    return db_get_result_list(conn, sql)


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
def db_get_result_list(connection_id, sql):
    try:
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


def log_debug(s, module_name="ibmi_util", ):
    get_logger("ibmi_util", logging.DEBUG).debug(str(datetime.datetime.now()) + " " + module_name + ": " + s)


def log_info(s, module_name="ibmi_util", ):
    get_logger("ibmi_util", logging.DEBUG).info(str(datetime.datetime.now()) + " " + module_name + ": " + s)


def log_error(s, module_name="ibmi_util", ):
    get_logger("ibmi_util", logging.ERROR).error(str(datetime.datetime.now()) + " " + module_name + ": " + s)


def log_warning(s, module_name="ibmi_util", ):
    get_logger("ibmi_util", logging.WARNING).warning(str(datetime.datetime.now()) + " " + module_name + ": " + s)


def get_logger(module_name, log_level=logging.INFO):
    ibmi_logging = setup_logging(log_level)
    return ibmi_logging.getLogger(module_name)


def setup_logging(
    default_level="INFO",
):
    """Setup logging configuration"""
    env_log_path = "LOG_PATH"
    env_log_level = "LOG_LEVEL"

    default_log_path = tempfile.gettempdir()
    log_path = os.getenv(env_log_path, default_log_path)
    log_level_str = os.getenv(env_log_level, default_level)
    log_level = logging.getLevelName(log_level_str)
    log_file_path = os.path.join(log_path, "ibmi_ansible_module.log")
    logging.basicConfig(filename=log_file_path, filemode="a", level=log_level)
    return logging
