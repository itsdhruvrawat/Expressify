import pytest  # noqa
import json
from unittest.mock import MagicMock, patch

# Import expressify functions
from expressify import expressify


def test_expressify_instance():
    """Test the creation of an expressify application instance."""
    app = expressify()
    assert app is not None
    assert hasattr(app, 'get')
    assert hasattr(app, 'post')
    assert hasattr(app, 'put')
    assert hasattr(app, 'delete')
    assert hasattr(app, 'patch')
    assert hasattr(app, 'all')


def test_route_registration_decorator():
    """Test registering routes using decorators."""
    app = expressify()
    
    @app.get('/test')
    def test_route(req, res):
        res.send('Test')
    
    # Check that the route was registered
    assert len(app.routes) > 0
    assert any(r['path'] == '/test' and r['method'] == 'GET' for r in app.routes)


def test_route_registration_method():
    """Test registering routes using methods."""
    app = expressify()
    
    def test_route(req, res):
        res.send('Test')
    
    app.get('/test', test_route)
    
    # Check that the route was registered
    assert len(app.routes) > 0
    assert any(r['path'] == '/test' and r['method'] == 'GET' for r in app.routes)


def test_route_with_parameters():
    """Test routes with parameters."""
    app = expressify()
    
    @app.get('/users/:id')
    def get_user(req, res):
        user_id = req.params.get('id')
        res.send(f'User {user_id}')
    
    # Create mock request and response
    req = MagicMock()
    req.params = {'id': '42'}
    
    res = MagicMock()
    
    # Find and call the route handler
    for route in app.routes:
        if route['path'] == '/users/:id' and route['method'] == 'GET':
            route['handler'](req, res)
            break
    
    # Check that res.send was called with the expected argument
    res.send.assert_called_once_with('User 42')


def test_middleware_execution():
    """Test middleware execution."""
    app = expressify()
    
    # Define middleware
    middleware_called = False
    
    def test_middleware(req, res, next):
        nonlocal middleware_called
        middleware_called = True
        req.user = 'test_user'
        next()
    
    @app.get('/protected', middleware=[test_middleware])
    def protected_route(req, res):
        res.send(f'Hello, {req.user}')
    
    # Create mock request and response
    req = MagicMock()
    req.user = None
    
    res = MagicMock()
    
    # Find and call the route handler with middleware
    for route in app.routes:
        if route['path'] == '/protected' and route['method'] == 'GET':
            # Execute middleware chain manually
            middleware = route.get('middleware', [])
            for m in middleware:
                m(req, res, lambda: None)
            route['handler'](req, res)
            break
    
    # Check that middleware was called and modified the request
    assert middleware_called
    assert req.user == 'test_user'
    res.send.assert_called_once_with('Hello, test_user')


def test_json_response():
    """Test JSON response handling."""
    app = expressify()
    
    @app.get('/api/data')
    def get_data(req, res):
        res.json({'name': 'Test', 'value': 42})
    
    # Create mock request and response
    req = MagicMock()
    res = MagicMock()
    
    # Find and call the route handler
    for route in app.routes:
        if route['path'] == '/api/data' and route['method'] == 'GET':
            route['handler'](req, res)
            break
    
    # Check that res.json was called with the expected argument
    res.json.assert_called_once_with({'name': 'Test', 'value': 42})


def test_status_code_setting():
    """Test setting status codes."""
    app = expressify()
    
    @app.post('/api/items')
    def create_item(req, res):
        res.status(201).json({'message': 'Created'})
    
    # Create mock request and response
    req = MagicMock()
    res = MagicMock()
    # Make status return the response object for chaining
    res.status.return_value = res
    
    # Find and call the route handler
    for route in app.routes:
        if route['path'] == '/api/items' and route['method'] == 'POST':
            route['handler'](req, res)
            break
    
    # Check that res.status and res.json were called with the expected arguments
    res.status.assert_called_once_with(201)
    res.json.assert_called_once_with({'message': 'Created'}) 