from time import ctime


def send(s, msg):
    s.send(msg.encode("utf-8"))


def get_date_string():
    return "[%s] = " % ctime()