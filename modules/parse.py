import urllib

class Parse:
    def __init__(self):
        pass

    def URI2query(self, request):
        """
        Takes an HTTP request and splits to
        -request
        -query represented as dictionary
        Query split:
            Example - "123?var1=value1&var2=value2" => {"var1":"value1", "var2:"value2"}

        Resources:
        http://www.w3.org/Protocols/rfc1341/4_Content-Type.html

        :return: requested file, vars
        """
        request = urllib.unquote(request).decode('utf8')  # Decode the Percent-encoding
        slitted = str(request).split("?", 1)
        URI = slitted[0]
        dic = {}
        if len(slitted) > 1:  # If there is query split the parameters else keep empty
            query = slitted[1].split("&")
            for pair in query:
                var = pair.split("=")
                if var[0] not in dic:
                    dic.update({var[0]: var[1]})
        return URI, dic

    def headers2dict(self, headers):
        """
        Receive headers and
        :param headers:
        :return:
        """
        headers = headers.split("\r\n")[:-1]
        return dict([(x.split(":", 1)[0].strip(), x.split(":", 1)[1].strip()) for x in headers if x.index(": ")])

    def query2table(self, query):
        data = '<table border="1">' \
               '<tr>' \
               '<th>parameter</th><th>value</th>' \
               '</tr>'
        for pair in query:
            data += "<tr>"
            data +="<td>{}</td><td>{}</td>".format(pair, query[pair])
            data += "</tr>"
        data += '</table>'
        return data