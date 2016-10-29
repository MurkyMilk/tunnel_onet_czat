#!/usr/bin/env python

############### CONFIG ###############
import threading

from auth import auth, authorization
from encoding import applyEncoding
from fromClientParser import process_message_from_client
from fromOnetParser import parse_and_send_incomining_message
from util import send

color = 0  # obsluga kolorow, 0 aby wylaczyc;
bold = 0  # obsluga pogrubienia czcionki;
encoding = 2  # Kodowanie 0 - ISO, 1 - WIN, 2 - UTF;
emoty = 1  # Emoty 0 - %Ihihi%, 1 - <hihi>, 2 - //hihi;
#
TUNEL_PASS = ""  # haslo do zabezpieczenia tunelu;
local_ip = ""  # vHost, lub puste
port = 6601  # port, bez ""
realname = "Mlecko"  # nazwa

######################################


from socket import *
from re import findall
from time import ctime
import select

import sys

wersja = sys.version[0] + sys.version[2]
if wersja <= "":
    pass
else:
    pass


def get_date_string():
    return "[%s] = " % ctime()


def time(cz):
    a = ""
    try:
        a = [x for x in ctime(int(cz)).split(' ') if x.find(':') != -1][0]
    except:
        a = cz
    return a


def init(sock, ID):
    bufor = ""
    end = 0
    nickname = ""
    password = ""
    encode = encoding
    lkolor = color
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

    send_welcome_messages(lbold, lkolor, sock)
    if not TUNEL_PASS == "":
        password = password.split(':')
        if not len(password) == 2:
            return wrong_password_parsing(ID, nickname, password, sock)
        if not password[0] == TUNEL_PASS:
            return inform_wrong_tunnel_password(ID, nickname, password, sock)
        password = password[1]
    sys.stdout.write("nick: %s\n" % nickname)
    try:

        UOkey = authorization(nickname, password)

    # sock.send((":fake.host 666 nik : 10[Tunel] \r\n"
    #             ":fake.host 2012 " + nickname + " : 10[Tunel] Twoj UOkey: " + UOkey + "\r\n"))
    #  sock.send((":Tunel!fake@fake.fake PRIVMSG fake :VERSION\r\n"))
    except:
        print(sys.exc_info()[0])
        get_date_string()
        my_err = "[%3d] ERROR: sprawdz swoje polaczenie sieciowe z internetem, poprawnosc wprowadzonego hasla i nicka lub dostepnosc serwerow onet.pl (zmiany autoryzacji)\r\n" % ID
        sys.stdout.write(my_err)
        sock.send(str.encode(my_err))
        sock.close()
        return
    sockets = [sock]
    onet = connect_to_onet(UOkey, nickname, sock, sockets)
    mainLoop(ID, UOkey, encode, end, lbold, lemoty, lkolor, nickname, onet, sock, sockets)


def wrong_password_parsing(ID, nickname, password, sock):
    sys.stdout.write("[%3d]nick: %s :: pass: %s\n" % (ID, nickname, ':'.join(password)))
    send(sock, "uzywaj: /server host port haslo_do_tunel:haslo_do_nick\r\n")
    sock.close()
    return


def inform_wrong_tunnel_password(ID, nickname, password, sock):
    sys.stdout.write("[%3d]nick: %s :: pass: %s\n" % (ID, nickname, ':'.join(password)))
    send(sock, "zle haslo do tunela\r\n")
    sock.close()
    return


def connect_to_onet(UOkey, nickname, sock, sockets):
    onet = socket(AF_INET, SOCK_STREAM)
    sockets.append(onet)
    onet.bind((local_ip, 0))
    onet.connect(("czat-app.onet.pl", 5015))
    sock.send(onet.recv(1024))
    onet.send(str.encode("AUTHKEY\r\n"))
    onet.send(str.encode("NICK " + nickname + "\r\n"))
    onet.send(str.encode("USER * " + UOkey + " czat-app.onet.pl :" + nickname + "\r\n"))
    # onet.send("USER * %s czat-app.onet.pl :%s\r\n" % (UOkey, realname))
    authkey = auth(findall(":.*?801.*?:(.*?)\r", onet.recv(1024).decode("utf-8", "ignore"))[0])
    onet.send(str.encode("AUTHKEY " + authkey + "\r\n"))
    return onet


