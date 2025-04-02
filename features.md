# Expressify Features

Expressify is designed to provide a robust yet easy-to-use web framework for Python developers. This document outlines the core features and capabilities of the framework.

## Routing System

### Decorator-Based Routing
```python
@app.get('/users')
def get_users(req, res):
    res.json(users)
```

### Express-Style Method-Based Routing
```python
def get_users(req, res):
    res.json(users)

app.get('/users', get_users)
```

### Support for All HTTP Methods
- GET: `@app.get()` or `app.get()`
- POST: `@app.post()` or `app.post()`
- PUT: `@app.put()` or `app.put()`
- DELETE: `@app.delete()` or `app.delete()`
- PATCH: `@app.patch()` or `app.patch()`
- All methods: `@app.all()` or `app.all()`

### Route Parameters
```python
@app.get('/users/:id')
def get_user(req, res):
    user_id = req.params.get('id')
    res.json(find_user(user_id))
```

### Query Parameters
```python
@app.get('/users')
def get_users(req, res):
    limit = req.query.get('limit', 10)
    page = req.query.get('page', 1)
    res.json(paginate_users(limit, page))
```

## Request Object

### Property Access
- `req.method`: HTTP method (GET, POST, etc.)
- `req.path`: URL path
- `req.query`: Query parameters
- `req.params`: Route parameters
- `req.headers`: HTTP headers
- `req.cookies`: Cookies
- `req.body`: Request body (parsed for JSON and form data)
- `req.files`: Uploaded files

### Helper Methods
- `req.get_header(name)`: Get a specific header
- `req.is_json()`: Check if request has JSON content type
- `req.is_form()`: Check if request has form content type

## Response Object

### Response Methods
- `res.send(data)`: Send a response (auto-detects string/HTML vs JSON)
- `res.json(data)`: Send a JSON response
- `res.html(html)`: Send an HTML response
- `res.render(template, context)`: Render a template
- `res.redirect(url)`: Redirect to another URL
- `res.status(code)`: Set HTTP status code
- `res.set_header(name, value)`: Set a response header
- `res.set_cookie(name, value, options)`: Set a cookie
- `res.clear_cookie(name)`: Clear a cookie
- `res.sendFile(path)`: Send a file

### Chaining
```python
res.status(201).set_header('X-Custom', 'Value').json(data)
```

## Middleware Support

### Global Middleware
```python
def logger_middleware(req, res, next):
    print(f"Request: {req.method} {req.path}")
    next()

app.use(logger_middleware)
```

### Path-Specific Middleware
```python
def auth_middleware(req, res, next):
    if not req.headers.get('Authorization'):
        return res.status(401).send('Unauthorized')
    next()

app.use('/admin', auth_middleware)
```

### Route-Specific Middleware
```python
@app.get('/dashboard', middleware=[auth_middleware])
def dashboard(req, res):
    res.render('dashboard.html')
```

### Middleware Order
Middleware executes in the order defined, allowing for request processing pipelines.

## Template Rendering

### Template Setup
```python
app.set('view engine', 'jinja2')
app.set('views', './views')
```

### Rendering Templates
```python
@app.get('/profile')
def profile(req, res):
    user = get_user()
    res.render('profile.html', {'user': user})
```

### Template Features
- Template inheritance
- Conditional rendering
- Loops and iterations
- Custom filters and functions
- Variable interpolation

## Static File Serving

### Setting Up Static Files
```python
app.use('/public', app.static('static'))
```

### Accessing Static Files
```
http://localhost:3000/public/css/styles.css
http://localhost:3000/public/js/script.js
http://localhost:3000/public/images/logo.png
```

## Error Handling

### Custom Error Handlers
```python
@app.error(404)
def not_found(req, res, err):
    res.status(404).render('404.html')

@app.error(500)
def server_error(req, res, err):
    res.status(500).render('500.html', {'error': str(err)})
```

### Global Error Handling
```python
def error_middleware(err, req, res, next):
    print(f"Error: {err}")
    res.status(500).send('An error occurred')

app.use(error_middleware)
```

### Try-Catch in Route Handlers
```python
@app.get('/users/:id')
def get_user(req, res):
    try:
        user_id = req.params.get('id')
        user = find_user(user_id)
        if not user:
            return res.status(404).send('User not found')
        res.json(user)
    except Exception as e:
        res.status(500).send(f'Error: {str(e)}')
```

## Sessions & Cookies

### Cookie Management
```python
@app.get('/set-cookie')
def set_cookie(req, res):
    res.set_cookie('username', 'john', {'httpOnly': True, 'maxAge': 3600})
    res.send('Cookie set')

@app.get('/get-cookie')
def get_cookie(req, res):
    username = req.cookies.get('username', 'Guest')
    res.send(f'Hello, {username}')
```

### Session Management
```python
app.use(session_middleware)

@app.get('/login')
def login(req, res):
    req.session['user_id'] = 123
    res.redirect('/dashboard')

@app.get('/dashboard')
def dashboard(req, res):
    if 'user_id' not in req.session:
        return res.redirect('/login')
    user = get_user(req.session['user_id'])
    res.render('dashboard.html', {'user': user})
```

## Development Features

### Hot Reloading
Using the built-in development server:
```bash
python dev.py app.py
```

### Debug Logging
```python
app.set('debug', True)
```

### Environment Configuration
```python
if app.get('env') == 'development':
    app.use(development_middleware)
else:
    app.use(production_middleware)
```

## API Development Features

### CORS Support
```python
app.use(cors_middleware)
```

### JSON Parsing and Validation
```python
app.use(json_middleware)

@app.post('/api/users')
def create_user(req, res):
    user_data = req.body
    # Validate user data
    new_user = create_user(user_data)
    res.status(201).json(new_user)
```

### Response Transformers
```python
def api_transformer(req, res, next):
    old_json = res.json
    def new_json(data):
        return old_json({'status': 'success', 'data': data})
    res.json = new_json
    next()

app.use('/api', api_transformer)
```

## Performance Features

### Router Optimization
Fast path matching with optimized parameter extraction.

### Request Processing
Efficient middleware chain execution with early termination.

### Response Handling
Optimized response generation and delivery.

## Integration Capabilities

### Database Support
Easy integration with any database library:

```python
# SQLAlchemy example
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)

@app.get('/users')
def get_users(req, res):
    session = Session()
    users = session.query(User).all()
    res.json([user.to_dict() for user in users])
    session.close()
```

### Authentication Libraries
Integrate with any authentication system:

```python
# JWT example
import jwt

def jwt_middleware(req, res, next):
    token = req.headers.get('Authorization', '').replace('Bearer ', '')
    if token:
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            req.user = payload
        except:
            pass
    next()

app.use(jwt_middleware)
```

### File Upload
Support for multipart form data and file uploads:

```python
@app.post('/upload')
def upload_file(req, res):
    file = req.files.get('image')
    if file:
        filename = secure_filename(file.filename)
        file.save(f'uploads/{filename}')
        res.json({'filename': filename})
    else:
        res.status(400).send('No file uploaded')
```

## Advanced Features

### Sub-Applications (Router)
Create modular applications with sub-routers:

```python
users_router = router()

@users_router.get('/')
def get_users(req, res):
    res.json(users)

@users_router.get('/:id')
def get_user(req, res):
    user_id = req.params.get('id')
    res.json(find_user(user_id))

app.use('/api/users', users_router)
```

### WebSocket Support
Integration with WebSocket libraries for real-time applications.

### Async/Await Support
Support for async route handlers for non-blocking I/O operations. 