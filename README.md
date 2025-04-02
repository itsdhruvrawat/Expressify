# Expressify

<div align="center">
  <img src="docs/assets/images/expressify.jpeg" alt="Expressify Logo" width="200">
  <h3>A lightweight Express.js-inspired web framework for Python</h3>
  <p>
    <a href="https://express-ify.netlify.app" target="_blank">Documentation</a> •
    <a href="https://github.com/itsdhruvrawat/expressify/issues">Report Bug</a> •
    <a href="https://github.com/itsdhruvrawat/expressify/issues">Request Feature</a>
  </p>
</div>

---

## ⚠️ Development Status

**This project is currently under active development and is not yet ready for production use.**

Issues, bugs, and incomplete features may be present. We welcome feedback, bug reports, and contributions to help improve the framework.

## 🚀 Overview

Expressify is a minimalist web framework for Python inspired by Express.js. It provides a simple and intuitive API for building web applications and APIs with minimal boilerplate.

```python
from expressify import Expressify

app = Expressify()

@app.get('/')
def home(req, res):
    return res.send('Hello from Expressify!')

@app.get('/api/users/:id')
def get_user(req, res):
    user_id = req.params['id']
    return res.json({'id': user_id, 'name': 'John Doe'})

app.listen(port=3000)
```

## 🔥 Features

- **Intuitive Routing**: Define routes using decorators and HTTP method verbs
- **Middleware Support**: Process requests and responses with middleware functions
- **Request/Response Objects**: Simplify HTTP handling with powerful abstractions
- **Template Rendering**: Built-in support for Jinja2 templates
- **Static File Serving**: Easily serve CSS, JavaScript, and image files
- **Error Handling**: Graceful error management and custom error handlers
- **Hot Reloading**: Development server with automatic reloading

## 📋 Documentation

- [Getting Started](docs/pages/getting-started.html)
- [API Reference](docs/pages/api-reference.html)
- [Examples](docs/pages/examples.html)
- [Project Structure](examples/PROJECT_STRUCTURE.md)

## 💻 Installation

```bash
# Not yet available on PyPI
git clone https://github.com/itsdhruvrawat/expressify.git
cd expressify
pip install -e .
```

## 📚 Examples

The `examples/` directory contains various example applications demonstrating different features of the framework:

- Basic routing
- Middleware usage
- Template rendering
- Static file serving
- API development
- Form handling

To run an example:

```bash
cd examples/01-hello-world
python app.py
```

## 🔄 Development Server with Hot Reloading

Expressify comes with a development server that automatically reloads your application when files change, making development faster and more efficient.

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run your application with hot reloading
python dev.py examples/01-hello-world/app.py
```

Features of the development server:
- Detects file changes in real-time
- Automatically restarts your application
- Shows application output in the console
- Works on Windows, macOS, and Linux

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Report Issues**: If you find a bug or have a feature request, please open an issue
2. **Submit Pull Requests**: Code contributions are welcome
3. **Improve Documentation**: Help make the documentation clearer and more comprehensive
4. **Spread the Word**: Star the repository and share it with others

Please see our [contribution guidelines](CONTRIBUTING.md) for more details.

## 🔍 Known Issues

- Template rendering may require additional configuration
- Middleware chaining has some limitations
- Static file serving path resolution is still being refined
- Error handling for certain edge cases needs improvement

See the [BUGS_AND_ISSUES.md](BUGS_AND_ISSUES.md) file for a comprehensive list of known issues and bugs, or visit the [issues page](https://github.com/itsdhruvrawat/expressify/issues) on GitHub.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>Created by <a href="https://github.com/itsdhruvrawat">Dhruv Rawat</a></p>
</div> 