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
    form += '''<form method='POST' enctype='multipart/form-data' action='/restaurants'>
                <h2>What's the name of the restaurant?</h2>
                <input name="restaurant_name" type="text" >
                <input type="submit" value="Submit"> </form>'''

    return form

def build_del_restaurant_form(id):
    """
    Build a form for adding a deleting a restaurant from the database

    Args: String - id of the restaurant to delete
    """

    current_name = db_command.get_restaurant(int(id)).name

    form = ''
    form += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/delete'>
                <h2>Hit submit to delete {}</h2>
                <input type="hidden" name="restaurant_id" type="text" value="'''.format(current_name)
    form += str(id)            
    form += '''"><input type="submit" value="Submit"> </form>'''

    return form

def build_update_restaurant_form(id):
    """
    Build a form for adding a updating a restaurant from the database

    Args: String - Name of the restaurant TODO: format this like other function code headings
    """
    current_name = db_command.get_restaurant(int(id)).name
    form = ''
    form += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/update'>
                <h2>Make your name change:</h2>
                <input name="restaurant_id" type="hidden" value="'''
    form += id
    form += '''"><input name="restaurant_name" type="text" value="'''
    form += current_name
    form += '''">
                <input type="submit" value="Submit"> </form>'''

    return form

def path_parser(self):
    """
    Purpose: Figure out the purpose of the path
    """

    primary_path = self.path.partition('/')[2]
    dir1 = primary_path.partition('/')[0]
    action_path = primary_path.partition('/')[2]
    id = action_path.partition('/')[0]
    action = action_path.partition('/')[2]
    return dir1,id,action

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
                output = ""
                output += "<html><body>"                
                if self.path.endswith("/restaurants"):
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

                    output += "<h2> Restaurant Added:</h2>"
                    output += "<h3> %s </h3>" % restaurant_name
                    output += build_new_restaurant_form()
                    output += restaurants_views.restaurant_list(db_command.get_all_restaurants())
                    # pdb.set_trace()
                    print(output)

                elif self.path.endswith("/restaurant/delete"):
                    try:
                        restaurant_id = fields.get('restaurant_id')[0]
                        print(restaurant_id)
                        db_command.delete_restaurant(int(restaurant_id)) 
                        output += "<h3> Restaurant " + restaurant_id + " deleted.</h3>"    

                    except:
                        print("Wasn't able to get the restaurant ID or delete it without error")
                        output += "<h3> Wasn't able to get the restaurant ID or delete it without error:"
                        output += "<br> ID: " + restaurant_id + " not deleted.</h3>"
                        pass

                elif self.path.endswith("/restaurant/update"):
                    try:
                        restaurant_id = fields.get('restaurant_id')[0]
                        # print(restaurant_id)
                        restaurant_name = fields.get('restaurant_name')[0]
                        # print(restaurant_name)
                        print("Trying to update restaurant id : " + str(restaurant_id) )
                        db_command.update_restaurant(int(restaurant_id), restaurant_name) 
                        output += "<h3> Restaurant " + str(restaurant_id) + " updated with name: "
                        output += str(restaurant_name) + ".</h3>"    

                    except:
                        print("Wasn't able to get the restaurant ID or update it without error")
                        output += "<h3> Wasn't able to get the restaurant ID or update it without error:"
                        output += "<br> ID: " + restaurant_id + " not updated.</h3>"
                        pass

                elif self.path.endswith("/hello"):
                    messagecontent = fields.get('message[0]')
                    output += "  <h2> Okay, this:</h2>"
                    output += "<h1> %s </h1>" % messagecontent[0]
                    output += build_form()
                    
                else:
                    output += "  <h2> Okay, this:</h2>"
                    output += "<h1> %s </h1>" % "Hmm, we go lost..."
                    output += build_form()


            # pdb.set_trace()
            output += "</body></html>"

            self.wfile.write(output)
            print("Made it...\n")
        except:
            print("Problem")
            # pdb.set_trace()
            pass

    def do_GET(self):




        try:
            
            #parse the path to figure out what to do
            path = path_parser(self)
            action = path[2]
            id = path[1]
            obj = path[0]

            # Send the headers as long as it makes sense ???
            # if obj != '':
                # self.send_response(200)
                # self.send_header('Content-type', 'text/html')
                # self.end_headers()

            output = ""
            output += "<html><body>"

            if action == 'edit':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # form to edit an item
                output += build_update_restaurant_form(id)


            elif action == 'delete':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                # form to delete an item
                output += build_del_restaurant_form(id)
            
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

            
                output += "<h1> Hello to you! </h1>"
                output += build_form()
                

                # self.wfile.write(output)
                # print(output)
                # return

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
                # self.wfile.write(output)
                # print(output)
                # return

            elif self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += restaurants_views.restaurant_list(db_command.get_all_restaurants())
                output += "</body></html>"

                # self.wfile.write(output)
                # print(output)
                # return        
            
            elif self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Hello to you! </h1>"
                output += build_new_restaurant_form()
                output += "</body></html>"

                # self.wfile.write(output)
                # print(output)
                # return

            elif self.path.endswith("/restaurant/delete"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = db_command.get_all_restaurants()
                output = ""
                output += "<html><body>"
                output += "<h1>They come and they go! </h1>"
                output += build_del_restaurant_form(str(restaurants[0].res_id)) # TODO this no longer makes sense the 1 is a bandaid
                output += restaurants_views.restaurant_list(restaurants)
                output += "</body></html>"

                # self.wfile.write(output)
                # print(output)
                # return

            elif self.path.endswith("/restaurant/update"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                restaurants = db_command.get_all_restaurants()
                output = ""
                output += "<html><body>"
                output += "<h1>Change is fine! </h1>"
                output += build_update_restaurant_form(str(restaurants[0].res_id)) # TODO this no longer makes sense. the 1 is a bandaid
                output += restaurants_views.restaurant_list(restaurants)
                output += "</body></html>"

            # Wrap up the output, and send
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
