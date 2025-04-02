"""
Expressify Templates Example

This example demonstrates how to use templates in Expressify:
- Setting up the template engine
- Rendering templates with data
- Using template inheritance
- Working with conditionals and loops in templates
"""

from expressify import expressify
from expressify.lib.template import create_engine
import os

# Create a new Expressify application
app = expressify()

# Set up the template engine (Jinja2)
# Configure the template engine with the views directory
template_dir = os.path.join(os.path.dirname(__file__), 'views')
create_engine('jinja2', template_dir)

# Sample data (in a real app, this would come from a database)
products = [
    {'id': 1, 'name': 'Laptop', 'price': 999.99, 'category': 'Electronics', 'in_stock': True},
    {'id': 2, 'name': 'Smartphone', 'price': 699.99, 'category': 'Electronics', 'in_stock': True},
    {'id': 3, 'name': 'Headphones', 'price': 199.99, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Coffee Maker', 'price': 89.99, 'category': 'Kitchen', 'in_stock': True},
    {'id': 5, 'name': 'Blender', 'price': 49.99, 'category': 'Kitchen', 'in_stock': True}
]

users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com', 'role': 'admin'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com', 'role': 'user'},
    {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com', 'role': 'user'}
]

# ------------------------------------------------------------
# Routes
# ------------------------------------------------------------

# Home route
@app.get('/')
def home(req, res):
    """Home page - uses the index.html template"""
    # Render the index.html template with data
    res.render('index.html', {
        'title': 'Expressify Templates',
        'message': 'Welcome to the Expressify Templates Example',
        'description': 'This example demonstrates how to use templates in Expressify.',
        'features': [
            'Rendering templates with Jinja2',
            'Template inheritance',
            'Passing data to templates',
            'Using conditionals and loops in templates'
        ]
    })

# About page
@app.get('/about')
def about(req, res):
    """About page - uses the about.html template"""
    res.render('about.html', {
        'title': 'About Expressify Templates',
        'content': 'Expressify uses the Jinja2 template engine, which is powerful and flexible. It supports template inheritance, loops, conditionals, filters, and more.'
    })

# Products page
@app.get('/products')
def product_list(req, res):
    """Products page - displays a list of products"""
    # Get query parameter for category filter
    category = req.query.get('category', None)
    
    # Filter products by category if provided
    filtered_products = products
    if category:
        filtered_products = [p for p in products if p['category'].lower() == category.lower()]
    
    # Render the products.html template with the filtered products
    res.render('products.html', {
        'title': 'Product List',
        'products': filtered_products,
        'category': category,
        'categories': sorted(set(p['category'] for p in products))
    })

# Product detail page
@app.get('/products/:id')
def product_detail(req, res):
    """Product detail page - displays information about a specific product"""
    # Get the product ID from the URL parameter
    try:
        product_id = int(req.params.get('id'))
    except (ValueError, TypeError):
        # If the ID is not a valid integer, return a 404 page
        return res.status(404).render('404.html', {
            'title': 'Product Not Found',
            'message': 'The requested product does not exist'
        })
    
    # Find the product with the given ID
    product = next((p for p in products if p['id'] == product_id), None)
    
    # If the product doesn't exist, return a 404 page
    if not product:
        return res.status(404).render('404.html', {
            'title': 'Product Not Found',
            'message': 'The requested product does not exist'
        })
    
    # Render the product_detail.html template with the product data
    res.render('product_detail.html', {
        'title': f'Product: {product["name"]}',
        'product': product
    })

# Users page
@app.get('/users')
def user_list(req, res):
    """Users page - displays a list of users"""
    res.render('users.html', {
        'title': 'User List',
        'users': users
    })

