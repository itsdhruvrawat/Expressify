import pytest  # noqa
from unittest.mock import MagicMock, patch
import json

# Import expressify components
from expressify import expressify
from expressify.lib.request import Request
from expressify.lib.response import Response


class TestRequest:
    """Tests for the Request class."""
    
    def test_request_properties(self):
        """Test accessing request properties."""
        # Create a mock HTTP request
        mock_http_request = MagicMock()
        mock_http_request.method = 'GET'
        mock_http_request.path = '/test'
        mock_http_request.query_string = b'name=test&page=1'
        mock_http_request.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer token123'}
        mock_http_request.get_data.return_value = json.dumps({'key': 'value'}).encode('utf-8')
        
        # Create request object
        request = Request(mock_http_request)
        
        # Test basic properties
        assert request.method == 'GET'
        assert request.path == '/test'
        
        # Test query parameters
        assert 'name' in request.query
        assert request.query.get('name') == 'test'
        assert request.query.get('page') == '1'
        
        # Test headers
        assert request.get_header('Content-Type') == 'application/json'
        assert request.get_header('Authorization') == 'Bearer token123'
        
        # Test body parsing
        assert request.is_json() == True
        assert request.body == {'key': 'value'}
    
    def test_params_access(self):
        """Test accessing route parameters."""
        # Create a mock HTTP request
        mock_http_request = MagicMock()
        
        # Create request object with route parameters
        request = Request(mock_http_request)
        request.params = {'id': '42', 'name': 'test'}
        
        # Test params access
        assert request.params.get('id') == '42'
        assert request.params.get('name') == 'test'
        assert request.params.get('missing', 'default') == 'default'


class TestResponse:
    """Tests for the Response class."""
    
    def test_send_string(self):
        """Test sending a string response."""
        # Create a mock HTTP response
        mock_http_response = MagicMock()
        
        # Create response object
        response = Response(mock_http_response)
        
        # Send a string response
        result = response.send('Hello, World!')
        
        # Verify the response was set correctly
        mock_http_response.data = 'Hello, World!'.encode('utf-8')
        mock_http_response.content_type = 'text/html; charset=utf-8'
        
        # Test method chaining
        assert result == response
    
    def test_send_json(self):
        """Test sending a JSON response."""
        # Create a mock HTTP response
        mock_http_response = MagicMock()
        
        # Create response object
        response = Response(mock_http_response)
        
        # Send a JSON response
        data = {'message': 'Success', 'code': 200}
        result = response.json(data)
        
        # Verify the response was set correctly
        mock_http_response.data = json.dumps(data).encode('utf-8')
        mock_http_response.content_type = 'application/json'
        
        # Test method chaining
        assert result == response
    
    def test_status_code(self):
        """Test setting status code."""
        # Create a mock HTTP response
        mock_http_response = MagicMock()
        
        # Create response object
        response = Response(mock_http_response)
        
        # Set status code
        result = response.status(201)
        
        # Verify the status was set correctly
        mock_http_response.status_code = 201
        
        # Test method chaining
        assert result == response
    
    def test_header_setting(self):
        """Test setting response headers."""
        # Create a mock HTTP response
        mock_http_response = MagicMock()
        mock_http_response.headers = {}
        
        # Create response object
        response = Response(mock_http_response)
        
        # Set a header
        result = response.set_header('X-Custom', 'Value')
        
        # Verify the header was set correctly
        assert mock_http_response.headers['X-Custom'] == 'Value'
        
        # Test method chaining
        assert result == response
    
    def test_redirect(self):
        """Test redirect response."""
        # Create a mock HTTP response
        mock_http_response = MagicMock()
        
        # Create response object
        response = Response(mock_http_response)
        
        # Redirect to a URL
        with patch('expressify.lib.response.redirect') as mock_redirect:
            mock_redirect.return_value = 'REDIRECT_RESPONSE'
            result = response.redirect('/other-page')
            
            # Verify redirect was called correctly
            mock_redirect.assert_called_once_with('/other-page')
            
            # Verify the response
            assert result == 'REDIRECT_RESPONSE' 