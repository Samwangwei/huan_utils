import json
import os

from common import string
from data.accessing import mysql


def load_config():
    with open('conf/default.conf', 'r', encoding='utf-8') as fp:
        conf = json.load(fp)
        return conf


def get_data_source():
    config = load_config()
    ds = config['data_source']['ams']['test']
    return ds['host'], ds['port'], ds['user'], ds['pass'], ds['db']


def get_view_history(days=1):
    print("从大数据读取%d天内观看历史" % days, end="...")
    host, port, user, passwd, db = get_data_source()
    conn = mysql.create_conn(host, port, user, passwd, db)
    sql = "select video_id,video_name,distinct_id,user_id,mac,create_time from bp_video_detail"
    sql += " where create_time>'%s'" % string.str_datetime_in_N_day(days)
    sql += " and video_play_time>10 and video_id is not NULL"
    sql += " order by create_time desc"
    # sql += " limit 100"
    view_history = mysql.execute_select(sql, conn)
    print("完毕\t共%d条有效记录" % len(view_history))
    return view_history


def writeOut(view_history):
    print("写出观看历史", end="...")
    error_count = 0
    write_count = 0
    with open('view_history.txt', 'w', encoding='utf-8') as fp:
        for re in view_history:
            try:
                str_info = ''
                for key in re:
                    if key == 'video_name':
                        re[key] = re[key].replace("\n", ' ').replace("\t", ' ')
                    str_info += str(re[key]) + '\t'
                str_info = str_info + '\n'
                fp.write(str_info)
                write_count += 1
            except:
                error_count += 1
    print("完毕")
    print("总结:共%d条，写出%d条，异常%d条" % (write_count + error_count, write_count, error_count))


def read_history_from_file():
    print("从文件读取%d天内观看历史" % days, end="...")
    history_list = []
    with open('view_history.txt', 'r', encoding='utf-8') as fp:
        line = fp.readline()
        while line:
            try:
                segs = line.split('\t')
                hitem = {}
                hitem['video_id'] = segs[0]
                hitem['video_name'] = segs[1]
                hitem['distinct_id'] = segs[2]
                hitem['user_id'] = segs[3]
                hitem['mac'] = segs[4]
                hitem['create_time'] = segs[5]
                history_list.append(hitem)
                line = fp.readline()
            except:
                print(line, ":", segs)
                line = fp.readline()
    print("完毕\t共%d条有效记录" % len(history_list))
    return history_list


def if_history_text_exist():
    if os.path.exists("view_history.txt"):
        print("发现历史记录文件")
        return True
    else:
        print("未发现历史记录文件")
        return False


def test():
    string_list = ['\t', '', '\r', 'a']
    for s in string_list:
        print(repr(s), string.is_none_or_empty(s))


if __name__ == "__main__":
    print('running test')
    days = 15
    if if_history_text_exist():
        view_history = read_history_from_file()
    else:
        view_history = get_view_history(days=days)
        writeOut(view_history)
        pass
    exit(0)