# User detail page
@app.get('/users/:id')
def user_detail(req, res):
    """User detail page - displays information about a specific user"""
    # Get the user ID from the URL parameter
    try:
        user_id = int(req.params.get('id'))
    except (ValueError, TypeError):
        # If the ID is not a valid integer, return a 404 page
        return res.status(404).render('404.html', {
            'title': 'User Not Found',
            'message': 'The requested user does not exist'
        })
    
    # Find the user with the given ID
    user = next((u for u in users if u['id'] == user_id), None)
    
    # If the user doesn't exist, return a 404 page
    if not user:
        return res.status(404).render('404.html', {
            'title': 'User Not Found',
            'message': 'The requested user does not exist'
        })
    
    # Render the user_detail.html template with the user data
    res.render('user_detail.html', {
        'title': f'User: {user["name"]}',
        'user': user
    })

# Form example page
@app.get('/form')
def form(req, res):
    """Form example page - displays a form"""
    # Get the message query parameter (for displaying feedback)
    message = req.query.get('message', None)
    
    res.render('form.html', {
        'title': 'Form Example',
        'message': message
    })

# Handle form submission
@app.post('/form')
def handle_form(req, res):
    """Process the form submission"""
    # Get the form data
    name = req.body.get('name', '')
    email = req.body.get('email', '')
    message = req.body.get('message', '')
    
    # In a real app, you would validate and save the data
    # For this example, we'll just redirect back to the form with a success message
    
    # Redirect to the form page with a success message
    res.redirect(f'/form?message=Thanks for your submission, {name}!')

# Express.js style template rendering example
@app.get('/express-style')
def express_style(req, res):
    """Demonstrates Express.js style template rendering with data"""
    # Data to pass to the view
    data = {
        'title': 'Express.js Style',
        'message': 'Welcome to my Expressify app!',
        'user': {
            'name': 'John Doe',
            'age': 30
        },
        'items': ['Item 1', 'Item 2', 'Item 3']
    }
    
    # Render the view and pass the data directly
    res.render('express_style.html', data)

# ------------------------------------------------------------
# Start the Server
# ------------------------------------------------------------

