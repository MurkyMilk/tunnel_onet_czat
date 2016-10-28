#!/usr/bin/env python

############### CONFIG ###############
import threading

kolor = 0  # obsluga kolorow, 0 aby wylaczyc;
bold = 0  # obsluga pogrubienia czcionki;
kodowanie = 2  # Kodowanie 0 - ISO, 1 - WIN, 2 - UTF;
emoty = 1  # Emoty 0 - %Ihihi%, 1 - <hihi>, 2 - //hihi;
#
TUNEL_PASS = ""  # haslo do zabezpieczenia tunelu;
local_ip = ""  # vHost, lub puste
port = 6601  # port, bez ""
realname = "Mlecko"  # nazwa

######################################


from socket import *
from threading import _start_new_thread
from re import findall, sub, search
import time
from time import ctime
import select

import sys

wersja = sys.version[0] + sys.version[2]
if (wersja <= ""):
    import _ssl
else:
    import ssl

print("onettunel.py v.2010-04 / by Olo (2008-2010) unix.onlinewebshop.net")
print("poprawki Husar, 08-07-2011\r\n\r\n")
if (realname == ""):
    realname = ""
if kolor == 1:
    print("Wlaczona obsluga kolorow")
else:
    print("Wylaczona obsluga kolorow")
if bold == 1: print("Wlaczona obsluga pogrubienia czcionki")
if kodowanie == 1: print("Wlaczona obsluga kodowania CP1250")

def send(s, msg):
    s.send(msg.encode("utf-8"))

def dawaj_date():
    sys.stdout.write("[%s] = " % ctime())


if len(sys.argv) == 2:
    BindPort = int(sys.argv[1])
else:
    BindPort = port


def czas(cz):
    a = ""
    try:
        a = [x for x in ctime(int(cz)).split(' ') if x.find(':') != -1][0]
    except:
        a = cz
    return a


def auth(s):
    stringbuffer = ""
    i_list = range(16)
    ai = []
    pomoc = []
    f1 = [
        29, 43, 7, 5, 52, 58, 30, 59, 26, 35,
        35, 49, 45, 4, 22, 4, 0, 7, 4, 30,
        51, 39, 16, 6, 32, 13, 40, 44, 14, 58,
        27, 41, 52, 33, 9, 30, 30, 52, 16, 45,
        43, 18, 27, 52, 40, 52, 10, 8, 10, 14,
        10, 38, 27, 54, 48, 58, 17, 34, 6, 29,
        53, 39, 31, 35, 60, 44, 26, 34, 33, 31,
        10, 36, 51, 44, 39, 53, 5, 56
    ]
    f2 = [
        7, 32, 25, 39, 22, 26, 32, 27, 17, 50,
        22, 19, 36, 22, 40, 11, 41, 10, 10, 2,
        10, 8, 44, 40, 51, 7, 8, 39, 34, 52,
        52, 4, 56, 61, 59, 26, 22, 15, 17, 9,
        47, 38, 45, 10, 0, 12, 9, 20, 51, 59,
        32, 58, 19, 28, 11, 40, 8, 28, 6, 0,
        13, 47, 34, 60, 4, 56, 21, 60, 59, 16,
        38, 52, 61, 44, 8, 35, 4, 11
    ]
    f3 = [
        60, 30, 12, 34, 33, 7, 15, 29, 16, 20,
        46, 25, 8, 31, 4, 48, 6, 44, 57, 16,
        12, 58, 48, 59, 21, 32, 2, 18, 51, 8,
        50, 29, 58, 6, 24, 34, 11, 23, 57, 43,
        59, 50, 10, 56, 27, 32, 12, 59, 16, 4,
        40, 39, 26, 10, 49, 56, 51, 60, 21, 37,
        12, 56, 39, 15, 53, 11, 33, 43, 52, 37,
        30, 25, 19, 55, 7, 34, 48, 36
    ]
    p1 = [
        11, 9, 12, 0, 1, 4, 10, 13, 3,
        6, 7, 8, 15, 5, 2, 14
    ]
    p2 = [
        1, 13, 5, 8, 7, 10, 0, 15, 12, 3,
        14, 11, 2, 9, 6, 4
    ]

    if len(s) < 16:
        return "(key to short)"

    for c in s:
        if c > '9':
            if c > 'Z':
                ai.append((ord(c) - 97) + 36)
            else:
                ai.append((ord(c) - 65) + 10)
        else:
            ai.append(ord(c) - 48)

    for i in i_list:
        ai[i] = f1[ai[i] + i]

    for i in i_list:
        pomoc.insert(i, (ai[i] + ai[p1[i]]) % 62)
    ai = pomoc

    for i in i_list:
        ai[i] = f2[ai[i] + i]

    pomoc = []
    for i in i_list:
        pomoc.insert(i, (ai[i] + ai[p2[i]]) % 62)
    ai = pomoc

    for i in i_list:
        ai[i] = f3[ai[i] + i]

    for j in ai:
        if j >= 10:
            if j >= 36:
                stringbuffer += chr((97 + j) - 36)
            else:
                stringbuffer += chr((65 + j) - 10)
        else:
            stringbuffer += chr(48 + j)

    return stringbuffer


