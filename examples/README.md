# Expressify Framework

**Note: This project is currently under development. Issues and bugs may be present.**

## About

Expressify is a lightweight, Express.js-inspired web framework for Python. It provides a simple and intuitive API for building web applications and APIs with minimal boilerplate.

## Examples

This directory contains example applications demonstrating various features of Expressify:

- **01-hello-world**: Basic "Hello World" example
- **02-routing**: Various routing patterns and HTTP methods
- **03-middleware**: Middleware functions for request/response processing
- **04-request-response**: Request and response object features
- **05-templates**: Template rendering with Jinja2
- **06-static-files**: Serving static files (CSS, JavaScript, images)

## Contributing

We welcome contributions to the Expressify framework! If you encounter bugs, issues, or have feature requests, please:

1. **Report Issues**: Create an issue on GitHub describing what you found
2. **Suggest Improvements**: We appreciate feedback on the API design and documentation
3. **Submit Pull Requests**: Code contributions are welcome

## Common Issues

When running the examples, you might encounter the following issues:

- Template rendering errors: Ensure you have the Jinja2 library installed
- Static files not loading: Check that file paths match your operating system conventions
- Middleware not executing: Verify the order of middleware registration

## Getting Started

To run any example:

```bash
cd examples/[example-directory]
python app.py
```

Most examples will start a server on http://localhost:3000 that you can access in your browser.

See [PROJECT_STRUCTURE.md](./PROJECT_STRUCTURE.md) for a detailed explanation of the project organization.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
