import socket

def main():
    for _ in range(10):
        # HOST = socket.gethostbyname("www.ynet.co.il")
        HOST = "localhost"
        print HOST
        sock = socket.socket()
        sock.connect((HOST, 8080))
        print "Connected..."
        sock.sendall("GET /index.html ")
        print "Sent 'GET'..."
        for _ in range(10):
            sock.send("HTTP/1.1\r\n")
        print "Sent Long"
        # print sock.recv(8096)
        # sock.close()

if __name__ == '__main__':
    main()