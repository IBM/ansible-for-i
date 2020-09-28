from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import datetime
import binascii
import sys

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

from ansible_collections.ibm.power_ibmi.plugins.module_utils.ibmi import ibmi_util


class IBMiLogon(object):
    def __init__(self, conn, name, pwd):
        self.name = name
        self.pwd = pwd
        self.conn = conn
        self.handle = None

    def __del__(self):
        if self.handle and self.conn:
            # self.release_profile_handle(self.conn, self.handle)
            pass

    def get_handle(self):
        return self.handle

    def qsygetph(self):
        special_value = False
        if self.pwd in ['*NOPWD', '*NOPWDCHK', '*NOPWDSTS']:
            self.pwd = ibmi_util.fmtTo10(self.pwd)
            special_value = True

        len_of_password = len(self.pwd)
        # Chang Le: the user name should be converted to upper case
        input_user = self.name.ljust(10).upper()
        input_password_len = str(len_of_password) + 'A'

        itransport = DatabaseTransport(self.conn)
        itool = iToolKit()
        if not special_value:
            itool.add(
                iPgm('qsygetph', 'qsygetph')
                .addParm(iData('userId', '10A', input_user))
                .addParm(iData('pwd', input_password_len, self.pwd))
                .addParm(iData('handle', '12A', '', {'hex': 'on'}))
                .addParm(
                    iDS('ERRC0100_t', {'len': 'errlen'})
                    .addData(iData('errRet', '10i0', ''))
                    .addData(iData('errAvl', '10i0', ''))
                    .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                    .addData(iData('errRsv', '1A', ''))
                )
                .addParm(iData('len', '10i0', str(len_of_password)))
                .addParm(iData('ccsid', '10i0', '37'))
            )
        else:
            itool.add(
                iPgm('qsygetph', 'qsygetph')
                .addParm(iData('userId', '10A', input_user))
                .addParm(iData('pwd', '10A', self.pwd))
                .addParm(iData('handle', '12A', '', {'hex': 'on'}))
                .addParm(
                    iDS('ERRC0100_t', {'len': 'errlen'})
                    .addData(iData('errRet', '10i0', ''))
                    .addData(iData('errAvl', '10i0', ''))
                    .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                    .addData(iData('errRsv', '1A', ''))
                )
            )
        itool.call(itransport)
        qsygetph = itool.dict_out('qsygetph')
        if 'success' in qsygetph:
            return qsygetph['handle']
        else:
            return None

    def qwtsetp(self):
        itransport = DatabaseTransport(self.conn)
        itool = iToolKit()
        itool.add(
            iPgm('qwtsetp', 'QWTSETP')
            .addParm(iData('handle', '12A', self.handle, {'hex': 'on'}))
            .addParm(
                iDS('ERRC0100_t', {'len': 'errlen'})
                .addData(iData('errRet', '10i0', ''))
                .addData(iData('errAvl', '10i0', ''))
                .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                .addData(iData('errRsv', '1A', ''))
            )
        )
        itool.call(itransport)
        qwtsetp = itool.dict_out('qwtsetp')
        ibmi_util.log_info(str(qwtsetp), 'qwtsetp')
        if 'success' in qwtsetp:
            return True
        else:
            return False

    def switch(self):
        self.handle = self.qsygetph()
        if self.handle:
            return self.qwtsetp()
        else:
            return False

    def release_profile_handle(self):
        if not self.handle:
            return True
        itransport = DatabaseTransport(self.conn)
        itool = iToolKit()
        itool.add(
            iPgm('qsyrlsph', 'QSYRLSPH')
            .addParm(iData('handle', '12A', self.handle, {'hex': 'on'}))
            .addParm(
                iDS('ERRC0100_t', {'len': 'errlen'})
                .addData(iData('errRet', '10i0', ''))
                .addData(iData('errAvl', '10i0', ''))
                .addData(iData('errExp', '7A', '', {'setlen': 'errlen'}))
                .addData(iData('errRsv', '1A', ''))
            )
        )
        itool.call(itransport)
        qsyrlsph = itool.dict_out('qsyrlsph')
        ibmi_util.log_info(str(qsyrlsph), 'qsyrlsph')
        if 'success' in qsyrlsph:
            return True
        else:
            return False


