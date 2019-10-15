import os
import http.server
import socketserver

def serve(directory, host, port):
    os.chdir(directory)
    handler = http.server.SimpleHTTPRequestHandler
    server = socketserver.TCPServer((host, port), handler)
    print(f'Serving on http://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nClosing server.')
    server.server_close()