def zassaj(host, z, mssl):
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


def zassaj_http(host, z, get_uo=0, mssl=0):

    a = zassaj(host, z, mssl)
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


def autoryzuj(nickname, password):
    Cookie = "Cookie:"
    Cookie += zassaj_http("kropka.onet.pl",
                          "GET /_s/kropka/1?DV=czat/applet/FULL HTTP/1.1\r\n" \
                          "Host: kropka.onet.pl\r\n" \
                          "Connection: keep-alive\r\n\r\n")
    Cookie += zassaj_http("czat.onet.pl",
                          "GET /myimg.gif HTTP/1.1\r\n" \
                          "Host: czat.onet.pl\r\n" + Cookie + "\r\n\r\n")
    POST = "api_function=getUoKey&params=a:3:{" \
           "s:4:\"nick\";s:%d:\"%s\";" \
           "s:8:\"tempNick\";i:%d;" \
           "s:7:\"version\";s:22:\"1.1(20110425-2020 - R)\";}"
    if nickname[0] == '~':
        POST = POST % (len(nickname) - 1, nickname[1:], 1)
    else:
        POST = POST % (len(nickname), nickname, 0)
        POST_s = "r=&url=&login=%s&haslo=%s&app_id=20&ssl=1&ok=1" % (nickname, password)
        POST_OVERRIDE = "api_function=userOverride&params=a:3:{s:4:\"nick\";s:%d:\"%s\";}" % (len(nickname), nickname)
        zassaj_http("secure.onet.pl",
                    "POST /mlogin.html HTTP/1.1\r\n" \
                    "Content-Type: application/x-www-form-urlencoded\r\n" \
                    "Content-Length: %d\r\n" \
                    "Cache-Control: no-cache\r\n" \
                    "Pragma: no-cache\r\n" \
                    "User-Agent: Mozilla/4.0 (Windows NT 5.0)\r\n" \
                    "Host: secure.onet.pl\r\n" \
                    "Connection: keep-alive\r\n" \
                    "%s\r\n\r\n" \
                    "%s" % (len(POST_s), Cookie, POST_s), 0, 1)
        zassaj_http("czat.onet.pl",
                    "POST /include/ajaxapi.xml.php3 HTTP/1.1\r\n" \
                    "Content-Type: application/x-www-form-urlencoded\r\n" \
                    "Content-Length: %d\r\n" \
                    "Cache-Control: no-cache\r\n" \
                    "Pragma: no-cache\r\n" \
                    "User-Agent: Mozilla/4.0 (Windows NT 5.0)\r\n" \
                    "Host: czat.onet.pl\r\n" \
                    "Accept: text/html, image/gif, image/jpeg, *; q=.2, */*;" \
                    "q=.2\r\n" \
                    "Connection: close\r\n" \
                    "%s\r\n\r\n" \
                    "%s" % (len(POST_OVERRIDE), Cookie, POST_OVERRIDE), 1)

    uoKey = \
        zassaj_http("czat.onet.pl",
                    "POST /include/ajaxapi.xml.php3 HTTP/1.1\r\n" \
                    "Content-Type: application/x-www-form-urlencoded\r\n" \
                    "Content-Length: %d\r\n" \
                    "Cache-Control: no-cache\r\n" \
                    "Pragma: no-cache\r\n" \
                    "User-Agent: Mozilla/4.0 (Windows NT 5.0)\r\n" \
                    "Host: czat.onet.pl\r\n" \
                    "Accept: text/html, image/gif, image/jpeg, *; q=.2, */*;" \
                    "q=.2\r\n" \
                    "Connection: close\r\n" \
                    "%s\r\n\r\n" \
                    "%s" % (len(POST), Cookie, POST), 1)
    return uoKey


