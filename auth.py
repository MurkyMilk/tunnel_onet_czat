from http_fetching import get_http


def auth(s):
    stringbuffer = ""
    i_list = range(16)
    ai = []
    help = []
    f1 = [
        29, 43, 7, 5, 52, 58, 30, 59, 26, 35,
        35, 49, 45, 4, 22, 4, 0, 7, 4, 30,
        51, 39, 16, 6, 32, 13, 40, 44, 14, 58,
        27, 41, 52, 33, 9, 30, 30, 52, 16, 45,
        43, 18, 27, 52, 40, 52, 10, 8, 10, 14,
        10, 38, 27, 54, 48, 58, 17, 34, 6, 29,
        53, 39, 31, 35, 60, 44, 26, 34, 33, 31,
        10, 36, 51, 44, 39, 53, 5, 56
    ]
    f2 = [
        7, 32, 25, 39, 22, 26, 32, 27, 17, 50,
        22, 19, 36, 22, 40, 11, 41, 10, 10, 2,
        10, 8, 44, 40, 51, 7, 8, 39, 34, 52,
        52, 4, 56, 61, 59, 26, 22, 15, 17, 9,
        47, 38, 45, 10, 0, 12, 9, 20, 51, 59,
        32, 58, 19, 28, 11, 40, 8, 28, 6, 0,
        13, 47, 34, 60, 4, 56, 21, 60, 59, 16,
        38, 52, 61, 44, 8, 35, 4, 11
    ]
    f3 = [
        60, 30, 12, 34, 33, 7, 15, 29, 16, 20,
        46, 25, 8, 31, 4, 48, 6, 44, 57, 16,
        12, 58, 48, 59, 21, 32, 2, 18, 51, 8,
        50, 29, 58, 6, 24, 34, 11, 23, 57, 43,
        59, 50, 10, 56, 27, 32, 12, 59, 16, 4,
        40, 39, 26, 10, 49, 56, 51, 60, 21, 37,
        12, 56, 39, 15, 53, 11, 33, 43, 52, 37,
        30, 25, 19, 55, 7, 34, 48, 36
    ]
    p1 = [
        11, 9, 12, 0, 1, 4, 10, 13, 3,
        6, 7, 8, 15, 5, 2, 14
    ]
    p2 = [
        1, 13, 5, 8, 7, 10, 0, 15, 12, 3,
        14, 11, 2, 9, 6, 4
    ]

    if len(s) < 16:
        return "(key to short)"

    for c in s:
        if c > '9':
            if c > 'Z':
                ai.append((ord(c) - 97) + 36)
            else:
                ai.append((ord(c) - 65) + 10)
        else:
            ai.append(ord(c) - 48)

    for i in i_list:
        ai[i] = f1[ai[i] + i]

    for i in i_list:
        help.insert(i, (ai[i] + ai[p1[i]]) % 62)
    ai = help

    for i in i_list:
        ai[i] = f2[ai[i] + i]

    help = []
    for i in i_list:
        help.insert(i, (ai[i] + ai[p2[i]]) % 62)
    ai = help

    for i in i_list:
        ai[i] = f3[ai[i] + i]

    for j in ai:
        if j >= 10:
            if j >= 36:
                stringbuffer += chr((97 + j) - 36)
            else:
                stringbuffer += chr((65 + j) - 10)
        else:
            stringbuffer += chr(48 + j)

    return stringbuffer


def authorization(nickname, password):
    Cookie = "Cookie:"
    Cookie += get_http("kropka.onet.pl",
                       "GET /_s/kropka/1?DV=czat/applet/FULL HTTP/1.1\r\n" \
                       "Host: kropka.onet.pl\r\n" \
                       "Connection: keep-alive\r\n\r\n")
    Cookie += get_http("czat.onet.pl",
                       "GET /myimg.gif HTTP/1.1\r\n" \
                       "Host: czat.onet.pl\r\n" + Cookie + "\r\n\r\n")
    POST = "api_function=getUoKey&params=a:3:{" \
           "s:4:\"nick\";s:%d:\"%s\";" \
           "s:8:\"tempNick\";i:%d;" \
           "s:7:\"version\";s:22:\"1.1(20110425-2020 - R)\";}"
    if nickname[0] == '~':
        POST = POST % (len(nickname) - 1, nickname[1:], 1)
    else:
        POST = POST % (len(nickname), nickname, 0)
        POST_s = "r=&url=&login=%s&haslo=%s&app_id=20&ssl=1&ok=1" % (nickname, password)
        POST_OVERRIDE = "api_function=userOverride&params=a:3:{s:4:\"nick\";s:%d:\"%s\";}" % (len(nickname), nickname)
        get_http("secure.onet.pl",
                 "POST /mlogin.html HTTP/1.1\r\n" \
                 "Content-Type: application/x-www-form-urlencoded\r\n" \
                 "Content-Length: %d\r\n" \
                 "Cache-Control: no-cache\r\n" \
                 "Pragma: no-cache\r\n" \
                 "User-Agent: Mozilla/4.0 (Windows NT 5.0)\r\n" \
                 "Host: secure.onet.pl\r\n" \
                 "Connection: keep-alive\r\n" \
                 "%s\r\n\r\n" \
                 "%s" % (len(POST_s), Cookie, POST_s), 0, 1)
        get_http("czat.onet.pl",
                 "POST /include/ajaxapi.xml.php3 HTTP/1.1\r\n" \
                 "Content-Type: application/x-www-form-urlencoded\r\n" \
                 "Content-Length: %d\r\n" \
                 "Cache-Control: no-cache\r\n" \
                 "Pragma: no-cache\r\n" \
                 "User-Agent: Mozilla/4.0 (Windows NT 5.0)\r\n" \
                 "Host: czat.onet.pl\r\n" \
                 "Accept: text/html, image/gif, image/jpeg, *; q=.2, */*;" \
                 "q=.2\r\n" \
                 "Connection: close\r\n" \
                 "%s\r\n\r\n" \
                 "%s" % (len(POST_OVERRIDE), Cookie, POST_OVERRIDE), 1)

    uoKey = \
        get_http("czat.onet.pl",
                 "POST /include/ajaxapi.xml.php3 HTTP/1.1\r\n" \
                 "Content-Type: application/x-www-form-urlencoded\r\n" \
                 "Content-Length: %d\r\n" \
                 "Cache-Control: no-cache\r\n" \
                 "Pragma: no-cache\r\n" \
                 "User-Agent: Mozilla/4.0 (Windows NT 5.0)\r\n" \
                 "Host: czat.onet.pl\r\n" \
                 "Accept: text/html, image/gif, image/jpeg, *; q=.2, */*;" \
                 "q=.2\r\n" \
                 "Connection: close\r\n" \
                 "%s\r\n\r\n" \
                 "%s" % (len(POST), Cookie, POST), 1)
    return uoKey
