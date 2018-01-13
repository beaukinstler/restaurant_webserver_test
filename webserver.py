#!/usr/bin/python


from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi
import db_command
import restaurants_views
import pdb

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


def build_new_restaurant_form():
    """
    Build a form for adding a new restaurant to the database

    Args: String - Name of the restaurant TODO: format this like other function code headings
    """

    form = ''
    form += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>
                <h2>What's the name of the restaurant?</h2>
                <input name="restaurant_name" type="text" >
                <input type="submit" value="Submit"> </form>'''

    return form


class webserverHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            print(type(ctype))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                if self.path.endswith("/restaurant/new"):
                    # handle the restaurant add form
                    # print("made it here 02")
                    restaurant_name = fields.get('restaurant_name')
                    # print("made it here 03")
                    # pdb.set_trace()
                    print("Restaurant name: " + restaurant_name[0] )
                    id = db_command.add_restaurant(restaurant_name[0])
                    restaurant_name = str(db_command.get_restaurant(id).name)
                    # print("Restaurant name: " + str(restaurant_name[0]))
                    output = ""
                    output += "<html><body>"
                    output += "<h2> Restaurant Added:</h2>"
                    output += "<h3> %s </h3>" % restaurant_name
                    output += build_new_restaurant_form()
                    output += "</body></html>"
                    # pdb.set_trace()
                    print(output)

                elif self.path.endswith("/hello"):
                    messagecontent = fields.get('message[0]')
                    output = ""
                    output += "<html><body>"
                    output += "  <h2> Okay, this:</h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += build_form()
                    output += "</body></html>"

                else:
                    output = ""
                    output += "<html><body>"
                    output += "  <h2> Okay, this:</h2>"
                    output += "<h1> %s </h1>" % "Hmm, we go lost..."
                    output += build_form()
                    output += "</body></html>"

            # pdb.set_trace()
            self.wfile.write(output)
            print("Made it...\n")
        except:
            print("Problem")
            # pdb.set_trace()
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

            elif self.path.endswith("/hola"):
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

            elif self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                # output += "<html><body>"
                # output += "<h1> Restaurants: </h1>"
                output += restaurants_views.restaurant_list(db_command.get_all_restaurants())
                # output += "</body></html>"

                self.wfile.write(output)
                print(output)
                return        
            
            elif self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Hello to you! </h1>"
                output += build_new_restaurant_form()
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
