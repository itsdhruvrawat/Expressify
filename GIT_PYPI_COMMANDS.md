# Essential Commands for GitHub and PyPI

## GitHub Setup

```bash
# Initialize git in your project folder
git init

# Create a new repository on GitHub named 'expressify' first, then:
git remote add origin https://github.com/YOUR_USERNAME/expressify.git

# Add all files (except those in .gitignore)
git add .

# Commit your changes
git commit -m "Initial commit of Expressify framework"

# Push to GitHub
git push -u origin main
```

## PyPI Publishing

```bash
# Install required tools
pip install --upgrade build twine

# Build distribution packages
python -m build

# Upload to Test PyPI (optional but recommended)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*

# Test installation
pip install expressify
```

## Common PyPI Publishing Issues

1. If you get "File exists" errors, you need to increment the version number in `setup.py`
2. For authentication issues, use a PyPI API token:
   ```bash
   python -m twine upload --username __token__ --password pypi-your-token dist/*
   ```
3. Make sure your setup.py has all the required dependencies listed 