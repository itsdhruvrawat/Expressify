# Expressify Static Files Example

This directory contains an example of serving static files with Expressify, demonstrating how to serve CSS, JavaScript, and image files to enhance your web applications.

## What You'll Learn

- How to set up static files middleware in Expressify
- How to organize static assets in your project
- How to serve CSS, JavaScript, and image files
- How to reference static files in your HTML

## Files in This Example

- `app.py` - The main application that sets up static file serving
- `public/` - Directory containing static assets:
  - `css/styles.css` - CSS styles for the example
  - `js/script.js` - JavaScript code for interactive elements
  - `images/logo.png` - Sample image

## Running the Example

To run this example:

```bash
cd examples/06-static-files
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000).

## How Static Files Work

In Expressify, static files are served using the `use_static` middleware:

```python
# Serve files from the 'public' directory at the '/static' URL path
app.use_static('public', '/static')
```

This allows you to organize your static assets in a dedicated directory and serve them at a specific URL path. For example:

- A file at `public/css/styles.css` will be available at `http://localhost:3000/static/css/styles.css`
- A file at `public/js/script.js` will be available at `http://localhost:3000/static/js/script.js`
- A file at `public/images/logo.png` will be available at `http://localhost:3000/static/images/logo.png`

## Structure for Static Assets

It's a good practice to organize your static files into subdirectories based on their type:

```
public/
├── css/         # Stylesheets
│   └── styles.css
├── js/          # JavaScript files
│   └── script.js
└── images/      # Images and other media
    └── logo.png
```

## Referencing Static Files in HTML

In your HTML, you can reference static files using the URL path you configured:

```html
<!-- Link to CSS file -->
<link rel="stylesheet" href="/static/css/styles.css">

<!-- Include image -->
<img src="/static/images/logo.png" alt="Logo">

<!-- Link to JavaScript file -->
<script src="/static/js/script.js"></script>
```

## Benefits of Static File Middleware

- **Organization**: Keep static assets separate from application code
- **Caching**: Browsers can cache static files for better performance
- **Security**: Control which files are publicly accessible
- **Flexibility**: You can change the URL path without changing file locations 