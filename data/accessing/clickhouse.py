import traceback

from clickhouse_driver import Client
from common import string

host = ''
port = ''
user = ''
pwd = ''
db = ''


def get_conn():
    return Client(host=host, user=user, password=pwd, database=db)

if __name__ == "__main__":
    conn = get_conn()
    print('读取观看历史记录', end='...')
    sql = "select * from ht_short_play_history"
    str_date = string.str_datetime_in_N_day(10).split(' ')[0]
    sql += " where event_date >'%s' and current_play_time>'10'" % str_date
    his = conn.execute(sql)
    print('完毕\t共%d条记录' % len(his))
