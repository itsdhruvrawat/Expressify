"""
Simple HTTP server for testing middleware concepts
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os

# Configuration
HOST = "127.0.0.1"
PORT = 5000

# Ensure the public directory exists
PUBLIC_DIR = "public"
os.makedirs(PUBLIC_DIR, exist_ok=True)

# Create a simple HTML file for testing
with open(os.path.join(PUBLIC_DIR, "test.html"), "w") as f:
    f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Simple Test</title>
</head>
<body>
    <h1>It works!</h1>
    <p>This is a simple test page.</p>
</body>
</html>
""")

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            # Serve a simple home page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
<!DOCTYPE html>
<html>
<head>
    <title>Simple Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>Simple HTTP Server</h1>
    <p>Welcome to the simple HTTP server!</p>
    <ul>
        <li><a href="/test">Test Route</a></li>
        <li><a href="/api">API Route</a></li>
        <li><a href="/public/test.html">Static File</a></li>
    </ul>
</body>
</html>
""")
        elif self.path == '/test':
            # Return a simple text response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'This is a test route')
        elif self.path == '/api':
            # Return a JSON response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                'message': 'API route works!',
                'status': 'success'
            }
            self.wfile.write(json.dumps(response).encode('utf-8'))
        elif self.path.startswith('/public/'):
            # Serve a static file from the public directory
            file_path = os.path.join(os.getcwd(), self.path[1:])  # Remove leading /
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.send_response(200)
                
                # Determine content type based on file extension
                if file_path.endswith('.html'):
                    self.send_header('Content-type', 'text/html')
                elif file_path.endswith('.css'):
                    self.send_header('Content-type', 'text/css')
                elif file_path.endswith('.js'):
                    self.send_header('Content-type', 'application/javascript')
                else:
                    self.send_header('Content-type', 'text/plain')
                
                self.end_headers()
                
                # Read and send the file
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                # File not found
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            # Route not found
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')

def run_server():
    """Start the HTTP server"""
    server = HTTPServer((HOST, PORT), SimpleHandler)
    print(f"Server started at http://{HOST}:{PORT}")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        server.server_close()

if __name__ == "__main__":
    print("\nSimple HTTP Server")
    print("=================")
    print(f"Server running at http://{HOST}:{PORT}")
    print("\nAvailable Routes:")
    print(f"  - GET  http://{HOST}:{PORT}/             - Home page")
    print(f"  - GET  http://{HOST}:{PORT}/test         - Test route")
    print(f"  - GET  http://{HOST}:{PORT}/api          - API route")
    print(f"  - GET  http://{HOST}:{PORT}/public/test.html - Static file")
    
    # Run the server
    run_server() 