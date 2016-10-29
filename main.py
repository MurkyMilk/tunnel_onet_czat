#!/usr/bin/env python

############### CONFIG ###############
import select
import sys
import threading
from re import findall
from socket import *

from auth import auth, authorization
from connection import createSocketConnection, create_client_socket
from encoding import applyEncoding, get_proper_encoding
from fromClientMsgHandler import handleMessageFromClient
from fromOnetMsgHandler import handleMessageFromOnet
from util import send, recv
from welcome_information import send_welcome_messages

config = {'encode': 2, #Kodowanie 0 - ISO, 1 - WIN, 2 - UTF;
          'lkolor': 0, # obsluga kolorow, 0 aby wylaczyc;
          'lbold': 0, # obsluga pogrubienia czcionki;
          'lemoty': 1, # Emoty 0 - %Ihihi%, 1 - <hihi>, 2 - //hihi;
          'TUNEL_PASS': "", # haslo do zabezpieczenia tunelu;
           'local_ip': "",  # vHost, lub puste
           'port': 6601,  # port, bez ""
          'realname' : "Mlecko"  # nazwa

          }

######################################

def receive_nickname_and_password(client_socket):

    password = ""
    nickname = ""

    while (password == "") or (nickname == ""):
        msg = client_socket.recv(1024)
        if msg == "": return
        msg = msg.decode()
        if not msg.find("NICK") == -1:
            nickname = get_nick(msg)
        if not msg.find("PASS") == -1:
            password = get_password(msg)
    return nickname, password


def splitPassword(password, TUNEL_PASS):
    if TUNEL_PASS:
        password = password.split(':')
        if len(password) != 2:
            raise Exception("wrong password parsing!")
        password = password[1]
    return password

def checkTunnelPassword(password, TUNEL_PASS):
    if TUNEL_PASS and password[0] != TUNEL_PASS:
        raise Exception("wrong password for tunnel!")


def get_password(whole_message):
    password = findall("PASS (.*?)(\r|\n)", whole_message)[0][0]
    return password


def get_nick(whole_message):
    nickname = findall("NICK (.*?)(\r|\n)", whole_message)[0][0]
    return nickname


def connect_to_onet(UOkey, nickname, sock):
    onet = socket(AF_INET, SOCK_STREAM)
    onet.bind((config['local_ip'], 0))
    onet.connect(("czat-app.onet.pl", 5015))
    send(sock, recv(onet, 1024))
    send(onet, "AUTHKEY\r\n")
    send(onet, "NICK " + nickname + "\r\n")
    send(onet, ("USER * " + UOkey + " czat-app.onet.pl :" + nickname + "\r\n"))
    authkey = auth(findall(":.*?801.*?:(.*?)\r", recv(onet, 1024))[0])
    send(onet, "AUTHKEY " + authkey + "\r\n")
    return onet


def mainLoop(client_socket, config):

    config['nickname'], config['password'] = receive_nickname_and_password(client_socket)

    try:
        checkTunnelPassword(config['password'],config['TUNEL_PASS'])
        config['password'] = splitPassword(config['password'], config['TUNEL_PASS'])
        config['UOkey'] = authorization(config['nickname'], config['password'])
    except Exception as e:
        print(e)
        client_socket.close()
        return

    onet_socket = connect_to_onet(config['UOkey'], config['nickname'], client_socket)

    send_welcome_messages(config, client_socket)
    while 1:
        (sockets_with_ready_messages, dw, de) = select.select([client_socket, onet_socket], [], [])
        for socket_with_ready_msg in sockets_with_ready_messages:
            if socket_with_ready_msg == client_socket:
                try:
                    received_message = recv(socket_with_ready_msg, 1024)
                    if received_message:
                        config['encode'] = get_proper_encoding(received_message, config['encode'])
                        received_message = applyEncoding(received_message, config['encode'], config['lemoty'])
                        config = handleMessageFromClient(received_message, config, onet_socket, client_socket)
                    else:
                        client_socket.close()
                        onet_socket.close()
                        break

                except Exception as e:
                    print(e)
                    client_socket.close()
                    onet_socket.close()

            if socket_with_ready_msg == onet_socket:
                received_message = ""
                try:
                    while 1:
                        chunk_of_received_msg = recv(socket_with_ready_msg, 1024)
                        if chunk_of_received_msg:
                            if chunk_of_received_msg[len(chunk_of_received_msg) - 1] == '\n':
                                received_message += chunk_of_received_msg
                                break
                        else:
                            client_socket.close()
                            onet_socket.close()
                            break
                        received_message += chunk_of_received_msg
                    handleMessageFromOnet(config, client_socket, received_message)
                except:
                    client_socket.close()
                    onet_socket.close()

##HERE COMES THE DRAGONS

client_socket = create_client_socket()
createSocketConnection(client_socket, config['port'], config['local_ip'])
client_socket.listen(5)

while 1:
    socket_accepted, cinfo = client_socket.accept()
    threading.Thread(target=mainLoop, args=[socket_accepted, config]).start()
client_socket.close()
