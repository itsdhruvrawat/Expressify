"""
Expressify - A lightweight Express.js-inspired web framework for Python
"""

from expressify.lib.application import Application
from expressify.lib.router import Router
from expressify.lib.request import Request
from expressify.lib.response import Response
from expressify.lib.middleware import Middleware
from expressify.lib.template import create_engine, get_default_engine

# Create the main application factory
def expressify():
    """
    Create a new expressify application
    Similar to Express.js express() function
    """
    return Application()

# Common HTTP status codes
class HttpStatus:
    # Informational responses
    CONTINUE = 100
    SWITCHING_PROTOCOLS = 101
    PROCESSING = 102
    
    # Successful responses
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # Redirections
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    
    # Client errors
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    CONFLICT = 409
    GONE = 410
    UNSUPPORTED_MEDIA_TYPE = 415
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    
    # Server errors
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

# Version
__version__ = '0.1.0'

# Export public API
__all__ = [
    'expressify', 
    'Application', 
    'Router', 
    'Request', 
    'Response', 
    'Middleware',
    'create_engine',
    'get_default_engine',
    'HttpStatus'
] 