def mainLoop(ID, UOkey, encode, end, lbold, lemoty, lkolor, nickname, onet, sock, sockets):
    while 1:
        (dr, dw, de) = select.select(sockets, [], [])
        for ready in dr:
            if ready == sock:
                try:
                    bufor = ready.recv(1024).decode("utf-8", "ignore")
                    if bufor == "":
                        end = 1
                        break
                    encode = set_proper_encoding(bufor, encode, sock)
                    bufor = applyEncoding(bufor, encode, lemoty)
                    tmpb = bufor.split(' ')
                    encode, lbold, lemoty, lkolor = process_message_from_client(UOkey, bufor, encode, lbold, lemoty,
                                                                                lkolor, nickname, onet, sock, tmpb)
                except:
                    get_date_string()
                    print("[%3d] nick: %s = blad odczytu/zapisu z/do gniazda", (ID, nickname))
                    end = 1
                    break
            if ready == onet:
                bufor = ""
                try:
                    while 1:
                        bu2 = ready.recv(1024).decode("utf-8", "ignore")
                        if bu2 == "":
                            end = 1
                            break
                        if bu2[len(bu2) - 1] == '\n':
                            bufor += bu2
                            break
                        bufor += bu2
                    tab = findall("(.*?\n)", bufor)
                    parse_and_send_incomining_message(encode, lbold, lemoty, lkolor, nickname, sock, tab)
                except:
                    get_date_string()
                    print("[%3d] nick: %s = blad odczytu/zapisu z/do gniazda", (ID, nickname))
                    end = 1
                    break
        if end == 1:
            sock.close()
            onet.close()
            break


def set_proper_encoding(bufor, encode, sock):
    if bufor.find("NOTICE") != -1 and bufor.find("VERSION") != -1:
        if bufor.find("mIRC v6") != -1:
            encode = 1
        elif bufor.find("mIRC v7") != -1:
            encode = 2
        else:
            encode = 0
        sock.send(
            ":fake.host 666 nik : 10[Tunel] ustawiono typ kodowania:5                %d\r\n" % (
                encode))
    return encode


def send_welcome_messages(lbold, lkolor, sock):
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
        ":fake.host 666 nik : 10[Tunel] /sets emoty 0 10<---5 010: %Ihihi%,5 110: <hihi>,5 210: //hihi\r\n"))



##HERE COMES THE DRAGONS

def printWelcomeInfo():
    global realname
    print("onettunel.py v.2010-04 / by Olo (2008-2010) unix.onlinewebshop.net")
    print("poprawki Husar, 08-07-2011\r\n\r\n")
    if realname == "":
        realname = ""
    if color == 1:
        print("Wlaczona obsluga kolorow")
    else:
        print("Wylaczona obsluga kolorow")
    if bold == 1: print("Wlaczona obsluga pogrubienia czcionki")
    if encoding == 1: print("Wlaczona obsluga kodowania CP1250")



def getBindPort():
    global BindPort
    if len(sys.argv) == 2:
        BindPort = int(sys.argv[1])
    else:
        BindPort = port

def bindSocket(s):
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

def createSocketConnection(s):
    getBindPort()
    bindSocket(s)


def create_socket():
    return socket(AF_INET, SOCK_STREAM)


global s
s = create_socket()

printWelcomeInfo()
createSocketConnection(s)
s.listen(5)
cID = 1
while 1:
    c, cinfo = s.accept()
    get_date_string()
    sys.stdout.write("[%3d] %s:%s = " % ((cID,) + cinfo))

    threading.Thread(target=init,
                     args=(c, cID)
                     ).start()
    cID += 1
s.close()
