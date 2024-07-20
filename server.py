# server.py contains get request routines to serve YogonDexLite on a browser. Currently configured to run on an EC2 instance on AWS.
# usage: run using python3 server.py portnum. depending where the server is being executed access to YogonDexLite on a browser can be accessed in two ways. 1. If the server is being run locally you may access the application through the url localhost:58061/main.html. 2. If the server is run on an EC2 instance the application can be accessed through the instances public ip and port like the following url publicip:portnum/main.html.
import sys
import cgi
import os
import json
import logging

import pkquiz as pq

# web server parts
from http.server import HTTPServer, BaseHTTPRequestHandler

# used to parse the URL and extract form data for GET requests
from urllib.parse import urlparse, parse_qs, parse_qsl, unquote

logging.basicConfig(level=logging.INFO)

# handler for our web-server - handles both GET and POST requests
class MyHandler( BaseHTTPRequestHandler ):

    #service get requests
    def do_GET(self):

        parsed  = urlparse( self.path )

        # give main as default
        if parsed.path in [ '/' ]:

            try:
                self.path = '/main.html'

                fp = open( '.'+self.path )
                content = fp.read()

                self.send_response( 200 )
                self.send_header( "Content-type", "text/html" )
                self.send_header( "Content-length", len( content ) )
                self.end_headers()

                self.wfile.write( bytes( content, "utf-8" ) )
                fp.close()
            except FileNotFoundError:
                self.send_error(404, "File Not Found: %s" % self.path)
            except BrokenPipeError:
                logging.error("Broken pipe error while writing response to client.")
            except Exception as e:
                logging.error(f"Unexpected error: {e}") 

        # give main
        elif parsed.path in [ '/main.html' ]:

            try:
                fp = open( '.'+self.path )
                content = fp.read()

                self.send_response( 200 )
                self.send_header( "Content-type", "text/html" )
                self.send_header( "Content-length", len( content ) )
                self.end_headers()

                self.wfile.write( bytes( content, "utf-8" ) )
                fp.close()
            except FileNotFoundError:
                self.send_error(404, "File Not Found: %s" % self.path)
            except BrokenPipeError:
                logging.error("Broken pipe error while writing response to client.")
            except Exception as e:
                logging.error(f"Unexpected error: {e}") 

        elif parsed.path.endswith(".getquestion"):

            try:

                if "mono" in parsed.path:
                    if "cycle" in parsed.path:
                        cycle = int(parsed.path.split('.')[2])
                        content = pq.askCycleMono(cycle)
                    else:
                        content = pq.askWeakMono()
                else:
                    if "cycle" in parsed.path:
                        cycle = int(parsed.path.split('.')[2])
                        content = pq.askCycleDual(cycle)
                    else:
                        content = pq.askWeakDual()

                print("CONTENT", content)

                content = json.dumps(content)

                self.send_response( 200 )
                self.send_header( "Content-type", "application/json" )
                self.send_header( "Content-length", len(content.encode('utf-8')) )
                self.end_headers()

                self.wfile.write( bytes( content, "utf-8" ) )

            except FileNotFoundError:
                self.send_error(404, "File Not Found: %s" % self.path)
            except BrokenPipeError:
                logging.error("Broken pipe error while writing response to client.")
            except Exception as e:
                logging.error(f"Unexpected error: {e}") 

        #otherwise 404
        else:
            self.send_response( 404 )
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

    #I never need to use post so i dont, keeping it simple
    def do_POST(self):

        parsed = urlparse( self.path )

        self.send_response( 404 )
        self.end_headers()
        self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )

#main
if __name__ == "__main__":

    #overhead


    #start server
    httpd = HTTPServer( ( '0.0.0.0', int(sys.argv[1]) ), MyHandler )
    print( "Server listing in port:  ", int(sys.argv[1]) )
    httpd.serve_forever()