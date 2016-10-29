from util import send


def handleMessageFromClient(received_message, config, onet_socket, client_socket):
    splitted_msg = received_message.split(' ')
    if splitted_msg[0] == "PRIVMSG":
        if splitted_msg[1][0:2] == '#^':
            splitted_msg[1] = splitted_msg[1].replace('#^', '^')
            received_message = ' '.join(splitted_msg)
    elif (splitted_msg[0] == "JOIN") and (splitted_msg[1][0:2] == '#^'):
        splitted_msg[1] = splitted_msg[1].replace('#^', '^')
        received_message = ' '.join(splitted_msg)
    elif (splitted_msg[0] == "PART") and (splitted_msg[1][0:2] == '#^'):
        splitted_msg[1] = splitted_msg[1].replace('#^', '^')
        received_message = ' '.join(splitted_msg)
    elif (splitted_msg[0] == "INVITE") and (splitted_msg[2][0:2] == '#^'):
        splitted_msg[2] = splitted_msg[2].replace('#^', '^')
        received_message = ' '.join(splitted_msg)
    elif splitted_msg[0][:2] == "UO":
        pass
    elif splitted_msg[0][:4] == "SETS":
        try:
            if splitted_msg[1] == "kolor":
                try:
                    config['lkolor'] = int(splitted_msg[2][0])
                except:
                    send(client_socket, "onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
            elif splitted_msg[1] == "kodowanie":
                try:
                    config['encode'] = int(splitted_msg[2][0])
                except:
                    send(client_socket, "onettunel.py - dozwolone wartosci: 1 i 0\r\n")
            elif splitted_msg[1] == "bold":
                try:
                    config['lbold'] = int(splitted_msg[2][0])
                except:
                    send(client_socket, "onettunel.py - dozwolone wartosci: 1 i 0\r\n")
            elif splitted_msg[1] == "emoty":
                try:
                    config['lemoty'] = int(splitted_msg[2][0])
                except:
                    send(client_socket, "onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
        except:
            pass
            send(client_socket, (":fake.host 666 nik : 10[Tunel] ustawienia polaczenia:\r\n"
                        ":fake.host 666 nik : 10[Tunel]  kolor:5     %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  kodowanie:5 %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  bold:5      %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  emoty:5     %d\r\n") % (
                config['lkolor'], config['encode'], config['lbold'], config['lemoty']))
    elif splitted_msg[0] == "LIST":
        received_message = "SLIST\r\n"
    elif splitted_msg[0] == "PROTOCTL":
        received_message = received_message.replace("NAMESX", "ONETNAMESX")
    elif splitted_msg[0] == "CAM":
        if splitted_msg[3][:2] == "on":
            cammsg = ":WebcamServ!service@service.onet MODE " + splitted_msg[2] + " +Cam " + splitted_msg[1] + "\r\n"
        if splitted_msg[3][:3] == "off":
            cammsg = ":WebcamServ!service@service.onet MODE " + splitted_msg[2] + " -Cam " + splitted_msg[1] + "\r\n"
        if config['encode'] == 1:
            cammsg = cammsg.replace('\xa1', '\xa5')
            cammsg = cammsg.replace('\xb1', '\xb9')
            cammsg = cammsg.replace('\xa6', '\x8c')
            cammsg = cammsg.replace('\xb6', '\x9c')
            cammsg = cammsg.replace('\xac', '\x8f')
            cammsg = cammsg.replace('\xbc', '\x9f')
        if config['encode'] == 2:
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
            send(client_socket, cammsg)
    send(onet_socket, received_message)
    return config