class IBMiModule(object):
    def __init__(self, db_name=ibmi_util.SYSBAS, become_user_name=None, become_user_password=None):
        self.ibmi_logon = None
        self.conn = None
        self.startd = datetime.datetime.now()

        if not HAS_ITOOLKIT:
            raise ImportError("itoolkit package is required.")
        if not HAS_IBM_DB:
            raise ImportError("ibm_db package is required.")
        re_raise = False  # workaround to pass the raise-missing-from pylint issue
        exp_msg = ''
        try:
            if db_name != ibmi_util.SYSBAS:
                self.conn = dbi.connect(database='{db_pattern}'.format(db_pattern=db_name))
            else:
                self.conn = dbi.connect()
            job_name_info = self.get_current_job_name()
            ibmi_util.log_info("Job of the connection to execute the task: {0}".format(
                job_name_info), "Connection Initialization")
        except Exception as inst:
            self.close_db_connection()
            re_raise = True
            exp_msg = "Fail to connect to database {0}: {1}.".format(
                db_name, str(inst))
            if db_name != ibmi_util.SYSBAS:
                exp_msg = exp_msg + " Check if IASP {0} is exist and varied on.".format(db_name)
            else:
                exp_msg = exp_msg + " Check if *LOCAL Relational Database Directory Entry(RDBDIRE) is exist."
        if re_raise:
            raise Exception(exp_msg)

        if become_user_name and self.conn:
            self.ibmi_logon = IBMiLogon(
                self.conn, become_user_name, "*NOPWD" if (become_user_password is None) else become_user_password)
            become_result = self.ibmi_logon.switch()
            if not become_result:
                exp_msg = "Failed to become user {0} to excute the task. Invaild user or password or user is disabled".format(become_user_name)
                raise Exception(exp_msg)

    def __del__(self):
        self.itoolkit_close_connection()

    def get_connection(self):
        return self.conn

    def get_ibmi_logon(self):
        return self.ibmi_logon

    def release_ibmi_logon_handler(self):
        if self.ibmi_logon:
            self.ibmi_logon.release_profile_handle()

    def close_db_connection(self):
        if self.conn:
            re_raise = False  # workaround to pass the raise-missing-from pylint issue
            exp_msg = ''
            try:
                self.conn.close()
            except Exception as inst:
                re_raise = True
                exp_msg = "Failed to close connect from database: {0}".format(
                    str(inst))
            finally:
                self.conn = None
                if re_raise:
                    raise Exception(exp_msg)

    def itoolkit_close_connection(self):
        self.release_ibmi_logon_handler()
        self.close_db_connection()

    def itoolkit_get_job_log(self, time):
        return self.get_job_log('*', str(time))

    def itoolkit_run_sql(self, sql, hex_convert_columns=None):
        return self.db_get_result_list(sql, hex_convert_columns)

    def itoolkit_run_sql_once(self, sql, hex_convert_columns=None):
        '''This method equals to itoolkit_run_sql and itoolkit_get_job_log'''
        rc, out_list, error = self.itoolkit_run_sql(sql, hex_convert_columns)
        job_log = self.get_job_log('*', self.startd)
        return rc, out_list, error, job_log

    def itoolkit_sql_callproc(self, sql):
        itransport = DatabaseTransport(self.conn)
        itool = iToolKit(iparm=1)
        itool.add(iSqlQuery('query', sql))
        itool.add(iSqlFree('free'))
        itool.call(itransport)
        command_output = itool.dict_out('query')

        out = ''
        err = ''

        if 'success' in command_output:
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            out = str(command_output)
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            err = str(command_output)
        return rc, out, err

    def itoolkit_sql_callproc_once(self, sql):
        '''This method equals to itoolkit_sql_callproc and itoolkit_get_job_log'''
        rc, out_list, error = self.itoolkit_sql_callproc(sql)
        job_log = self.get_job_log('*', self.startd)
        return rc, out_list, error, job_log

    def itoolkit_run_command(self, command):
        '''IBM i XMLSERVICE call *CMD not returning *OUTPUT'''
        itool = iToolKit()
        itransport = DatabaseTransport(self.conn)
        itool.add(iCmd('command', command))
        itool.call(itransport)
        command_output = itool.dict_out('command')

        out = ''
        err = ''

        if 'success' in command_output:
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            out = str(command_output)
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            err = str(command_output)
        return rc, out, err

    def itoolkit_run_command_once(self, command):
        '''This method equals to itoolkit_run_command and itoolkit_get_job_log'''
        rc, out, error = self.itoolkit_run_command(command)
        job_log = self.get_job_log('*', self.startd)
        return rc, out, error, job_log

    def itoolkit_run_command5250(self, command):
        '''IBM i XMLSERVICE call 5250 *CMD returning *OUTPUT'''
        itool = iToolKit()
        itransport = DatabaseTransport(self.conn)
        if command:
            command = command.upper().replace('OUTPUT(*)', '')
        itool.add(iCmd5250('command', command))
        itool.call(itransport)
        command_output = itool.dict_out('command')
        ibmi_util.log_debug("command_output " + str(command_output), sys._getframe().f_code.co_name)

        out = ''
        err = ''

        if 'error' in command_output:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            err = str(command_output)
        else:
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            out = str(command_output['command'])
        return rc, out, err

    def itoolkit_run_command5250_once(self, command):
        '''This method equals to itoolkit_run_command5250 and itoolkit_get_job_log'''
        rc, out, error = self.itoolkit_run_command5250(command)
        job_log = self.get_job_log('*', self.startd)
        return rc, out, error, job_log

    def itoolkit_run_rtv_command(self, command, args_dict):
        '''IBM i XMLSERVICE call *CMD with REXX'''
        itool = iToolKit(iparm=0, iret=0, ids=1, irow=0)
        itransport = DatabaseTransport(self.conn)
        args = ' '
        for (k, v) in args_dict.items():
            parm = '(?) '
            if v == 'number':
                parm = '(?N) '
            args = args + k + parm
        itool.add(iCmd('rtv_command', command + args))
        itool.call(itransport)
        rtv_command = itool.dict_out('rtv_command')
        ibmi_util.log_debug("rtv_command " + str(rtv_command), sys._getframe().f_code.co_name)
        if 'error' in rtv_command:
            rc = ibmi_util.IBMi_COMMAND_RC_ERROR
            out_dict = dict()
            error = str(rtv_command)
        else:
            # remove the key 'success' and its value, just left the result
            del rtv_command['success']
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            out_dict = rtv_command
            error = ''
        return rc, out_dict, error

    def itoolkit_run_rtv_command_once(self, command, args_dict):
        '''This method equals to itoolkit_run_rtv_command and itoolkit_get_job_log'''
        rc, out, error = self.itoolkit_run_rtv_command(command, args_dict)
        job_log = self.get_job_log('*', self.startd)
        return rc, out, error, job_log

    def db_get_result_list(self, sql, hex_convert_columns):
        '''returns the result list containing maps with column name as key, column value as value'''
        result_list = []
        try:
            # Already known hex column names
            known_hex_convert_columns = ['MESSAGE_KEY', 'ASSOCIATED_MESSAGE_KEY', 'INTERNAL_JOB_ID']
            if not hex_convert_columns:
                hex_convert_columns = []
            hex_convert_columns.extend(known_hex_convert_columns)
            cur = self.conn.cursor()
            cur.execute(sql)
            field_map = self.db_get_fields_from_cursor(cur)

            for row in cur:
                row_map = dict()
                for (k, v) in field_map.items():
                    col_num = v[0]
                    # wy: convert the db data type to python data type
                    # do not do changes to those types we cannot find a python type to convert
                    col_type = v[1]
                    # if not row[col_num]:
                    if row[col_num] is None:
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
            rc = ibmi_util.IBMi_COMMAND_RC_SUCCESS
            error = None
        except Exception as inst:
            rc = ibmi_util.IBMi_SQL_RC_ERROR
            error = str(inst)
        return rc, result_list, error

    def db_get_fields_from_cursor(self, cursor):
        results = {}
        column = 0
        for d in cursor.description:
            # wy: d[0] is the name of the column, d[1] is the type of the column.
            cur_result_val = [column, d[1]]
            results[d[0]] = cur_result_val
            column = column + 1
        return results

    def ibm_dbi_sql_query(self, sql):
        out = ''
        err = ''
        try:
            cursor_id = self.conn.cursor()

            result_set = cursor_id.execute(sql)
            if not result_set:
                err = "Failed to execute the SQL statement."
                return out, err

            result_set = cursor_id.fetchall()
            if not result_set:
                err = "Failed to fetch the result set."
                return out, err

            out = result_set
        except Exception as inst:
            err = str(inst)
            return out, err

        return out, err

    def get_job_log(self, job_name, time=None):
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
                  "FROM TABLE(QSYS2.JOBLOG_INFO('" + job_name + \
                "')) A ORDER BY ORDINAL_POSITION DESC"
        out_result_set, err = self.ibm_dbi_sql_query(sql)

        out = []
        if (not out_result_set) and (not err):
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

    def get_current_job_info(self):
        sql = "SELECT SUBSTR(JOB_NAME,1,6) AS JOB_NUMBER, " \
              "SUBSTR(JOB_NAME,8,POSSTR(SUBSTR(JOB_NAME,8),'/')-1) AS JOB_USER, " \
              "SUBSTR(SUBSTR(JOB_NAME,8),POSSTR(SUBSTR(JOB_NAME,8),'/')+1)  AS JOB_NAME, " \
              "JOB_NAME AS FULL_JOB_NAME " \
              "FROM TABLE (QSYS2.ACTIVE_JOB_INFO(JOB_NAME_FILTER => '*')) AS X"

        out_result_set, err = self.ibm_dbi_sql_query(sql)

        out = []
        if (not out_result_set) and (not err):
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

    def get_current_job_name(self):
        out = self.get_current_job_info()
        if len(out) == 0:
            return "Job name not available. "
        else:
            return out[0]["FULL_JOB_NAME"]

    def get_ibmi_release(self):
        sql = "SELECT OS_VERSION, OS_RELEASE FROM SYSIBMADM.ENV_SYS_INFO"
        out_result_set, err = self.ibm_dbi_sql_query(sql)
        release_info = {"version": 7, "release": 0, "version_release": 7.0}
        if (not out_result_set) and (not err):
            err = "Nothing returned for OS version and release."
        else:
            for result in out_result_set:
                release_info["version"] = int(result[0])
                release_info["release"] = int(result[1])
                release_info["version_release"] = float(result[0]) + float(result[1]) / 10.0

        return release_info, err
