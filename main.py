#!/usr/bin/env python

############### CONFIG ###############
import threading

from auth import auth, authorization
from encoding import applyEncoding

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
from re import findall, sub
import time
from time import ctime
import select

import sys

wersja = sys.version[0] + sys.version[2]
if (wersja <= ""):
    pass
else:
    pass

print("onettunel.py v.2010-04 / by Olo (2008-2010) unix.onlinewebshop.net")
print("poprawki Husar, 08-07-2011\r\n\r\n")
if (realname == ""):
    realname = ""
if color == 1:
    print("Wlaczona obsluga kolorow")
else:
    print("Wylaczona obsluga kolorow")
if bold == 1: print("Wlaczona obsluga pogrubienia czcionki")
if encoding == 1: print("Wlaczona obsluga kodowania CP1250")

def send(s, msg):
    s.send(msg.encode("utf-8"))

def get_date():
    sys.stdout.write("[%s] = " % ctime())


if len(sys.argv) == 2:
    BindPort = int(sys.argv[1])
else:
    BindPort = port


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
        get_date()
        my_err = "[%3d] ERROR: sprawdz swoje polaczenie sieciowe z internetem, poprawnosc wprowadzonego hasla i nicka lub dostepnosc serwerow onet.pl (zmiany autoryzacji)\r\n" % ID
        sys.stdout.write(my_err)
        sock.send(str.encode(my_err))
        sock.close()
        return
    sockets = []
    sockets.append(sock)
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
                    get_date()
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
                    get_date()
                    print("[%3d] nick: %s = blad odczytu/zapisu z/do gniazda", (ID, nickname))
                    end = 1
                    break
        if end == 1:
            sock.close()
            onet.close()
            break


