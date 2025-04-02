# Expressify RESTful API Example

This directory contains an example of building a RESTful API with Expressify, demonstrating how to create a complete CRUD (Create, Read, Update, Delete) API for a task management application.

## What You'll Learn

- How to create RESTful API endpoints
- How to implement CRUD operations
- How to handle JSON request and response data
- How to validate input data
- How to use proper HTTP methods and status codes
- How to organize API routes and documentation
- How to persist data to a JSON file

## Files in This Example

- `app.py` - The main application with API routes and logic
- `data/tasks.json` - JSON file for storing task data (created automatically)

## Running the Example

To run this example:

```bash
cd examples/08-restful-api
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000) to see the API documentation.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tasks` | GET | Get all tasks, with optional filtering |
| `/api/tasks/:id` | GET | Get a single task by ID |
| `/api/tasks` | POST | Create a new task |
| `/api/tasks/:id` | PUT | Update an existing task |
| `/api/tasks/:id` | DELETE | Delete a task |

## Testing the API with cURL

### Get All Tasks

```bash
curl http://localhost:3000/api/tasks
```

### Get Completed Tasks

```bash
curl http://localhost:3000/api/tasks?completed=true
```

### Get a Single Task

```bash
# Replace [TASK_ID] with an actual task ID
curl http://localhost:3000/api/tasks/[TASK_ID]
```

### Create a New Task

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description", "completed": false}' \
  http://localhost:3000/api/tasks
```

### Update a Task

```bash
# Replace [TASK_ID] with an actual task ID
curl -X PUT -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description", "completed": true}' \
  http://localhost:3000/api/tasks/[TASK_ID]
```

### Delete a Task

```bash
# Replace [TASK_ID] with an actual task ID
curl -X DELETE http://localhost:3000/api/tasks/[TASK_ID]
```

## Task Data Structure

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Learn Expressify",
  "description": "Study the Expressify framework documentation",
  "completed": false,
  "created_at": "2023-03-26T12:34:56.789Z"
}
```

## RESTful Design Principles Demonstrated

1. **Resource-Based URLs**: URLs represent resources (tasks)
2. **HTTP Methods**: Using proper HTTP methods for operations (GET, POST, PUT, DELETE)
3. **Status Codes**: Returning appropriate HTTP status codes (200, 201, 400, 404, etc.)
4. **JSON Data**: Using JSON for data exchange
5. **Statelessness**: All requests contain all necessary information
6. **Input Validation**: Validating input data before processing
7. **Consistent Responses**: Using consistent response formats

## Key Components

### JSON Parser Middleware

```python
def json_parser_middleware(req, res, next):
    # Parses JSON request body
    # ...
```

### Data Validation

```python
def validate_task(task):
    # Validates task data and returns errors if any
    # ...
```

### RESTful Routes

```python
@app.get('/api/tasks')        # List tasks
@app.get('/api/tasks/:id')    # Get a single task
@app.post('/api/tasks')       # Create a new task
@app.put('/api/tasks/:id')    # Update a task
@app.delete('/api/tasks/:id') # Delete a task
``` 