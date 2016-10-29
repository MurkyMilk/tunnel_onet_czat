from re import findall


def applyEncoding(bufor, encode, lemoty):
    if encode == 1:
        bufor = bufor.replace('\xa5', '\xa1')
        bufor = bufor.replace('\xb9', '\xb1')
        bufor = bufor.replace('\x8c', '\xa6')
        bufor = bufor.replace('\x9c', '\xb6')
        bufor = bufor.replace('\x8f', '\xac')
        bufor = bufor.replace('\x9f', '\xbc')
    elif encode == 2:
        bufor = bufor.replace("\xc4\x84", "\xa1")
        bufor = bufor.replace("\xc4\x86", "\xc6")
        bufor = bufor.replace("\xc4\x98", "\xca")
        bufor = bufor.replace("\xc5\x81", "\xa3")
        bufor = bufor.replace("\xc5\x83", "\xd1")
        bufor = bufor.replace("\xc3\x93", "\xd3")
        bufor = bufor.replace("\xc5\x9a", "\xa6")
        bufor = bufor.replace("\xc5\xb9", "\xac")
        bufor = bufor.replace("\xc5\xbb", "\xaf")
        bufor = bufor.replace("\xc4\x85", "\xb1")
        bufor = bufor.replace("\xc4\x87", "\xe6")
        bufor = bufor.replace("\xc4\x99", "\xea")
        bufor = bufor.replace("\xc5\x82", "\xb3")
        bufor = bufor.replace("\xc5\x84", "\xf1")
        bufor = bufor.replace("\xc3\xb3", "\xf3")
        bufor = bufor.replace("\xc5\x9b", "\xb6")
        bufor = bufor.replace("\xc5\xba", "\xbc")
        bufor = bufor.replace("\xc5\xbc", "\xbf")
    bufor = bufor.replace('\x03' + "14", "%C959595%")
    bufor = bufor.replace('\x03' + "5", "%C990033%")
    bufor = bufor.replace('\x03' + "7", "%Cc86c00%")
    bufor = bufor.replace('\x03' + "5", "%C623c00%")
    bufor = bufor.replace('\x03' + "13", "%Cce00ff%")
    bufor = bufor.replace('\x03' + "4", "%Ce40f0f%")
    bufor = bufor.replace('\x03' + "12", "%C3030ce%")
    bufor = bufor.replace('\x03' + "3", "%C008100%")
    bufor = bufor.replace('\x03' + "10", "%C1a866e%")
    bufor = bufor.replace('\x03' + "11", "%C006699%")
    bufor = bufor.replace('\x03' + "6", "%C8800ab%")
    bufor = bufor.replace('\x03' + "2", "%C0f2ab1%")
    bufor = bufor.replace('\x03' + "7", "%Cff6500%")
    bufor = bufor.replace('\x03' + "4", "%Cff0000%")
    if lemoty == 1:
        b = findall("(<(.+?)>)", bufor)
        for c in b:
            bufor = bufor.replace(c[0], "%I" + c[1] + "%")
    elif lemoty == 2:
        b = findall("(//(\w+))", bufor)
        for c in b:
            bufor = bufor.replace(c[0], "%I" + c[1] + "%")
    return bufor


def get_proper_encoding(bufor, encode):
    if bufor.find("NOTICE") != -1 and bufor.find("VERSION") != -1:
        if bufor.find("mIRC v6") != -1:
            encode = 1
        elif bufor.find("mIRC v7") != -1:
            encode = 2
        else:
            encode = 0
    return encode