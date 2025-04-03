from typing import Dict, Any, Optional, Union, List
from urllib.parse import urlparse


class Request:
    """
    Request class to handle HTTP requests
    Similar to Express.js req object
    """
    
    def __init__(self, method: str, path: str, params: Dict[str, str], query: Dict[str, list],
                 headers: Dict[str, str], body: Any = None):
        self.method = method
        self.path = path
        self.params = params  # URL parameters
        self.query = self._flatten_query(query)  # Query parameters
        self.headers = headers  # HTTP headers (lowercased)
        self.body = body  # Request body
        self.cookies = self._parse_cookies()
        self.originalUrl = path  # Original URL, like Express
        
        # Parse URL components
        parsed_url = urlparse(path)
        self.baseUrl = ""  # Will be set by router if path is mounted
        self.url = path
        self.hostname = headers.get('host', '').split(':')[0]
        self.port = headers.get('host', '').split(':')[1] if ':' in headers.get('host', '') else None
        self.protocol = headers.get('x-forwarded-proto', 'http')
        self.secure = self.protocol == 'https'
        self.ip = headers.get('x-forwarded-for', headers.get('remote-addr', ''))
        
    def _flatten_query(self, query: Dict[str, list]) -> Dict[str, Union[str, list]]:
        """
        Flatten query parameters that have a single value
        """
        result = {}
        for key, values in query.items():
            if len(values) == 1:
                result[key] = values[0]
            else:
                result[key] = values
        return result
    
    def _parse_cookies(self) -> Dict[str, str]:
        """
        Parse cookies from the Cookie header
        """
        cookies = {}
        cookie_header = self.headers.get('cookie', '')
        
        if cookie_header:
            cookie_pairs = cookie_header.split(';')
            for pair in cookie_pairs:
                if '=' in pair:
                    key, value = pair.strip().split('=', 1)
                    cookies[key] = value
                    
        return cookies
        
    def get(self, field: str, default: Any = None) -> Any:
        """
        Get a value from headers, query params, or body
        """
        if field in self.headers:
            return self.headers[field]
        elif field in self.query:
            return self.query[field]
        elif isinstance(self.body, dict) and field in self.body:
            return self.body[field]
        return default
    
    def get_header(self, name: str, default: Any = None) -> str:
        """
        Get a request header (case-insensitive)
        Similar to Express's req.get()
        """
        name = name.lower()
        return self.headers.get(name, default)
    
    def is_json(self) -> bool:
        """
        Check if the request has a JSON content-type
        """
        content_type = self.get_header('Content-Type', '')
        return 'application/json' in content_type.lower()
    
    def is_form(self) -> bool:
        """
        Check if the request has a form content-type
        """
        content_type = self.get_header('Content-Type', '')
        return 'application/x-www-form-urlencoded' in content_type.lower()
    
    def accepts(self, mime_type: str) -> bool:
        """
        Check if the request accepts a specific MIME type
        Similar to Express's req.accepts()
        """
        accept_header = self.get_header('Accept', '*/*')
        
        # Check for explicit match
        if mime_type in accept_header:
            return True
            
        # Check for wildcard match
        if '*/*' in accept_header:
            return True
            
        # Check for type/* match
        mime_type_parts = mime_type.split('/')
        if len(mime_type_parts) == 2:
            type_wildcard = f"{mime_type_parts[0]}/*"
            if type_wildcard in accept_header:
                return True
                
        return False
    
    def __repr__(self) -> str:
        return f"<Request {self.method} {self.path}>" 