def jedziesz(sock, ID):
    bufor = ""
    koniec = 0
    nickname = ""
    password = ""
    lkodowanie = kodowanie
    lkolor = kolor
    lbold = bold
    lemoty = emoty
    while 1:
        b1 = ""
        b1 = sock.recv(1024)
        if b1 == "": return
        bufor += b1.decode()
        if not bufor.find("NICK") == -1:
            nickname = findall("NICK (.*?)(\r|\n)", bufor)[0][0]
            if nickname[0] == '~':
                break
        if not bufor.find("PASS") == -1:
            password = findall("PASS (.*?)(\r|\n)", bufor)[0][0]
        if (password != "") and (nickname != ""):
            print("wtf")
            break

    sock.send((str.encode(":fake.host 666 nik : 10[Tunel] uzycie:\r\n"
               ":fake.host 666 nik : 10[Tunel] /set nick 10Twoj_nick\r\n"
               ":fake.host 666 nik : 10[Tunel] /server 127.0.0.1 7777 10haslo_do_nicka\r\n"
               ":fake.host 666 nik : 10[Tunel] \r\n"
               ":fake.host 666 nik : 10[Tunel] dla nicka tymczasowego: /set nick 10~Twoj_nick\r\n")))
    sock.send((str.encode(":fake.host 666 nik : 10[Tunel] \r\n"
               ":fake.host 666 nik : 10[Tunel] ustawienia polaczenia:\r\n"
               ":fake.host 666 nik : 10[Tunel] obsluga kolorow:5              %d\r\n"
               ":fake.host 666 nik : 10[Tunel] obsluga pogrubienia czcionki:5 %d\r\n"
               ":fake.host 666 nik : 10[Tunel] \r\n") % (lkolor, lbold)))
    sock.send((str.encode(":fake.host 666 nik : 10[Tunel] komendy:\r\n"
               ":fake.host 666 nik : 10[Tunel] /sets 10<--- pokazuje ustawienia\r\n"
               ":fake.host 666 nik : 10[Tunel] /uo 10<--- zwraca UoKey\r\n"
               ":fake.host 666 nik : 10[Tunel] /sets kolor 0 10<---5 010: wylacza kolor,5 110: wlaczyc\r\n"
               ":fake.host 666 nik : 10[Tunel] /sets kodowanie 0 10<---5 010: ISO 8859-2 (irssi),5 110: CP-1250 (mIRC 6.*),5 210: UTF-8 (mIRC 7.*)\r\n"
               ":fake.host 666 nik : 10[Tunel] /sets bold 0 10<---5 010: wylacza pogrubienie czcionki,5 110: wlacza\r\n")))
    sock.send(str.encode(
        (":fake.host 666 nik : 10[Tunel] /sets emoty 0 10<---5 010: %Ihihi%,5 110: <hihi>,5 210: //hihi\r\n")))
    if not TUNEL_PASS == "":
        password = password.split(':')
        if not len(password) == 2:
            sys.stdout.write("[%3d]nick: %s :: pass: %s\n" % (ID, nickname, ':'.join(password)))
            send(sock, "uzywaj: /server host port haslo_do_tunel:haslo_do_nick\r\n")
            sock.close()
            return
        if not password[0] == TUNEL_PASS:
            sys.stdout.write("[%3d]nick: %s :: pass: %s\n" % (ID, nickname, ':'.join(password)))
            send(sock, "zle haslo do tunela\r\n")
            sock.close()
            return
        password = password[1]
    sys.stdout.write("nick: %s\n" % nickname)
    try:

        UOkey = autoryzuj(nickname, password)

    # sock.send((":fake.host 666 nik : 10[Tunel] \r\n"
    #             ":fake.host 2012 " + nickname + " : 10[Tunel] Twoj UOkey: " + UOkey + "\r\n"))
    #  sock.send((":Tunel!fake@fake.fake PRIVMSG fake :VERSION\r\n"))
    except:
        print(sys.exc_info()[0])
        dawaj_date()
        my_err = "[%3d] ERROR: sprawdz swoje polaczenie sieciowe z internetem, poprawnosc wprowadzonego hasla i nicka lub dostepnosc serwerow onet.pl (zmiany autoryzacji)\r\n" % ID
        sys.stdout.write(my_err)
        sock.send(str.encode(my_err))
        sock.close()
        return
    print("1!")
    gniazda = []
    gniazda.append(sock)
    onet = socket(AF_INET, SOCK_STREAM)
    gniazda.append(onet)
    onet.bind((local_ip, 0))
    onet.connect(("czat-app.onet.pl", 5015))
    sock.send(onet.recv(1024))
    onet.send(str.encode("AUTHKEY\r\n"))
    onet.send(str.encode("NICK "+nickname+"\r\n"))
    onet.send(str.encode("USER * "+UOkey+" czat-app.onet.pl :" +nickname + "\r\n"))
    # onet.send("USER * %s czat-app.onet.pl :%s\r\n" % (UOkey, realname))
    authkey = auth(findall(":.*?801.*?:(.*?)\r", onet.recv(1024).decode("utf-8", "ignore"))[0])
    onet.send(str.encode("AUTHKEY "+ authkey + "\r\n"))
    while 1:
        (dr, dw, de) = select.select(gniazda, [], [])
        for gotowe in dr:
            if gotowe == sock:
                try:
                    bufor = gotowe.recv(1024).decode("utf-8", "ignore")
                    if bufor == "":
                        koniec = 1
                        break
                    if bufor.find("NOTICE") != -1 and bufor.find("VERSION") != -1:
                        if bufor.find("mIRC v6") != -1:
                            lkodowanie = 1
                        elif bufor.find("mIRC v7") != -1:
                            lkodowanie = 2
                        else:
                            lkodowanie = 0
                        sock.send(
                            (":fake.host 666 nik : 10[Tunel] ustawiono typ kodowania:5                %d\r\n") % (
                            lkodowanie))
                    if lkodowanie == 1:
                        bufor = bufor.replace('\xa5', '\xa1')
                        bufor = bufor.replace('\xb9', '\xb1')
                        bufor = bufor.replace('\x8c', '\xa6')
                        bufor = bufor.replace('\x9c', '\xb6')
                        bufor = bufor.replace('\x8f', '\xac')
                        bufor = bufor.replace('\x9f', '\xbc')
                    elif lkodowanie == 2:
                        bufor = bufor.replace("\xc4\x84", "\xa1")
                        bufor = bufor.replace("\xc4\x86", "\xc6")
                        bufor = bufor.replace("\xc4\x98", "\xca")
                        bufor = bufor.replace("\xc5\x81", "\xa3")
                        bufor = bufor.replace("\xc5\x83", "\xd1")
                        bufor = bufor.replace("\xc3\x93", "\xd3")
                        bufor = bufor.replace("\xc5\x9a", "\xa6")
                        bufor = bufor.replace("\xc5\xb9", "\xac")
                        bufor = bufor.replace("\xc5\xbb", "\xaf")
                        bufor = bufor.replace("\xc4\x85", "\xb1")
                        bufor = bufor.replace("\xc4\x87", "\xe6")
                        bufor = bufor.replace("\xc4\x99", "\xea")
                        bufor = bufor.replace("\xc5\x82", "\xb3")
                        bufor = bufor.replace("\xc5\x84", "\xf1")
                        bufor = bufor.replace("\xc3\xb3", "\xf3")
                        bufor = bufor.replace("\xc5\x9b", "\xb6")
                        bufor = bufor.replace("\xc5\xba", "\xbc")
                        bufor = bufor.replace("\xc5\xbc", "\xbf")
                    bufor = bufor.replace('\x03' + "14", "%C959595%")
                    bufor = bufor.replace('\x03' + "5", "%C990033%")
                    bufor = bufor.replace('\x03' + "7", "%Cc86c00%")
                    bufor = bufor.replace('\x03' + "5", "%C623c00%")
                    bufor = bufor.replace('\x03' + "13", "%Cce00ff%")
                    bufor = bufor.replace('\x03' + "4", "%Ce40f0f%")
                    bufor = bufor.replace('\x03' + "12", "%C3030ce%")
                    bufor = bufor.replace('\x03' + "3", "%C008100%")
                    bufor = bufor.replace('\x03' + "10", "%C1a866e%")
                    bufor = bufor.replace('\x03' + "11", "%C006699%")
                    bufor = bufor.replace('\x03' + "6", "%C8800ab%")
                    bufor = bufor.replace('\x03' + "2", "%C0f2ab1%")
                    bufor = bufor.replace('\x03' + "7", "%Cff6500%")
                    bufor = bufor.replace('\x03' + "4", "%Cff0000%")
                    if lemoty == 1:
                        b = findall("(<(.+?)>)", bufor)
                        for c in b:
                            bufor = bufor.replace(c[0], "%I" + c[1] + "%")
                    elif lemoty == 2:
                        b = findall("(//(\w+))", bufor)
                        for c in b:
                            bufor = bufor.replace(c[0], "%I" + c[1] + "%")
                    tmpb = bufor.split(' ')
                    if tmpb[0] == "PRIVMSG":
                        if tmpb[1][0:2] == '#^':
                            tmpb[1] = tmpb[1].replace('#^', '^')
                            bufor = ' '.join(tmpb)
                    elif (tmpb[0] == "JOIN") and (tmpb[1][0:2] == '#^'):
                        tmpb[1] = tmpb[1].replace('#^', '^')
                        bufor = ' '.join(tmpb)
                    elif (tmpb[0] == "PART") and (tmpb[1][0:2] == '#^'):
                        tmpb[1] = tmpb[1].replace('#^', '^')
                        bufor = ' '.join(tmpb)
                    elif (tmpb[0] == "INVITE") and (tmpb[2][0:2] == '#^'):
                        tmpb[2] = tmpb[2].replace('#^', '^')
                        bufor = ' '.join(tmpb)
                    elif tmpb[0][:2] == "UO":
                        send(sock, ":fake.host 2012 " + nickname + " : 10[Tunel] Twoj UOkey: " + UOkey + "\r\n")
                    elif tmpb[0][:4] == "SETS":
                        try:
                            if tmpb[1] == "kolor":
                                try:
                                    lkolor = int(tmpb[2][0])
                                except:
                                    send(sock,"onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
                            elif tmpb[1] == "kodowanie":
                                try:
                                    lkodowanie = int(tmpb[2][0])
                                except:
                                    send(sock,"onettunel.py - dozwolone wartosci: 1 i 0\r\n")
                            elif tmpb[1] == "bold":
                                try:
                                    lbold = int(tmpb[2][0])
                                except:
                                    send(sock,"onettunel.py - dozwolone wartosci: 1 i 0\r\n")
                            elif tmpb[1] == "emoty":
                                try:
                                    lemoty = int(tmpb[2][0])
                                except:
                                    send(sock,"onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
                        except:
                            pass
                            send(sock,(":fake.host 666 nik : 10[Tunel] ustawienia polaczenia:\r\n"
                                   ":fake.host 666 nik : 10[Tunel]  kolor:5     %d\r\n"
                                   ":fake.host 666 nik : 10[Tunel]  kodowanie:5 %d\r\n"
                                   ":fake.host 666 nik : 10[Tunel]  bold:5      %d\r\n"
                                   ":fake.host 666 nik : 10[Tunel]  emoty:5     %d\r\n") % (
                                  lkolor, lkodowanie, lbold, lemoty))
                    elif tmpb[0] == "LIST":
                        bufor = "SLIST\r\n"
                    elif (tmpb[0] == "PROTOCTL"):
                        bufor = bufor.replace("NAMESX", "ONETNAMESX")
                    elif tmpb[0] == "CAM":
                        if tmpb[3][:2] == "on":
                            cammsg = ":WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " + tmpb[1] + "\r\n"
                        if tmpb[3][:3] == "off":
                            cammsg = ":WebcamServ!service@service.onet MODE " + tmpb[2] + " -Cam " + tmpb[1] + "\r\n"
                        if lkodowanie == 1:
                            cammsg = cammsg.replace('\xa1', '\xa5')
                            cammsg = cammsg.replace('\xb1', '\xb9')
                            cammsg = cammsg.replace('\xa6', '\x8c')
                            cammsg = cammsg.replace('\xb6', '\x9c')
                            cammsg = cammsg.replace('\xac', '\x8f')
                            cammsg = cammsg.replace('\xbc', '\x9f')
                        if lkodowanie == 2:
                            cammsg = cammsg.replace("\xa1", "\xc4\x84")
                            cammsg = cammsg.replace("\xc6", "\xc4\x86")
                            cammsg = cammsg.replace("\xca", "\xc4\x98")
                            cammsg = cammsg.replace("\xa3", "\xc5\x81")
                            cammsg = cammsg.replace("\xd1", "\xc5\x83")
                            cammsg = cammsg.replace("\xd3", "\xc3\x93")
                            cammsg = cammsg.replace("\xa6", "\xc5\x9a")
                            cammsg = cammsg.replace("\xac", "\xc5\xb9")
                            cammsg = cammsg.replace("\xaf", "\xc5\xbb")
                            cammsg = cammsg.replace("\xb1", "\xc4\x85")
                            cammsg = cammsg.replace("\xe6", "\xc4\x87")
                            cammsg = cammsg.replace("\xea", "\xc4\x99")
                            cammsg = cammsg.replace("\xb3", "\xc5\x82")
                            cammsg = cammsg.replace("\xf1", "\xc5\x84")
                            cammsg = cammsg.replace("\xf3", "\xc3\xb3")
                            cammsg = cammsg.replace("\xb6", "\xc5\x9b")
                            cammsg = cammsg.replace("\xbc", "\xc5\xba")
                            cammsg = cammsg.replace("\xbf", "\xc5\xbc")
                            send(sock,cammsg)
                    send(onet ,bufor)
                except:
                    dawaj_date()
                    print("[%3d] nick: %s = blad odczytu/zapisu z/do gniazda",  (ID, nickname))
                    koniec = 1
                    break
            if gotowe == onet:
                bufor = ""
                try:
                    while 1:
                        bu2 = gotowe.recv(1024).decode("utf-8", "ignore")
                        if bu2 == "":
                            koniec = 1
                            break
                        if bu2[len(bu2) - 1] == '\n':
                            bufor += bu2
                            break
                        bufor += bu2
                    tab = findall("(.*?\n)", bufor)
                    for linia in tab:
                        if lkodowanie == 1:
                            linia = linia.replace('\xa1', '\xa5')
                            linia = linia.replace('\xb1', '\xb9')
                            linia = linia.replace('\xa6', '\x8c')
                            linia = linia.replace('\xb6', '\x9c')
                            linia = linia.replace('\xac', '\x8f')
                            linia = linia.replace('\xbc', '\x9f')
                        if lkodowanie == 2:
                            linia = linia.replace("\xa1", "\xc4\x84")
                            linia = linia.replace("\xc6", "\xc4\x86")
                            linia = linia.replace("\xca", "\xc4\x98")
                            linia = linia.replace("\xa3", "\xc5\x81")
                            linia = linia.replace("\xd1", "\xc5\x83")
                            linia = linia.replace("\xd3", "\xc3\x93")
                            linia = linia.replace("\xa6", "\xc5\x9a")
                            linia = linia.replace("\xac", "\xc5\xb9")
                            linia = linia.replace("\xaf", "\xc5\xbb")
                            linia = linia.replace("\xb1", "\xc4\x85")
                            linia = linia.replace("\xe6", "\xc4\x87")
                            linia = linia.replace("\xea", "\xc4\x99")
                            linia = linia.replace("\xb3", "\xc5\x82")
                            linia = linia.replace("\xf1", "\xc5\x84")
                            linia = linia.replace("\xf3", "\xc3\xb3")
                            linia = linia.replace("\xb6", "\xc5\x9b")
                            linia = linia.replace("\xbc", "\xc5\xba")
                            linia = linia.replace("\xbf", "\xc5\xbc")
                        if lkolor == 1:
                            linia = linia.replace("%C959595%", '\x03' + "14")
                            linia = linia.replace("%C990033%", '\x03' + "05")
                            linia = linia.replace("%Cc86c00%", '\x03' + "07")
                            linia = linia.replace("%C623c00%", '\x03' + "05")
                            linia = linia.replace("%Cce00ff%", '\x03' + "13")
                            linia = linia.replace("%Ce40f0f%", '\x03' + "04")
                            linia = linia.replace("%C3030ce%", '\x03' + "12")
                            linia = linia.replace("%C008100%", '\x03' + "03")
                            linia = linia.replace("%C1a866e%", '\x03' + "10")
                            linia = linia.replace("%C006699%", '\x03' + "11")
                            linia = linia.replace("%C8800ab%", '\x03' + "06")
                            linia = linia.replace("%C0f2ab1%", '\x03' + "02")
                            linia = linia.replace("%Cff6500%", '\x03' + "07")
                            linia = linia.replace("%Cff0000%", '\x03' + "04")
                        if lbold == 1:
                            linia = sub("%Fb.*?%", '\x02', linia)
                        linia = sub("%C[a-fA-F0-9]{6}%", '', linia)
                        linia = linia.replace("%C%", '')
                        linia = sub("%F.?.?:[a-z]+%", '', linia)
                        linia = sub("%F[bi]{0,2}%", '', linia)
                        if lemoty == 1:
                            tmpb = linia.split(' ')
                            if tmpb[1] != "353":
                                b = findall("(%I(.+?)%)", linia)
                                for c in b:
                                    linia = linia.replace(c[0], "<" + c[1] + ">")
                        elif lemoty == 2:
                            tmpb = linia.split(' ')
                            if tmpb[1] != "353":
                                b = findall("(%I(.+?)%)", linia)
                                for c in b:
                                    linia = linia.replace(c[0], "//" + c[1])
                        try:
                            tmpb = linia.split(' ')
                            if tmpb[1] == "PRIVMSG":
                                if tmpb[2][0] == '^':
                                    tmpb[2] = tmpb[2].replace('^', '#^')
                                    linia = ' '.join(tmpb)

                            elif tmpb[1] == "MODERMSG":
                                linia = "%s PRIVMSG %s :MODERMSG %s: %s" % (
                                tmpb[0], tmpb[4], tmpb[2], ' '.join(tmpb[5:])[1:])
                            elif tmpb[1] == "MODERNOTICE":
                                linia = "%s PRIVMSG %s :MODERNOTICE: %s" % (tmpb[0], tmpb[2], ' '.join(tmpb[3:])[1:])



                            elif tmpb[1] == "JOIN":
                                if tmpb[2][0] == '^':
                                    linia = linia.replace('^', '#^')
                                elif tmpb[3][:2] == ':W':
                                    tmpb[3] = sub(",[0-3]\r\n", '', tmpb[3])
                                    if tmpb[3][:3] == ":Wr":
                                        linia = tmpb[3].replace(":Wrx", tmpb[0] + " " + tmpb[1] + " " + tmpb[
                                            2] + "\r\n:WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " +
                                                                tmpb[0][1:].split('!')[0] + "\r\n")
                                    elif tmpb[3][:4] == ":Wbr":
                                        linia = tmpb[3].replace(":Wbrx", tmpb[0] + " " + tmpb[1] + " " + tmpb[
                                            2] + "\r\n:WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " +
                                                                tmpb[0][1:].split('!')[0] + "\r\n")
                            elif tmpb[1] == "MODE":
                                if tmpb[3][:2] == "+W":
                                    linia = tmpb[0] + " 2010 :CAM " + tmpb[2] + " on\r\n"
                                elif tmpb[3][:2] == "-W":
                                    linia = tmpb[0] + " 2010 :CAM " + tmpb[2] + " off\r\n"
                            elif tmpb[1] == "353":
                                if tmpb[4][0] == '^':
                                    tmpb[4] = tmpb[4].replace('^', '#^')
                                    linia = ' '.join(tmpb)
                                if linia.find('|') != -1:
                                    tmpstr = ""
                                    a1 = linia.split(':')
                                    a1[2] = a1[2].replace("\r\n", "")
                                    ta1 = a1[2].split(' ')
                                    for aa1 in ta1:
                                        if aa1 == '': continue
                                        xx = aa1.split('|')
                                        if (xx[1][:3] == "Wbr") or (xx[1][:2] == "Wr"):
                                            tmpstr += '=' + xx[0] + " "
                                        else:
                                            tmpstr += xx[0] + " "
                                    a1[2] = tmpstr
                                    linia = ':'.join(a1) + "\r\n"
                            elif tmpb[1] == "366":
                                if tmpb[3][0] == '^':
                                    tmpb[3] = tmpb[3].replace('^', '#^')
                                    linia = ' '.join(tmpb)
                            elif tmpb[1] == "341":
                                if tmpb[4][0] == '^':
                                    tmpb[4] = tmpb[4].replace('^', '#^')
                                    linia = ' '.join(tmpb)
                            elif tmpb[1] == "NOTICE":
                                if tmpb[2][0] == '^':
                                    tmpb[2] = tmpb[2].replace('^', '#^')
                                    linia = ' '.join(tmpb)
                            elif tmpb[1] == "PART":
                                if tmpb[2][0] == '^':
                                    tmpb[2] = tmpb[2].replace('^', '#^')
                                    linia = ' '.join(tmpb)
                            elif tmpb[1] == "INVITE":
                                if tmpb[3][1] == '^':
                                    tmpb[3] = tmpb[3].replace('^', '#^')
                                    linia = ' '.join(tmpb)
                            elif tmpb[1] == "817":
                                linia = ":_-_!name@host.org PRIVMSG %s :%s <%s> %s" % (
                                tmpb[3], czas(tmpb[4]), tmpb[5], ' '.join(tmpb[7:]))
                            elif tmpb[1] == "819":
                                onethost = tmpb[0]
                                tab3 = findall("(#.+?):.:(\d+)", linia)
                                for room in tab3:
                                    send(sock, "%s 322 %s %s %s :\r\n" % (onethost, nickname, room[0], room[1]))
                                linia = ""
                            elif tmpb[1] == "820":
                                linia = "%s 323 %s :End of LIST\r\n" % (tmpb[0], nickname)
                            elif tmpb[1] == "421":
                                linia = linia.replace(" MODE :This command has been disabled.", '')
                                linia = linia.replace(" SETS :Unknown command", '')
                                linia = linia.replace(" CAM :Unknown command", '')
                                linia = linia.replace(" UO :Unknown command", '')
                            elif tmpb[1] == "005":
                                linia = linia.replace(" PREFIX=(qaohXYv)`&@%!=+ ", ' PREFIX=(CqaohXv)=`&@%!+ ')
                        except:
                            pass
                        if linia != "":
                            send(sock, linia)
                except:
                    dawaj_date()
                    print("[%3d] nick: %s = blad odczytu/zapisu z/do gniazda", (ID, nickname))
                    koniec = 1
                    break
        if koniec == 1:
            sock.close()
            onet.close()
            break


s = socket(AF_INET, SOCK_STREAM)
try:
    s.bind(('', BindPort))
except:
    dawaj_date()
    print("ERROR: nie mozna zabindowac portu %s, wybierz inny BindPort")
    s.close()
    sys.exit()
dawaj_date()
if local_ip != '':
    print("server:  + $local_ip + $BindPort")
else:
    print("server:" + str(gethostbyname(gethostname())) + str(BindPort))
s.listen(5)
cID = 1
while 1:
    c, cinfo = s.accept()
    dawaj_date()
    sys.stdout.write("[%3d] %s:%s = " % ((cID,) + cinfo))

    threading.Thread(target=jedziesz,
                     args=(c, cID)
                     ).start()
    cID = cID + 1
s.close()