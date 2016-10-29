import sys
from _socket import gethostbyname, gethostname, AF_INET, SOCK_STREAM
from socket import socket

from util import get_date_string


def getBindPort(argv, port):
    if len(argv) == 2:
        return int(argv[1])
    else:
        return port


def bindSocket(s, BindPort, local_ip):
    try:
        s.bind(('', BindPort))
        get_date_string()
        if local_ip != '':
            print("server:  + $local_ip + $BindPort")
        else:
            print("server:" + str(gethostbyname(gethostname())) + str(BindPort))
    except Exception as e:
        print(e)
        get_date_string()
        print("ERROR: nie mozna zabindowac portu %s, wybierz inny BindPort")
        s.close()
        sys.exit()


def createSocketConnection(s,port, local_ip):
    bindSocket(s, getBindPort(sys.argv, port), local_ip)


def create_socket():
    return socket(AF_INET, SOCK_STREAM)