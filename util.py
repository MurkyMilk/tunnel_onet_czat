from time import ctime


def send(s, msg):
    s.send(msg.encode("utf-8"))

def recv(s, chunk_size):
    return s.recv(chunk_size).decode("utf-8", "ignore")

def get_date_string():
    return "[%s] = " % ctime()