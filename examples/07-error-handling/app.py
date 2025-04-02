"""
Expressify Error Handling Example

This example demonstrates how to handle errors in Expressify applications:
- Built-in error handling
- Custom error handlers
- Try/except blocks in route handlers
- Error handling middleware
- Different types of errors (404, 500, etc.)
"""

from expressify import expressify
import random

# Create a new Expressify application
app = expressify()

# ------------------------------------------------------------
# Custom Error Handler Middleware
# ------------------------------------------------------------

def error_handler_middleware(req, res, next):
    """
    Global error handling middleware
    
    This middleware catches any exceptions that occur during request processing
    and returns a formatted error response.
    """
    try:
        # Try to process the request normally
        next()
    except Exception as e:
        # Log the error (in a real app, you might use a logging framework)
        print(f"[ERROR] {str(e)}")
        
        # Send a friendly error response
        res.status(500).json({
            'error': 'Internal Server Error',
            'message': str(e),
            'path': req.path,
            'handled_by': 'Global error handler middleware'
        })

# Register the error handler middleware (should be registered first)
app.use(error_handler_middleware)

# ------------------------------------------------------------
# Home Route
# ------------------------------------------------------------

@app.get('/')
def home(req, res):
    """Home page with links to different error examples"""
    res.send('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expressify Error Handling</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1, h2 {
                color: #0066cc;
            }
            .card {
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }
            code {
                background-color: #f0f0f0;
                padding: 2px 4px;
                border-radius: 3px;
                font-family: monospace;
            }
            pre {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
            .error-type {
                font-weight: bold;
                color: #d9534f;
            }
            ul {
                list-style-type: none;
                padding-left: 0;
            }
            li {
                margin-bottom: 10px;
                padding-left: 20px;
                position: relative;
            }
            li:before {
                content: "→";
                position: absolute;
                left: 0;
                color: #0066cc;
            }
            a {
                color: #0066cc;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Expressify Error Handling</h1>
        <p>This example demonstrates different approaches to error handling in Expressify applications.</p>
        
        <div class="card">
            <h2>Error Examples</h2>
            <ul>
                <li><a href="/not-found">404 Not Found Error</a> - Access a non-existent route</li>
                <li><a href="/error/unhandled">500 Unhandled Exception</a> - Throws an exception caught by middleware</li>
                <li><a href="/error/handled">Handled Exception</a> - Exception handled in route with try/except</li>
                <li><a href="/error/custom">Custom Error Response</a> - Returns a custom error format</li>
                <li><a href="/error/random">Random Error</a> - Randomly succeeds or fails</li>
                <li><a href="/error/validation?id=123">Validation Success</a> - Valid parameter</li>
                <li><a href="/error/validation">Validation Error</a> - Missing required parameter</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>Error Handling Approaches</h2>
            <ol>
                <li><strong>Global Error Middleware</strong> - Catches all unhandled exceptions</li>
                <li><strong>Try/Except in Route Handlers</strong> - Handle errors in specific routes</li>
                <li><strong>Custom Error Responses</strong> - Format errors in a consistent way</li>
                <li><strong>Input Validation</strong> - Prevent errors by validating input</li>
            </ol>
        </div>
        
        <div class="card">
            <h2>Testing with cURL</h2>
            <pre>
# Test 404 error
curl http://localhost:3000/not-found

# Test unhandled exception
curl http://localhost:3000/error/unhandled

# Test handled exception
curl http://localhost:3000/error/handled

# Test custom error
curl http://localhost:3000/error/custom

# Test random error
curl http://localhost:3000/error/random

# Test validation (success)
curl http://localhost:3000/error/validation?id=123

# Test validation (error)
curl http://localhost:3000/error/validation
            </pre>
        </div>
    </body>
    </html>
    ''')

# ------------------------------------------------------------
# Error Example Routes
# ------------------------------------------------------------

# 404 Not Found - This is handled by the default router
# No need to define a special route for this

# Unhandled exception - will be caught by the middleware
@app.get('/error/unhandled')
def unhandled_error(req, res):
    """Demonstrates an unhandled exception caught by middleware"""
    # This will raise an exception
    result = 1 / 0  # Division by zero error
    
    # This line will never be reached
    res.send("This will never be sent")

# Handled exception - try/except in route handler
@app.get('/error/handled')
def handled_error(req, res):
    """Demonstrates handling an exception in the route handler"""
    try:
        # Try something that might fail
        value = req.query.get('value', '10')
        result = 100 / int(value)
        
        # If successful, return the result
        res.json({
            'success': True,
            'result': result,
            'message': f"100 divided by {value} is {result}"
        })
    except ZeroDivisionError:
        # Handle division by zero specifically
        res.status(400).json({
            'error': 'Bad Request',
            'message': 'Cannot divide by zero',
            'handled_by': 'Route handler (specific error type)'
        })
    except ValueError:
        # Handle value errors (e.g., non-integer input)
        res.status(400).json({
            'error': 'Bad Request',
            'message': 'Value must be an integer',
            'handled_by': 'Route handler (specific error type)'
        })
    except Exception as e:
        # Handle any other exceptions
        res.status(500).json({
            'error': 'Internal Server Error',
            'message': str(e),
            'handled_by': 'Route handler (generic catch-all)'
        })

# Custom error format
@app.get('/error/custom')
def custom_error(req, res):
    """Demonstrates a custom error response format"""
    res.status(400).json({
        'status': 'error',
        'code': 'INVALID_REQUEST',
        'message': 'The request could not be processed',
        'details': {
            'timestamp': '2023-03-26T12:34:56Z',
            'request_id': 'req_123456',
            'documentation_url': 'https://docs.example.com/errors/INVALID_REQUEST'
        },
        'handled_by': 'Custom error format handler'
    })

# Random error - sometimes succeeds, sometimes fails
@app.get('/error/random')
def random_error(req, res):
    """Randomly succeeds or fails to demonstrate error handling"""
    # Randomly decide if this request will succeed or fail
    if random.random() < 0.5:  # 50% chance of success
        res.json({
            'success': True,
            'message': 'The operation was successful',
            'data': {
                'random_value': random.random(),
                'timestamp': '2023-03-26T12:34:56Z'
            }
        })
    else:
        # Simulate a server error
        res.status(500).json({
            'error': 'Internal Server Error',
            'message': 'Random failure occurred',
            'handled_by': 'Random error generator'
        })

# Validation error - check if required parameter exists
@app.get('/error/validation')
def validation_error(req, res):
    """Demonstrates input validation to prevent errors"""
    # Check if the 'id' parameter exists
    if 'id' not in req.query:
        res.status(400).json({
            'error': 'Bad Request',
            'message': 'Missing required parameter: id',
            'handled_by': 'Input validation'
        })
        return
    
    # If we get here, the id parameter exists
    id_value = req.query.get('id')
    
    res.json({
        'success': True,
        'message': 'Validation passed',
        'id': id_value
    })

# ------------------------------------------------------------
# 404 Handler (catch-all route)
# ------------------------------------------------------------

# This should be the last route defined
@app.get('*')
def not_found(req, res):
    """Custom 404 handler for all unmatched routes"""
    res.status(404).json({
        'error': 'Not Found',
        'message': f"The requested path '{req.path}' does not exist",
        'handled_by': 'Custom 404 handler'
    })

# ------------------------------------------------------------
# Start the Server
# ------------------------------------------------------------

if __name__ == '__main__':
    print("Error handling example running on http://localhost:3000")
    print("Try different error scenarios by visiting the links on the home page")
    
    app.listen(port=3000, hostname='127.0.0.1') 