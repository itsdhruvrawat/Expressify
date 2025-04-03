from typing import Callable, Any, Dict, List, Optional
import time
import traceback


class Middleware:
    """
    Middleware class with common middleware functions
    """
    
    @staticmethod
    def json():
        """
        Middleware to parse JSON request bodies
        """
        async def json_middleware(req, res, next):
            if req.headers.get('Content-Type', '').startswith('application/json'):
                # JSON parsing is already handled in the request handler
                pass
            await next()
        return json_middleware
    
    @staticmethod
    def urlencoded(options: Dict[str, Any] = None):
        """
        Middleware to parse URL-encoded request bodies
        """
        if options is None:
            options = {'extended': False}
            
        async def urlencoded_middleware(req, res, next):
            if req.headers.get('Content-Type', '').startswith('application/x-www-form-urlencoded'):
                # Form parsing is already handled in the request handler
                pass
            await next()
        return urlencoded_middleware
    
    @staticmethod
    def cors(origins: List[str] = None, methods: List[str] = None, headers: List[str] = None):
        """
        Middleware to handle CORS (Cross-Origin Resource Sharing)
        """
        if origins is None:
            origins = ['*']
        if methods is None:
            methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS']
        if headers is None:
            headers = ['Content-Type', 'Authorization']
            
        async def cors_middleware(req, res, next):
            # Set CORS headers
            if isinstance(origins, list):
                res.set('Access-Control-Allow-Origin', ','.join(origins))
            else:
                res.set('Access-Control-Allow-Origin', origins)
                
            res.set('Access-Control-Allow-Methods', ','.join(methods))
            res.set('Access-Control-Allow-Headers', ','.join(headers))
            
            # Handle OPTIONS request for preflight
            if req.method == 'OPTIONS':
                return res.status(204).send()
                
            await next()
        
        return cors_middleware
    
    @staticmethod
    def logger(format_string: str = ':method :url :status :response-time ms'):
        """
        Middleware to log requests
        """
        async def logger_middleware(req, res, next):
            start_time = time.time()
            
            # Store original send method to intercept it
            original_send = res.send
            
            def send_interceptor(data):
                # Calculate response time
                response_time = time.time() - start_time
                
                # Format log message
                log_message = format_string
                log_message = log_message.replace(':method', req.method)
                log_message = log_message.replace(':url', req.path)
                log_message = log_message.replace(':status', str(res.status_code))
                log_message = log_message.replace(':response-time', f"{response_time*1000:.2f}")
                
                print(log_message)
                
                # Call the original send method
                return original_send(data)
                
            # Replace the send method with our interceptor
            res.send = send_interceptor
            
            # Continue to the next middleware/route handler
            await next()
        
        return logger_middleware
    
    @staticmethod
    def error_handler():
        """
        Middleware to handle errors
        """
        async def error_middleware(err, req, res, next):
            # Log the error
            print(f"Error: {str(err)}")
            traceback.print_exc()
            
            # Send error response
            if not res._is_sent:
                res.status(500).json({
                    'error': str(err),
                    'message': 'Internal Server Error'
                })
        return error_middleware
    
    @staticmethod
    def static(root_path: str, options: Dict[str, Any] = None):
        """
        Middleware to serve static files
        """
        import os
        import mimetypes
        
        if options is None:
            options = {}
            
        async def static_middleware(req, res, next):
            if req.method != 'GET' and req.method != 'HEAD':
                return await next()
                
            # Strip query string
            path = req.path.split('?')[0]
            
            # Determine file path
            file_path = os.path.join(root_path, path.lstrip('/'))
            
            # Check if file exists
            if os.path.isfile(file_path):
                try:
                    # Determine content type
                    content_type, _ = mimetypes.guess_type(file_path)
                    
                    # Serve the file
                    return res.send_file(file_path, content_type)
                except Exception as e:
                    print(f"Error serving static file {file_path}: {str(e)}")
            
            # If we get here, either the file doesn't exist or there was an error
            await next()
            
        return static_middleware
    
    @staticmethod
    def cookie_parser(secret: str = None):
        """
        Middleware to parse cookies in request
        Similar to Express.js cookie-parser
        """
        import hashlib
        import hmac
        
        async def cookie_middleware(req, res, next):
            # Cookies are already parsed in the Request class
            
            # If a secret is provided, also verify signed cookies
            if secret and hasattr(req, 'cookies'):
                req.signedCookies = {}
                
                for name, value in req.cookies.items():
                    if name.endswith('.sig') and name[:-4] in req.cookies:
                        # This is a signature cookie
                        continue
                        
                    # Check if we have a signature for this cookie
                    sig_name = f"{name}.sig"
                    if sig_name in req.cookies:
                        # Verify the signature
                        expected_sig = hmac.new(
                            secret.encode('utf-8'),
                            req.cookies[name].encode('utf-8'),
                            hashlib.sha256
                        ).hexdigest()
                        
                        if hmac.compare_digest(expected_sig, req.cookies[sig_name]):
                            # Signature is valid, add to signed cookies
                            req.signedCookies[name] = req.cookies[name]
                        else:
                            # Invalid signature, add as false
                            req.signedCookies[name] = False
            
            await next()
            
        return cookie_middleware
    
    @staticmethod
    def session(options: Dict[str, Any] = None):
        """
        Simple in-memory session middleware
        Similar to Express.js express-session
        """
        if options is None:
            options = {}
            
        # Default options
        secret = options.get('secret', 'expressify-secret')
        cookie_name = options.get('name', 'connect.sid')
        cookie_options = options.get('cookie', {'path': '/', 'httpOnly': True, 'maxAge': 86400000})  # 1 day
        
        # Session store
        session_store = {}
        
        async def session_middleware(req, res, next):
            # Get or generate session ID
            session_id = None
            if hasattr(req, 'cookies') and cookie_name in req.cookies:
                session_id = req.cookies[cookie_name]
                
            if not session_id or session_id not in session_store:
                # Generate a new session ID
                import uuid
                session_id = str(uuid.uuid4())
                session_store[session_id] = {}
                
                # Set the cookie
                res.cookie(cookie_name, session_id, cookie_options)
            
            # Attach session to request
            req.session = session_store[session_id]
            
            # Continue to next middleware
            await next()
            
        return session_middleware
    
    @staticmethod
    def body_parser():
        """
        Middleware that combines json and urlencoded parsers
        Similar to Express.js body-parser
        """
        json_parser = Middleware.json()
        urlencoded_parser = Middleware.urlencoded()
        
        async def body_parser_middleware(req, res, next):
            # Apply both parsers in sequence
            async def next_json():
                await urlencoded_parser(req, res, next)
                
            await json_parser(req, res, next_json)
            
        return body_parser_middleware
    
    @staticmethod
    def compression(level: int = 6):
        """
        Middleware to compress response bodies
        Similar to Express.js compression
        """
        import gzip
        
        async def compression_middleware(req, res, next):
            # Store original send method
            original_send = res.send
            
            def send_interceptor(data):
                # Check if client accepts gzip encoding
                accept_encoding = req.headers.get('accept-encoding', '')
                
                if 'gzip' in accept_encoding and len(data) > 300:  # Only compress if worth it
                    # Compress the data
                    if isinstance(data, str):
                        compressed_data = gzip.compress(data.encode('utf-8'), level)
                    elif isinstance(data, bytes):
                        compressed_data = gzip.compress(data, level)
                    else:
                        compressed_data = gzip.compress(str(data).encode('utf-8'), level)
                    
                    # Set headers
                    res.set('Content-Encoding', 'gzip')
                    res.set('Vary', 'Accept-Encoding')
                    
                    # Send compressed data
                    return original_send(compressed_data)
                
                # No compression, send as normal
                return original_send(data)
            
            # Replace send method
            res.send = send_interceptor
            
            await next()
            
        return compression_middleware 