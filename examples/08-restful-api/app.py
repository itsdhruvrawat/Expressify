"""
Expressify RESTful API Example

This example demonstrates how to build a RESTful API with Expressify:
- Building a complete CRUD API (Create, Read, Update, Delete)
- Using HTTP methods correctly (GET, POST, PUT, DELETE)
- Organizing routes in a RESTful way
- Handling JSON data
- Input validation
- Proper status codes and response formats
"""

from expressify import expressify
import json
import os
import uuid
from datetime import datetime

# Create a new Expressify application
app = expressify()

# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------

# JSON body parser middleware
def json_parser_middleware(req, res, next):
    """Parse JSON body if Content-Type is application/json"""
    content_type = req.headers.get('content-type', '')
    if 'application/json' in content_type and req.method in ['POST', 'PUT']:
        try:
            body_str = req.body_raw
            if body_str:
                req.body = json.loads(body_str)
            else:
                req.body = {}
        except json.JSONDecodeError:
            return res.status(400).json({
                'error': 'Invalid JSON',
                'message': 'Could not parse JSON body'
            })
    
    next()

# Logger middleware
def logger_middleware(req, res, next):
    """Log API requests"""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {req.method} {req.path}")
    next()

# Apply middleware
app.use(json_parser_middleware)
app.use(logger_middleware)

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------

# Path to the data file
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'tasks.json')

# Create the data directory if it doesn't exist
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

# Load tasks from the data file
def load_tasks():
    """Load tasks from the JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# Save tasks to the data file
def save_tasks(tasks):
    """Save tasks to the JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

