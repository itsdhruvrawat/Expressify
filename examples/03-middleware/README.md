# Middleware in Expressify

This example demonstrates how to use middleware in Expressify applications to handle common tasks like logging, authentication, and error handling.

## What is Middleware?

Middleware functions are functions that have access to the request object (`req`), the response object (`res`), and the next middleware function in the application's request-response cycle.

Middleware can:
- Execute any code
- Make changes to the request and response objects
- End the request-response cycle
- Call the next middleware in the stack

## Middleware Flow

Middleware functions are executed in the order they are added. Each middleware has the option to:
1. Pass control to the next middleware function by calling `next()`
2. End the request-response cycle by sending a response to the client

```
Client Request → Middleware 1 → Middleware 2 → Route Handler → Response
                      ↓             ↓              ↓
                 Can modify     Can modify     Can modify
                    req/res        req/res        req/res
```

## Types of Middleware in Expressify

### 1. Application-level Middleware

Application-level middleware is bound to the Expressify application instance using `app.use()` and is executed for every request to the application.

```python
def logger_middleware(req, res, next):
    """Log request information"""
    print(f"Request: {req.method} {req.path}")
    result = next()
    print(f"Response: {res.status_code}")
    return result

# Apply middleware to all routes
app.use(logger_middleware)
```

### 2. Router-level Middleware

Router-level middleware is bound to specific route handlers and is executed only when those routes are matched.

```python
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
    
    return next()

# Apply route-specific middleware
@app.get('/user/:id', [validate_id])
def get_user(req, res):
    user_id = int(req.params.get('id'))
    # ...
```

### 3. Error-handling Middleware

Error-handling middleware is used to catch and process errors that occur during request processing.

```python
def error_handler_middleware(req, res, next):
    """Handle errors in the middleware chain"""
    try:
        return next()
    except Exception as e:
        print(f"Error: {str(e)}")
        return res.status(500).json({
            'error': 'Internal Server Error',
            'message': str(e)
        })

app.use(error_handler_middleware)
```

### 4. Built-in Middleware

Expressify comes with some built-in middleware functions for common tasks, such as:

- `json_parser` - Parses JSON request bodies
- `static_files` - Serves static files from a specified directory
- `cors` - Handles Cross-Origin Resource Sharing (CORS)

```python
# Use built-in middleware
app.use(expressify.json_parser())
app.use(expressify.static_files('public'))
app.use(expressify.cors())
```

### 5. Third-party Middleware

You can also use third-party middleware with Expressify, as long as they follow the middleware function signature `(req, res, next)`.

## Creating and Using Middleware

### Writing Middleware Functions

A middleware function in Expressify follows this pattern:

```python
def my_middleware(req, res, next):
    # Do something with req and res
    
    # Call the next middleware or route handler
    result = next()
    
    # Do something after the next middleware has been executed
    
    # Return the result
    return result
```

### Error Handling in Middleware

If a middleware function needs to stop the request-response cycle due to an error, it should return a response object:

```python
def auth_middleware(req, res, next):
    """Check for API key"""
    api_key = req.get_header('x-api-key')
    
    if not api_key:
        return res.status(401).json({
            'error': 'Authentication required',
            'message': 'Missing API key'
        })
    
    if api_key != 'valid_key':
        return res.status(403).json({
            'error': 'Access denied',
            'message': 'Invalid API key'
        })
    
    # If authentication is successful, call the next middleware
    return next()
```

### Middleware as Decorators

You can also create middleware as decorators for individual route handlers:

```python
def require_auth(api_key='default_key'):
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
    # ...
```

## Common Middleware Examples

### 1. Logger Middleware

```python
def logger_middleware(req, res, next):
    start_time = time.time()
    print(f"Request: {req.method} {req.path}")
    
    result = next()
    
    duration = (time.time() - start_time) * 1000  # in ms
    print(f"Response: {res.status_code} - {duration:.2f}ms")
    
    return result
```

### 2. CORS Middleware

```python
def cors_middleware(req, res, next):
    res.set_header('Access-Control-Allow-Origin', '*')
    res.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    res.set_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    
    if req.method == 'OPTIONS':
        return res.status(204).send()
    
    return next()
```

### 3. Authentication Middleware

```python
def auth_middleware(req, res, next):
    if req.path.startswith('/protected'):
        api_key = req.get_header('x-api-key')
        
        if not api_key or api_key != 'abc123':
            return res.status(401).json({
                'error': 'Authentication required',
                'message': 'Invalid or missing API key'
            })
    
    return next()
```

### 4. JSON Parser Middleware

```python
def json_parser_middleware(req, res, next):
    if 'application/json' in req.get_header('content-type', ''):
        try:
            if req.body:
                req.json = json.loads(req.body)
        except json.JSONDecodeError:
            return res.status(400).json({
                'error': 'Invalid JSON',
                'message': 'Failed to parse request body as JSON'
            })
    
    return next()
```

## Running the Examples

This directory contains two example servers that demonstrate middleware concepts:

1. `simple_middleware.py` - A basic HTTP server that implements middleware pattern using Python's standard library
2. `middleware_example.py` - A more comprehensive example using the Expressify framework

To run the simple middleware example:

```bash
python simple_middleware.py
```

To run the Expressify middleware example:

```bash
python middleware_example.py
```

Both servers will run on `127.0.0.1:3001` and provide various endpoints to demonstrate middleware functionality.

## Best Practices

1. **Keep middleware functions focused** - Each middleware should have a single responsibility
2. **Order matters** - Consider the order in which middleware functions are added
3. **Don't forget to call next()** - Unless you're ending the request-response cycle
4. **Error handling** - Use try/catch blocks in middleware to catch errors
5. **Chain middleware effectively** - Combine middleware functions that work well together
6. **Monitor performance** - Middleware adds processing overhead, so monitor performance impacts 