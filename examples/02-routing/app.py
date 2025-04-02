"""
Expressify Routing Example

This example demonstrates various routing features and patterns in Expressify:
- Basic routes with different HTTP methods (GET, POST, PUT, DELETE)
- Route parameters
- Named parameters with patterns
- Route chaining (multiple handlers for the same route)
- Route modules with Router
- Wildcard routes
"""

from expressify import expressify, Router
import os

# Create a new Expressify application
app = expressify()

# ------------------------------------------------------------
# Basic Route Examples
# ------------------------------------------------------------

# Basic route for the root URL
@app.get('/')
def index(req, res):
    """Root route - responds to GET /"""
    res.type('text/html').send('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify - Routing Example</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
            h2 { color: #444; margin-top: 30px; }
            .container { max-width: 800px; margin: 0 auto; }
            ul { margin-bottom: 30px; }
            li { margin-bottom: 10px; }
            .method { display: inline-block; padding: 3px 6px; border-radius: 3px; font-size: 12px; font-weight: bold; margin-right: 8px; }
            .get { background: #61affe; color: white; }
            .post { background: #49cc90; color: white; }
            .put { background: #fca130; color: white; }
            .delete { background: #f93e3e; color: white; }
            .api { border-left: 4px solid #0066cc; padding-left: 15px; }
            .param { color: #e64980; font-family: monospace; }
            code { background: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: monospace; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Expressify Routing Examples</h1>
            <p>This page demonstrates various routing patterns supported by Expressify.</p>
            
            <h2>Basic Routes</h2>
            <ul>
                <li><span class="method get">GET</span> <a href="/">/</a> - This page</li>
                <li><span class="method get">GET</span> <a href="/about">/about</a> - About page</li>
                <li><span class="method post">POST</span> <a href="/data">/data</a> - Accepts form data</li>
                <li><span class="method put">PUT</span> <a href="/update">/update</a> - <a href="/update">Test form</a> for update route</li>
                <li><span class="method delete">DELETE</span> <a href="/delete">/delete</a> - <a href="/delete">Test form</a> for delete route</li>
            </ul>
            
            <h2>Route Parameters</h2>
            <ul>
                <li><span class="method get">GET</span> <a href="/users/42">/users/42</a> - User profile with <span class="param">:id</span> parameter</li>
                <li><span class="method get">GET</span> <a href="/products/electronics/laptop">/products/electronics/laptop</a> - Product with multiple parameters</li>
            </ul>
            
            <h2>API Routes</h2>
            <div class="api">
                <ul>
                    <li><span class="method get">GET</span> <a href="/api/users">/api/users</a> - Get all users</li>
                    <li><span class="method get">GET</span> <a href="/api/users/1">/api/users/1</a> - Get user by ID</li>
                    <li><span class="method post">POST</span> /api/users - Create new user</li>
                    <li><span class="method put">PUT</span> /api/users/1 - Update user</li>
                    <li><span class="method delete">DELETE</span> /api/users/1 - Delete user</li>
                </ul>
            </div>
            
            <h2>Testing Forms</h2>
            <p>For testing POST, PUT, and DELETE routes:</p>
            <ul>
                <li><a href="/update">Update Form</a> - Test the PUT /update route</li>
                <li><a href="/delete">Delete Form</a> - Test the DELETE /delete route</li>
            </ul>
            
            <h2>How to use this example</h2>
            <p>Click on any of the links above to test different routes. For the API routes, you can use tools like <code>curl</code>, <code>Postman</code> or browser extensions to test different HTTP methods.</p>
        </div>
    </body>
    </html>
    ''')

# Basic GET route
@app.get('/about')
def about(req, res):
    """About route - responds to GET /about"""
    res.type('text/html').send('This is the about page. <a href="/">Back to home</a>')

# POST route to handle form submission
@app.post('/data')
def handle_data(req, res):
    """Handle data - responds to POST /data"""
    # Get the form data from the request body
    name = req.body.get('name', 'Guest')
    email = req.body.get('email', 'No email provided')
    
    # In a real application, you would do something with this data
    res.type('application/json').json({
        'message': 'Data received successfully!',
        'name': name,
        'email': email
    })

# GET route for the data submission form
@app.get('/data')
def data_form(req, res):
    """GET method for data form - displays a test form for POST /data"""
    res.type('text/html').send('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify - Data Form</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
            .container { max-width: 600px; margin: 0 auto; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, button { padding: 8px; width: 100%; }
            button { background: #49cc90; color: white; border: none; cursor: pointer; }
            pre { background: #f4f4f4; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Data Submission</h1>
            <p>This form submits a POST request to /data</p>
            
            <form id="dataForm">
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" value="John" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" value="john@example.com" required>
                </div>
                <div class="form-group">
                    <button type="submit">Submit Data</button>
                </div>
            </form>
            
            <div id="result">
                <h3>Response:</h3>
                <pre id="response"></pre>
            </div>
            
            <p><a href="/">Back to Home</a></p>
        </div>
        
        <script>
            document.getElementById('dataForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                
                try {
                    const response = await fetch('/data', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams(formData),
                    });
                    
                    const result = await response.json();
                    document.getElementById('response').textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('response').textContent = 'Error: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    ''')

# Support GET method for the update route as well (for browser testing)
@app.get('/update')
def update_page(req, res):
    """GET method for update - displays a test form"""
    res.type('text/html').send('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify - Update Form</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
            .container { max-width: 600px; margin: 0 auto; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, button { padding: 8px; width: 100%; }
            button { background: #0066cc; color: white; border: none; cursor: pointer; }
            pre { background: #f4f4f4; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Update Route</h1>
            <p>This form submits a PUT request to /update</p>
            
            <form id="updateForm">
                <div class="form-group">
                    <label for="id">ID:</label>
                    <input type="text" id="id" name="id" value="1" required>
                </div>
                <div class="form-group">
                    <label for="name">Name:</label>
                    <input type="text" id="name" name="name" value="John" required>
                </div>
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" value="john@example.com" required>
                </div>
                <div class="form-group">
                    <button type="submit">Update</button>
                </div>
            </form>
            
            <div id="result">
                <h3>Response:</h3>
                <pre id="response"></pre>
            </div>
            
            <p><a href="/">Back to Home</a></p>
        </div>
        
        <script>
            document.getElementById('updateForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = {};
                for (let [key, value] of formData.entries()) {
                    data[key] = value;
                }
                
                try {
                    const response = await fetch('/update', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: new URLSearchParams(formData),
                    });
                    
                    const result = await response.json();
                    document.getElementById('response').textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('response').textContent = 'Error: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    ''')

# PUT route to handle updates
@app.put('/update')
def update_data(req, res):
    """Update data - responds to PUT /update"""
    # In a real application, you would update a database record
    id = req.body.get('id', 'unknown')
    
    res.type('application/json').json({
        'message': f'Update request received for ID: {id}',
        'success': True,
        'updated_fields': {k: v for k, v in req.body.items() if k != 'id'}
    })

# Support GET method for the delete route as well (for browser testing)
@app.get('/delete')
def delete_page(req, res):
    """GET method for delete - displays a test form"""
    res.type('text/html').send('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Expressify - Delete Form</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
            h1 { color: #0066cc; }
            .container { max-width: 600px; margin: 0 auto; }
            .form-group { margin-bottom: 15px; }
            label { display: block; margin-bottom: 5px; }
            input, button { padding: 8px; width: 100%; }
            button { background: #d9534f; color: white; border: none; cursor: pointer; }
            pre { background: #f4f4f4; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Test Delete Route</h1>
            <p>This form submits a DELETE request to /delete</p>
            
            <form id="deleteForm">
                <div class="form-group">
                    <label for="id">ID to delete:</label>
                    <input type="text" id="id" name="id" value="1" required>
                </div>
                <div class="form-group">
                    <button type="submit">Delete</button>
                </div>
            </form>
            
            <div id="result">
                <h3>Response:</h3>
                <pre id="response"></pre>
            </div>
            
            <p><a href="/">Back to Home</a></p>
        </div>
        
        <script>
            document.getElementById('deleteForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const id = document.getElementById('id').value;
                
                try {
                    const response = await fetch(`/delete?id=${id}`, {
                        method: 'DELETE'
                    });
                    
                    const result = await response.json();
                    document.getElementById('response').textContent = JSON.stringify(result, null, 2);
                } catch (error) {
                    document.getElementById('response').textContent = 'Error: ' + error.message;
                }
            });
        </script>
    </body>
    </html>
    ''')

# DELETE route to handle deletion
@app.delete('/delete')
def delete_data(req, res):
    """Delete data - responds to DELETE /delete"""
    # In a real application, you would delete a database record
    id = req.query.get('id', 'unknown')
    
    res.type('application/json').json({
        'message': f'Delete request received for ID: {id}',
        'success': True
    })

# ------------------------------------------------------------
# Route Parameters Examples
# ------------------------------------------------------------

# Route with a parameter (similar to Express.js :param syntax)
@app.get('/users/:id')
def get_user(req, res):
    """Get a user by ID - responds to GET /users/:id"""
    # Access the URL parameter from req.params
    user_id = req.params.get('id')
    
    # In a real app, you would fetch this from a database
    user = {
        'id': user_id,
        'name': f'User {user_id}',
        'email': f'user{user_id}@example.com'
    }
    
    res.type('application/json').json(user)

# Route with multiple parameters
@app.get('/products/:category/:product')
def get_product(req, res):
    """Get a product by category and product name"""
    category = req.params.get('category')
    product = req.params.get('product')
    
    res.type('application/json').json({
        'category': category,
        'product': product,
        'description': f'This is a {product} in the {category} category.'
    })

# Route with date parameters
@app.get('/articles/:year/:month/:day')
def get_article_by_date(req, res):
    """Get articles by date"""
    year = req.params.get('year')
    month = req.params.get('month')
    day = req.params.get('day')
    
    res.type('application/json').json({
        'date': f'{year}-{month}-{day}',
        'articles': [
            {'title': 'Article 1', 'excerpt': 'This is the first article.'},
            {'title': 'Article 2', 'excerpt': 'This is the second article.'}
        ]
    })

# ------------------------------------------------------------
# Router Module Example
# ------------------------------------------------------------

# Create a Router instance for API routes
api_router = Router()

# Define routes on the router
@api_router.get('/users')
def get_users(req, res):
    """Get all users - responds to GET /api/users"""
    users = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'}
    ]
    
    res.type('application/json').json(users)

@api_router.get('/users/:id')
def get_user_by_id(req, res):
    """Get a user by ID - responds to GET /api/users/:id"""
    user_id = req.params.get('id')
    
    # Simulate finding a user
    if user_id == '1':
        res.type('application/json').json({'id': 1, 'name': 'Alice', 'email': 'alice@example.com'})
    elif user_id == '2':
        res.type('application/json').json({'id': 2, 'name': 'Bob', 'email': 'bob@example.com'})
    elif user_id == '3':
        res.type('application/json').json({'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'})
    else:
        # Add proper error handling for user not found
        res.status(404).type('application/json').json({
            'error': 'User not found',
            'message': f'No user with ID {user_id} exists',
            'status': 404
        })

@api_router.post('/users')
def create_user(req, res):
    """Create a new user - responds to POST /api/users"""
    # In a real app, you would save this to a database
    res.status(201).type('application/json').json({
        'message': 'User created successfully',
        'user': req.body
    })

@api_router.put('/users/:id')
def update_user(req, res):
    """Update a user - responds to PUT /api/users/:id"""
    user_id = req.params.get('id')
    
    # Check if user exists first
    if user_id not in ['1', '2', '3']:
        return res.status(404).type('application/json').json({
            'error': 'User not found',
            'message': f'Cannot update user with ID {user_id} - user does not exist',
            'status': 404
        })
    
    res.type('application/json').json({
        'message': f'User {user_id} updated successfully',
        'updated_fields': req.body
    })

@api_router.delete('/users/:id')
def delete_user(req, res):
    """Delete a user - responds to DELETE /api/users/:id"""
    user_id = req.params.get('id')
    
    # Check if user exists first
    if user_id not in ['1', '2', '3']:
        return res.status(404).type('application/json').json({
            'error': 'User not found',
            'message': f'Cannot delete user with ID {user_id} - user does not exist',
            'status': 404
        })
    
    res.type('application/json').json({
        'message': f'User {user_id} deleted successfully'
    })

# Mount the router at the /api path
app.use('/api', api_router)

# ------------------------------------------------------------
# Start the Server
# ------------------------------------------------------------

if __name__ == '__main__':
    print("Routing example running on http://localhost:3000")
    print("Available routes:")
    print("  - GET http://127.0.0.1:3000/")
    print("  - GET http://127.0.0.1:3000/about")
    print("  - POST http://127.0.0.1:3000/data")
    print("  - PUT http://127.0.0.1:3000/update")
    print("  - DELETE http://127.0.0.1:3000/delete")
    print("  - GET http://127.0.0.1:3000/users/:id")
    print("  - GET http://127.0.0.1:3000/products/:category/:product")
    print("  - GET http://127.0.0.1:3000/articles/:year/:month/:day")
    print("  - API routes mounted at http://127.0.0.1:3000/api")
    print("  - GET http://127.0.0.1:3000/api/users")
    print("  - GET http://127.0.0.1:3000/api/users/:id")
    print("  - POST http://127.0.0.1:3000/api/users")
    print("  - PUT http://127.0.0.1:3000/api/users/:id")
    print("  - DELETE http://127.0.0.1:3000/api/users/:id")
    
    app.listen(port=3000, hostname='127.0.0.1') 