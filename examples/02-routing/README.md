# Expressify Routing Example

This directory contains examples of using Expressify's routing features, demonstrating how to define routes with different HTTP methods and patterns.

## What You'll Learn

- How to define routes for different HTTP methods (GET, POST, PUT, DELETE)
- How to use route parameters (e.g., `/users/:id`)
- How to create routes with multiple parameters
- How to organize routes using the Router module
- How to create wildcard routes for handling 404 errors

## Files in This Example

- `app.py` - A comprehensive example demonstrating various routing patterns and techniques

## Running the Example

To run this example:

```bash
cd examples/02-routing
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000) to see a user interface with links to test the various routes.

## Available Routes

### Basic Routes

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `/` | GET | Home page with links to all examples | [http://localhost:3000/](http://localhost:3000/) |
| `/about` | GET | Simple about page | [http://localhost:3000/about](http://localhost:3000/about) |
| `/data` | POST | Accept form data | Use cURL to test |
| `/update` | PUT | Update existing data | Use cURL to test |
| `/delete` | DELETE | Delete data | Use cURL to test |

### Routes with Parameters

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `/users/:id` | GET | Gets user by ID | [http://localhost:3000/users/42](http://localhost:3000/users/42) |
| `/products/:category/:product` | GET | Gets product by category and name | [http://localhost:3000/products/electronics/laptop](http://localhost:3000/products/electronics/laptop) |
| `/articles/:year/:month/:day` | GET | Gets articles by date | [http://localhost:3000/articles/2023/03/26](http://localhost:3000/articles/2023/03/26) |

### API Routes (Using Router)

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `/api/users` | GET | Get all users | [http://localhost:3000/api/users](http://localhost:3000/api/users) |
| `/api/users/:id` | GET | Get user by ID | [http://localhost:3000/api/users/1](http://localhost:3000/api/users/1) |
| `/api/users` | POST | Create a new user | Use cURL to test |
| `/api/users/:id` | PUT | Update a user | Use cURL to test |
| `/api/users/:id` | DELETE | Delete a user | Use cURL to test |

### Special Routes

| Route | Method | Description | Example |
|-------|--------|-------------|---------|
| `*` | GET | Wildcard route that catches all unmatched paths | [http://localhost:3000/does-not-exist](http://localhost:3000/does-not-exist) |

## Testing with cURL

You can test the various HTTP methods using cURL:

```bash
# POST request to submit data
curl -X POST -d "name=John&email=john@example.com" http://localhost:3000/data

# PUT request to update data
curl -X PUT -d "id=1&name=John&email=john@example.com" http://localhost:3000/update

# DELETE request
curl -X DELETE http://localhost:3000/delete?id=1

# API tests
curl -X POST -H "Content-Type: application/json" -d '{"name":"John","email":"john@example.com"}' http://localhost:3000/api/users
curl -X PUT -H "Content-Type: application/json" -d '{"name":"John Updated"}' http://localhost:3000/api/users/1
curl -X DELETE http://localhost:3000/api/users/1
```

## Key Concepts Demonstrated

### Defining Routes with HTTP Methods

```python
@app.get('/path')    # GET request
@app.post('/path')   # POST request
@app.put('/path')    # PUT request
@app.delete('/path') # DELETE request
```

### Route Parameters

```python
@app.get('/users/:id')
def get_user(req, res):
    user_id = req.params.get('id')  # Access URL parameter
    # ...
```

### Multiple Parameters

```python
@app.get('/products/:category/:product')
def get_product(req, res):
    category = req.params.get('category')
    product = req.params.get('product')
    # ...
```

### Using the Router Module

```python
# Create a router
api_router = Router()

# Define routes on the router
@api_router.get('/users')
def get_users(req, res):
    # ...

# Mount the router at a specific path
app.use('/api', api_router)
```

### Wildcard Route

```python
@app.get('*')
def not_found(req, res):
    res.status(404).send('Not Found')
``` 