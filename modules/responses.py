import mimetypes
import os
from const import Const
const = Const()

class Responses():
    def __init__(self):
        pass

    @staticmethod
    def Headers():
        """
        Some Headers
        :return:
        """
        headers = "Server: Misha's (X-platform)\r\n"
        return headers

    def Create(self, status, headers='',data ="", Type ="text/html", version="HTTP/1.1"):
        response = ""
        response += "{} {}\r\n".format(version, status)
        response += self.Headers()
        response += headers
        response += "Content-Type: {}\r\n".format(Type)
        if len(data):
            response += "Content-Length: {}\r\n\r\n{}".format(len(data), data)
        return response

    def OK(self, msg, mime="text/html" ):
        """
        Assemble the OK 200 response
        if given a path
            Guess the MIME
            Read file

        :return:
        """

        status = "200 OK"

        if os.path.exists(str(msg)):
            msg = open(msg, "rb").read()  # Read the file in bytes
            filename = os.path.split(msg)[1]  # splitting the file name from the path
            mime = mimetypes.guess_type(filename)[0]  # Guess the MIME
        else:
            msg = ''.join(msg)
        response = self.Create(status=status, data=msg, Type=mime)
        return response

    def Forbidden(self):
        status = "403 Forbidden"
        msg = "403 Forbidden"
        response = self.Create(status, data=msg)
        return response

    def MOVED(self, filename):
        status = "302 Found"
        headers = "Location: {}\r\n".format(const.MOVED_FILES[filename])
        response = self.Create(status, headers=headers)
        return response

    def NOT_FOUND(self):
        status = "404 Not found"
        msg = "404 Not found"
        response = self.Create(status, data=msg)
        return response

    def Bad_Request(self):
        status = "400 Bad Request"
        msg = "400 Bad Request"
        response = self.Create(status, data=msg)
        return response

    def Not_implemented(self):
        status = "501 Not implemented"
        msg = "501 Not implemented"
        response = self.Create(status, data=msg)
        return response