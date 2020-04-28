from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import glob
import os
import re

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

IBMi_COMMAND_RC_SUCCESS = 0
IBMi_COMMAND_RC_UNEXPECTED = 999
IBMi_COMMAND_RC_ERROR = 255
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG = 256
IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR = 257
IBMi_COMMAND_RC_UNEXPECTED_ROW_COUNT = 258
IBMi_COMMAND_RC_INVALID_EXPECTED_ROW_COUNT = 259
IBMi_NO_ROW_FOUND_ERROR = 260


def interpret_return_code(rc):
    if rc == IBMi_COMMAND_RC_SUCCESS:
        return 'Success'
    elif rc == IBMi_COMMAND_RC_ERROR:
        return 'Generic failure'
    elif rc == IBMi_COMMAND_RC_UNEXPECTED:
        return 'Unexpected error'
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG:
        return "iToolKit result dict does not have key 'joblog'"
    elif rc == IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR:
        return "iToolKit result dict does not have key 'error'"
    elif rc == IBMi_NO_ROW_FOUND_ERROR:
        return "No matched row exists"
    else:
        return "Unknown error"


def itoolkit_init(db_name):
    try:
        conn = dbi.connect(database='{db_pattern}'.format(db_pattern=db_name))
    except Exception as e_db_connect:
        raise Exception("Exception when trying to use IASP. " + str(e_db_connect))
    return conn


def itoolkit_init():
    conn = None
    try:
        conn = dbi.connect()
    except Exception as e_db_connect:
        raise Exception("Exception when connecting to IBM i Db2. " + str(e_db_connect))
    return conn


def itoolkit_run_sql_once(sql):
    out_list = []
    try:
        conn = itoolkit_init()
        return itoolkit_run_sql(conn, sql)
    except Exception as e_db_connect:
        raise Exception(str(e_db_connect))
    finally:
        itoolkti_close_connection(conn)


def itoolkit_run_sql(conn, sql):
    out_list = []
    rc = ''
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
        if 'error' not in command_output:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = command_output['row']
            if isinstance(out, dict):
                out_list.append(out)
            elif isinstance(out, list):
                out_list = out
        else:
            command_error = command_output['error']
            if 'joblog' in command_error:
                rc = IBMi_COMMAND_RC_ERROR
                error = command_error['joblog']
            elif 'xmlhint' in command_output:
                if "Row not found" in command_output['xmlhint']:
                    rc = IBMi_COMMAND_RC_SUCCESS
                    error = command_output['xmlhint']
            else:
                # should not be here, must xmlservice has internal error
                rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
                error = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
    except Exception as e_db_connect:
        raise Exception(str(e_db_connect))
    return rc, interpret_return_code(rc), out_list, error


def itoolkti_close_connection(conn):
    if conn is not None:
        try:
            conn.close()
        except Exception as e_disconnect:
            raise Exception("ERROR: Unable to disconnect from the database. " + str(e_disconnect))
        finally:
            conn = None


def itoolkit_run_command_once(command):
    conn = None
    try:
        conn = itoolkit_init()
        return itoolkit_rum_command(conn, command)
    except Exception as e_disconnect:
        raise Exception(str(e_disconnect))
    finally:
        itoolkti_close_connection(conn)


def itoolkit_rum_command(conn, command):
    try:
        itransport = DatabaseTransport(conn)
        itool = iToolKit()
        itool.add(iCmd('command', command, {'error': 'on'}))
        itool.call(itransport)
        rc = ''
        out = ''
        command_output = itool.dict_out('command')
        command_error = ''
        error = ''
        if 'success' in command_output:
            rc = IBMi_COMMAND_RC_SUCCESS
            out = command_output['success']
        elif 'error' in command_output:
            command_error = command_output['error']
            if 'joblog' in command_error:
                rc = IBMi_COMMAND_RC_ERROR
                error = command_error['joblog']
            else:
                # should not be here, must xmlservice has internal error
                rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_JOBLOG
                error = "iToolKit result dict does not have key 'joblog', the output is %s" % command_output
        else:
            # should not be here, must xmlservice has internal error
            rc = IBMi_COMMAND_RC_ITOOLKIT_NO_KEY_ERROR
            error = "iToolKit result dict does not have key 'error', the output is %s" % command_output
    except Exception as e_disconnect:
        raise Exception(str(e_disconnect))
    return rc, interpret_return_code(rc), out, error


def fmtTo10(str):
    return str.ljust(10) if len(str) <= 10 else str[0:10]
