# Expressify Request and Response Example

This directory contains examples that showcase working with Request and Response objects in Expressify, demonstrating how to access and use various properties and methods.

## What You'll Learn

- How to access request information (method, path, protocol)
- How to read URL parameters, query parameters, headers, and body data
- How to send different types of responses (text, HTML, JSON)
- How to set status codes and headers in responses
- How to use redirects

## Files in This Example

- `app.py` - An application demonstrating request and response features

## Running the Example

To run this example:

```bash
cd examples/04-request-response
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000).

## Request Object Examples

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `/request-info` | GET | Shows basic request information | [http://localhost:3000/request-info](http://localhost:3000/request-info) |
| `/query-params` | GET | Demonstrates query parameters | [http://localhost:3000/query-params?name=John&age=30](http://localhost:3000/query-params?name=John&age=30) |
| `/headers` | GET | Shows request headers | [http://localhost:3000/headers](http://localhost:3000/headers) |
| `/handle-form` | POST | Process form data | Submit the form on the home page |
| `/params/:id` | GET | URL parameters | [http://localhost:3000/params/42](http://localhost:3000/params/42) |

## Response Object Examples

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `/text` | GET | Plain text response | [http://localhost:3000/text](http://localhost:3000/text) |
| `/html` | GET | HTML response | [http://localhost:3000/html](http://localhost:3000/html) |
| `/json` | GET | JSON response | [http://localhost:3000/json](http://localhost:3000/json) |
| `/status` | GET | Custom status code (201) | [http://localhost:3000/status](http://localhost:3000/status) |
| `/headers-demo` | GET | Custom response headers | [http://localhost:3000/headers-demo](http://localhost:3000/headers-demo) |
| `/redirect` | GET | Redirect response | [http://localhost:3000/redirect](http://localhost:3000/redirect) |

## Testing with cURL

```bash
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
```

## Key Concepts Demonstrated

### Request Object Properties

```python
# Accessing request information
req.method     # HTTP method (GET, POST, etc.)
req.path       # URL path
req.protocol   # HTTP protocol (http/https)
req.headers    # HTTP headers dictionary
req.query      # Query parameters dictionary
req.params     # URL parameters dictionary
req.body       # Request body (form data or JSON)
```

### Response Object Methods

```python
# Sending responses
res.send('Plain text response')         # Send text response
res.json({'key': 'value'})              # Send JSON response
res.status(201).send('Created')         # Set status code
res.set_header('X-Custom', 'Value')     # Set response header
res.redirect('/other-route')            # Redirect response
```

### Practical Usage

```python
@app.get('/users/:id')
def get_user(req, res):
    # Get URL parameter
    user_id = req.params.get('id')
    
    # Get query parameter with default value
    format = req.query.get('format', 'json')
    
    # Read a header
    accept = req.headers.get('accept', '*/*')
    
    # Set a custom header
    res.set_header('X-User-Id', user_id)
    
    # Return JSON response
    res.json({'id': user_id, 'name': f'User {user_id}'})
``` 