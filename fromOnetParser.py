import time
from re import sub, findall




def tranform_message_from_onet(config, sock, splitted_msg):
    from util import send
    for line in splitted_msg:
        if  config['encode'] == 1:
            line = applyEncoding1(line)
        if  config['encode'] == 2:
            line = applyEncoding2(line)
        if config['lkolor'] == 1:
            line = applyEncoding3(line)
        if config['lbold'] == 1:
            line = sub("%Fb.*?%", '\x02', line)
        line = sub("%C[a-fA-F0-9]{6}%", '', line)
        line = line.replace("%C%", '')
        line = sub("%F.?.?:[a-z]+%", '', line)
        line = sub("%F[bi]{0,2}%", '', line)
        line = applyEmoticons(config['lemoty'], line)
        try:
            splitted_line = line.split(' ')
            if splitted_line[1] == "PRIVMSG":
                if splitted_line[2][0] == '^':
                    splitted_line[2] = splitted_line[2].replace('^', '#^')
                    line = ' '.join(splitted_line)

            elif splitted_line[1] == "MODERMSG":
                line = "%s PRIVMSG %s :MODERMSG %s: %s" % (
                    splitted_line[0], splitted_line[4], splitted_line[2], ' '.join(splitted_line[5:])[1:])
            elif splitted_line[1] == "MODERNOTICE":
                line = "%s PRIVMSG %s :MODERNOTICE: %s" % (splitted_line[0], splitted_line[2], ' '.join(splitted_line[3:])[1:])



            elif splitted_line[1] == "JOIN":
                line = parse_JOIN(line, splitted_line)
            elif splitted_line[1] == "MODE":
                line = parse_MODE(line, splitted_line)
            elif splitted_line[1] == "353":
                if splitted_line[4][0] == '^':
                    splitted_line[4] = splitted_line[4].replace('^', '#^')
                    line = ' '.join(splitted_line)
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
            elif splitted_line[1] == "366":
                if splitted_line[3][0] == '^':
                    splitted_line[3] = splitted_line[3].replace('^', '#^')
                    line = ' '.join(splitted_line)
            elif splitted_line[1] == "341":
                if splitted_line[4][0] == '^':
                    splitted_line[4] = splitted_line[4].replace('^', '#^')
                    line = ' '.join(splitted_line)
            elif splitted_line[1] == "NOTICE":
                if splitted_line[2][0] == '^':
                    splitted_line[2] = splitted_line[2].replace('^', '#^')
                    line = ' '.join(splitted_line)
            elif splitted_line[1] == "PART":
                if splitted_line[2][0] == '^':
                    splitted_line[2] = splitted_line[2].replace('^', '#^')
                    line = ' '.join(splitted_line)
            elif splitted_line[1] == "INVITE":
                if splitted_line[3][1] == '^':
                    splitted_line[3] = splitted_line[3].replace('^', '#^')
                    line = ' '.join(splitted_line)
            elif splitted_line[1] == "817":
                line = ":_-_!name@host.org PRIVMSG %s :%s <%s> %s" % (
                    splitted_line[3], time(splitted_line[4]), splitted_line[5], ' '.join(splitted_line[7:]))
            elif splitted_line[1] == "819":
                onethost = splitted_line[0]
                tab3 = findall("(#.+?):.:(\d+)", line)
                for room in tab3:
                    send(sock, "%s 322 %s %s %s :\r\n" % (onethost, config['nickname'], room[0], room[1]))
                line = ""
            elif splitted_line[1] == "820":
                line = "%s 323 %s :End of LIST\r\n" % (splitted_line[0], config['nickname'])
            elif splitted_line[1] == "421":
                line = line.replace(" MODE :This command has been disabled.", '')
                line = line.replace(" SETS :Unknown command", '')
                line = line.replace(" CAM :Unknown command", '')
                line = line.replace(" UO :Unknown command", '')
            elif splitted_line[1] == "005":
                line = line.replace(" PREFIX=(qaohXYv)`&@%!=+ ", ' PREFIX=(CqaohXv)=`&@%!+ ')
        except:
            pass
        if line != "":
            send(sock, line)


def parse_MODE(line, splitted_line):
    if splitted_line[3][:2] == "+W":
        line = splitted_line[0] + " 2010 :CAM " + splitted_line[2] + " on\r\n"
    elif splitted_line[3][:2] == "-W":
        line = splitted_line[0] + " 2010 :CAM " + splitted_line[2] + " off\r\n"
    return line


def parse_JOIN(line, tmpb):
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
    return line


def applyEmoticons(lemoty, line):
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
    return line


def applyEncoding3(line):
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
    return line


def applyEncoding2(line):
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
    return line


def applyEncoding1(line):
    line = line.replace('\xa1', '\xa5')
    line = line.replace('\xb1', '\xb9')
    line = line.replace('\xa6', '\x8c')
    line = line.replace('\xb6', '\x9c')
    line = line.replace('\xac', '\x8f')
    line = line.replace('\xbc', '\x9f')
    return line