"""
Middleware Utilities for Expressify

This module provides common middleware functions that can be imported and used in Expressify applications.
"""

import time
import json
from functools import wraps
import os

# Logger Middleware
def logger(log_format="basic"):
    """
    Creates a logging middleware function
    
    Args:
        log_format (str): Format style ("basic", "detailed", or "json")
    
    Returns:
        function: Middleware function for logging
    """
    def middleware(req, res, next):
        start_time = time.time()
        
        # Log request
        if log_format == "basic":
            print(f"[REQUEST] {req.method} {req.path}")
        elif log_format == "detailed":
            print(f"[REQUEST] {req.method} {req.path}")
            print(f"  Headers: {req.headers}")
            if hasattr(req, 'body') and req.body:
                print(f"  Body: {req.body[:200]}...")
        elif log_format == "json":
            log_data = {
                "type": "request",
                "method": req.method,
                "path": req.path,
                "headers": req.headers,
                "timestamp": time.time()
            }
            print(json.dumps(log_data))
        
        # Call next middleware
        result = next()
        
        # Calculate duration
        duration = (time.time() - start_time) * 1000  # Convert to ms
        
        # Log response
        if log_format == "basic":
            print(f"[RESPONSE] {res.status_code} - {duration:.2f}ms")
        elif log_format == "detailed":
            print(f"[RESPONSE] {res.status_code} - {duration:.2f}ms")
            print(f"  Headers: {res.headers}")
        elif log_format == "json":
            log_data = {
                "type": "response",
                "status_code": res.status_code,
                "duration_ms": round(duration, 2),
                "headers": res.headers,
                "timestamp": time.time()
            }
            print(json.dumps(log_data))
        
        return result
    
    return middleware

# CORS Middleware
def cors(origin="*", methods=None, headers=None, credentials=False):
    """
    Creates a CORS middleware function
    
    Args:
        origin (str): Allowed origin, defaults to "*" (all origins)
        methods (list): List of allowed HTTP methods
        headers (list): List of allowed headers
        credentials (bool): Whether to allow credentials
    
    Returns:
        function: Middleware function for CORS
    """
    if methods is None:
        methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    
    if headers is None:
        headers = ["Content-Type", "Authorization"]
    
    def middleware(req, res, next):
        # Set CORS headers
        res.set_header("Access-Control-Allow-Origin", origin)
        res.set_header("Access-Control-Allow-Methods", ", ".join(methods))
        res.set_header("Access-Control-Allow-Headers", ", ".join(headers))
        
        if credentials:
            res.set_header("Access-Control-Allow-Credentials", "true")
        
        # Handle preflight request
        if req.method == "OPTIONS":
            return res.status(204).send("")
        
        # Call next middleware
        return next()
    
    return middleware

# JSON Parser Middleware
def json_parser():
    """
    Creates a middleware function for parsing JSON request bodies
    
    Returns:
        function: Middleware function for JSON parsing
    """
    def middleware(req, res, next):
        content_type = req.get_header("content-type", "")
        
        if "application/json" in content_type and hasattr(req, "body") and req.body:
            try:
                req.json = json.loads(req.body)
            except json.JSONDecodeError as e:
                return res.status(400).json({
                    "error": "Invalid JSON",
                    "message": str(e)
                })
        
        return next()
    
    return middleware

