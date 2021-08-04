import pymysql

# encoding=utf-8
import traceback

import pymysql

from common.log import Log

TEST = False
DEBUG = True

log = Log(__name__).getlog()


def create_dict_cursor_conn(host, port, username, password, db, cursor_type=1):
    try:
        if cursor_type == 0:
            return pymysql.connect(host=host,
                                   port=port,
                                   user=username,
                                   passwd=password,
                                   db=db)
        if cursor_type == 1:
            return pymysql.connect(host=host,
                                   port=port,
                                   user=username,
                                   passwd=password,
                                   db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
    except:
        log.error("无法建立连接:%s,%s,%s,%s,%s" % (host, port, username, password, db))


def create_cursor(conn):
    try:
        cursor = conn.cursor()
        return cursor
    except:
        log.error("建立游标出错")
        return None


def _execute(sql, conn, op_type):
    if conn is None:
        return None
    cursor = create_cursor(conn)
    if cursor is None:
        return None
    try:
        if op_type == 'select':
            cursor.execute(sql)
            return cursor.fetchall()
        elif op_type == 'update' or op_type == 'delete' or op_type == 'insert':
            cursor.execute(sql)
            conn.commit()
            return True
        else:
            log.error("未知的sql类型:%s" % op_type)
            return None
    except:
        log.error("执行sql出错:%s" % sql)
        log.error(traceback.format_exc())
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def execute_select(sql, conn=None):
    res = _execute(sql, conn, 'select')


def execute_delete(sql, conn=None):
    _execute(sql, conn, 'delete')


def execute_update(sql, conn=None):
    _execute(sql, conn, 'update')


def execute_insert(sql, conn=None):
    _execute(sql, conn, 'insert')
