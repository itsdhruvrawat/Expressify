# Expressify Basics Example

This directory contains a basic example of using Expressify, demonstrating the core concepts and functionality of the framework.

## What You'll Learn

- How to create an Expressify application
- How to define routes with different HTTP methods
- How to handle requests and send responses in different formats (text, HTML, JSON)
- How to access query parameters
- How to handle form submissions with POST data

## Files in This Example

- `app.py` - The main application file with a well-commented example

## Running the Example

To run this example:

```bash
cd examples/01-basics
python app.py
```

The server will start on port 3000. You can then access the application at [http://localhost:3000](http://localhost:3000).

## Available Routes

The example includes the following routes:

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `/` | GET | Returns a simple text greeting | [http://localhost:3000/](http://localhost:3000/) |
| `/html` | GET | Returns an HTML page | [http://localhost:3000/html](http://localhost:3000/html) |
| `/json` | GET | Returns JSON data | [http://localhost:3000/json](http://localhost:3000/json) |
| `/echo` | GET | Echoes back a query parameter | [http://localhost:3000/echo?message=Hello](http://localhost:3000/echo?message=Hello) |
| `/submit` | POST | Handles form submissions | Send POST data with `name` and `email` fields |

## Testing with cURL

You can test the routes using cURL:

```bash
# Test the root route (plain text)
curl http://localhost:3000/

# Test the HTML route
curl http://localhost:3000/html

# Test the JSON route
curl http://localhost:3000/json

# Test the echo route with a query parameter
curl http://localhost:3000/echo?message=Hello%20Expressify

# Test the form submission route with POST data
curl -X POST -d "name=John&email=john@example.com" http://localhost:3000/submit
```

## Key Concepts Demonstrated

### Application Initialization

```python
from expressify import expressify
app = expressify()
```

### Route Definition

```python
@app.get('/path')
def handler(req, res):
    # Route handler logic
    res.send('Response')
```

### Response Methods

```python
# Send plain text
res.send('Hello World')

# Send HTML
res.send('<html>...</html>')

# Send JSON
res.json({'key': 'value'})
```

### Request Data Access

```python
# Access query parameters (?key=value)
value = req.query.get('key', 'default')

# Access form/POST data
data = req.body.get('field', 'default')
```

### Starting the Server

```python
app.listen(3000)
``` 