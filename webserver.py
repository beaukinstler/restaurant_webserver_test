#!/usr/bin/python


from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi


def build_form():

    form = ''
    form += '''<form method='POST' enctype='multipart/form-data' action='/hello'>
                <h2>What would you like me to say?</h2>
                <input name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
    output = ''
    output += "<form method='POST' enctype='multipart/form-data' action='/hello'>"
    output += "<h2>What would you like me to say?</h2>"
    output += "<input name='message' type='text'>"
    output += "<input type='submit' value='Submit'> </form>"

    return form


class webserverHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "  <h2> Okay, this:</h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += build_form()
            output += "</body></html>"
            self.wfile.write(output)
            print(output)
        except:
            pass

    def do_GET(self):

        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Hello to you! </h1>"
                output += build_form()
                output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> &#161Hola to you! </h1>"
                output += "<a href=/hello>back to hello</a></body><html>"
                output += build_form()
                output += "</body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

        except:
            self.send_error(400, "File not found: %s" % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print("Running web server on port %s", port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^c detected, stopping server...")
        server.socket.close()


if __name__ == "__main__":
    main()
