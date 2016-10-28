import ssl
from socket import socket




def zassaj(host, z, mssl, wersja):
    a = bytearray()
    s = socket()
    if mssl == 1:
        s.connect((host, 443))
        if (wersja <= "25"):
            sssl = ssl(s)
        else:
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