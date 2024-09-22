import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/assign_stand"):
            # Parse the URL parameters
            parsed_path = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed_path.query)
            airport_icao = params.get('airport', [None])[0]
            aircraft_type = params.get('type', [None])[0]

            if airport_icao and aircraft_type:
                # Query the database
                conn = sqlite3.connect('airports.db')
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT stand_number FROM BayStands
                    WHERE airport_icao = ? AND aircraft_type = ?
                """, (airport_icao, aircraft_type))
                stands = cursor.fetchall()
                conn.close()

                if stands:
                    assigned_stand = stands[0][0]  # Get the first available stand
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'assigned_stand': assigned_stand}).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'No stands available for this type.')
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid request.')

        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
