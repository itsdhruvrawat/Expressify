# Expressify Error Handling Example

This directory contains examples of how to handle errors in Expressify applications, demonstrating various techniques for catching, processing, and responding to different types of errors.

## What You'll Learn

- How to create global error handling middleware
- How to handle errors in individual route handlers using try/except
- How to create custom error response formats
- How to validate input to prevent errors
- How to create a custom 404 handler for not found routes

## Files in This Example

- `app.py` - An application demonstrating various error handling techniques

## Running the Example

To run this example:

```bash
cd examples/07-error-handling
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000) to see a user interface with links to test the various error scenarios.

## Error Scenarios Demonstrated

| Route | Description | Error Handling Approach |
|-------|-------------|-------------------------|
| `/not-found` | 404 Not Found Error | Custom 404 handler (catch-all route) |
| `/error/unhandled` | 500 Unhandled Exception | Global error middleware |
| `/error/handled` | Handled Exception | Try/except in route handler |
| `/error/custom` | Custom Error Format | Custom error response structure |
| `/error/random` | Random Success/Failure | Controlled error simulation |
| `/error/validation?id=123` | Input Validation (Success) | Parameter validation |
| `/error/validation` | Input Validation (Error) | Parameter validation |

## Error Handling Approaches

### Global Error Middleware

```python
def error_handler_middleware(req, res, next):
    try:
        next()
    except Exception as e:
        res.status(500).json({
            'error': 'Internal Server Error',
            'message': str(e)
        })

app.use(error_handler_middleware)
```

### Route-Level Error Handling

```python
@app.get('/route')
def handler(req, res):
    try:
        # Code that might fail
        result = some_operation()
        res.json({'success': True, 'result': result})
    except SomeSpecificError:
        res.status(400).json({'error': 'Specific error occurred'})
    except Exception as e:
        res.status(500).json({'error': 'Generic error occurred'})
```

### Custom 404 Handler

```python
# This should be the last route defined
@app.get('*')
def not_found(req, res):
    res.status(404).json({
        'error': 'Not Found',
        'message': f"The path '{req.path}' does not exist"
    })
```

### Input Validation

```python
@app.get('/validate')
def validate(req, res):
    if 'required_param' not in req.query:
        return res.status(400).json({'error': 'Missing required parameter'})
    
    # Continue with normal processing if validation passes
    res.json({'success': True})
```

## Testing with cURL

```bash
# Test 404 error
curl http://localhost:3000/not-found

# Test unhandled exception
curl http://localhost:3000/error/unhandled

# Test handled exception
curl http://localhost:3000/error/handled

# Test custom error format
curl http://localhost:3000/error/custom

# Test random error (may succeed or fail)
curl http://localhost:3000/error/random

# Test validation (success)
curl http://localhost:3000/error/validation?id=123

# Test validation (error)
curl http://localhost:3000/error/validation
```

## Best Practices

1. **Use Global Middleware**: Catch all unhandled exceptions with global middleware
2. **Be Specific**: Handle specific error types differently when possible
3. **Validate Input**: Prevent errors by validating input before processing
4. **Consistent Format**: Use a consistent error response format
5. **Don't Expose Sensitive Info**: Don't include sensitive stack traces in production
6. **Log Errors**: Always log errors for debugging and monitoring 