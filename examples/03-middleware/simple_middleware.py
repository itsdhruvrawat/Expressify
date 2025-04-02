"""
Simple HTTP server with middleware functionality

This is a basic HTTP server that implements middleware pattern for handling requests.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
from datetime import datetime
import os
import urllib.parse
import sys
import traceback

# Configuration
HOST = "127.0.0.1"
PORT = 3001

# Set up basic logging
def log(message):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}")
    sys.stdout.flush()  # Force output to be written immediately

log("Starting server initialization")

# Ensure the public directory exists
PUBLIC_DIR = "public"
os.makedirs(PUBLIC_DIR, exist_ok=True)
log(f"Public directory ensured at: {os.path.abspath(PUBLIC_DIR)}")

# Create some test files if they don't exist
if not os.path.exists(os.path.join(PUBLIC_DIR, "index.html")):
    log("Creating index.html")
    with open(os.path.join(PUBLIC_DIR, "index.html"), "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Middleware Demo</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #0066cc; }
        .container { max-width: 800px; margin: 0 auto; }
        .route { background: #f4f4f4; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .method { display: inline-block; padding: 3px 6px; border-radius: 3px; color: white; font-size: 12px; margin-right: 10px; }
        .get { background-color: #61affe; }
        .post { background-color: #49cc90; }
        .protected { border-left: 4px solid #ff6b6b; padding-left: 10px; }
        code { background: #eee; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Middleware Demo</h1>
        <p>This example demonstrates middleware functionality in a simple HTTP server.</p>
        
        <h2>Available Routes</h2>
        <div class="route">
            <span class="method get">GET</span> <a href="/">/</a> - Home page
        </div>
        <div class="route">
            <span class="method get">GET</span> <a href="/about">/about</a> - About page
        </div>
        <div class="route">
            <span class="method get">GET</span> <a href="/api">/api</a> - API endpoint
        </div>
        <div class="route protected">
            <span class="method get">GET</span> <a href="/protected">/protected</a> - Protected route (requires API key)
            <div>Header: <code>X-API-Key: abc123</code></div>
        </div>
        <div class="route">
            <span class="method get">GET</span> <a href="/public/test.html">/public/test.html</a> - Static file
        </div>
        <div class="route">
            <span class="method post">POST</span> <a href="/echo">/echo</a> - Echo API (use curl or Postman)
        </div>
        
        <h2>Middleware Functionality</h2>
        <ul>
            <li><strong>Logger:</strong> Logs all requests with timing information</li>
            <li><strong>Authentication:</strong> Checks for API key on protected routes</li>
            <li><strong>Static Files:</strong> Serves files from the public directory</li>
            <li><strong>JSON Parser:</strong> Parses JSON request bodies</li>
        </ul>
    </div>
</body>
</html>
""")

if not os.path.exists(os.path.join(PUBLIC_DIR, "test.html")):
    log("Creating test.html")
    with open(os.path.join(PUBLIC_DIR, "test.html"), "w") as f:
        f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Static File Test</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>Static File Serving Works!</h1>
    <p>This file is being served from the <code>public</code> directory.</p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