# Initialize with some sample data if the file doesn't exist
if not os.path.exists(DATA_FILE):
    sample_tasks = [
        {
            'id': str(uuid.uuid4()),
            'title': 'Learn Expressify',
            'description': 'Study the Expressify framework documentation',
            'completed': False,
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Build a RESTful API',
            'description': 'Create a complete CRUD API with Expressify',
            'completed': True,
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'title': 'Deploy the application',
            'description': 'Deploy the application to a production server',
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
    ]
    save_tasks(sample_tasks)

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def validate_task(task):
    """Validate task data"""
    errors = []
    
    if 'title' not in task or not task['title'].strip():
        errors.append('Title is required')
    
    if 'description' not in task:
        errors.append('Description is required')
    
    if 'completed' in task and not isinstance(task['completed'], bool):
        errors.append('Completed must be a boolean')
    
    return errors

# ------------------------------------------------------------
# Home Route - API Documentation
# ------------------------------------------------------------

@app.get('/')
def home(req, res):
    """API home page with documentation"""
    res.send('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Expressify RESTful API Example</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1, h2, h3 {
                color: #0066cc;
            }
            .endpoint {
                background-color: #f8f9fa;
                padding: 15px;
                margin-bottom: 15px;
                border-radius: 5px;
                border-left: 4px solid #0066cc;
            }
            .method {
                display: inline-block;
                padding: 4px 8px;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 8px;
                font-size: 14px;
                color: white;
            }
            .get { background-color: #61affe; }
            .post { background-color: #49cc90; }
            .put { background-color: #fca130; }
            .delete { background-color: #f93e3e; }
            pre {
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }
            code {
                font-family: monospace;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
        </style>
    </head>
    <body>
        <h1>Expressify RESTful API Example</h1>
        <p>This is an example of a RESTful API built with Expressify for managing tasks.</p>
        
        <h2>API Endpoints</h2>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/tasks</code>
            <p>Get all tasks</p>
            <h3>Query Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Type</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>completed</td>
                    <td>boolean</td>
                    <td>Filter tasks by completion status</td>
                </tr>
            </table>
            <h3>Example Response</h3>
            <pre><code>[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Learn Expressify",
    "description": "Study the Expressify framework documentation",
    "completed": false,
    "created_at": "2023-03-26T12:34:56.789Z"
  },
  ...
]</code></pre>
        </div>
        
        <div class="endpoint">
            <span class="method get">GET</span>
            <code>/api/tasks/:id</code>
            <p>Get a single task by ID</p>
            <h3>Path Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>id</td>
                    <td>The task ID</td>
                </tr>
            </table>
            <h3>Example Response</h3>
            <pre><code>{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Learn Expressify",
  "description": "Study the Expressify framework documentation",
  "completed": false,
  "created_at": "2023-03-26T12:34:56.789Z"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <span class="method post">POST</span>
            <code>/api/tasks</code>
            <p>Create a new task</p>
            <h3>Request Body</h3>
            <pre><code>{
  "title": "New Task",
  "description": "Description of the new task",
  "completed": false
}</code></pre>
            <h3>Example Response</h3>
            <pre><code>{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "New Task",
  "description": "Description of the new task",
  "completed": false,
  "created_at": "2023-03-26T12:34:56.789Z"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <span class="method put">PUT</span>
            <code>/api/tasks/:id</code>
            <p>Update an existing task</p>
            <h3>Path Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>id</td>
                    <td>The task ID</td>
                </tr>
            </table>
            <h3>Request Body</h3>
            <pre><code>{
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true
}</code></pre>
            <h3>Example Response</h3>
            <pre><code>{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Updated Task",
  "description": "Updated description",
  "completed": true,
  "created_at": "2023-03-26T12:34:56.789Z"
}</code></pre>
        </div>
        
        <div class="endpoint">
            <span class="method delete">DELETE</span>
            <code>/api/tasks/:id</code>
            <p>Delete a task</p>
            <h3>Path Parameters</h3>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Description</th>
                </tr>
                <tr>
                    <td>id</td>
                    <td>The task ID</td>
                </tr>
            </table>
            <h3>Example Response</h3>
            <pre><code>{
  "message": "Task deleted successfully"
}</code></pre>
        </div>
        
        <h2>Testing with cURL</h2>
        <pre><code># Get all tasks
curl http://localhost:3000/api/tasks

# Get completed tasks
curl http://localhost:3000/api/tasks?completed=true

# Get a single task
curl http://localhost:3000/api/tasks/[TASK_ID]

# Create a new task
curl -X POST -H "Content-Type: application/json" -d '{"title": "New Task", "description": "Task description", "completed": false}' http://localhost:3000/api/tasks

# Update a task
curl -X PUT -H "Content-Type: application/json" -d '{"title": "Updated Task", "description": "Updated description", "completed": true}' http://localhost:3000/api/tasks/[TASK_ID]

# Delete a task
curl -X DELETE http://localhost:3000/api/tasks/[TASK_ID]
</code></pre>
    </body>
    </html>
    ''')

# ------------------------------------------------------------
# API Routes
# ------------------------------------------------------------

# GET /api/tasks - Get all tasks
@app.get('/api/tasks')
def get_tasks(req, res):
    """Get all tasks, with optional filtering by completion status"""
    tasks = load_tasks()
    
    # Filter by completed status if the query parameter is present
    if 'completed' in req.query:
        completed = req.query.get('completed').lower() == 'true'
        tasks = [task for task in tasks if task['completed'] == completed]
    
    res.json(tasks)

# GET /api/tasks/:id - Get a single task
@app.get('/api/tasks/:id')
def get_task(req, res):
    """Get a single task by ID"""
    task_id = req.params.get('id')
    tasks = load_tasks()
    
    # Find the task with the specified ID
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task:
        res.json(task)
    else:
        res.status(404).json({
            'error': 'Not Found',
            'message': f'Task with ID {task_id} not found'
        })

# POST /api/tasks - Create a new task
@app.post('/api/tasks')
def create_task(req, res):
    """Create a new task"""
    # Validate the request body
    validation_errors = validate_task(req.body)
    if validation_errors:
        return res.status(400).json({
            'error': 'Bad Request',
            'message': 'Task validation failed',
            'details': validation_errors
        })
    
    # Create a new task with the data from the request body
    new_task = {
        'id': str(uuid.uuid4()),
        'title': req.body.get('title'),
        'description': req.body.get('description'),
        'completed': req.body.get('completed', False),
        'created_at': datetime.now().isoformat()
    }
    
    # Add the new task to the list and save
    tasks = load_tasks()
    tasks.append(new_task)
    save_tasks(tasks)
    
    # Return the created task with a 201 Created status code
    res.status(201).json(new_task)

# PUT /api/tasks/:id - Update a task
@app.put('/api/tasks/:id')
def update_task(req, res):
    """Update an existing task"""
    task_id = req.params.get('id')
    tasks = load_tasks()
    
    # Find the task with the specified ID
    task_index = None
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            task_index = i
            break
    
    if task_index is None:
        return res.status(404).json({
            'error': 'Not Found',
            'message': f'Task with ID {task_id} not found'
        })
    
    # Validate the request body
    validation_errors = validate_task(req.body)
    if validation_errors:
        return res.status(400).json({
            'error': 'Bad Request',
            'message': 'Task validation failed',
            'details': validation_errors
        })
    
    # Update the task with the data from the request body
    updated_task = tasks[task_index].copy()
    updated_task.update({
        'title': req.body.get('title'),
        'description': req.body.get('description'),
        'completed': req.body.get('completed', updated_task['completed'])
    })
    
    # Replace the old task and save
    tasks[task_index] = updated_task
    save_tasks(tasks)
    
    # Return the updated task
    res.json(updated_task)

# DELETE /api/tasks/:id - Delete a task
@app.delete('/api/tasks/:id')
def delete_task(req, res):
    """Delete a task"""
    task_id = req.params.get('id')
    tasks = load_tasks()
    
    # Find the task with the specified ID
    task_index = None
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            task_index = i
            break
    
    if task_index is None:
        return res.status(404).json({
            'error': 'Not Found',
            'message': f'Task with ID {task_id} not found'
        })
    
    # Remove the task and save
    deleted_task = tasks.pop(task_index)
    save_tasks(tasks)
    
    # Return a success message
    res.json({
        'message': 'Task deleted successfully',
        'deleted_task': deleted_task
    })

# ------------------------------------------------------------
# Start the Server
# ------------------------------------------------------------

if __name__ == '__main__':
    print("RESTful API example running on http://localhost:3000")
    print("API endpoints available at /api/tasks")
    
    app.listen(port=3000, hostname='127.0.0.1') 