# Static Files Middleware
def static_files(directory, cache_control=None):
    """
    Creates a middleware function for serving static files
    
    Args:
        directory (str): Directory containing static files
        cache_control (str): Cache-Control header value
    
    Returns:
        function: Middleware function for serving static files
    """
    # Ensure directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Map file extensions to content types
    CONTENT_TYPES = {
        ".html": "text/html",
        ".css": "text/css",
        ".js": "application/javascript",
        ".json": "application/json",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".svg": "image/svg+xml",
        ".ico": "image/x-icon",
        ".txt": "text/plain"
    }
    
    def get_content_type(file_path):
        """Determine content type based on file extension"""
        _, ext = os.path.splitext(file_path)
        return CONTENT_TYPES.get(ext.lower(), "application/octet-stream")
    
    def middleware(req, res, next):
        if req.method != "GET":
            return next()
        
        # Remove any query parameters
        path = req.path.split("?")[0]
        
        # Check if path starts with /static or is just a filename
        if path.startswith("/static/"):
            file_path = os.path.join(directory, path[8:])  # Remove "/static/" prefix
        else:
            # Don't try to serve non-static files
            return next()
        
        # Normalize path to prevent directory traversal attacks
        norm_path = os.path.normpath(file_path)
        if not norm_path.startswith(os.path.abspath(directory)):
            return res.status(403).json({
                "error": "Forbidden",
                "message": "Access denied"
            })
        
        # Check if file exists
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            return next()  # Let next middleware handle it
        
        try:
            # Set content type based on file extension
            content_type = get_content_type(file_path)
            res.set_header("Content-Type", content_type)
            
            # Set cache header if provided
            if cache_control:
                res.set_header("Cache-Control", cache_control)
            
            # Read file and send response
            with open(file_path, "rb") as f:
                content = f.read()
            
            return res.send(content)
        except Exception as e:
            return res.status(500).json({
                "error": "Internal Server Error",
                "message": str(e)
            })
    
    return middleware

# Authentication Middleware
def auth(strategy="bearer", secret=None, header_name="authorization"):
    """
    Creates an authentication middleware function
    
    Args:
        strategy (str): Authentication strategy ("bearer", "api-key", "basic")
        secret (str): Secret token or key for validation
        header_name (str): Name of the header containing auth info
    
    Returns:
        function: Middleware function for authentication
    """
    def middleware(req, res, next):
        auth_header = req.get_header(header_name)
        
        if not auth_header:
            return res.status(401).json({
                "error": "Unauthorized",
                "message": f"Missing {header_name} header"
            })
        
        if strategy == "bearer":
            if not auth_header.startswith("Bearer "):
                return res.status(401).json({
                    "error": "Unauthorized",
                    "message": "Invalid authorization format"
                })
            
            token = auth_header[7:]  # Remove "Bearer " prefix
            
            if token != secret:
                return res.status(401).json({
                    "error": "Unauthorized",
                    "message": "Invalid token"
                })
            
            # Add user info to request
            req.user = {"authenticated": True}
            
        elif strategy == "api-key":
            if auth_header != secret:
                return res.status(401).json({
                    "error": "Unauthorized",
                    "message": "Invalid API key"
                })
            
            # Add user info to request
            req.user = {"authenticated": True}
            
        elif strategy == "basic":
            # Implement Basic Authentication
            pass
        
        return next()
    
    return middleware

# Rate Limiter Middleware
def rate_limiter(max_requests=100, window_seconds=60):
    """
    Creates a rate limiting middleware function
    
    Args:
        max_requests (int): Maximum number of requests allowed
        window_seconds (int): Time window in seconds
    
    Returns:
        function: Middleware function for rate limiting
    """
    # Store request timestamps for each client
    clients = {}
    
    def middleware(req, res, next):
        client_ip = req.get_header("x-forwarded-for") or req.remote_addr
        
        # Initialize client record if doesn't exist
        if client_ip not in clients:
            clients[client_ip] = []
        
        # Get current time
        now = time.time()
        
        # Remove requests outside the window
        clients[client_ip] = [t for t in clients[client_ip] if now - t < window_seconds]
        
        # Check if client has exceeded rate limit
        if len(clients[client_ip]) >= max_requests:
            return res.status(429).json({
                "error": "Too Many Requests",
                "message": f"Rate limit of {max_requests} requests per {window_seconds} seconds exceeded"
            })
        
        # Add current request timestamp
        clients[client_ip].append(now)
        
        # Add rate limit headers
        remaining = max_requests - len(clients[client_ip])
        res.set_header("X-RateLimit-Limit", str(max_requests))
        res.set_header("X-RateLimit-Remaining", str(remaining))
        res.set_header("X-RateLimit-Reset", str(int(now + window_seconds)))
        
        return next()
    
    return middleware

