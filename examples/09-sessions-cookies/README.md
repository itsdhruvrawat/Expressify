# Expressify Sessions and Cookies Example

This directory contains an example of working with sessions and cookies in Expressify, demonstrating how to implement user authentication and session management.

## What You'll Learn

- How to set and read cookies
- How to create and manage user sessions
- How to implement basic user authentication (login/logout/register)
- How to create protected routes that require authentication

## Files in This Example

- `app.py` - The main application with cookie handling, session management, and authentication
- `data/users.json` - JSON file storing user data (created automatically)
- `data/sessions.json` - JSON file storing session data (created automatically)

## Running the Example

To run this example:

```bash
cd examples/09-sessions-cookies
python app.py
```

The server will start on port 3000. You can access the application at [http://localhost:3000](http://localhost:3000).

## Test Accounts

For testing purposes, the following accounts are available:

- Username: `admin`, Password: `password`
- Username: `user`, Password: `password`

## Available Routes

| Route | Method | Description | Authentication Required |
|-------|--------|-------------|------------------------|
| `/` | GET | Home page with navigation | No |
| `/cookies` | GET | Demonstrates cookies functionality | No |
| `/login` | GET | Shows login form | No |
| `/profile` | GET | User profile page | Yes |
| `/logout` | GET | Logs out the user | No | 