""")

log("Test files created")

# Simple request and response objects
class Request:
    def __init__(self, handler):
        self.handler = handler
        self.method = handler.command
        self.path = handler.path.split('?')[0]
        self.headers = {k.lower(): v for k, v in handler.headers.items()}
        self.query = {}
        self.body = {}
        self.body_raw = ""
        
        # Parse query string
        if '?' in handler.path:
            query_string = handler.path.split('?', 1)[1]
            self.query = {k: v[0] for k, v in urllib.parse.parse_qs(query_string).items()}
        
        # Read and parse body if present
        content_length = int(self.headers.get('content-length', 0))
        if content_length > 0:
            body_data = handler.rfile.read(content_length).decode('utf-8')
            self.body_raw = body_data
            
            # Parse JSON body
            if 'application/json' in self.headers.get('content-type', ''):
                try:
                    self.body = json.loads(body_data)
                except:
                    self.body = {}
            # Parse form data
            elif 'application/x-www-form-urlencoded' in self.headers.get('content-type', ''):
                self.body = {k: v[0] for k, v in urllib.parse.parse_qs(body_data).items()}

class Response:
    def __init__(self, handler):
        self.handler = handler
        self.status_code = 200
        self.headers = {'Content-Type': 'text/html'}
    
    def status(self, code):
        self.status_code = code
        return self
    
    def set_header(self, name, value):
        self.headers[name] = value
        return self
    
    def json(self, data):
        self.headers['Content-Type'] = 'application/json'
        self.send(json.dumps(data))
        return self
    
    def send(self, content):
        self.handler.send_response(self.status_code)
        
        for name, value in self.headers.items():
            self.handler.send_header(name, value)
        
        self.handler.end_headers()
        
        if isinstance(content, str):
            self.handler.wfile.write(content.encode('utf-8'))
        elif isinstance(content, bytes):
            self.handler.wfile.write(content)
        
        return self
    
    def redirect(self, url):
        self.status(302)
        self.set_header('Location', url)
        self.send('')
        return self

log("Request and Response classes initialized")

# Middleware functions
def logger_middleware(req, res, next):
    """Log request details"""
    start_time = time.time()
    log(f"Request: {req.method} {req.path}")
    log(f"Headers: {req.headers}")
    
    if req.body:
        log(f"Body: {req.body}")
    
    result = next()
    
    end_time = time.time()
    duration = (end_time - start_time) * 1000  # Convert to ms
    log(f"Response: {res.status_code} - {duration:.2f}ms")
    
    return result

def auth_middleware(req, res, next):
    """Check for API key on protected routes"""
    if req.path.startswith('/protected'):
        api_key = req.headers.get('x-api-key')
        
        if not api_key:
            log("Auth failed: No API key provided")
            res.status(401).json({
                'error': 'Authentication required',
                'message': 'Missing API key. Please provide X-API-Key header.'
            })
            return res
        
        if api_key != 'abc123':
            log(f"Auth failed: Invalid API key: {api_key}")
            res.status(403).json({
                'error': 'Access denied',
                'message': 'Invalid API key'
            })
            return res
        
        log("Auth successful")
    
    return next()

def static_files_middleware(req, res, next):
    """Serve static files from the public directory"""
    if req.method == 'GET':
        # Special handling for root path
        if req.path == '/':
            file_path = os.path.join(PUBLIC_DIR, "index.html")
        # Serve files from public directory
        elif req.path.startswith('/public/'):
            file_path = os.path.join(os.getcwd(), req.path[1:])
        else:
            return next()
        
        log(f"Looking for file: {file_path}")
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            # Determine content type
            if file_path.endswith('.html'):
                content_type = 'text/html'
            elif file_path.endswith('.css'):
                content_type = 'text/css'
            elif file_path.endswith('.js'):
                content_type = 'application/javascript'
            elif file_path.endswith('.json'):
                content_type = 'application/json'
            elif file_path.endswith('.png'):
                content_type = 'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                content_type = 'image/jpeg'
            else:
                content_type = 'text/plain'
            
            # Read and send the file
            try:
                with open(file_path, 'rb') as f:
                    content = f.read()
                
                log(f"Serving file: {file_path}")
                res.status(200)
                res.set_header('Content-Type', content_type)
                res.send(content)
                return res
            except Exception as e:
                log(f"Error reading file: {e}")
        
    return next()

def routes_middleware(req, res, next):
    """Handle application routes"""
    if req.method == 'GET':
        if req.path == '/about':
            return res.send("""
<!DOCTYPE html>
<html>
<head>
    <title>About</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #0066cc; }
    </style>
</head>
<body>
    <h1>About Page</h1>
    <p>This is the about page of our middleware demo.</p>
    <p><a href="/">Back to Home</a></p>