# Error Handler Middleware
def error_handler(include_stack_trace=False):
    """
    Creates an error handling middleware function
    
    Args:
        include_stack_trace (bool): Whether to include stack trace in error response
    
    Returns:
        function: Middleware function for error handling
    """
    def middleware(req, res, next):
        try:
            return next()
        except Exception as e:
            status_code = getattr(e, "status_code", 500)
            error_message = str(e)
            
            # Create error response
            error_response = {
                "error": type(e).__name__,
                "message": error_message
            }
            
            # Include stack trace if enabled and in development mode
            if include_stack_trace:
                import traceback
                error_response["stack"] = traceback.format_exc()
            
            # Log error
            print(f"Error: {error_message}")
            
            return res.status(status_code).json(error_response)
    
    return middleware

# Compression Middleware
def compression():
    """
    Creates a middleware function for response compression
    
    Returns:
        function: Middleware function for compression
    """
    def middleware(req, res, next):
        # Store original send method
        original_send = res.send
        
        # Override send method to add compression
        def compressed_send(content):
            # Check if client accepts gzip encoding
            accept_encoding = req.get_header("accept-encoding", "")
            
            if "gzip" in accept_encoding:
                import gzip
                
                # Don't compress if already compressed or content is too small
                if isinstance(content, str):
                    content = content.encode("utf-8")
                
                if len(content) > 1000:  # Only compress if content is large enough
                    # Compress content
                    compressed = gzip.compress(content)
                    
                    # Set headers
                    res.set_header("Content-Encoding", "gzip")
                    res.set_header("Vary", "Accept-Encoding")
                    
                    # Send compressed content
                    return original_send(compressed)
            
            # If compression not applicable, use original method
            return original_send(content)
        
        # Replace send method
        res.send = compressed_send
        
        return next()
    
    return middleware

# Request Validator Middleware
def validate_request(schema):
    """
    Creates a middleware function for request validation
    
    Args:
        schema (dict): Validation schema for request
    
    Returns:
        function: Middleware function for request validation
    """
    def middleware(req, res, next):
        errors = []
        
        # Validate headers
        if "headers" in schema:
            for header, rules in schema["headers"].items():
                value = req.get_header(header)
                
                if "required" in rules and rules["required"] and not value:
                    errors.append(f"Missing required header: {header}")
        
        # Validate query parameters
        if "query" in schema:
            for param, rules in schema["query"].items():
                value = req.query.get(param)
                
                if "required" in rules and rules["required"] and not value:
                    errors.append(f"Missing required query parameter: {param}")
        
        # Validate body
        if "body" in schema and hasattr(req, "json"):
            for field, rules in schema["body"].items():
                if "required" in rules and rules["required"] and field not in req.json:
                    errors.append(f"Missing required field in body: {field}")
        
        if errors:
            return res.status(400).json({
                "error": "Validation Error",
                "message": "Request validation failed",
                "details": errors
            })
        
        return next()
    
    return middleware

# Security Headers Middleware
def security_headers():
    """
    Creates a middleware function for adding security headers
    
    Returns:
        function: Middleware function for security headers
    """
    def middleware(req, res, next):
        # Set security headers
        res.set_header("X-Content-Type-Options", "nosniff")
        res.set_header("X-Frame-Options", "DENY")
        res.set_header("X-XSS-Protection", "1; mode=block")
        res.set_header("Strict-Transport-Security", "max-age=31536000; includeSubDomains")
        res.set_header("Content-Security-Policy", "default-src 'self'")
        res.set_header("Referrer-Policy", "strict-origin-when-cross-origin")
        
        return next()
    
    return middleware 