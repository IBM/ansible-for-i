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


def get_job_log(connection_id, job_name, time=None):
    if time:
        sql = "SELECT ORDINAL_POSITION, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, SEVERITY, " + \
              "MESSAGE_TIMESTAMP, FROM_LIBRARY, FROM_PROGRAM, FROM_MODULE, FROM_PROCEDURE, FROM_INSTRUCTION, " + \
              "TO_LIBRARY, TO_PROGRAM, TO_MODULE, TO_PROCEDURE, TO_INSTRUCTION, FROM_USER, MESSAGE_FILE, " + \
              "MESSAGE_LIBRARY, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT " + \
              "FROM TABLE(QSYS2.JOBLOG_INFO('" + job_name + "')) A WHERE MESSAGE_TIMESTAMP >= '" + str(time) + "' " + \
              "ORDER BY ORDINAL_POSITION DESC"
    else:
        sql = "SELECT ORDINAL_POSITION, MESSAGE_ID, MESSAGE_TYPE, MESSAGE_SUBTYPE, SEVERITY, " + \
              "MESSAGE_TIMESTAMP, FROM_LIBRARY, FROM_PROGRAM, FROM_MODULE, FROM_PROCEDURE, FROM_INSTRUCTION, " + \
              "TO_LIBRARY, TO_PROGRAM, TO_MODULE, TO_PROCEDURE, TO_INSTRUCTION, FROM_USER, MESSAGE_FILE, " + \
              "MESSAGE_LIBRARY, MESSAGE_TEXT, MESSAGE_SECOND_LEVEL_TEXT " + \
              "FROM TABLE(QSYS2.JOBLOG_INFO('" + job_name + "')) A ORDER BY ORDINAL_POSITION DESC"
    out_result_set, err = ibm_dbi_sql_query(connection_id, sql)

    out = []
    if (out_result_set is None) and (err is None):
        err = {"FATAL": "Job not found."}
        out.append(err)
    else:
        for result in out_result_set:
            result_map = {"ORDINAL_POSITION": result[0],
                          "MESSAGE_ID": result[1],
                          "MESSAGE_TYPE": result[2],
                          "MESSAGE_SUBTYPE": result[3],
                          "SEVERITY": result[4],
                          "MESSAGE_TIMESTAMP": result[5],
                          "FROM_LIBRARY": result[6],
                          "FROM_PROGRAM": result[7],
                          "FROM_MODULE": result[8],
                          "FROM_PROCEDURE": result[9],
                          "FROM_INSTRUCTION": result[10],
                          "TO_LIBRARY": result[11],
                          "TO_PROGRAM": result[12],
                          "TO_MODULE": result[13],
                          "TO_PROCEDURE": result[14],
                          "TO_INSTRUCTION": result[15],
                          "FROM_USER": result[16],
                          "MESSAGE_FILE": result[17],
                          "MESSAGE_LIBRARY": result[18],
                          "MESSAGE_TEXT": result[19],
                          "MESSAGE_SECOND_LEVEL_TEXT": result[20],
                          }
            out.append(result_map)
    return out


def get_current_job_info(connection_id):
    sql = "SELECT SUBSTR(JOB_NAME,1,6) AS JOB_NUMBER, " \
          "SUBSTR(JOB_NAME,8,POSSTR(SUBSTR(JOB_NAME,8),'/')-1) AS JOB_USER, " \
          "SUBSTR(SUBSTR(JOB_NAME,8),POSSTR(SUBSTR(JOB_NAME,8),'/')+1)  AS JOB_NAME, " \
          "JOB_NAME AS FULL_JOB_NAME " \
          "FROM TABLE (QSYS2.ACTIVE_JOB_INFO(JOB_NAME_FILTER => '*')) AS X"

    out_result_set, err = ibm_dbi_sql_query(connection_id, sql)

    out = []
    if (out_result_set is None) and (err is None):
        err = {"FATAL": "Job not found."}
        out.append(err)
    else:
        for result in out_result_set:
            result_map = {"JOB_NUMBER": result[0],
                          "JOB_USER": result[1],
                          "JOB_NAME": result[2],
                          "FULL_JOB_NAME": result[3]
                          }
            out.append(result_map)
    return out


def get_current_job_name(connection_id):
    out = get_current_job_info(connection_id)
    if len(out) == 0:
        return "Job name not available. "
    else:
        return out[0]["FULL_JOB_NAME"]


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
