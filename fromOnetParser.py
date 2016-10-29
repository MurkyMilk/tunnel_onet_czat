import time
from re import sub, findall




def parse_and_send_incomining_message(encode, lbold, lemoty, lkolor, nickname, sock, tab):
    from util import send
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