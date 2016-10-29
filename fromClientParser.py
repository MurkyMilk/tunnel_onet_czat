from util import send


def transform_message_from_client(UOkey, bufor, config , onet, sock, tmpb):
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
        send(sock, ":fake.host 2012 " + config['nickname'] + " : 10[Tunel] Twoj UOkey: " + UOkey + "\r\n")
    elif tmpb[0][:4] == "SETS":
        try:
            if tmpb[1] == "kolor":
                try:
                    config['lkolor'] = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
            elif tmpb[1] == "kodowanie":
                try:
                    config['encode'] = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 1 i 0\r\n")
            elif tmpb[1] == "bold":
                try:
                    config['lbold'] = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 1 i 0\r\n")
            elif tmpb[1] == "emoty":
                try:
                    config['lemoty'] = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
        except:
            pass
            send(sock, (":fake.host 666 nik : 10[Tunel] ustawienia polaczenia:\r\n"
                        ":fake.host 666 nik : 10[Tunel]  kolor:5     %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  kodowanie:5 %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  bold:5      %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  emoty:5     %d\r\n") % (
                config['lkolor'], config['encode'], config['lbold'], config['lemoty']))
    elif tmpb[0] == "LIST":
        bufor = "SLIST\r\n"
    elif tmpb[0] == "PROTOCTL":
        bufor = bufor.replace("NAMESX", "ONETNAMESX")
    elif tmpb[0] == "CAM":
        if tmpb[3][:2] == "on":
            cammsg = ":WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " + tmpb[1] + "\r\n"
        if tmpb[3][:3] == "off":
            cammsg = ":WebcamServ!service@service.onet MODE " + tmpb[2] + " -Cam " + tmpb[1] + "\r\n"
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
            send(sock, cammsg)
    send(onet, bufor)
    return config
