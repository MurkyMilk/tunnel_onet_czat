import ssl
from re import findall
from socket import socket



def fetch(host, z, mssl):
    a = bytearray()
    s = socket()
    if mssl == 1:
        s.connect((host, 443))
        sssl = ssl.wrap_socket(s)
        sssl.write(str.encode(z))
        sssl.read()
        del sssl
        s.close()
        return ""
    s.connect((host, 80))
    s.send(str.encode(z))
    while True:
        b = s.recv(1024)
        if b == b'':
            break
        a.extend(b)
        print(a)
    s.close()
    return a.decode("utf-8", "ignore")


def get_http(host, z, get_uo=0, mssl=0):
    print("MICHAL")
    a = fetch(host, z, mssl)
    if get_uo == 1:
        x = a.find("<uoKey>")
        if x == -1:
            return ""
        x2 = a.find("</uoKey>")
        return a[x + 7:x2]
    c = findall("Cookie:(.+?;)", a)
    c += findall("cookie:(.+?;)", a)

    if len(c) > 0:
        return ''.join(c)
    else:
        return ""