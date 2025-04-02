"""
Basic Expressify Application Example

This example demonstrates the fundamental concepts of creating an Expressify application:
- Initializing the application
- Creating routes with different HTTP methods (GET/POST)
- Handling requests and sending responses
- Starting the server
"""

# Import the expressify framework
from expressify import expressify

# Create a new Expressify application instance
# This is similar to how you would use `express()` in Express.js
app = expressify()

# Define a basic route for the root path ('/')
# The @app.get decorator registers a handler for HTTP GET requests
@app.get('/')
def home(req, res):
    """
    Home route handler.
    
    Parameters:
    - req: The request object containing information about the HTTP request
    - res: The response object used to send data back to the client
    """
    # Send a simple text response
    res.send('Hello, World! Welcome to Expressify!')

# Define a route that returns HTML content
@app.get('/html')
def html_example(req, res):
    """Route that returns HTML content."""
    # Send HTML content to the browser
    res.type('text/html').send("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify HTML Example</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
            .container { max-width: 800px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Hello from Expressify!</h1>
            <p>This is an HTML response.</p>
            <ul>
                <li><a href="/">Plain text response</a></li>
                <li><a href="/json">JSON response</a></li>
                <li><a href="/echo?message=Hello">Query parameters example</a></li>
            </ul>
        </div>
    </body>
    </html>
    """)

# Define a route that returns JSON data
@app.get('/json')
def json_example(req, res):
    """Route that returns JSON data."""
    # Send a JSON response
    # This automatically sets the Content-Type header to application/json
    res.json({
        'message': 'Hello from Expressify!',
        'framework': 'Expressify',
        'language': 'Python',
        'features': [
            'Routing',
            'Middleware',
            'Templates',
            'Static files',
            'Error handling'
        ]
    })

# Define a route with query parameters
@app.get('/echo')
def echo(req, res):
    """Route that echoes back query parameters."""
    # Access query parameters from the request object
    message = req.query.get('message', 'No message provided')
    
    # Send a response that includes the query parameter
    res.send(f'You said: {message}')

# Define a POST route to handle form submissions
@app.post('/submit')
def handle_submission(req, res):
    """Route that handles POST data."""
    # Access form data from the request body
    name = req.body.get('name', 'Anonymous')
    email = req.body.get('email', 'No email provided')
    
    # Send a response based on the submitted data
    res.send(f'Received submission from {name} ({email})')

# This block is executed when the script is run directly
if __name__ == '__main__':
    # Print information about the server
    print("Basic Expressify example running on http://127.0.0.1:3000")
    print("Available routes:")
    print("  - GET http://127.0.0.1:3000/")
    print("  - GET http://127.0.0.1:3000/html")
    print("  - GET http://127.0.0.1:3000/json")
    print("  - GET http://127.0.0.1:3000/echo?message=YourMessage")
    print("  - POST http://127.0.0.1:3000/submit (accepts 'name' and 'email' fields)")
    
    # Start the server with explicitly required parameters
    # Both port and hostname are required parameters
    # This is a blocking call that will run until the server is stopped
    app.listen(port=3000, hostname='127.0.0.1')