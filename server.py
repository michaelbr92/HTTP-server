#!/usr/local/bin/python

import socket
import re
import os
import threading
import sys
# =============================
# Code starts here
# =============================

class HTTP():

    def receive(self, conn):
        """ Receive the request from the client

        Go through the request components
        read them and check validation
        if not valid return None

        Sourse: RFC 2616
        url: http://www.w3.org/Protocols/rfc2616/rfc2616-sec5.html

        :param conn: Client socket
        :return: None or Request components
        """
        methods = ["OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]

        # Method (Read\Check)
        method = ""
        for _ in xrange(7):
            method += conn.recv(1)
            # Log.Log("[e]" + method + "\n")
            if method[-1:] == ' ': break
        if method.strip() not in methods:
            return None

        # URI (Read\Check)
        URI = ""
        while True:
            URI += conn.recv(1)
            if URI[-1] == ' ': break

        # Version (Read\Check)
        version = ""
        for _ in xrange(10):
            version += conn.recv(1)
            if version[-2:] == "\r\n": break
        re_version = re.compile("HTTP/\d\.\d\r\n")
        if not re_version.match(version):
            return None

        # Headers (Read\Check)
        headers = ""
        while True:
            headers += conn.recv(1)
            if headers == "\r\n" or headers[-4:] == "\r\n\r\n":
                headers = headers[:-2]
                break
        Valid_header = re.compile(r"\S+:\s+\S+")
        for header in headers.split("\r\n")[:-1]:
            if not Valid_header.match(header):
                return None
        # Data (Read\Check)
        data = ''
        if method in ["POST ", "PUT "]:
            if "Transfer-Encoding: chunked" in headers:
                data = ""
                while True:
                    length = ''
                    while length[-2:] != "\r\n":
                        length += conn.recv(1)
                    length = length[:-2]
                    data += conn.recv(length + 2).replace("\r\n", "")
                    if not length: break

            elif "Content-Length:" in headers:
                SPLIT_LENGTH = re.compile(r"Content-Length:\s*(\d+)\s*\r\n")
                data_len = int(SPLIT_LENGTH.findall(headers)[0].strip())
                data = conn.recv(data_len)

        return method, URI, version, headers, data

    def receive_new(self, conn): # TODO: Change the receiving function
        methods = ["OPTIONS", "GET", "HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]
        # Method (Read\Check)
        method = ""
        for _ in xrange(7):
            method += conn.recv(1)
            # Log.Log("[e]" + method + "\n")
            if method[-1:] == ' ': break
        if method.strip() not in methods:
            return None

    def __init__(self, conn):
        """
        Receive a request from the client
        if request matches the HTTP pattern
            split it

        :type self: object
        :param conn:
        """

        self.request = self.receive(conn)
        # Split the request if HTTP Request
        self.valid = bool(self.request)
        if self.valid:
            self.method, \
            self.URI, \
            self.version, \
            self.headers, \
            self.data = self.request

            self.method = self.method.strip()
            self.URI = self.URI.strip()

            self.PATH, self.query = Parse.URI2query(self.URI)
            self.headers = Parse.headers2dict(self.headers)  # Parse the headers to a dictionary

            self.custom_redirection = {"/params_info.html": Parse.query2table}

    def handle_request(self, method=""): # TODO Finish the rest of the handler
        """
        Handle the request
        :param method: request method
        :return: the popper response
        """
        if not method: method = self.method

        if method in ["GET", "POST", "HEAD"]:
            # add the parameters in the data to the query if method is POST
            if method == "POST" and self.data:
                parameters = self.data.split("&")
                for pair in parameters:
                    var = pair.split("=")
                    if var[0] not in self.query:
                        self.query.update({var[0]: var[1]})
            # prepare the filename and path
            request_file = self.PATH.replace('/', Const.DIR_SPLITTER)
            path = (os.getcwd() + request_file)
            filename = os.path.split(path)[1]

            if self.PATH in self.custom_redirection:
                data = self.custom_redirection[self.PATH](self.query)
                response = Responses.OK(data)

            elif os.path.isfile(path):
                if filename in Const.FORBIDDEN_FILES:
                    response = Responses.Forbidden()
                else:
                    response = Responses.OK(path)

            else:
                if filename in Const.MOVED_FILES:
                    response = Responses.MOVED(filename)
                else:
                    response = Responses.NOT_FOUND()

            if method == "HEAD":
                response = response.split("\r\n\r\n")[0] + "\r\n\r\n"

            return response


    def Respond(self):
        """
        Returns a response
        if not implemented yet
            sends 501 response
        if method available
            call it from the method dictionary
        :return:
        """

        # Methods dictionary
        self.methods = {"GET": self.GET, "HEAD": self.HEAD, "TRACE": self.TRACE,
                        "OPTIONS": self.OPTIONS, "POST": self.POST}
        if not self.valid:
            return Responses.Bad_Request()
        if self.method in self.methods:
            return self.methods[self.method]()
        else:
            return Responses.Not_implemented()

    def GET(self):
        """
        Handle the 'GET' method
        :return:
        """
        request_file = self.PATH.replace('/', Const.DIR_SPLITTER)  # Change the slashes to fit the OS
        path = (os.getcwd() + request_file)  # Add CWD to the path
        filename = os.path.split(path)[1]  # Split the file name from the tail and take the file name

        if self.PATH in self.custom_redirection:
            data = self.custom_redirection[self.PATH](self.query)
            response = Responses.OK(data)
        elif os.path.isfile(path):
            # Check if the file exists

            if filename in Const.FORBIDDEN_FILES:
                response = Responses.Forbidden()
            else:
                response = Responses.OK(path)
        else:
            if filename in Const.MOVED_FILES:
                response = Responses.MOVED(filename)
            else:
                response = Responses.NOT_FOUND()

        return response

    def HEAD(self):
        """
        Uses GET and removes the data section
        """
        response = self.GET().split("\r\n\r\n")[0] + "\r\n\r\n"
        return response

    def POST(self):
        """
        Splits the parameters from the data
        combines them with the URL query
        :return:
        """
        parameters = self.data.split("&")
        for pair in parameters:
            var = pair.split("=")
            if var[0] not in self.query:
                self.query.update({var[0]: var[1]})
        data = self.custom_redirection[self.PATH](self.query)
        return Responses.OK(data)

    def TRACE(self):
        return Responses.OK(self.request)

    def OPTIONS(self):
        available = ""
        for method in self.methods:
            available += method + ","
        available = available[:-1]
        response = "HTTP/1.1 200 OK\r\n" \
                   "Allow: {}\r\n" \
                   "\r\n".format(available)
        return response


class Client(threading.Thread):
    ID = 0  # ID counter
    available_ID = []  # List of old ID not in use

    def __init__(self, server_socket):
        """
        Create a client connection from welcome socket
        Add an ID to the client
        (if old ID not in use take him)

        LOG: about the new connection

        :param server_socket:
        :return:
        """
        threading.Thread.__init__(self)
        self.conn, self.addr = server_socket.accept()
        if Client.available_ID:
            self.ID = Client.available_ID.pop()
        else:
            self.ID = Client.ID + 1
            Client.ID += 1
        Log.new_connection(self)

    def run(self):
        self.HandleRequest()
        self.__del__()

    def HandleRequest(self):
        """
        Handle the request if valid call response
        else call 400 Bad_request response
        and send it to the client

        Log: the response

        :return: The request
        """
        HTTP_request = HTTP(self.conn)  # Create an HTTP request class
        if HTTP_request.valid:
            Log.request(HTTP_request.request, self)  # Log the connection
        else:
            Log.Log("[d] Bad request from {}:{}\n".format(self.addr[0], self.addr[1]))
        if HTTP_request.valid:
            response = HTTP_request.Respond()
        else:
            response = Responses.Bad_Request()

        Log.response(response, self)
        self.conn.send(response)
        return HTTP_request

    def __del__(self):
        Client.available_ID.append(self.ID)
        self.conn.close()
        del self


def d_main():
    from modules.const import Const as const
    from modules.log import Log as log
    from modules.parse import Parse as parse
    from modules.responses import Responses as responses

    global Const, Log, Parse, Responses

    Const = const()
    os.chdir(Const.ROOT)
    Log = log(log=True, debug=False, colors=True)
    Parse = parse()
    Responses = responses()

    # Create a socket and bind it
    server_socket = socket.socket()
    server_socket.bind(Const.ADDRESS)
    server_socket.listen(Const.max_threads)
    Log.server_info()
    Log.server_start()
    threads = []
    while True:
        if threading.activeCount() <= Const.max_threads:
            c = Client(server_socket)
            threads.append(c)
            c.start()


def main():
    """ Creates a new socket and searches for clients

    """
    from modules.const import Const as const
    from modules.log import Log as log
    from modules.parse import Parse as parse
    from modules.responses import Responses as responses

    global Const, Log, Parse, Responses

    Const = const()
    Log = log(log=True, debug=False, colors=True)
    Parse = parse()
    Responses = responses()

    # Create a socket and bind it

    server_socket = socket.socket()
    try:
        server_socket.bind(Const.ADDRESS)
    except Exception as e:
        Log.Log("[e]{}\n".format(str(e)))
        sys.exit()
    server_socket.listen(Const.max_threads)
    # Log the server info and starting msg
    Log.server_info()
    Log.server_start()

    while True:
        try:
            c = Client(server_socket)
            threading.Thread(target=c.run).run()
        except Exception as e:
            Log.Log("[e]" + str(e) + "\n")


if __name__ == '__main__':
    d_main()