if __name__ == '__main__':
    # Create the views directory if it doesn't exist
    os.makedirs(os.path.join(os.path.dirname(__file__), 'views'), exist_ok=True)
    
    # Create the template files if they don't exist
    template_dir = os.path.join(os.path.dirname(__file__), 'views')
    
    # Base layout template
    if not os.path.exists(os.path.join(template_dir, 'layout.html')):
        with open(os.path.join(template_dir, 'layout.html'), 'w') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ title }}{% endblock %} - Expressify</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 80%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background-color: #0066cc;
            color: white;
            padding: 1rem 0;
        }
        nav {
            background-color: #0055aa;
            padding: 0.5rem 0;
        }
        nav ul {
            list-style-type: none;
            margin: 0;
            padding: 0;
            display: flex;
        }
        nav li {
            margin: 0 15px 0 0;
        }
        nav a {
            color: white;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        main {
            padding: 20px 0;
        }
        footer {
            background-color: #f4f4f4;
            padding: 1rem 0;
            text-align: center;
            margin-top: 2rem;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .alert {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
        }
        .alert-success {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .btn {
            display: inline-block;
            background-color: #0066cc;
            color: white;
            padding: 8px 16px;
            border-radius: 4px;
            text-decoration: none;
            border: none;
            cursor: pointer;
        }
        .btn:hover {
            background-color: #0055aa;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        form {
            margin-bottom: 15px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input[type="text"],
        input[type="email"],
        textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
    {% block head %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <h1>Expressify Templates</h1>
        </div>
    </header>
    <nav>
        <div class="container">
            <ul>
                <li><a href="/">Home</a></li>
                <li><a href="/about">About</a></li>
                <li><a href="/products">Products</a></li>
                <li><a href="/users">Users</a></li>
                <li><a href="/form">Form Example</a></li>
            </ul>
        </div>
    </nav>
    <main>
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>
    <footer>
        <div class="container">
            <p>Expressify Templates Example &copy; 2023</p>
        </div>
    </footer>
</body>
</html>''')
    
    # Index template
    if not os.path.exists(os.path.join(template_dir, 'index.html')):
        with open(os.path.join(template_dir, 'index.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    <div class="card">
        <h2>{{ message }}</h2>
        <p>{{ description }}</p>
    </div>
    
    <h2>Features</h2>
    <ul>
        {% for feature in features %}
            <li>{{ feature }}</li>
        {% endfor %}
    </ul>
    
    <h2>Examples</h2>
    <div class="card">
        <p>Check out these examples:</p>
        <ul>
            <li><a href="/products">Product List</a> - View all products with filtering</li>
            <li><a href="/products/1">Product Detail</a> - View details of a specific product</li>
            <li><a href="/users">User List</a> - View all users</li>
            <li><a href="/users/1">User Detail</a> - View details of a specific user</li>
            <li><a href="/form">Form Example</a> - Try submitting a form</li>
        </ul>
    </div>
    
    <h2>Template Code</h2>
    <div class="card">
        <p>This page is rendered using the following template:</p>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto;">
{% raw %}
{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    <div class="card">
        <h2>{{ message }}</h2>
        <p>{{ description }}</p>
    </div>
    
    <h2>Features</h2>
    <ul>
        {% for feature in features %}
            <li>{{ feature }}</li>
        {% endfor %}
    </ul>
    
    <!-- More HTML here -->
{% endblock %}
{% endraw %}
        </pre>
    </div>
{% endblock %}''')
    
    # About template
    if not os.path.exists(os.path.join(template_dir, 'about.html')):
        with open(os.path.join(template_dir, 'about.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    <div class="card">
        <p>{{ content }}</p>
    </div>
    
    <h2>How Templates Work in Expressify</h2>
    <div class="card">
        <p>Templates in Expressify are rendered using the following pattern:</p>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto;">
# Set up the template engine
app.set('view engine', 'jinja2')
app.set('views', './views')

# Render a template with data
@app.get('/route')
def handler(req, res):
    res.render('template.html', {
        'title': 'Page Title',
        'data': some_data
    })
        </pre>
    </div>
    
    <h2>Template Features</h2>
    <div class="card">
        <h3>Variables</h3>
        <code>{{ "{{ variable_name }}" }}</code>
        
        <h3>Conditionals</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto;">
{% raw %}
{% if condition %}
    <!-- HTML when condition is true -->
{% else %}
    <!-- HTML when condition is false -->
{% endif %}
{% endraw %}
        </pre>
        
        <h3>Loops</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto;">
{% raw %}
{% for item in items %}
    <!-- HTML for each item -->
    {{ item.name }}
{% endfor %}
{% endraw %}
        </pre>
        
        <h3>Template Inheritance</h3>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto;">
{% raw %}
<!-- In layout.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- In page.html -->
{% extends "layout.html" %}

{% block title %}Page Title{% endblock %}

{% block content %}
    <h1>Page Content</h1>
{% endblock %}
{% endraw %}
        </pre>
    </div>
{% endblock %}''')
    
    # Products template
    if not os.path.exists(os.path.join(template_dir, 'products.html')):
        with open(os.path.join(template_dir, 'products.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    
    <!-- Category Filter -->
    <div class="card">
        <h3>Filter by Category</h3>
        <p>
            <a href="/products" class="btn {% if not category %}btn-primary{% endif %}">All</a>
            {% for cat in categories %}
                <a href="/products?category={{ cat }}" class="btn {% if category == cat %}btn-primary{% endif %}">{{ cat }}</a>
            {% endfor %}
        </p>
    </div>
    
    <!-- Product List -->
    {% if products %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Category</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for product in products %}
                    <tr>
                        <td>{{ product.id }}</td>
                        <td>{{ product.name }}</td>
                        <td>${{ product.price }}</td>
                        <td>{{ product.category }}</td>
                        <td>
                            {% if product.in_stock %}
                                <span style="color: green;">In Stock</span>
                            {% else %}
                                <span style="color: red;">Out of Stock</span>
                            {% endif %}
                        </td>
                        <td><a href="/products/{{ product.id }}">View</a></td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="card">
            <p>No products found{% if category %} in the "{{ category }}" category{% endif %}.</p>
        </div>
    {% endif %}
{% endblock %}''')
    
    # Product detail template
    if not os.path.exists(os.path.join(template_dir, 'product_detail.html')):
        with open(os.path.join(template_dir, 'product_detail.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ product.name }}</h1>
    
    <div class="card">
        <p><strong>ID:</strong> {{ product.id }}</p>
        <p><strong>Price:</strong> ${{ product.price }}</p>
        <p><strong>Category:</strong> {{ product.category }}</p>
        <p>
            <strong>Status:</strong>
            {% if product.in_stock %}
                <span style="color: green;">In Stock</span>
            {% else %}
                <span style="color: red;">Out of Stock</span>
            {% endif %}
        </p>
    </div>
    
    <p><a href="/products" class="btn">&larr; Back to Products</a></p>
{% endblock %}''')
    
    # Users template
    if not os.path.exists(os.path.join(template_dir, 'users.html')):
        with open(os.path.join(template_dir, 'users.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    
    {% if users %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.email }}</td>
                        <td>{{ user.role }}</td>
                        <td><a href="/users/{{ user.id }}">View</a></td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="card">
            <p>No users found.</p>
        </div>
    {% endif %}
{% endblock %}''')
    
    # User detail template
    if not os.path.exists(os.path.join(template_dir, 'user_detail.html')):
        with open(os.path.join(template_dir, 'user_detail.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ user.name }}</h1>
    
    <div class="card">
        <p><strong>ID:</strong> {{ user.id }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Role:</strong> {{ user.role }}</p>
    </div>
    
    <p><a href="/users" class="btn">&larr; Back to Users</a></p>
{% endblock %}''')
    
    # Form template
    if not os.path.exists(os.path.join(template_dir, 'form.html')):
        with open(os.path.join(template_dir, 'form.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <h1>{{ title }}</h1>
    
    {% if message %}
        <div class="alert alert-success">
            {{ message }}
        </div>
    {% endif %}
    
    <div class="card">
        <form action="/form" method="post">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="message">Message:</label>
                <textarea id="message" name="message" rows="4"></textarea>
            </div>
            
            <button type="submit" class="btn">Submit</button>
        </form>
    </div>
    
    <h2>How Form Handling Works</h2>
    <div class="card">
        <p>This form is processed by a route handler that:</p>
        <ol>
            <li>Receives the form data in the <code>req.body</code> object</li>
            <li>Processes the data (in a real app, it would save to a database)</li>
            <li>Redirects back to this page with a success message</li>
        </ol>
        <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 4px; overflow-x: auto;">
@app.post('/form')
def handle_form(req, res):
    # Get form data
    name = req.body.get('name', '')
    email = req.body.get('email', '')
    message = req.body.get('message', '')
    
    # Process data...
    
    # Redirect with success message
    res.redirect(f'/form?message=Thanks for your submission, {name}!')
        </pre>
    </div>
{% endblock %}''')
    
    # 404 template
    if not os.path.exists(os.path.join(template_dir, '404.html')):
        with open(os.path.join(template_dir, '404.html'), 'w') as f:
            f.write('''{% extends "layout.html" %}

{% block title %}{{ title }}{% endblock %}

{% block content %}
    <div class="card" style="text-align: center;">
        <h1 style="color: #d9534f;">404 - Not Found</h1>
        <p>{{ message }}</p>
        <p><a href="/" class="btn">Return to Home</a></p>
    </div>
{% endblock %}''')
    
    print("Templates example running on http://localhost:3000")
    print("Available routes:")
    print("  - GET http://localhost:3000/ (Home page)")
    print("  - GET http://localhost:3000/about (About page)")
    print("  - GET http://localhost:3000/products (Product list)")
    print("  - GET http://localhost:3000/products/:id (Product detail)")
    print("  - GET http://localhost:3000/users (User list)")
    print("  - GET http://localhost:3000/users/:id (User detail)")
    print("  - GET http://localhost:3000/form (Form example)")
    print("  - POST http://localhost:3000/form (Form submission)")
    
    app.listen(port=3000, hostname='127.0.0.1') 