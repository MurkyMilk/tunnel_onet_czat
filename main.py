#!/usr/bin/env python

############### CONFIG ###############
import select
import sys
import threading
from re import findall
from socket import *

from auth import auth, authorization
from connection import createSocketConnection, create_socket
from encoding import applyEncoding, get_proper_encoding
from fromClientParser import process_message_from_client
from fromOnetParser import parse_and_send_incomining_message
from util import send, get_date_string, recv
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

    try:
        checkTunnelPassword(password)
        password = extractPassword(password)
        UOkey = authorization(nickname, password)
    except Exception as e:
        print(e)
        sock.close()
        return

    sockets = [sock]
    onet = connect_to_onet(UOkey, nickname, sock, sockets)
    mainLoop(UOkey, encode, end, lbold, lemoty, lkolor, nickname, onet, sock, sockets)


def extractPassword(password):
    if TUNEL_PASS:
        password = password.split(':')
        if len(password) != 2:
            raise Exception("wrong password parsing!")
        password = password[1]
    return password

def checkTunnelPassword(password):
    if TUNEL_PASS and password[0] != TUNEL_PASS:
        raise Exception("wrong password for tunnel!")


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
    send(sock, recv(onet, 1024))
    send(onet, "AUTHKEY\r\n")
    send(onet, "NICK " + nickname + "\r\n")
    send(onet, ("USER * " + UOkey + " czat-app.onet.pl :" + nickname + "\r\n"))
    authkey = auth(findall(":.*?801.*?:(.*?)\r", recv(onet, 1024))[0])
    send(onet, "AUTHKEY " + authkey + "\r\n")
    return onet


def mainLoop(UOkey, encode, end, lbold, lemoty, lkolor, nickname, onet_socket, client_socket, sockets):
    while 1:
        (sockets_with_ready_messages, dw, de) = select.select(sockets, [], [])
        for socket_with_ready_msg in sockets_with_ready_messages:
            if socket_with_ready_msg == client_socket:
                try:
                    received_message = recv(socket_with_ready_msg, 1024)
                    if received_message == "":
                        end = 1
                        break
                    encode = get_proper_encoding(received_message, encode)
                    received_message = applyEncoding(received_message, encode, lemoty)
                    splitted_received_message = received_message.split(' ')
                    encode, lbold, lemoty, lkolor = process_message_from_client(UOkey, received_message, encode, lbold, lemoty,
                                                                                lkolor, nickname, onet_socket, client_socket, splitted_received_message)
                except Exception as e:
                    print(e)
                    end = 1
                    break
            if socket_with_ready_msg == onet_socket:
                received_message = ""
                try:
                    while 1:
                        chunk_of_received_msg = socket_with_ready_msg.recv(1024).decode("utf-8", "ignore")
                        if chunk_of_received_msg == "":
                            end = 1
                            break
                        if chunk_of_received_msg[len(chunk_of_received_msg) - 1] == '\n':
                            received_message += chunk_of_received_msg
                            break
                        received_message += chunk_of_received_msg
                    splitted_received_message = findall("(.*?\n)", received_message)
                    parse_and_send_incomining_message(encode, lbold, lemoty, lkolor, nickname, client_socket, splitted_received_message)
                except:
                    end = 1
                    break
        if end == 1:
            client_socket.close()
            onet_socket.close()
            break


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