</body>
</html>
""")
        elif req.path == '/api':
            return res.json({
                'message': 'API endpoint',
                'timestamp': datetime.now().isoformat()
            })
        elif req.path == '/protected':
            return res.json({
                'message': 'You have accessed a protected endpoint',
                'timestamp': datetime.now().isoformat()
            })
    elif req.method == 'POST':
        if req.path == '/echo':
            return res.json({
                'echo': req.body,
                'headers': req.headers,
                'timestamp': datetime.now().isoformat()
            })
    
    return next()

log("Middleware functions defined")

# Main HTTP request handler
class MiddlewareHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        log(f"Server log: {format % args}")
    
    def handle_error(self, e):
        log(f"Error handling request: {str(e)}")
        log("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        try:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'error': 'Internal Server Error',
                'message': str(e)
            }).encode('utf-8'))
        except:
            log("Error sending error response")
    
    def do_GET(self):
        try:
            log(f"Handling GET request for {self.path}")
            self.process_request()
        except Exception as e:
            self.handle_error(e)
        
    def do_POST(self):
        try:
            log(f"Handling POST request for {self.path}")
            self.process_request()
        except Exception as e:
            self.handle_error(e)
        
    def do_PUT(self):
        try:
            log(f"Handling PUT request for {self.path}")
            self.process_request()
        except Exception as e:
            self.handle_error(e)
        
    def do_DELETE(self):
        try:
            log(f"Handling DELETE request for {self.path}")
            self.process_request()
        except Exception as e:
            self.handle_error(e)
    
    def process_request(self):
        log("Processing request")
        # Create request and response objects
        req = Request(self)
        res = Response(self)
        
        # Create middleware chain
        middleware_chain = [
            logger_middleware,
            auth_middleware,
            static_files_middleware,
            routes_middleware
        ]
        
        # Function to execute middleware chain
        def execute_middleware(index=0):
            if index < len(middleware_chain):
                return middleware_chain[index](req, res, lambda: execute_middleware(index + 1))
            else:
                # End of middleware chain, return 404
                res.status(404).json({
                    'error': 'Not Found',
                    'message': f'No route found for {req.method} {req.path}'
                })
                return res
        
        # Execute middleware chain
        log("Executing middleware chain")
        execute_middleware()
        log("Middleware chain execution completed")

log("MiddlewareHandler class defined")

def run_server():
    """Start the HTTP server"""
    try:
        log(f"Creating HTTP server on {HOST}:{PORT}")
        server = HTTPServer((HOST, PORT), MiddlewareHandler)
        log(f"Server created successfully at http://{HOST}:{PORT}")
        
        log("Starting server...")
        server.serve_forever()
    except KeyboardInterrupt:
        log("Keyboard interrupt received, shutting down")
    except Exception as e:
        log(f"Error starting server: {str(e)}")
        log("".join(traceback.format_exception(type(e), e, e.__traceback__)))
    finally:
        log("Server stopped")
        try:
            server.server_close()
            log("Server closed successfully")
        except Exception as e:
            log(f"Error closing server: {str(e)}")

log("Server runner function defined")

if __name__ == "__main__":
    try:
        log("\nMiddleware Demo Server")
        log("=====================")
        log(f"Server running at http://{HOST}:{PORT}")
        
        log("\nAvailable Routes:")
        log(f"  - GET  http://{HOST}:{PORT}/             - Home page")
        log(f"  - GET  http://{HOST}:{PORT}/about        - About page")
        log(f"  - GET  http://{HOST}:{PORT}/api          - API endpoint")
        log(f"  - GET  http://{HOST}:{PORT}/protected    - Protected route (requires API key)")
        log(f"  - GET  http://{HOST}:{PORT}/public/test.html - Static file")
        log(f"  - POST http://{HOST}:{PORT}/echo         - Echo API")
        
        log("\nAPI Key for testing protected routes:")
        log("  Header: X-API-Key: abc123")
        
        # Run the server
        log("Calling run_server function")
        run_server()
    except Exception as e:
        log(f"Unhandled exception: {str(e)}")
        log("".join(traceback.format_exception(type(e), e, e.__traceback__)))
        sys.exit(1) 