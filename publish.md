# Publishing Expressify to PyPI

This guide outlines the steps to publish the Expressify package to the Python Package Index (PyPI), making it available for installation via pip.

## Prerequisites

Before publishing, ensure you have the following:

1. A PyPI account (register at [https://pypi.org/account/register/](https://pypi.org/account/register/))
2. Required Python packaging tools:
   ```bash
   pip install build twine
   ```
3. Proper project structure:
   - `setup.py` with correct metadata
   - `README.md` for package description
   - Properly formatted code in modules
   - Version properly set in `__init__.py`

## Step 1: Prepare Your Package

### 1.1 Verify Package Structure

Ensure your project has the following structure:

```
expressify/
├── expressify/
│   ├── __init__.py
│   ├── application.py
│   ├── router.py
│   ├── request.py
│   ├── response.py
│   └── ... (other modules)
├── tests/
│   └── ... (test files)
├── examples/
│   └── ... (example applications)
├── setup.py
├── README.md
├── LICENSE
└── requirements.txt
```

### 1.2 Update Version Number

Update the version number in `expressify/__init__.py`:

```python
__version__ = '1.0.0'  # Change to your new version
```

Follow [Semantic Versioning](https://semver.org/) (MAJOR.MINOR.PATCH):
- MAJOR: Incompatible API changes
- MINOR: Add functionality in a backward-compatible manner
- PATCH: Backward-compatible bug fixes

### 1.3 Verify setup.py

Ensure your `setup.py` file has correct metadata:

```python
from setuptools import setup, find_packages
import os
import re

# Read version from __init__.py
with open('expressify/__init__.py', 'r') as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError('Unable to find version string')

# Read long description from README
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='expressify',
    version=version,
    description='A lightweight Express.js-inspired web framework for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Dhruv Rawat',
    author_email='dhruvrwt12@gmail.com',
    url='https://github.com/itsdhruvrawat/expressify',
    packages=find_packages(exclude=['tests', 'examples']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='web framework, express, http, api, routing, middleware',
    python_requires='>=3.7',
    install_requires=[
        'jinja2>=3.0.0',
        'werkzeug>=2.0.0',
        'python-dotenv>=0.19.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'flake8>=4.0.0',
            'black>=21.5b2',
            'isort>=5.9.0',
            'mypy>=0.910',
        ],
    },
    project_urls={
        'Bug Tracker': 'https://github.com/itsdhruvrawat/expressify/issues',
        'Documentation': 'https://github.com/itsdhruvrawat/expressify',
        'Source Code': 'https://github.com/itsdhruvrawat/expressify',
    },
)
```

### 1.4 Create Distribution Files

Build distribution packages:

```bash
python -m build
```

This creates:
- A wheel file (`.whl`) in `dist/` directory
- A source distribution (`.tar.gz`) in `dist/` directory

## Step 2: Test Your Package Locally

Test the built package locally before publishing:

### 2.1 Create a Virtual Environment

```bash
python -m venv testenv
source testenv/bin/activate  # On Windows: testenv\Scripts\activate
```

### 2.2 Install the Package Locally

```bash
pip install dist/expressify-1.0.0-py3-none-any.whl
```

### 2.3 Verify the Installation

```bash
python -c "import expressify; print(expressify.__version__)"
```

Create a simple test app to verify functionality:

```python
from expressify import expressify

app = expressify()

@app.get('/')
def home(req, res):
    res.send('Hello, World!')

if __name__ == '__main__':
    app.listen(port=3000, hostname='127.0.0.1')
```

## Step 3: Upload to PyPI

### 3.1 Upload to TestPyPI (Recommended)

TestPyPI is a test version of PyPI that allows you to test your package without affecting the real PyPI:

```bash
python -m twine upload --repository testpypi dist/*
```

You'll be prompted for your TestPyPI username and password.

Test the installation from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ expressify
```

### 3.2 Upload to PyPI

Once you're confident the package works correctly, upload to the real PyPI:

```bash
python -m twine upload dist/*
```

You'll be prompted for your PyPI username and password.

## Step 4: Verify the Published Package

Verify that your package is published correctly:

1. Check the PyPI page: https://pypi.org/project/expressify/
2. Install the package from PyPI:
   ```bash
   pip install expressify
   ```
3. Create a sample app to verify functionality:
   ```python
   from expressify import expressify
   
   app = expressify()
   
   @app.get('/')
   def home(req, res):
       res.send('Hello, World!')
   
   if __name__ == '__main__':
       app.listen(port=3000, hostname='127.0.0.1')
   ```

## Step 5: Update Documentation

After publishing:

1. Update the documentation website with the new version information
2. Announce the release on GitHub with release notes
3. Update any relevant examples or tutorials to use the new version

## Continuous Integration/Deployment

Consider setting up automated publishing with GitHub Actions:

```yaml
name: Publish Python Package

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install build twine
    - name: Build and publish
      env:
        TWINE_USERNAME: ${{ secrets.PYPI_USERNAME }}
        TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}
      run: |
        python -m build
        twine upload dist/*
```

## Troubleshooting

### Common Issues

1. **Version conflict**: Make sure each upload has a unique version number
2. **Description rendering issues**: Ensure your README.md is properly formatted
3. **Missing dependencies**: Verify all dependencies are listed in setup.py
4. **Import errors after installation**: Check your package structure and imports

### Resolution Steps

1. Check the PyPI error messages if upload fails
2. Use the PyPI rendering preview tool to check README.md formatting
3. Test in a clean virtual environment before publishing
4. Consult the [PyPI documentation](https://packaging.python.org/en/latest/) for specific issues

## Additional Resources

- [Python Packaging User Guide](https://packaging.python.org/)
- [PyPI Help Documentation](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.readthedocs.io/) 