def process_message_from_client(UOkey, bufor, encode, lbold, lemoty, lkolor, nickname, onet, sock, tmpb):
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
                    send(sock, "onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
            elif tmpb[1] == "kodowanie":
                try:
                    encode = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 1 i 0\r\n")
            elif tmpb[1] == "bold":
                try:
                    lbold = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 1 i 0\r\n")
            elif tmpb[1] == "emoty":
                try:
                    lemoty = int(tmpb[2][0])
                except:
                    send(sock, "onettunel.py - dozwolone wartosci: 2, 1 i 0\r\n")
        except:
            pass
            send(sock, (":fake.host 666 nik : 10[Tunel] ustawienia polaczenia:\r\n"
                        ":fake.host 666 nik : 10[Tunel]  kolor:5     %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  kodowanie:5 %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  bold:5      %d\r\n"
                        ":fake.host 666 nik : 10[Tunel]  emoty:5     %d\r\n") % (
                     lkolor, encode, lbold, lemoty))
    elif tmpb[0] == "LIST":
        bufor = "SLIST\r\n"
    elif (tmpb[0] == "PROTOCTL"):
        bufor = bufor.replace("NAMESX", "ONETNAMESX")
    elif tmpb[0] == "CAM":
        if tmpb[3][:2] == "on":
            cammsg = ":WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " + tmpb[1] + "\r\n"
        if tmpb[3][:3] == "off":
            cammsg = ":WebcamServ!service@service.onet MODE " + tmpb[2] + " -Cam " + tmpb[1] + "\r\n"
        if encode == 1:
            cammsg = cammsg.replace('\xa1', '\xa5')
            cammsg = cammsg.replace('\xb1', '\xb9')
            cammsg = cammsg.replace('\xa6', '\x8c')
            cammsg = cammsg.replace('\xb6', '\x9c')
            cammsg = cammsg.replace('\xac', '\x8f')
            cammsg = cammsg.replace('\xbc', '\x9f')
        if encode == 2:
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
    return encode, lbold, lemoty, lkolor


def parse_and_send_incomining_message(encode, lbold, lemoty, lkolor, nickname, sock, tab):
    for line in tab:
        if encode == 1:
            line = line.replace('\xa1', '\xa5')
            line = line.replace('\xb1', '\xb9')
            line = line.replace('\xa6', '\x8c')
            line = line.replace('\xb6', '\x9c')
            line = line.replace('\xac', '\x8f')
            line = line.replace('\xbc', '\x9f')
        if encode == 2:
            line = line.replace("\xa1", "\xc4\x84")
            line = line.replace("\xc6", "\xc4\x86")
            line = line.replace("\xca", "\xc4\x98")
            line = line.replace("\xa3", "\xc5\x81")
            line = line.replace("\xd1", "\xc5\x83")
            line = line.replace("\xd3", "\xc3\x93")
            line = line.replace("\xa6", "\xc5\x9a")
            line = line.replace("\xac", "\xc5\xb9")
            line = line.replace("\xaf", "\xc5\xbb")
            line = line.replace("\xb1", "\xc4\x85")
            line = line.replace("\xe6", "\xc4\x87")
            line = line.replace("\xea", "\xc4\x99")
            line = line.replace("\xb3", "\xc5\x82")
            line = line.replace("\xf1", "\xc5\x84")
            line = line.replace("\xf3", "\xc3\xb3")
            line = line.replace("\xb6", "\xc5\x9b")
            line = line.replace("\xbc", "\xc5\xba")
            line = line.replace("\xbf", "\xc5\xbc")
        if lkolor == 1:
            line = line.replace("%C959595%", '\x03' + "14")
            line = line.replace("%C990033%", '\x03' + "05")
            line = line.replace("%Cc86c00%", '\x03' + "07")
            line = line.replace("%C623c00%", '\x03' + "05")
            line = line.replace("%Cce00ff%", '\x03' + "13")
            line = line.replace("%Ce40f0f%", '\x03' + "04")
            line = line.replace("%C3030ce%", '\x03' + "12")
            line = line.replace("%C008100%", '\x03' + "03")
            line = line.replace("%C1a866e%", '\x03' + "10")
            line = line.replace("%C006699%", '\x03' + "11")
            line = line.replace("%C8800ab%", '\x03' + "06")
            line = line.replace("%C0f2ab1%", '\x03' + "02")
            line = line.replace("%Cff6500%", '\x03' + "07")
            line = line.replace("%Cff0000%", '\x03' + "04")
        if lbold == 1:
            line = sub("%Fb.*?%", '\x02', line)
        line = sub("%C[a-fA-F0-9]{6}%", '', line)
        line = line.replace("%C%", '')
        line = sub("%F.?.?:[a-z]+%", '', line)
        line = sub("%F[bi]{0,2}%", '', line)
        if lemoty == 1:
            tmpb = line.split(' ')
            if tmpb[1] != "353":
                b = findall("(%I(.+?)%)", line)
                for c in b:
                    line = line.replace(c[0], "<" + c[1] + ">")
        elif lemoty == 2:
            tmpb = line.split(' ')
            if tmpb[1] != "353":
                b = findall("(%I(.+?)%)", line)
                for c in b:
                    line = line.replace(c[0], "//" + c[1])
        try:
            tmpb = line.split(' ')
            if tmpb[1] == "PRIVMSG":
                if tmpb[2][0] == '^':
                    tmpb[2] = tmpb[2].replace('^', '#^')
                    line = ' '.join(tmpb)

            elif tmpb[1] == "MODERMSG":
                line = "%s PRIVMSG %s :MODERMSG %s: %s" % (
                    tmpb[0], tmpb[4], tmpb[2], ' '.join(tmpb[5:])[1:])
            elif tmpb[1] == "MODERNOTICE":
                line = "%s PRIVMSG %s :MODERNOTICE: %s" % (tmpb[0], tmpb[2], ' '.join(tmpb[3:])[1:])



            elif tmpb[1] == "JOIN":
                if tmpb[2][0] == '^':
                    line = line.replace('^', '#^')
                elif tmpb[3][:2] == ':W':
                    tmpb[3] = sub(",[0-3]\r\n", '', tmpb[3])
                    if tmpb[3][:3] == ":Wr":
                        line = tmpb[3].replace(":Wrx", tmpb[0] + " " + tmpb[1] + " " + tmpb[
                            2] + "\r\n:WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " +
                                               tmpb[0][1:].split('!')[0] + "\r\n")
                    elif tmpb[3][:4] == ":Wbr":
                        line = tmpb[3].replace(":Wbrx", tmpb[0] + " " + tmpb[1] + " " + tmpb[
                            2] + "\r\n:WebcamServ!service@service.onet MODE " + tmpb[2] + " +Cam " +
                                               tmpb[0][1:].split('!')[0] + "\r\n")
            elif tmpb[1] == "MODE":
                if tmpb[3][:2] == "+W":
                    line = tmpb[0] + " 2010 :CAM " + tmpb[2] + " on\r\n"
                elif tmpb[3][:2] == "-W":
                    line = tmpb[0] + " 2010 :CAM " + tmpb[2] + " off\r\n"
            elif tmpb[1] == "353":
                if tmpb[4][0] == '^':
                    tmpb[4] = tmpb[4].replace('^', '#^')
                    line = ' '.join(tmpb)
                if line.find('|') != -1:
                    tmpstr = ""
                    a1 = line.split(':')
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
                    line = ':'.join(a1) + "\r\n"
            elif tmpb[1] == "366":
                if tmpb[3][0] == '^':
                    tmpb[3] = tmpb[3].replace('^', '#^')
                    line = ' '.join(tmpb)
            elif tmpb[1] == "341":
                if tmpb[4][0] == '^':
                    tmpb[4] = tmpb[4].replace('^', '#^')
                    line = ' '.join(tmpb)
            elif tmpb[1] == "NOTICE":
                if tmpb[2][0] == '^':
                    tmpb[2] = tmpb[2].replace('^', '#^')
                    line = ' '.join(tmpb)
            elif tmpb[1] == "PART":
                if tmpb[2][0] == '^':
                    tmpb[2] = tmpb[2].replace('^', '#^')
                    line = ' '.join(tmpb)
            elif tmpb[1] == "INVITE":
                if tmpb[3][1] == '^':
                    tmpb[3] = tmpb[3].replace('^', '#^')
                    line = ' '.join(tmpb)
            elif tmpb[1] == "817":
                line = ":_-_!name@host.org PRIVMSG %s :%s <%s> %s" % (
                    tmpb[3], time(tmpb[4]), tmpb[5], ' '.join(tmpb[7:]))
            elif tmpb[1] == "819":
                onethost = tmpb[0]
                tab3 = findall("(#.+?):.:(\d+)", line)
                for room in tab3:
                    send(sock, "%s 322 %s %s %s :\r\n" % (onethost, nickname, room[0], room[1]))
                line = ""
            elif tmpb[1] == "820":
                line = "%s 323 %s :End of LIST\r\n" % (tmpb[0], nickname)
            elif tmpb[1] == "421":
                line = line.replace(" MODE :This command has been disabled.", '')
                line = line.replace(" SETS :Unknown command", '')
                line = line.replace(" CAM :Unknown command", '')
                line = line.replace(" UO :Unknown command", '')
            elif tmpb[1] == "005":
                line = line.replace(" PREFIX=(qaohXYv)`&@%!=+ ", ' PREFIX=(CqaohXv)=`&@%!+ ')
        except:
            pass
        if line != "":
            send(sock, line)


def set_proper_encoding(bufor, encode, sock):
    if bufor.find("NOTICE") != -1 and bufor.find("VERSION") != -1:
        if bufor.find("mIRC v6") != -1:
            encode = 1
        elif bufor.find("mIRC v7") != -1:
            encode = 2
        else:
            encode = 0
        sock.send(
            (":fake.host 666 nik : 10[Tunel] ustawiono typ kodowania:5                %d\r\n") % (
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
        (":fake.host 666 nik : 10[Tunel] /sets emoty 0 10<---5 010: %Ihihi%,5 110: <hihi>,5 210: //hihi\r\n")))


s = socket(AF_INET, SOCK_STREAM)
try:
    s.bind(('', BindPort))
except Exception as e:
    print(e)
    get_date()
    print("ERROR: nie mozna zabindowac portu %s, wybierz inny BindPort")
    s.close()
    sys.exit()
get_date()
if local_ip != '':
    print("server:  + $local_ip + $BindPort")
else:
    print("server:" + str(gethostbyname(gethostname())) + str(BindPort))
s.listen(5)
cID = 1
while 1:
    c, cinfo = s.accept()
    get_date()
    sys.stdout.write("[%3d] %s:%s = " % ((cID,) + cinfo))

    threading.Thread(target=init,
                     args=(c, cID)
                     ).start()
    cID = cID + 1
s.close()