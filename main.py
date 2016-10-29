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

def worker(sock):
    whole_message = ""
    end = 0
    nickname = ""
    password = ""
    encode = encoding
    lkolor = color
    lbold = bold
    lemoty = emoty

    while ((password == "") or (nickname == "")):
        received_chunk = sock.recv(1024)
        if received_chunk == "": return
        whole_message += received_chunk.decode()
        if not whole_message.find("NICK") == -1:
            nickname = extract_nick(whole_message)
        if not whole_message.find("PASS") == -1:
            password = extract_password(whole_message)

    send_welcome_messages(lbold, lkolor, sock)

    if TUNEL_PASS:
        password = password.split(':')
        if len(password) != 2:
            wrong_password_parsing(sock)
            sock.close()
            return
        if password[0] != TUNEL_PASS:
            inform_wrong_tunnel_password(sock)
            sock.close()
            return
        password = password[1]
    sys.stdout.write("nick: %s\n" % nickname)
    try:

        UOkey = authorization(nickname, password)
    except Exception as e:
        print(e)
        sock.send(str.encode("ERROR: sprawdz swoje polaczenie sieciowe z internetem, poprawnosc wprowadzonego hasla i nicka lub dostepnosc serwerow onet.pl"))
        sock.close()
        return

    sockets = [sock]
    onet = connect_to_onet(UOkey, nickname, sock, sockets)
    mainLoop(UOkey, encode, end, lbold, lemoty, lkolor, nickname, onet, sock, sockets)


def extract_password(whole_message):
    password = findall("PASS (.*?)(\r|\n)", whole_message)[0][0]
    return password


def extract_nick(whole_message):
    nickname = findall("NICK (.*?)(\r|\n)", whole_message)[0][0]
    return nickname


def wrong_password_parsing(sock):
    send(sock, "uzywaj: /server host port haslo_do_tunel:haslo_do_nick\r\n")


def inform_wrong_tunnel_password(sock):
    send(sock, "zle haslo do tunela\r\n")


def connect_to_onet(UOkey, nickname, sock, sockets):
    onet = socket(AF_INET, SOCK_STREAM)
    sockets.append(onet)
    onet.bind((local_ip, 0))
    onet.connect(("czat-app.onet.pl", 5015))
    sock.send(onet.recv(1024))
    onet.send(str.encode("AUTHKEY\r\n"))
    onet.send(str.encode("NICK " + nickname + "\r\n"))
    onet.send(str.encode("USER * " + UOkey + " czat-app.onet.pl :" + nickname + "\r\n"))
    authkey = auth(findall(":.*?801.*?:(.*?)\r", onet.recv(1024).decode("utf-8", "ignore"))[0])
    onet.send(str.encode("AUTHKEY " + authkey + "\r\n"))
    return onet


def mainLoop(UOkey, encode, end, lbold, lemoty, lkolor, nickname, onet, sock, sockets):
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
                    print("nick: %s = blad odczytu/zapisu z/do gniazda", (nickname))
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
while 1:
    c, cinfo = s.accept()
    threading.Thread(target=worker, args=[c]).start()
s.close()
