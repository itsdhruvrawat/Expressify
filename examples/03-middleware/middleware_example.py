"""
Middleware Example for Expressify

This example demonstrates how to use middleware in Expressify applications
to handle common tasks like logging, authentication, and error handling.
"""

from expressify import Expressify, Request, Response
import time
import json
from functools import wraps

# Create the application
app = Expressify()

# Middleware functions

def logger_middleware(req, res, next):
    """Log request information and timing data"""
    start_time = time.time()
    
    print(f"Request: {req.method} {req.path}")
    
    # Call the next middleware/route handler
    result = next()
    
    # Calculate and log timing
    duration = (time.time() - start_time) * 1000  # Convert to ms
    print(f"Response: {res.status_code} - {duration:.2f}ms")
    
    return result

def cors_middleware(req, res, next):
    """Add CORS headers to enable cross-origin requests"""
    # Set CORS headers
    res.set_header('Access-Control-Allow-Origin', '*')
    res.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    res.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    # Handle OPTIONS requests for CORS preflight
    if req.method == 'OPTIONS':
        return res.status(204).send()
    
    # Call the next middleware/route handler
    return next()

def json_parser_middleware(req, res, next):
    """Parse JSON request bodies"""
    if 'application/json' in req.get_header('content-type', ''):
        try:
            if req.body:
                req.json = json.loads(req.body)
        except json.JSONDecodeError:
            return res.status(400).json({
                'error': 'Invalid JSON',
                'message': 'Failed to parse request body as JSON'
            })
    
    # Call the next middleware/route handler
    return next()

def auth_middleware(req, res, next):
    """Check for API key on protected routes"""
    if req.path.startswith('/protected'):
        api_key = req.get_header('x-api-key')
        
        if not api_key:
            return res.status(401).json({
                'error': 'Authentication required',
                'message': 'Missing API key. Please provide X-API-Key header.'
            })
        
        if api_key != 'abc123':
            return res.status(403).json({
                'error': 'Access denied',
                'message': 'Invalid API key'
            })
    
    # Call the next middleware/route handler
    return next()

def error_handler_middleware(req, res, next):
    """Handle errors in the middleware chain"""
    try:
        # Call the next middleware/route handler
        return next()
    except Exception as e:
        print(f"Error: {str(e)}")
        return res.status(500).json({
            'error': 'Internal Server Error',
            'message': str(e)
        })

# Apply middleware to all routes
app.use(logger_middleware)
app.use(cors_middleware)
app.use(json_parser_middleware)
app.use(auth_middleware)
app.use(error_handler_middleware)

# Define routes

@app.get('/')
def home(req, res):
    return res.send("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify Middleware Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
            ul { list-style-type: square; }
            .route { background: #f4f4f4; padding: 10px; margin-bottom: 10px; border-radius: 5px; }
            code { background: #eee; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
        </style>
    </head>
    <body>
        <h1>Expressify Middleware Demo</h1>
        <p>This example demonstrates how to use middleware in Expressify applications.</p>
        
        <h2>Available Routes</h2>
        <div class="route"><a href="/about">/about</a> - About page</div>
        <div class="route"><a href="/api/data">/api/data</a> - API endpoint</div>
        <div class="route"><a href="/protected/data">/protected/data</a> - Protected route (requires API key)</div>
        
        <h2>Active Middleware</h2>
        <ul>
            <li><b>Logger:</b> Logs all requests with timing information</li>
            <li><b>CORS:</b> Adds Cross-Origin Resource Sharing headers</li>
            <li><b>JSON Parser:</b> Automatically parses JSON request bodies</li>
            <li><b>Auth:</b> Requires API key for protected routes</li>
            <li><b>Error Handler:</b> Catches errors and returns formatted responses</li>
        </ul>
    </body>
    </html>
    """)

@app.get('/about')
def about(req, res):
    return res.send("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>About - Middleware Demo</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
        </style>
    </head>
    <body>
        <h1>About Middleware</h1>
        <p>Middleware functions are functions that have access to the request object (req), 
        the response object (res), and the next middleware function in the application's 
        request-response cycle.</p>
        
        <p>Middleware can:</p>
        <ul>
            <li>Execute any code</li>
            <li>Make changes to the request and response objects</li>
            <li>End the request-response cycle</li>
            <li>Call the next middleware in the stack</li>
        </ul>
        
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """)

@app.get('/api/data')
def api_data(req, res):
    return res.json({
        'message': 'This is data from the API',
        'timestamp': time.time()
    })

@app.post('/api/data')
def api_post_data(req, res):
    # The JSON parser middleware will have already parsed the JSON body
    if hasattr(req, 'json'):
        return res.status(201).json({
            'message': 'Data received successfully',
            'data': req.json
        })
    else:
        return res.status(400).json({
            'error': 'No data provided',
            'message': 'Request body should contain JSON data'
        })

@app.get('/protected/data')
def protected_data(req, res):
    # The auth middleware will have already verified the API key
    return res.json({
        'message': 'This is protected data',
        'timestamp': time.time()
    })

# Route-specific middleware example
def validate_id(req, res, next):
    """Validate that the id parameter is a number"""
    try:
        user_id = int(req.params.get('id'))
        if user_id <= 0:
            return res.status(400).json({
                'error': 'Invalid ID',
                'message': 'ID must be a positive number'
            })
    except (ValueError, TypeError):
        return res.status(400).json({
            'error': 'Invalid ID',
            'message': 'ID must be a number'
        })
    
    # Call the next middleware/route handler
    return next()

# Apply route-specific middleware
@app.get('/user/:id', [validate_id])
def get_user(req, res):
    user_id = int(req.params.get('id'))
    
    # Example user data
    user = {
        'id': user_id,
        'name': 'User ' + str(user_id),
        'email': f'user{user_id}@example.com'
    }
    
    return res.json(user)

# Creating middleware with decorators
def require_auth(api_key='abc123'):
    """Decorator to require authentication for a specific route"""
    def decorator(handler):
        @wraps(handler)
        def wrapped_handler(req, res):
            # Check for API key
            if req.get_header('x-api-key') != api_key:
                return res.status(401).json({
                    'error': 'Authentication required',
                    'message': 'Invalid or missing API key'
                })
            
            # Call the original handler
            return handler(req, res)
        return wrapped_handler
    return decorator

# Apply decorator middleware
@app.get('/admin/dashboard')
@require_auth(api_key='admin123')
def admin_dashboard(req, res):
    return res.json({
        'message': 'Admin dashboard',
        'sensitive_data': 'This is sensitive data that requires authentication'
    })

# Start the server
if __name__ == '__main__':
    app.listen(3001, '127.0.0.1')
    print(f"Server running at http://127.0.0.1:3001")
    print("\nAvailable routes:")
    print("  - GET  /                 - Home page")
    print("  - GET  /about            - About page")
    print("  - GET  /api/data         - API endpoint")
    print("  - POST /api/data         - API endpoint (accepts JSON)")
    print("  - GET  /protected/data   - Protected route (requires x-api-key: abc123)")
    print("  - GET  /user/:id         - User data (with ID validation)")
    print("  - GET  /admin/dashboard  - Admin route (requires x-api-key: admin123)")
    print("\nActive middleware:")
    print("  - Logger middleware")
    print("  - CORS middleware")
    print("  - JSON parser middleware")
    print("  - Auth middleware")
    print("  - Error handler middleware") 