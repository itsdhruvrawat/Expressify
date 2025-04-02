# Expressify Templates Example

This directory contains examples of using templates with Expressify, demonstrating how to set up and use the Jinja2 template engine to create dynamic HTML pages.

## What You'll Learn

- How to set up the template engine in Expressify
- How to render templates with dynamic data
- How to use template inheritance for consistent layouts
- How to use conditionals and loops in templates
- How to process form submissions and display feedback

## Files in This Example

- `app.py` - The main application with routes that render templates
- `views/` - Directory containing template files:
  - `layout.html` - Base template with common layout elements
  - `index.html` - Home page template
  - `about.html` - About page with template features explanation
  - `products.html` - Product list with filtering
  - `product_detail.html` - Product detail page
  - `users.html` - User list
  - `user_detail.html` - User detail page
  - `form.html` - Form example with feedback
  - `404.html` - Error page template

## Running the Example

To run this example:

```bash
cd examples/05-templates
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000).

## Available Routes

| Route | Method | Description | Template Used |
|-------|--------|-------------|--------------|
| `/` | GET | Home page with example links | `index.html` |
| `/about` | GET | About page with template info | `about.html` |
| `/products` | GET | List of products with category filter | `products.html` |
| `/products/:id` | GET | Product detail page | `product_detail.html` |
| `/users` | GET | List of users | `users.html` |
| `/users/:id` | GET | User detail page | `user_detail.html` |
| `/form` | GET | Form example | `form.html` |
| `/form` | POST | Process form submission | Redirects to `/form` |

## Template Features Demonstrated

### Template Setup

```python
# Set up the template engine
app.set('view engine', 'jinja2')
app.set('views', './views')
```

### Rendering Templates with Data

```python
@app.get('/route')
def handler(req, res):
    res.render('template.html', {
        'title': 'Page Title',
        'data': some_data
    })
```

### Template Inheritance

```html
<!-- Base layout template with blocks -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- Page template extending the layout -->
{% extends "layout.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <h1>Page Content</h1>
{% endblock %}
```

### Variables

```html
<h1>{{ title }}</h1>
<p>Welcome, {{ user.name }}!</p>
```

### Conditionals

```html
{% if product.in_stock %}
    <span style="color: green;">In Stock</span>
{% else %}
    <span style="color: red;">Out of Stock</span>
{% endif %}
```

### Loops

```html
<ul>
    {% for item in items %}
        <li>{{ item.name }} - ${{ item.price }}</li>
    {% endfor %}
</ul>
```

### Form Processing

```python
@app.post('/form')
def handle_form(req, res):
    name = req.body.get('name', '')
    # Process form data...
    res.redirect(f'/form?message=Thanks, {name}!')
```

```html
{% if message %}
    <div class="alert">{{ message }}</div>
{% endif %}
```

## Testing the Templates

Navigate through the application to see how templates are rendered with different data. The about page includes detailed information about template features and syntax. 