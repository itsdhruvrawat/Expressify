import json
from typing import Dict, Any, Optional, Union, List
import datetime


class Response:
    """
    Response class to handle HTTP responses
    Similar to Express.js res object
    """
    
    def __init__(self):
        self.status_code = 200
        self.headers = {
            'Content-Type': 'text/plain',
        }
        self.body = None
        self._is_sent = False
    
    def status(self, code: int):
        """
        Set the HTTP status code
        """
        self.status_code = code
        return self
    
    def set(self, header: str, value: str):
        """
        Set an HTTP header
        """
        self.headers[header] = value
        return self
    
    def append(self, header: str, value: str):
        """
        Append to an HTTP header
        Similar to Express's res.append()
        """
        if header in self.headers:
            current_value = self.headers[header]
            if isinstance(current_value, list):
                current_value.append(value)
            else:
                self.headers[header] = [current_value, value]
        else:
            self.headers[header] = value
        return self
    
    def type(self, content_type: str):
        """
        Set the Content-Type header
        """
        self.headers['Content-Type'] = content_type
        return self
    
    def json(self, data: Any):
        """
        Send a JSON response
        """
        self.headers['Content-Type'] = 'application/json'
        self.body = json.dumps(data).encode('utf-8')
        self._is_sent = True
        return self
    
    def send(self, data: Union[str, bytes, dict] = ''):
        """
        Send a response
        """
        if self._is_sent:
            raise RuntimeError('Response already sent')
            
        if isinstance(data, dict):
            # Auto-convert dict to JSON
            return self.json(data)
            
        if isinstance(data, str):
            self.body = data.encode('utf-8')
        elif isinstance(data, bytes):
            self.body = data
        else:
            self.body = str(data).encode('utf-8')
            
        self._is_sent = True
        return self
    
    def redirect(self, url: str, status_code: int = 302):
        """
        Redirect to another URL
        """
        self.status_code = status_code
        self.headers['Location'] = url
        self.body = f'Redirecting to {url}'.encode('utf-8')
        self._is_sent = True
        return self
    
    def send_file(self, filename: str, content_type: Optional[str] = None):
        """
        Send a file
        """
        with open(filename, 'rb') as f:
            content = f.read()
            
        if content_type:
            self.headers['Content-Type'] = content_type
        else:
            # Try to guess content type based on extension
            ext = filename.split('.')[-1].lower()
            content_types = {
                'html': 'text/html',
                'css': 'text/css',
                'js': 'application/javascript',
                'json': 'application/json',
                'png': 'image/png',
                'jpg': 'image/jpeg',
                'jpeg': 'image/jpeg',
                'gif': 'image/gif',
                'svg': 'image/svg+xml',
                'ico': 'image/x-icon',
            }
            self.headers['Content-Type'] = content_types.get(ext, 'application/octet-stream')
            
        self.body = content
        self._is_sent = True
        return self
    
    def render(self, template: str, data: Dict[str, Any] = None, engine=None):
        """
        Render a template with data
        """
        try:
            from expressify.lib.template import get_default_engine
            
            if data is None:
                data = {}
                
            # Use provided engine or try to get default
            renderer = engine or get_default_engine()
            
            if renderer is None:
                raise ValueError("Template engine not configured. Use expressify.lib.template.create_engine() to configure a template engine.")
            
            content = renderer.render(template, data)
            self.headers['Content-Type'] = 'text/html'
            self.body = content.encode('utf-8')
            self._is_sent = True
            return self
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.status(500).send(f"Template rendering error: {str(e)}")
            return self
    
    def format(self, formats_dict: Dict[str, Any]):
        """
        Content negotiation based on Accept header
        Similar to Express's res.format()
        """
        # Get the request object from the calling context
        import inspect
        frame = inspect.currentframe().f_back
        request = frame.f_locals.get('req')
        
        if not request:
            return self.status(406).send('Not Acceptable')
            
        accept = request.get_header('Accept', '*/*')
        
        # Default case
        if 'default' in formats_dict:
            default_handler = formats_dict['default']
        else:
            default_handler = lambda: self.status(406).send('Not Acceptable')
            
        # Try to match content types
        for format_type, handler in formats_dict.items():
            if format_type == 'default':
                continue
                
            content_type = {
                'html': 'text/html',
                'json': 'application/json',
                'text': 'text/plain',
                'xml': 'application/xml'
            }.get(format_type, format_type)
            
            if content_type in accept or '*/*' in accept:
                self.type(content_type)
                if callable(handler):
                    handler()
                else:
                    self.send(handler)
                return self
                
        # No match found, use default
        if callable(default_handler):
            default_handler()
        else:
            self.send(default_handler)
            
        return self
    
    def cookie(self, name: str, value: str, options: Dict[str, Any] = None):
        """
        Set a cookie
        Similar to Express's res.cookie()
        """
        options = options or {}
        
        cookie_str = f"{name}={value}"
        
        if 'maxAge' in options:
            expires = datetime.datetime.now() + datetime.timedelta(milliseconds=options['maxAge'])
            options['expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
            
        if 'expires' in options:
            cookie_str += f"; Expires={options['expires']}"
            
        if 'domain' in options:
            cookie_str += f"; Domain={options['domain']}"
            
        if 'path' in options:
            cookie_str += f"; Path={options['path']}"
        else:
            cookie_str += "; Path=/"
            
        if options.get('secure', False):
            cookie_str += "; Secure"
            
        if options.get('httpOnly', False):
            cookie_str += "; HttpOnly"
            
        self.append('Set-Cookie', cookie_str)
        return self
    
    def clear_cookie(self, name: str, options: Dict[str, Any] = None):
        """
        Clear a cookie
        Similar to Express's res.clearCookie()
        """
        options = options or {}
        options['expires'] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        options['maxAge'] = 0
        
        return self.cookie(name, '', options)
    
    def end(self):
        """
        End the response without any data
        Similar to Express's res.end()
        """
        if not self._is_sent:
            self.body = b''
            self._is_sent = True
        return self 