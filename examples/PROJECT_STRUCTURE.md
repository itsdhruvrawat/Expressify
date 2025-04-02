# Expressify Project Structure

This document explains the organization of the Expressify framework and examples.

## Repository Structure

```
expressify/
├── expressify/             # Core framework source code
│   ├── __init__.py         # Main package initialization
│   ├── app.py              # The Expressify application class
│   ├── request.py          # Request object implementation
│   ├── response.py         # Response object implementation
│   ├── router.py           # Routing implementation
│   └── lib/                # Framework utilities and extensions
│       ├── middleware.py   # Built-in middleware functions
│       ├── template.py     # Template rendering support
│       └── static.py       # Static file handling utilities
│
├── examples/               # Example applications
│   ├── 01-hello-world/     # Basic hello world example
│   ├── 02-routing/         # Routing examples
│   ├── 03-middleware/      # Middleware examples
│   ├── 04-request-response/ # Request/response handling examples
│   ├── 05-templates/       # Template rendering examples
│   └── 06-static-files/    # Static file serving examples
│
├── docs/                   # Documentation
│   ├── index.html          # Main documentation page
│   └── pages/              # Documentation sections
│       ├── api-reference.html  # API reference documentation
│       ├── examples.html       # Example documentation
│       └── getting-started.html  # Getting started guide
│
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
│
├── requirements.txt        # Project dependencies
├── requirements-dev.txt    # Development dependencies
├── setup.py                # Package installation script
├── dev.py                  # Development server with hot reloading
├── README.md               # Project overview
├── BUGS_AND_ISSUES.md      # Known bugs and issues tracking
├── CONTRIBUTING.md         # Contribution guidelines
└── LICENSE                 # MIT License file
```

## Examples Structure

Each example directory follows a similar structure:

```
[example-name]/
├── app.py          # Main application file
├── public/         # Static files (if applicable)
│   ├── css/        # Stylesheets
│   ├── js/         # JavaScript files
│   └── images/     # Image files
├── views/          # Template files (if applicable)
└── README.md       # Example-specific documentation
```

## Core Components

### Application (`app.py`)

The main application class (`Expressify`) that handles:
- HTTP server initialization
- Route registration
- Middleware management
- Application settings

### Request (`request.py`)

The `Request` class represents an incoming HTTP request with properties for:
- HTTP method
- URL path and query parameters
- Headers
- Request body
- Route parameters

### Response (`response.py`)

The `Response` class represents an outgoing HTTP response with methods for:
- Setting status codes
- Adding headers
- Sending different content types (JSON, HTML, etc.)
- Redirecting

### Router (`router.py`)

Handles route matching and dispatching requests to the appropriate handlers.

### Middleware (`lib/middleware.py`)

Contains built-in middleware functions for:
- CORS handling
- Request body parsing
- Authentication
- Logging
- Static file serving

### Templates (`lib/template.py`)

Provides template rendering capabilities using the Jinja2 template engine.

### Static Files (`lib/static.py`)

Handles serving static files like CSS, JavaScript, and images.

## Development Workflow

1. **Framework Development**:
   - Modify files in the `expressify/` directory
   - Run tests to verify changes

2. **Example Development**:
   - Create or modify examples to demonstrate features
   - Test examples with the latest framework code

3. **Documentation**:
   - Update documentation in the `docs/` directory
   - Ensure examples and documentation stay in sync

## Testing

Tests are organized in the `tests/` directory:

- **Unit Tests**: Tests for individual components
- **Integration Tests**: Tests for how components work together
- **Example Tests**: Tests to ensure examples function correctly

## Future Roadmap

Areas being developed:
- Advanced middleware support
- Enhanced template capabilities
- WebSocket support
- Database integration utilities
- CLI tools for project scaffolding 