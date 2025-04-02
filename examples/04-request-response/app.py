"""
Expressify Request and Response Example

This example demonstrates various features of the Request and Response objects in Expressify:
- Request object: Accessing parameters, query strings, headers, and body
- Response object: Setting status codes, headers, and sending different response types
"""

from expressify import expressify

# Create a new Expressify application
app = expressify()

# ------------------------------------------------------------
# Request Object Examples
# ------------------------------------------------------------

# Home route
@app.get('/')
def home(req, res):
    """Home route with links to examples"""
    res.type('html').send('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify Request/Response Examples</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1, h2 { color: #0066cc; }
            .container { max-width: 800px; margin: 0 auto; }
            ul { margin-bottom: 20px; }
            pre { background: #f4f4f4; padding: 10px; border-radius: 5px; }
            .card { border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 15px; }
            .method { display: inline-block; padding: 3px 6px; border-radius: 3px; color: white; font-size: 12px; }
            .get { background-color: #5cb85c; }
            .post { background-color: #f0ad4e; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Expressify Request and Response Examples</h1>
            <p>This example demonstrates how to work with Request and Response objects in Expressify.</p>
            
            <div class="card">
                <h2>Request Object Examples</h2>
                <ul>
                    <li><a href="/request-info"><span class="method get">GET</span> /request-info</a> - Shows basic request information</li>
                    <li><a href="/query-params?name=John&age=30"><span class="method get">GET</span> /query-params?name=John&age=30</a> - Demonstrates query parameters</li>
                    <li><a href="/headers"><span class="method get">GET</span> /headers</a> - Shows request headers</li>
                    <li><span class="method post">POST</span> /handle-form - Process form data (see form below)</li>
                    <li><a href="/params/42"><span class="method get">GET</span> /params/42</a> - URL parameters</li>
                </ul>
            </div>
            
            <div class="card">
                <h2>Response Object Examples</h2>
                <ul>
                    <li><a href="/text"><span class="method get">GET</span> /text</a> - Plain text response</li>
                    <li><a href="/html"><span class="method get">GET</span> /html</a> - HTML response</li>
                    <li><a href="/json"><span class="method get">GET</span> /json</a> - JSON response</li>
                    <li><a href="/status"><span class="method get">GET</span> /status</a> - Custom status code (201)</li>
                    <li><a href="/headers-demo"><span class="method get">GET</span> /headers-demo</a> - Custom response headers</li>
                    <li><a href="/redirect"><span class="method get">GET</span> /redirect</a> - Redirect response</li>
                    <li><a href="/content-types"><span class="method get">GET</span> /content-types</a> - Content-Type examples</li>
                </ul>
            </div>
            
            <div class="card">
                <h2>Test Form Submission</h2>
                <form action="/handle-form" method="post">
                    <div style="margin-bottom: 10px;">
                        <label for="name">Name:</label>
                        <input type="text" id="name" name="name" required style="width: 100%; padding: 8px; margin-top: 5px;">
                    </div>
                    <div style="margin-bottom: 10px;">
                        <label for="email">Email:</label>
                        <input type="email" id="email" name="email" required style="width: 100%; padding: 8px; margin-top: 5px;">
                    </div>
                    <div style="margin-bottom: 10px;">
                        <label for="message">Message:</label>
                        <textarea id="message" name="message" rows="4" style="width: 100%; padding: 8px; margin-top: 5px;"></textarea>
                    </div>
                    <button type="submit" style="background-color: #0066cc; color: white; border: none; padding: 10px 15px; border-radius: 5px; cursor: pointer;">Submit</button>
                </form>
            </div>
            
            <div class="card">
                <h2>Testing with cURL</h2>
                <pre>
# Get request info
curl http://localhost:3000/request-info

# Query parameters
curl http://localhost:3000/query-params?name=John&age=30

# Get request headers
curl http://localhost:3000/headers

# Submit form data
curl -X POST -d "name=John&email=john@example.com&message=Hello" http://localhost:3000/handle-form

# URL parameters
curl http://localhost:3000/params/42

# Response examples
curl http://localhost:3000/text
curl http://localhost:3000/html
curl http://localhost:3000/json
curl http://localhost:3000/status
curl -v http://localhost:3000/headers-demo
curl -v http://localhost:3000/redirect
                </pre>
            </div>
        </div>
    </body>
    </html>
    ''')

# Request information
@app.get('/request-info')
def request_info(req, res):
    """Shows basic information about the request"""
    info = {
        'method': req.method,
        'path': req.path,
        'protocol': req.protocol,
        'host': req.headers.get('host', ''),
        'user_agent': req.headers.get('user-agent', ''),
        'content_type': req.headers.get('content-type', ''),
        'query_params': dict(req.query),
        'url': f"{req.protocol}://{req.headers.get('host', '')}{req.path}"
    }
    
    res.json(info)

# Query parameters example
@app.get('/query-params')
def query_params(req, res):
    """Demonstrates how to access query parameters"""
    name = req.query.get('name', 'Guest')
    age = req.query.get('age', 'Unknown')
    
    res.json({
        'message': f'Hello, {name}!',
        'name': name,
        'age': age,
        'all_params': dict(req.query),
        'tip': 'Try adding different query parameters to the URL'
    })

# Headers example
@app.get('/headers')
def headers(req, res):
    """Shows all request headers"""
    headers_dict = {name: value for name, value in req.headers.items()}
    
    res.json({
        'message': 'Request Headers',
        'headers': headers_dict
    })

# Form handling example
@app.post('/handle-form')
def handle_form(req, res):
    """Process form data from POST request"""
    name = req.body.get('name', '')
    email = req.body.get('email', '')
    message = req.body.get('message', '')
    
    res.json({
        'message': 'Form submission received',
        'data': {
            'name': name,
            'email': email,
            'message': message
        },
        'all_form_data': dict(req.body)
    })

# URL parameters example
@app.get('/params/:id')
def url_params(req, res):
    """Demonstrates URL parameters"""
    param_id = req.params.get('id', 'unknown')
    
    res.json({
        'message': f'You requested item {param_id}',
        'id': param_id,
        'all_params': dict(req.params),
        'tip': 'Try changing the ID in the URL'
    })

# ------------------------------------------------------------
# Response Object Examples
# ------------------------------------------------------------

# Plain text response
@app.get('/text')
def text_response(req, res):
    """Sends a plain text response"""
    res.type('text/plain').send('This is a plain text response from Expressify')

# HTML response
@app.get('/html')
def html_response(req, res):
    """Sends an HTML response"""
    res.type('text/html').send('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>HTML Response</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
            h1 { color: #0066cc; }
            .container { max-width: 600px; margin: 0 auto; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HTML Response</h1>
            <p>This is an HTML response from Expressify.</p>
            <p><a href="/">Back to Examples</a></p>
        </div>
    </body>
    </html>
    ''')

# JSON response
@app.get('/json')
def json_response(req, res):
    """Sends a JSON response"""
    data = {
        'message': 'This is a JSON response',
        'framework': 'Expressify',
        'timestamp': '2023-03-26T12:34:56Z',
        'items': [
            {'id': 1, 'name': 'Item 1'},
            {'id': 2, 'name': 'Item 2'},
            {'id': 3, 'name': 'Item 3'}
        ]
    }
    
    res.json(data)

# Status code example
@app.get('/status')
def status_code(req, res):
    """Demonstrates setting a custom status code"""
    res.status(201).json({
        'message': 'This response has a 201 Created status code',
        'status_code': 201,
        'note': 'Check the network tab in your browser\'s developer tools'
    })

# Custom headers example
@app.get('/headers-demo')
def headers_demo(req, res):
    """Demonstrates setting custom response headers"""
    res.headers['X-Custom-Header'] = 'Custom Value'
    res.headers['X-Powered-By'] = 'Expressify'
    res.headers['X-Demo'] = 'Custom Headers Example'
    
    res.json({
        'message': 'This response includes custom headers',
        'note': 'Check the network tab in your browser\'s developer tools, or use curl -v'
    })

# Redirect example
@app.get('/redirect')
def redirect_demo(req, res):
    """Demonstrates a redirect response"""
    res.redirect('/')

# Content-Type examples
@app.get('/content-types')
def content_types(req, res):
    """Demonstrates different content types using res.type()"""
    content_type = req.query.get('type', 'html')
    
    if content_type == 'text':
        res.type('text/plain').send('This is plain text content')
    
    elif content_type == 'html':
        res.type('text/html').send('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Content-Type Example</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #0066cc; }
                .container { max-width: 800px; margin: 0 auto; }
                .code { font-family: monospace; background: #f4f4f4; padding: 3px; }
                .examples { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 20px; }
                .example { padding: 8px 15px; background: #eee; border-radius: 5px; text-decoration: none; color: #333; }
                .example:hover { background: #ddd; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Content-Type Examples</h1>
                <p>This example demonstrates using <span class="code">res.type()</span> to set different content types.</p>
                <p>Current content type: <span class="code">text/html</span></p>
                
                <div class="examples">
                    <a href="/content-types?type=text" class="example">text/plain</a>
                    <a href="/content-types?type=html" class="example">text/html</a>
                    <a href="/content-types?type=json" class="example">application/json</a>
                    <a href="/content-types?type=xml" class="example">application/xml</a>
                    <a href="/content-types?type=css" class="example">text/css</a>
                    <a href="/content-types?type=js" class="example">application/javascript</a>
                    <a href="/content-types?type=custom" class="example">custom/type</a>
                </div>
                
                <p><a href="/">Back to Examples</a></p>
            </div>
        </body>
        </html>
        ''')
    
    elif content_type == 'json':
        res.type('application/json').send('{"message": "This is JSON content", "format": "application/json"}')
    
    elif content_type == 'xml':
        res.type('application/xml').send('''<?xml version="1.0" encoding="UTF-8"?>
<root>
  <message>This is XML content</message>
  <format>application/xml</format>
</root>''')
    
    elif content_type == 'css':
        res.type('text/css').send('''
body {
  font-family: Arial, sans-serif;
  background-color: #f0f0f0;
  color: #333;
}

h1 {
  color: #0066cc;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}
''')
    
    elif content_type == 'js':
        res.type('application/javascript').send('''
function greeting(name) {
  return `Hello, ${name}!`;
}

console.log(greeting('Expressify User'));

document.addEventListener('DOMContentLoaded', () => {
  console.log('Document loaded');
});
''')
    
    elif content_type == 'custom':
        res.type('application/x-custom-type').send('This is a custom content type example')
    
    else:
        res.type('text/plain').send('Unknown content type requested')

# ------------------------------------------------------------
# Start the Server
# ------------------------------------------------------------

if __name__ == '__main__':
    print("Request/Response examples running on http://localhost:3000")
    print("Visit http://localhost:3000 to see the examples")
    
    app.listen(port=3000, hostname='127.0.0.1') 