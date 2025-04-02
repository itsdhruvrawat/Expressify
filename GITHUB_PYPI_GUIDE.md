# Publishing Expressify to GitHub and PyPI

This guide covers step-by-step instructions for:
1. Creating a GitHub repository for Expressify
2. Pushing your code to GitHub
3. Publishing your package to PyPI

## 1. Creating a GitHub Repository

### Step 1: Create the repository on GitHub
1. Go to [GitHub](https://github.com/) and sign in to your account
2. Click on the "+" icon in the top-right corner, then select "New repository"
3. Enter "expressify" as the repository name
4. Add a description: "A lightweight Express.js-inspired web framework for Python"
5. Choose "Public" visibility
6. Check "Add a README file"
7. Check "Add .gitignore" and select "Python" template
8. Choose an appropriate license (MIT is recommended for open-source packages)
9. Click "Create repository"

### Step 2: Clone the repository locally (if you haven't already)
```bash
# Clone the repository to your local machine
git clone https://github.com/YOUR_USERNAME/expressify.git
cd expressify
```

### Step 3: Initialize Git in your existing project
If you already have your project files in a different folder, you'll need to:
```bash
# Navigate to your project directory
cd path/to/expressify

# Initialize git (if not already initialized)
git init

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/expressify.git
```

## 2. Pushing Your Code to GitHub

### Step 1: Review and update .gitignore
Your .gitignore file should already be configured to ignore the virtual environment folder but include all other project files.

### Step 2: Add and commit your files
```bash
# Add all files
git add .

# Commit with an initial message
git commit -m "Initial commit of Expressify framework"
```

### Step 3: Sync with remote repository
```bash
# Pull any changes from remote (if repository was created with files)
git pull origin main --allow-unrelated-histories

# Push your code to GitHub
git push -u origin main
```

## 3. Publishing to PyPI

### Step 1: Prepare your package
Ensure your package structure is correct:
```
expressify/
├── expressify/
│   ├── __init__.py
│   ├── [other module files]
├── setup.py
├── README.md
├── LICENSE
├── requirements.txt
```

### Step 2: Verify setup.py
Make sure your setup.py file is properly configured:
```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="expressify",
    version="0.1.0",
    author="YOUR_NAME",
    author_email="YOUR_EMAIL",
    description="A lightweight Express.js-inspired web framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/expressify",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "jinja2",
        # list other dependencies from requirements.txt
    ],
)
```

### Step 3: Create an account on PyPI
1. Go to [PyPI](https://pypi.org/account/register/) and create an account
2. Verify your email address

### Step 4: Install required publishing tools
```bash
# Install build and twine tools
pip install --upgrade build twine
```

### Step 5: Build your package
```bash
# Create the package distribution files
python -m build
```

This will create two files in the dist/ directory:
- A source archive (.tar.gz)
- A wheel distribution (.whl)

### Step 6: Upload to PyPI
```bash
# First test with TestPyPI (optional but recommended)
python -m twine upload --repository testpypi dist/*

# Once tested, upload to the real PyPI
python -m twine upload dist/*
```

You'll be prompted for your PyPI username and password.

### Step 7: Verify your package
After publishing, verify your package is available:
1. Visit https://pypi.org/project/expressify/
2. Try installing it in a new virtual environment:
```bash
pip install expressify
```

## 4. Publishing Updates

When you make changes to your package and want to publish a new version:

1. Update the version number in setup.py
2. Commit and push changes to GitHub
3. Rebuild the package: `python -m build`
4. Upload the new version: `python -m twine upload dist/*`

## Automation with GitHub Actions

Consider setting up GitHub Actions for automated testing and deployment to PyPI.

## Using GitHub Releases

1. Go to your GitHub repository
2. Click on "Releases" on the right sidebar
3. Click "Create a new release"
4. Tag version (e.g., v0.1.0)
5. Add release notes
6. Publish release

## Common Issues and Solutions

1. **Authentication Errors with PyPI**: Consider using the API token instead of your password
   ```bash
   python -m twine upload --username __token__ --password pypi-your-token dist/*
   ```

2. **Version Conflicts**: Ensure you increment your version number in setup.py for each new release

3. **README Not Displaying on PyPI**: Verify your long_description is properly set in setup.py and the markdown is valid 