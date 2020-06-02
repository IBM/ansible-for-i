from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import glob
import os
import re
import datetime

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
        raise Exception("Exception when connecting to IBM i Db2. {0}. Check if the database {1} existed or varied on".format(str(e_db_connect), db_name))
    return conn


def itoolkit_run_sql_once(sql, db_name=SYSBAS):
    conn = None
    out_list = []
    job_log = []
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out_list, error = itoolkit_run_sql(conn, sql)
        job_log = itoolkit_get_job_log(conn, startd)
        return rc, out_list, error, job_log
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_list, str(e_import), job_log
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_list, str(e_db_connect), job_log
    finally:
        itoolkti_close_connection(conn)


def itoolkit_get_job_log(conn, time):
    sql = "SELECT ORDINAL_POSITION, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, SEVERITY, " + \
          "MESSAGE_TIMESTAMP, FROM_LIBRARY, FROM_PROGRAM, FROM_MODULE, FROM_PROCEDURE, FROM_INSTRUCTION, " + \
          "TO_LIBRARY, TO_PROGRAM, TO_MODULE, TO_PROCEDURE, TO_INSTRUCTION, FROM_USER, MESSAGE_FILE, " + \
          "MESSAGE_LIBRARY, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT " + \
          "FROM TABLE(QSYS2.JOBLOG_INFO('*')) A WHERE MESSAGE_TIMESTAMP >= '" + str(time) + "'"
    rc, out, error = itoolkit_run_sql(conn, sql)
    return out


def itoolkit_run_sql(conn, sql):
    out_list = []
    try:
        itransport = DatabaseTransport(conn)
        itool = iToolKit()
        itool.add(iSqlQuery('query', sql, {'error': 'on'}))
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
                if "Row not found" in error:
                    # treat as success but also indicate the Row not found message in stderr
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
    out_list = []
    job_log = []
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out_list, error = itoolkit_run_command(conn, command, db_name)
        job_log = itoolkit_get_job_log(conn, startd)
        return rc, out_list, error, job_log
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_list, str(e_import), job_log
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_list, str(e_db_connect), job_log
    finally:
        itoolkti_close_connection(conn)


def itoolkit_run_command(conn, command, asp_group=SYSBAS):
    try:
        command = command.upper()
        itool = iToolKit()
        # Handle the command which has ASPDEV(iasp_name) parameter
        if 'ASPDEV(' in command:
            parm_aspdev = command.split('ASPDEV(', 1)[1]
            if parm_aspdev and (not parm_aspdev.startswith('*')) and ')' in parm_aspdev:
                parm_aspdev = parm_aspdev.split(')', 1)[0]
                asp_group = parm_aspdev
        if asp_group != SYSBAS:
            itransport = DirectTransport()
            itool.add(iCmd('command', "QSYS/SETASPGRP ASPGRP({asp_group_pattern})".format(asp_group_pattern=asp_group), {'error': 'on'}))
        else:
            itransport = DatabaseTransport(conn)
        itool.add(iCmd('command', command, {'error': 'on'}))
        itool.call(itransport)

        out = ''
        err = ''

        if asp_group != SYSBAS and isinstance(itool.dict_out('command'), list) and len(itool.dict_out('command')) > 1:
            command_output = itool.dict_out('command')[1]
        else:
            command_output = itool.dict_out('command')

        if 'success' in command_output:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = command_output['success']
        elif 'error' in command_output:
            command_error = command_output['error']
            if 'joblog' in command_error:
                rc = IBMi_COMMAND_RC_ERROR
                err = command_error['joblog']
            else:
                # should not be here, must xmlservice has internal error
                rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
                err = "iToolKit result dict does not have key 'joblog', the output is {0}".format(str(command_output))
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
            err = "iToolKit result dict does not have key 'error', the output is {0}".format(str(command_output))
    except Exception as e_disconnect:
        raise Exception(str(e_disconnect))
    return rc, out, err


def itoolkit_sql_callproc(conn, sql):
    try:
        itransport = DatabaseTransport(conn)
        itool = iToolKit(iparm=1)
        itool.add(iSqlQuery('query', sql, {'error': 'on'}))
        itool.add(iSqlFree('free'))
        itool.call(itransport)

        command_output = itool.dict_out('query')

        out = ''
        err = ''
        if 'success' in command_output:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = command_output['success']
        elif 'error' in command_output:
            command_error = command_output['error']
            if 'joblog' in command_error:
                rc = IBMi_COMMAND_RC_ERROR
                err = command_error['joblog']
            else:
                # should not be here, must xmlservice has internal error
                rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
                err = "iToolKit result dict does not have key 'joblog', the output is {0}".format(str(command_output))
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
            err = "iToolKit result dict does not have key 'error', the output is {0}".format(str(command_output))
    except Exception as e_db_connect:
        raise Exception(str(e_db_connect))
    return rc, out, err


def itoolkit_sql_callproc_once(sql, db_name=SYSBAS):
    conn = None
    out_list = []
    job_log = []
    try:
        startd = datetime.datetime.now()
        conn = itoolkit_init(db_name)
        rc, out_list, error = itoolkit_sql_callproc(conn, sql)
        job_log = itoolkit_get_job_log(conn, startd)
        return rc, out_list, error, job_log
    except ImportError as e_import:
        return IBMi_PACKAGES_NOT_FOUND, out_list, str(e_import), job_log
    except Exception as e_db_connect:
        return IBMi_DB_CONNECTION_ERROR, out_list, str(e_db_connect), job_log
    finally:
        itoolkti_close_connection(conn)


def fmtTo10(str):
    return str.ljust(10) if len(str) <= 10 else str[0:10]
