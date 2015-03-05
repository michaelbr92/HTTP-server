import socket
import os

while 1:
    HOST = raw_input("Host (blank if localhost): ")
    if not HOST:
        HOST = 'localhost'
    PORT = int(raw_input("PORT: "))
    s = socket.socket()
    s.connect((HOST, PORT))

    print "Connected to {}:{}- \n" \
          "Write the massage and add 'END' in the last line \n " \
          "('END' wont be part of the request)".format(HOST, PORT)
    request = ''
    while 1:
        line = raw_input(">")
        if "END" in line: break
        request += line + "\r\n"
    s.send(request)
    response = s.recv(4096)
    s.close()
    os.system(['clear', 'cls'][os.name == 'nt'])
    print response
    print "=================================="
    print "Sent & closing the connection!"
    print "=================================="