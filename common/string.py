# encoding=utf-8
import datetime


def is_none_or_empty(string):
    if string is None:
        return True
    if len(string.strip()) == 0:
        return True
    return False


def list2str(list_obj, delimiter=','):
    if len(list_obj) == 0:
        return ''
    str_return = ''
    for _ in list_obj:
        str_return += str(_) + delimiter
    return str_return[:-len(delimiter)]


def str2list(str_obj, delimiter=','):
    if len(str_obj) == 0:
        return []
    return str_obj.split(delimiter)


def datetime2str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def str2datetime(datetime_str):
    return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")


def str_datetime_in_N_day(n_days):
    """
    返回若干天之内的零点零分字符串

    :param n_days: 时间范围
    :return:表达几天之内的sql语句
    """

    date = datetime.datetime.now() - datetime.timedelta(days=(n_days - 1))
    time_format = date.strftime('%Y-%m-%d' + " 00:00:00")
    return time_format
