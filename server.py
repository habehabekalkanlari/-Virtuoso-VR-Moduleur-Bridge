import http.server, socketserver
PORT=8000
Handler=http.server.SimpleHTTPRequestHandler
print("Open http://localhost:8000")
with socketserver.TCPServer(("",PORT),Handler) as httpd:
 httpd.serve_forever()
