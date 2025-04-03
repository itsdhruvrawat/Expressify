# Contributing to Expressify

Thank you for your interest in contributing to Expressify! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Pull Request Process](#pull-request-process)
- [Coding Guidelines](#coding-guidelines)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How Can I Contribute?

There are many ways to contribute to Expressify:

### Reporting Bugs

- Check if the bug has already been reported in the [GitHub Issues](https://github.com/itsdhruvrawat/expressify/issues).
- If not, create a new issue with a descriptive title and clear description.
- Include steps to reproduce the issue, expected behavior, and actual behavior.
- If possible, include code examples, screenshots, or error messages.

### Suggesting Enhancements

- Check if the enhancement has already been suggested in the [GitHub Issues](https://github.com/itsdhruvrawat/expressify/issues).
- If not, create a new issue with a descriptive title and clear description.
- Describe the enhancement in detail, including use cases and potential implementations.
- Reference any related issues or pull requests.

### Pull Requests

- Start by looking at issues labeled `good first issue` or `help wanted`.
- See our [improvements.md](improvements.md) file for ideas on what could be enhanced.
- Follow the [Pull Request Process](#pull-request-process) described below.

### Documentation

- Help improve the documentation by fixing typos, clarifying explanations, or adding examples.
- Update documentation when you add or modify features.

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Getting Started

1. **Fork the repository**:
   - Visit the [GitHub repository](https://github.com/itsdhruvrawat/expressify)
   - Click the "Fork" button in the top right
   
2. **Clone your fork**:
   ```bash
   git clone https://github.com/itsdhruvrawat/expressify.git
   cd expressify
   ```

3. **Set up the development environment**:
   ```bash
   # Create a virtual environment (optional but recommended)
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install the package in development mode
   pip install -e .
   
   # Install development dependencies
   pip install -r requirements-dev.txt
   ```

## Development Workflow

1. **Create a new branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**: Implement your fixes or features

3. **Write tests**: Ensure your changes are covered by tests

4. **Run the test suite**:
   ```bash
   pytest
   ```

5. **Follow coding standards**:
   - Use consistent naming conventions
   - Write docstrings for functions and classes
   - Format code with [black](https://black.readthedocs.io/)
   - Check code with [flake8](https://flake8.pycqa.org/)

6. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Brief description of your changes"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**:
   - Visit your fork on GitHub
   - Click "Pull Request" and "New Pull Request"
   - Select your branch and provide a description of your changes
   - Submit the pull request

## Pull Request Process

1. Ensure your code meets the [Coding Guidelines](#coding-guidelines) and passes all tests.
2. Update the README.md and/or documentation with details of changes if applicable.
3. The PR should work for Python 3.7 and higher. Ensure it passes CI tests.
4. Include a descriptive title and detailed description of your changes.
5. Reference any related issues using the GitHub issue number (e.g., "Fixes #123").
6. A maintainer will review your PR, request changes if necessary, and merge it when approved.

## Coding Guidelines

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code style.
- Use [Black](https://github.com/psf/black) for code formatting.
- Use [isort](https://pycqa.github.io/isort/) for import sorting.
- Use [docstrings](https://peps.python.org/pep-0257/) for all public functions, classes, and methods.
- Keep code modular and maintain separation of concerns.
- Write readable code with descriptive variable and function names.
- Add comments for complex logic, but prefer to write self-documenting code.

## Testing Guidelines

- Write tests for all new features and bug fixes.
- Aim for high test coverage of the codebase.
- Use pytest for testing.
- Structure tests in the `tests/` directory, mirroring the package structure.
- Write both unit tests and integration tests as appropriate.
- Include test cases for edge cases and error handling.

## Documentation Guidelines

- Use Markdown for documentation.
- Document all public APIs with docstrings.
- Include examples in the documentation when applicable.
- Keep documentation up to date with code changes.
- For the website, ensure documentation is clear and well-structured.

## License

By contributing to Expressify, you agree that your contributions will be licensed under the project's [MIT License](LICENSE).

## Questions?

If you have any questions or need help, feel free to:
- Open an issue on GitHub
- Contact the maintainer at [dhruvrwt12@gmail.com](mailto:dhruvrwt12@gmail.com)

## Types of Contributions

### Bug Fixes

If you find a bug, please first check our [BUGS_AND_ISSUES.md](BUGS_AND_ISSUES.md) file and [GitHub Issues](https://github.com/itsdhruvrawat/expressify/issues) to see if it's already known. If not, please report it by creating a new issue.

When fixing bugs:
- Reference the issue number in your commit message
- Add a test case that demonstrates the bug
- Verify that the test fails without your fix and passes with it

### Feature Additions

For new features:
- First discuss the feature by creating an issue
- Reference the feature discussion in your pull request
- Add tests for the new feature
- Update documentation to cover the new feature

### Documentation Improvements

Documentation contributions are highly valued:
- Fix typos or clarify existing documentation
- Add examples or improve tutorials
- Ensure documentation stays in sync with code

## Working with Issues

- **Check existing issues** before creating a new one
- **Use issue templates** if available
- **Be specific** about the problem or feature
- **Include reproduction steps** for bugs
- **Mention versions** of relevant software

## Code Review Process

- All submissions require review
- Changes may be requested before a pull request is merged
- Reviewers will check for:
  - Code quality and style
  - Test coverage
  - Documentation updates

## Development Setup Tips

- Run examples to test your changes:
  ```bash
  cd examples/01-hello-world
  python app.py
  ```
- Check examples work on different platforms if possible
- Test with different Python versions

## Additional Resources

- [GitHub documentation on contributing to projects](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)
- [Python documentation style guide](https://devguide.python.org/documentation/style-guide/)

Thank you for contributing to Expressify! 
