from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    import ibm_db_dbi as dbi
    HAS_IBM_DB = True
except ImportError:
    HAS_IBM_DB = False


# If your SQL is not passed by the user, you can use this function
# This is a sample shows you how everything works
# However, normally you need to use ibm_dbi_sql_query to pass in both sql and connection
def ibm_dbi_sql_query_sample(sql):
    out = []
    # Attempt To Establish A Connection To The Database Specified
    connection_id = None
    try:
        connection_id = dbi.connect()
    except Exception:
        pass

    if connection_id is None:
        err = "ERROR: Unable to connect to the database."
        return out, err

    if connection_id is not None:
        cursor_id = connection_id.cursor()

    try:
        result_set = cursor_id.execute(sql)
    except Exception:
        pass

    if result_set is False:
        connection_id.close()
        err = "ERROR: Unable to execute the SQL statement specified."
        return out, err

    try:
        result_set = cursor_id.fetchall()
    except Exception:
        pass

    if result_set is None:
        connection_id.close()
        err = "ERROR: Unable to obtain the results desired."
        return out, err

    out = result_set

    if connection_id is not None:
        try:
            return_code = connection_id.close()
        except Exception:
            return_code = False
            pass

        if return_code is False:
            err = "ERROR: Unable to disconnect from the database."
            return out, err

    err = None
    return out, err


def ibm_dbi_sql_query(connection_id, sql):
    out = None
    # Attempt To Establish A Connection To The Database Specified

    if connection_id is None:
        err = "ERROR: Connection is None. "
        return out, err

    try:
        cursor_id = connection_id.cursor()
        result_set = cursor_id.execute(sql)

        if result_set is False:
            err = "ERROR: Unable to execute the SQL statement specified."
            return out, err

        result_set = cursor_id.fetchall()

        if result_set is None:
            err = "ERROR: Unable to fetch the result desired."
            return out, err

        out = result_set
    except Exception as e:
        err = str(e)
        return out, err

    err = None
    return out, err


def get_job_log(connection_id, job_name):
    sql = "SELECT MESSAGE_ID, MESSAGE_TYPE, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT" \
          " FROM TABLE(QSYS2.JOBLOG_INFO('" + job_name + "')) A"
    out_result_set, err = ibm_dbi_sql_query(connection_id, sql)

    out = []
    if (out_result_set is None) and (err is None):
        err = "Job not found."
    else:
        for result in out_result_set:
            result_map = {"MESSAGE_ID": result[0], "MESSAGE_TYPE": result[1],
                          "MESSAGE_TEXT": result[2]
                          }
            out.append(result_map)
    return out, err


def get_ibmi_release(connection_id):
    sql = "SELECT OS_VERSION, OS_RELEASE FROM SYSIBMADM.ENV_SYS_INFO"
    out_result_set, err = ibm_dbi_sql_query(connection_id, sql)
    release_info = {"version": 7, "release": 0, "version_release": 7.0}
    if (out_result_set is None) and (err is None):
        err = "Nothing returned for OS version and release."
    else:
        for result in out_result_set:
            release_info["version"] = int(result[0])
            release_info["release"] = int(result[1])
            release_info["version_release"] = float(result[0]) + float(result[1]) / 10.0

    return release_info, err
