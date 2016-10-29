

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
        ":fake.host 666 nik : 10[Tunel] /sets emoty 0 10<---5 010: %Ihihi%,5 110: <hihi>,5 210: //hihi\r\n"))


def printWelcomeInfo(color, bold, encoding):
    print("onettunel.py v.2010-04 / by Olo (2008-2010) unix.onlinewebshop.net")
    print("poprawki Husar, 08-07-2011\r\n\r\n")
    if color == 1:
        print("Wlaczona obsluga kolorow")
    else:
        print("Wylaczona obsluga kolorow")
    if bold == 1: print("Wlaczona obsluga pogrubienia czcionki")
    if encoding == 1: print("Wlaczona obsluga kodowania CP1250")