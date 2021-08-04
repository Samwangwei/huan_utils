import traceback

from clickhouse_driver import Client
from common import string

host = '159.75.238.142'
port = '8123'
user = 'default'
pwd = 'DpZUlmm8pZkqNcBx'
db = 'bp'
send_receive_time = 5


def get_conn():
    return Client(host=host, user=user, password=pwd, database=db)


# def execute(sql):
#     try:
#         cd_conn = get_conn()
#         res = cd_conn.execute(sql)
#         return res
#     except:
#         print(sql)
#         traceback.print_exc()


if __name__ == "__main__":
    conn = get_conn()
    print('读取观看历史记录', end='...')
    sql = "select * from ht_short_play_history"
    str_date = string.str_datetime_in_N_day(10).split(' ')[0]
    sql += " where event_date >'%s' and current_play_time>'10'" % str_date
    his = conn.execute(sql)
    print('完毕\t共%d条记录' % len(his))
