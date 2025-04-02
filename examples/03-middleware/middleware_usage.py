"""
Middleware Usage Example

This example demonstrates how to use middleware utilities with Expressify.
"""

from expressify import Expressify, Request, Response
import middleware_utils as mw
import os
import json

# Create the application
app = Expressify()

# Create a public directory for static files
os.makedirs("public/static", exist_ok=True)

# Create a sample static file
with open("public/static/style.css", "w") as f:
    f.write("""
/* Sample CSS file */
body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 20px;
    color: #333;
    background-color: #f5f5f5;
}

h1 {
    color: #0066cc;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.btn {
    display: inline-block;
    padding: 8px 16px;
    background: #0066cc;
    color: white;
    border-radius: 4px;
    text-decoration: none;
}

.btn:hover {
    background: #0052a3;
}
""")

# Apply global middleware
app.use(mw.logger("detailed"))  # Detailed logging
app.use(mw.cors())  # CORS with default settings
app.use(mw.json_parser())  # Parse JSON request bodies
app.use(mw.static_files("public", "max-age=3600"))  # Serve files from the public directory
app.use(mw.security_headers())  # Add security headers
app.use(mw.error_handler(include_stack_trace=True))  # Error handling

# Define a validation schema for user data
user_schema = {
    "body": {
        "name": {"required": True},
        "email": {"required": True}
    }
}

# Define a rate limiter for the API
api_rate_limiter = mw.rate_limiter(max_requests=5, window_seconds=10)

# Define routes

@app.get('/')
def home(req, res):
    return res.send("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Middleware Utilities Demo</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
        <div class="container">
            <h1>Middleware Utilities Demo</h1>
            <p>This example demonstrates how to use middleware utilities in Expressify.</p>
            
            <h2>Available Routes</h2>
            <ul>
                <li><a href="/api/public">/api/public</a> - Public API (no authentication required)</li>
                <li><a href="/api/protected">/api/protected</a> - Protected API (requires Bearer token)</li>
                <li><a href="/api/users">/api/users</a> - User API (with rate limiting and validation)</li>
                <li><a href="/test-error">/test-error</a> - Test error handling</li>
            </ul>
            
            <h2>Test API with curl</h2>
            <pre>
# Get public data
curl http://localhost:3001/api/public

# Access protected route (will fail without token)
curl http://localhost:3001/api/protected

# Access protected route with token
curl -H "Authorization: Bearer secret123" http://localhost:3001/api/protected

# Create a user (with validation)
curl -X POST -H "Content-Type: application/json" -d '{"name":"John","email":"john@example.com"}' http://localhost:3001/api/users

# Test rate limiting (call multiple times quickly)
curl http://localhost:3001/api/status

# Test error handling
curl http://localhost:3001/test-error
            </pre>
        </div>
    </body>
    </html>
    """)

@app.get('/api/public')
def api_public(req, res):
    return res.json({
        "message": "This is public data that anyone can access",
        "timestamp": req.timestamp
    })

# Apply route-specific middleware to protect this route
@app.get('/api/protected')
@mw.auth(strategy="bearer", secret="secret123")
def api_protected(req, res):
    return res.json({
        "message": "This is protected data that requires authentication",
        "user": req.user,
        "timestamp": req.timestamp
    })

# Apply multiple middleware to this route group
@app.post('/api/users', [
    mw.validate_request(user_schema),  # Validate request data
    api_rate_limiter  # Apply rate limiting
])
def create_user(req, res):
    # The request has already been validated by the middleware
    user = req.json
    
    # Add user ID
    user["id"] = 123
    
    return res.status(201).json({
        "message": "User created successfully",
        "user": user
    })

@app.get('/api/status', [api_rate_limiter])
def api_status(req, res):
    return res.json({
        "status": "online",
        "timestamp": req.timestamp
    })

@app.get('/test-error')
def test_error(req, res):
    # Deliberately throw an error to test error handling
    raise ValueError("This is a test error to demonstrate error handling middleware")

# Add request timestamp middleware
@app.use
def add_timestamp(req, res, next):
    req.timestamp = import_time().time()
    return next()

def import_time():
    """Helper function to import time module"""
    import time
    return time

# Start the server
if __name__ == '__main__':
    app.listen(3001, '127.0.0.1')
    print(f"Server running at http://127.0.0.1:3001")
    print("\nAvailable routes:")
    print("  - GET  /                - Home page")
    print("  - GET  /api/public      - Public API endpoint")
    print("  - GET  /api/protected   - Protected API endpoint (requires Bearer token)")
    print("  - POST /api/users       - Create user (with validation)")
    print("  - GET  /api/status      - API status (with rate limiting)")
    print("  - GET  /test-error      - Test error handling middleware")
    print("  - GET  /static/*        - Static files (served from public/static)")
    
    print("\nActive middleware:")
    print("  - Logger middleware (detailed mode)")
    print("  - CORS middleware")
    print("  - JSON parser middleware")
    print("  - Static files middleware")
    print("  - Security headers middleware")
    print("  - Error handler middleware")
    print("  - Custom timestamp middleware") 