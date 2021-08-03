from common import string


def test():
    string_list = ['\t', '', '\r', 'a']
    for s in string_list:
        print(repr(s), string.is_none_or_empty(s))


if __name__ == "__main__":
    print('running test')
    test()
    exit(0)
