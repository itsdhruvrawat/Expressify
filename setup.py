from setuptools import setup, find_packages
import os
import re

# Try to get version from __init__.py if it exists
version = '0.1.0'  # Default version
try:
    with open('expressify/__init__.py', 'r') as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
        if version_match:
            version = version_match.group(1)
except FileNotFoundError:
    pass

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
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Operating System :: OS Independent',
    ],
    keywords='web framework, express, http, api, routing, middleware',
    python_requires='>=3.7',
    install_requires=[
        'jinja2>=2.11.0',
        'uvicorn>=0.15.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'black>=21.5b2',
            'flake8>=3.9.2',
            'isort>=5.9.1',
        ],
    },
    project_urls={
        'Bug Tracker': 'https://github.com/itsdhruvrawat/expressify/issues',
        'Documentation': 'https://express-ify.netlify.app',
        'Source Code': 'https://github.com/itsdhruvrawat/expressify',
    },
) 