import sys
from const import Const

const = Const()


class Log:
    def __init__(self, log=True, debug=False, colors=False):
        self.log_s = log
        self.d_status = debug
        self.colors = colors

    def Log(self, msg):
        if self.colors:
            colors = {"d": '\033[96m', "i": "\033[92m", "e": '\033[91m'}
            if msg.find("[") + 1:
                msg = colors[msg[msg.find("[") + 1]] + msg + '\033[0m'
        sys.stdout.write(msg)

    def server_info(self, PORT=const.PORT, ROOT=const.ROOT,
                    default_page=const.default_page, max_threads=const.max_threads):
        msg = ''
        if self.log_s:
            msg += "[d]Server Port - {}\n".format(const.ADDRESS[1])
            msg += "[d]Server Root Directory  - {}\n".format(const.ROOT)
            msg += "[d]Server Default Page - {}\n".format(default_page)
            msg += "[d]Server Max Threads - {}\n".format(max_threads)
        self.Log(msg)

    def server_start(self, PORT=const.PORT):
        msg = ''
        if self.log_s:
            msg += "[i]Server Starting time - {}\n".format(const.time_stamp())
            msg += "[i]Server Running ... {}\n".format(PORT)
        self.Log(msg)

    def request(self, request, c):
        msg = ''
        request = ''.join(request)
        if self.log_s:
            split = request.split("\r\n")
            headers = split[:-1]
            data = split[-1]
            msg += "[d] ID {} : Request Line: {}\n".format(c.ID, headers[0])
            msg += "[d] ID {} : Full Request:\n".format(c.ID)
            for line in headers:
                msg += "\t[d] {} {}\n".format(line, "[CRLF]")
            self.debug("Data" + data, 1)
        self.Log(msg)

    def response(self, response, c):
        msg = ''
        if self.log_s:
            msg += "[d] ID {} : Responding:\n".format(c.ID)
            headers = response.split("\r\n\r\n")[0].split("\r\n")
            for line in headers:
                msg += "\t[d] {} {}\n".format(line, "[CRLF]")
        self.Log(msg)

    def new_connection(self, c):
        msg = ''
        if self.log_s:
            msg += "[i] Connection from {}:{} With ID {}\n".format(c.addr[0], c.addr[1], c.ID)
        self.Log(msg)

    def debug(self, msg, level=0):
        msg = ''
        if self.d_status:
            msg = msg.splitlines()
            for line in msg:
                msg += "{}[debug] {}\n".format("\t" * level, line)
        self.Log(msg)