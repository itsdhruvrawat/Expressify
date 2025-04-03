import inspect
import traceback
import json
from typing import Dict, List, Callable, Any, Optional, Union, Tuple

from expressify.lib.request import Request
from expressify.lib.response import Response
from expressify.lib.middleware import Middleware
from expressify.lib.router import Router

class Application(Router):
    """
    Main application class that extends Router functionality
    Using ASGI with uvicorn for better performance
    """
    def __init__(self):
        super().__init__()
        self.settings = {}
        self.server = None
        
    def set(self, setting: str, value: Any):
        """Configure application settings"""
        self.settings[setting] = value
        return self
        
    async def __call__(self, scope, receive, send):
        """
        ASGI application interface
        """
        if scope["type"] != "http":
            return
            
        # Parse request information
        method = scope["method"]
        path = scope["path"]
        headers = dict([(k.decode('utf-8'), v.decode('utf-8')) for k, v in scope["headers"]])
        query_string = scope.get("query_string", b"").decode('utf-8')
        
        # Parse query parameters
        query = {}
        if query_string:
            import urllib.parse
            parsed_qs = urllib.parse.parse_qs(query_string)
            query = {k: v for k, v in parsed_qs.items()}
        
        # Receive request body
        body = None
        if method in ["POST", "PUT", "PATCH"]:
            body_chunks = []
            more_body = True
            
            while more_body:
                message = await receive()
                body_chunks.append(message.get("body", b""))
                more_body = message.get("more_body", False)
                
            body_data = b"".join(body_chunks)
            
            # Parse body based on content type
            content_type = headers.get("content-type", "")
            
            if body_data:
                if "application/json" in content_type:
                    try:
                        body = json.loads(body_data.decode('utf-8'))
                    except json.JSONDecodeError:
                        body = body_data.decode('utf-8')
                elif "application/x-www-form-urlencoded" in content_type:
                    import urllib.parse
                    body = urllib.parse.parse_qs(body_data.decode('utf-8'))
                else:
                    body = body_data.decode('utf-8')
        
        # Find matching route
        handler, params = self.find_route(method, path)
        
        # Create request and response objects
        request = Request(
            method=method,
            path=path,
            params=params,
            query=query,
            headers=headers,
            body=body
        )
        
        response = Response()
        
        # Process middleware and handler
        try:
            middleware_chain = self.middleware.copy()
            
            # Add handler as the last step in the chain
            async def execute_handler():
                if handler:
                    if inspect.iscoroutinefunction(handler):
                        await handler(request, response)
                    else:
                        handler(request, response)
                else:
                    # No route handler found, send 404
                    response.status(404).send(f"Cannot {method} {path}")
            
            # If we have middleware, process it
            if middleware_chain:
                async def process_chain(index=0):
                    if index >= len(middleware_chain):
                        # End of middleware chain, execute handler
                        await execute_handler()
                        return
                        
                    middleware_item = middleware_chain[index]
                    
                    # Handle both simple middleware and path-specific middleware
                    middleware_func = middleware_item
                    middleware_path = None
                    
                    # Check if middleware is path-specific
                    if isinstance(middleware_item, tuple) and len(middleware_item) == 2:
                        middleware_path, middleware_func = middleware_item
                        
                        # Skip if path doesn't match
                        if not path.startswith(middleware_path):
                            await process_chain(index + 1)
                            return
                    
                    # Create next function that will call the next middleware
                    async def next_step():
                        await process_chain(index + 1)
                    
                    # Execute current middleware
                    if inspect.iscoroutinefunction(middleware_func):
                        await middleware_func(request, response, next_step)
                    else:
                        # Handle non-async middleware
                        result = middleware_func(request, response, next_step)
                        # If result is a coroutine, await it
                        if inspect.iscoroutine(result):
                            await result
                
                # Start the middleware chain
                await process_chain()
            else:
                # No middleware, just execute the handler
                await execute_handler()
            
        except Exception as e:
            traceback.print_exc()
            response.status(500).send(f"Internal Server Error: {str(e)}")
        
        # Send the response
        await send({
            "type": "http.response.start",
            "status": response.status_code,
            "headers": [
                [k.encode('utf-8'), v.encode('utf-8')] 
                for k, v in response.headers.items()
            ],
        })
        
        # Send the response body
        if response.body:
            if isinstance(response.body, str):
                response_body = response.body.encode('utf-8')
            elif isinstance(response.body, bytes):
                response_body = response.body
            else:
                response_body = str(response.body).encode('utf-8')
                
            await send({
                "type": "http.response.body",
                "body": response_body,
                "more_body": False,
            })
        else:
            await send({
                "type": "http.response.body",
                "body": b"",
                "more_body": False,
            })
    
    def listen(self, port, hostname, callback=None):
        """
        Start the uvicorn server
        
        Parameters:
        - port: Required port number to run the server on.
        - hostname: Required hostname to bind to.
        - callback: Optional callback function to be called after the server starts.
        
        Returns:
        - The server thread object if running in a separate thread.
        """
        import uvicorn
        import threading
        
        # Convert port to integer if needed
        port = int(port)
        
        # Create a function to run the server
        def run_server():
            uvicorn.run(self, host=hostname, port=port)
            
        # If we're not in the main thread, start in a new thread
        if threading.current_thread() is not threading.main_thread():
            server_thread = threading.Thread(target=run_server)
            server_thread.daemon = True
            server_thread.start()
            self.server = server_thread
            
            print(f"Expressify server running at http://{hostname}:{port}/")
            
            if callback:
                callback()
                
            return self.server
        else:
            # If we are in the main thread, just run the server directly
            print(f"Expressify server running at http://{hostname}:{port}/")
            
            if callback:
                callback()
                
            uvicorn.run(self, host=hostname, port=port)
    
    def close(self):
        """
        No explicit stop needed for uvicorn when running in a thread
        """
        print("Expressify server has been stopped") 