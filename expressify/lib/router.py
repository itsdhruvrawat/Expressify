from typing import Dict, List, Callable, Any, Optional, Union, Tuple

class Router:
    """
    Router class to handle route definitions and matching
    Similar to Express.js Router for creating modular route handlers
    """
    def __init__(self, root_path: str = ''):
        self.routes = []
        self.middleware = []
        self.root_path = root_path.rstrip('/')  # Remove trailing slash for consistency
    
    def _add_route(self, method: str, path: str, handler: Callable):
        """Add a route with method, path and handler"""
        # Store normalized path (ensure it starts with /)
        normalized_path = path if path.startswith('/') else f'/{path}'
        # Add the route with full path including root_path prefix
        full_path = f"{self.root_path}{normalized_path}"
        self.routes.append((method, full_path, handler))
        return self
    
    def get(self, path: str, handler: Callable = None):
        """Route HTTP GET requests to the specified path with the specified callback functions"""
        # Support for decorator style routes
        if handler is None:
            # Use as decorator
            def decorator(func):
                self._add_route('GET', path, func)
                return func
            return decorator
        # Use as normal method
        return self._add_route('GET', path, handler)
    
    def post(self, path: str, handler: Callable = None):
        """Route HTTP POST requests to the specified path with the specified callback functions"""
        if handler is None:
            def decorator(func):
                self._add_route('POST', path, func)
                return func
            return decorator
        return self._add_route('POST', path, handler)
    
    def put(self, path: str, handler: Callable = None):
        """Route HTTP PUT requests to the specified path with the specified callback functions"""
        if handler is None:
            def decorator(func):
                self._add_route('PUT', path, func)
                return func
            return decorator
        return self._add_route('PUT', path, handler)
    
    def delete(self, path: str, handler: Callable = None):
        """Route HTTP DELETE requests to the specified path with the specified callback functions"""
        if handler is None:
            def decorator(func):
                self._add_route('DELETE', path, func)
                return func
            return decorator
        return self._add_route('DELETE', path, handler)
    
    def patch(self, path: str, handler: Callable = None):
        """Route HTTP PATCH requests to the specified path with the specified callback functions"""
        if handler is None:
            def decorator(func):
                self._add_route('PATCH', path, func)
                return func
            return decorator
        return self._add_route('PATCH', path, handler)
    
    def all(self, path: str, handler: Callable = None):
        """Route requests of all HTTP methods to the specified path with the specified callback functions"""
        if handler is None:
            def decorator(func):
                for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                    self._add_route(method, path, func)
                return func
            return decorator
        
        for method in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
            self._add_route(method, path, handler)
        return self
    
    def use(self, path_or_middleware=None, middleware=None):
        """
        Mount middleware function(s) or router at the specified path
        
        Routes use:
        - If path_or_middleware is callable and middleware is None: Mount middleware with no path
        - If path_or_middleware is a string and middleware is callable: Mount middleware at path
        - If path_or_middleware is a Router instance: Mount router routes at root
        - If path_or_middleware is string and middleware is Router: Mount router at path
        - If path_or_middleware is None: Used as a decorator
        """
        # Used as a decorator - @router.use
        if path_or_middleware is None:
            def decorator(middleware_func):
                self.middleware.append(middleware_func)
                return middleware_func
            return decorator
        
        # Called as app.use(middleware_func)
        if callable(path_or_middleware) and middleware is None:
            self.middleware.append(path_or_middleware)
            return self
            
        # Called as app.use('/path', middleware_func)
        if isinstance(path_or_middleware, str) and callable(middleware):
            # Store middleware with path info for later filtering
            self.middleware.append((path_or_middleware, middleware))
            return self
            
        # Called as app.use(router)
        if hasattr(path_or_middleware, 'routes') and middleware is None:
            # Mount another router at root path
            for method, path, handler in path_or_middleware.routes:
                self._add_route(method, path, handler)
            # Add any middleware from the router
            self.middleware.extend(path_or_middleware.middleware)
            return self
            
        # Called as app.use('/path', router)
        if isinstance(path_or_middleware, str) and hasattr(middleware, 'routes'):
            route_prefix = path_or_middleware
            router = middleware
            # Mount router at the specified path
            for method, path, handler in router.routes:
                # Add path prefix to each route
                prefixed_path = path if route_prefix.endswith('/') and path.startswith('/') else f"{route_prefix}{path}"
                self._add_route(method, prefixed_path, handler)
            # Add any middleware from the router
            # TODO: Handle path-specific middleware from the router
            self.middleware.extend(router.middleware)
            return self
            
        return self
    
    def route(self, path: str):
        """
        Create a new router for the specified route path
        This allows chaining multiple HTTP methods for the same path
        """
        route_handler = Router(path)
        self.use(route_handler)
        return route_handler
    
    def find_route(self, method: str, path: str) -> Tuple[Optional[Callable], Dict[str, str]]:
        """Find a matching route handler and extract URL parameters"""
        for route_method, route_path, handler in self.routes:
            if route_method != method:
                continue
                
            # Check for exact match
            if route_path == path:
                return handler, {}
                
            # Check for parameterized routes (basic implementation)
            route_parts = route_path.split('/')
            path_parts = path.split('/')
            
            if len(route_parts) != len(path_parts):
                continue
                
            params = {}
            match = True
            
            for route_part, path_part in zip(route_parts, path_parts):
                if route_part.startswith(':'):
                    # This is a parameter
                    param_name = route_part[1:]
                    params[param_name] = path_part
                elif route_part != path_part:
                    match = False
                    break
                    
            if match:
                return handler, params
                
        return None, {} 