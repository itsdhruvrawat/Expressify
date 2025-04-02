# Known Bugs and Issues

This document tracks known bugs, issues, and limitations in the Expressify framework. We're actively working to resolve these issues, and contributions are welcome!

## Core Framework Issues

### Application (`app.py`)
- [ ] Hot-reloading not working consistently on Windows
- [ ] Application shutdown hooks not properly executing in some cases

### Router (`router.py`)
- [ ] Path parameters with special characters may cause routing issues
- [ ] Route conflict detection doesn't handle some edge cases

### Request/Response (`request.py` & `response.py`)
- [ ] Large file uploads are not properly streamed and may cause memory issues
- [ ] Request body parsing fails with certain content types
- [ ] Response streaming is not fully implemented

## Middleware Issues

### General Middleware
- [ ] Middleware execution order can be inconsistent in complex chains
- [ ] Error handling in middleware doesn't properly propagate in some cases
- [ ] Middleware applied to route groups doesn't work with path parameters

### Static Files Middleware
- [ ] Caching headers not properly implemented
- [ ] Directory traversal protection needs improvement
- [ ] Windows path separators cause issues in static file paths

### Auth Middleware
- [ ] Token validation doesn't handle all JWT edge cases
- [ ] API key authentication doesn't support multiple keys
- [ ] Session-based authentication not fully implemented

### CORS Middleware
- [ ] Doesn't handle all preflight request scenarios
- [ ] Complex origin matching patterns not supported

### Body Parser Middleware
- [ ] JSON parsing fails with deeply nested structures
- [ ] Form data with file uploads not properly handled

## Template Engine Issues

- [ ] Template caching strategy needs optimization
- [ ] Some Jinja2 features not fully supported
- [ ] Template inheritance with complex paths doesn't resolve correctly

## Performance Issues

- [ ] Route matching becomes slow with a large number of routes
- [ ] Memory usage increases significantly under load
- [ ] Concurrent request handling needs optimization

## Platform-Specific Issues

### Windows
- [ ] Path handling inconsistencies
- [ ] File locking issues when serving static files

### macOS
- [ ] Unicode filename issues in static file serving

### Linux
- [ ] Socket handling issues on some distributions

## Documentation Issues

- [ ] Some examples are outdated
- [ ] API documentation incomplete for newer features
- [ ] Inconsistencies between code examples and actual API

## Feature Requests

Features that have been requested but not yet implemented:

- [ ] WebSocket support
- [ ] GraphQL integration
- [ ] Built-in rate limiting
- [ ] Database connection pooling utilities
- [ ] CLI for project scaffolding

## How to Report a New Issue

If you encounter a bug or issue not listed here, please report it on our [GitHub Issues page](https://github.com/itsdhruvrawat/expressify/issues) with the following information:

1. Issue description
2. Steps to reproduce
3. Expected behavior
4. Actual behavior
5. Environment details (OS, Python version, etc.)
6. Code sample demonstrating the issue
7. Stack trace or error messages

## Recently Fixed Issues

- [x] ~~Fixed template rendering error with create_engine~~ (Fixed in v0.1.0)
- [x] ~~Fixed middleware chain termination when next() not called~~ (Fixed in v0.1.0)
- [x] ~~Fixed static file MIME type detection~~ (Fixed in v0.1.0) 