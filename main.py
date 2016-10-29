#!/usr/bin/env python

############### CONFIG ###############
import select
import threading
from re import findall
from socket import *
import sys

from auth import auth, authorization
from connection import createSocketConnection, create_socket
from encoding import applyEncoding
from fromClientParser import process_message_from_client
from fromOnetParser import parse_and_send_incomining_message
from util import send, get_date_string
from welcome_information import send_welcome_messages, printWelcomeInfo

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


##HERE COMES THE DRAGONS



global s
s = create_socket()
printWelcomeInfo(color, bold, encoding)
createSocketConnection(s, port, local_ip)
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
