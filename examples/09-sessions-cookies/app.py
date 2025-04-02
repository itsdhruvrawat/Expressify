"""
Expressify Sessions and Cookies Example

This example demonstrates how to use sessions and cookies in Expressify:
- Setting and reading cookies
- Creating and managing sessions
- Implementing a simple user authentication system
- Creating protected routes
"""

from expressify import expressify
import os
import json
import uuid
import hashlib
import time
from datetime import datetime, timedelta

# Create a new Expressify application
app = expressify()

# ------------------------------------------------------------
# Setup
# ------------------------------------------------------------

# Path to the user data file
USERS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'users.json')
SESSIONS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'sessions.json')

# Create the data directory if it doesn't exist
os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)

# Initialize the users file with sample data if it doesn't exist
if not os.path.exists(USERS_FILE):
    sample_users = [
        {
            'id': '1',
            'username': 'admin',
            'password': hashlib.sha256('password'.encode()).hexdigest(),
            'name': 'Admin User',
            'email': 'admin@example.com',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': '2',
            'username': 'user',
            'password': hashlib.sha256('password'.encode()).hexdigest(),
            'name': 'Regular User',
            'email': 'user@example.com',
            'created_at': datetime.now().isoformat()
        }
    ]
    with open(USERS_FILE, 'w') as f:
        json.dump(sample_users, f, indent=2)

# Initialize the sessions file if it doesn't exist
if not os.path.exists(SESSIONS_FILE):
    with open(SESSIONS_FILE, 'w') as f:
        json.dump([], f, indent=2)

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------

def load_users():
    """Load users from the JSON file"""
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def load_sessions():
    """Load sessions from the JSON file"""
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)

def save_sessions(sessions):
    """Save sessions to the JSON file"""
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=2)

def create_session(user_id):
    """Create a new session for the user"""
    sessions = load_sessions()
    
    # Remove any existing sessions for this user
    sessions = [s for s in sessions if s['user_id'] != user_id]
    
    # Create a new session
    session_id = str(uuid.uuid4())
    expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
    
    session = {
        'id': session_id,
        'user_id': user_id,
        'created_at': datetime.now().isoformat(),
        'expires_at': expires_at
    }
    
    sessions.append(session)
    save_sessions(sessions)
    
    return session_id

def get_session(session_id):
    """Get a session by ID and check if it's valid"""
    if not session_id:
        return None
    
    sessions = load_sessions()
    session = next((s for s in sessions if s['id'] == session_id), None)
    
    if not session:
        return None
    
    # Check if the session has expired
    expires_at = datetime.fromisoformat(session['expires_at'])
    if datetime.now() > expires_at:
        # Session has expired, remove it
        sessions = [s for s in sessions if s['id'] != session_id]
        save_sessions(sessions)
        return None
    
    return session

def get_user_by_id(user_id):
    """Get a user by ID"""
    users = load_users()
    user = next((u for u in users if u['id'] == user_id), None)
    
    if user:
        # Don't include the password in the returned user object
        user_copy = user.copy()
        del user_copy['password']
        return user_copy
    
    return None

def get_user_by_credentials(username, password):
    """Validate user credentials and return the user if valid"""
    users = load_users()
    
    # Hash the password for comparison
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Find a user with matching username and password
    user = next((u for u in users if u['username'] == username and u['password'] == hashed_password), None)
    
    if user:
        # Don't include the password in the returned user object
        user_copy = user.copy()
        del user_copy['password']
        return user_copy
    
    return None

# ------------------------------------------------------------
# Middleware
# ------------------------------------------------------------

def session_middleware(req, res, next):
    """
    Middleware to load the user's session
    
    This middleware checks for a session cookie and loads the associated user
    if the session is valid. It attaches the user object to the request.
    """
    # Get the session ID from the cookie
    session_id = req.cookies.get('session_id')
    req.session = get_session(session_id)
    
    if req.session:
        # Load the user associated with this session
        req.user = get_user_by_id(req.session['user_id'])
    else:
        req.user = None
    
    next()

# Apply middleware
app.use(session_middleware)

# ------------------------------------------------------------
# Authentication Middleware (for protected routes)
# ------------------------------------------------------------

def auth_required(req, res, next):
    """
    Authentication middleware for protected routes
    
    This middleware checks if the user is authenticated. If not, it redirects
    to the login page.
    """
    if not req.user:
        return res.redirect('/login?redirect=' + req.path)
    
    next()

# ------------------------------------------------------------
# Home Route
# ------------------------------------------------------------

@app.get('/')
def home(req, res):
    """Home page with links to examples"""
    res.send(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sessions and Cookies Example</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2 {{
                color: #0066cc;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }}
            nav {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            nav a {{
                margin-right: 15px;
                text-decoration: none;
                color: #0066cc;
                font-weight: bold;
            }}
            nav a:hover {{
                text-decoration: underline;
            }}
            .user-status {{
                margin-left: auto;
                color: #666;
            }}
            pre {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Expressify Sessions and Cookies Example</h1>
        
        <nav>
            <a href="/">Home</a>
            <a href="/cookies">Cookies Demo</a>
            {'<a href="/profile">Profile</a>' if req.user else '<a href="/login">Login</a>'}
            {'<a href="/logout">Logout</a>' if req.user else '<a href="/register">Register</a>'}
            <span class="user-status">{'Logged in as: ' + req.user['name'] if req.user else 'Not logged in'}</span>
        </nav>
        
        <div class="card">
            <h2>About This Example</h2>
            <p>This example demonstrates how to work with cookies and sessions in Expressify, including:</p>
            <ul>
                <li>Setting and reading cookies</li>
                <li>Creating and managing user sessions</li>
                <li>User authentication (login/logout)</li>
                <li>Protected routes that require authentication</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>Available Routes</h2>
            <ul>
                <li><a href="/cookies">Cookies Demo</a> - Shows how to set, read, and clear cookies</li>
                <li><a href="/login">Login</a> - User login form</li>
                <li><a href="/register">Register</a> - User registration form</li>
                <li><a href="/profile">Profile</a> - Protected route that requires authentication</li>
                <li><a href="/logout">Logout</a> - Log out the user by clearing the session</li>
            </ul>
        </div>
        
        <div class="card">
            <h2>Test Users</h2>
            <p>For testing purposes, the following users are available:</p>
            <pre>
Username: admin
Password: password

Username: user
Password: password
            </pre>
        </div>
    </body>
    </html>
    ''')

# ------------------------------------------------------------
# Cookies Demo
# ------------------------------------------------------------

@app.get('/cookies')
def cookies_demo(req, res):
    """Demonstrates how to work with cookies"""
    # Get the current visit count from cookies, default to 0
    visit_count = int(req.cookies.get('visit_count', 0))
    
    # Increment the visit count
    visit_count += 1
    
    # Set the updated visit count cookie
    res.set_cookie('visit_count', str(visit_count), max_age=60*60*24*30)  # 30 days
    
    # Get the last visit time from cookies
    last_visit = req.cookies.get('last_visit', 'This is your first visit')
    
    # Set the current time as the last visit
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    res.set_cookie('last_visit', current_time, max_age=60*60*24*30)  # 30 days
    
    res.send(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cookies Demo</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2 {{
                color: #0066cc;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }}
            nav {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            nav a {{
                margin-right: 15px;
                text-decoration: none;
                color: #0066cc;
                font-weight: bold;
            }}
            pre {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
            .cookie-info {{
                font-size: 1.2em;
                font-weight: bold;
                color: #0066cc;
            }}
            .button {{
                display: inline-block;
                background-color: #0066cc;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                text-decoration: none;
                margin-top: 10px;
            }}
            .button:hover {{
                background-color: #0055aa;
            }}
        </style>
    </head>
    <body>
        <h1>Cookies Demo</h1>
        
        <nav>
            <a href="/">Home</a>
            <a href="/cookies">Cookies Demo</a>
            {'<a href="/profile">Profile</a>' if req.user else '<a href="/login">Login</a>'}
            {'<a href="/logout">Logout</a>' if req.user else '<a href="/register">Register</a>'}
        </nav>
        
        <div class="card">
            <h2>Your Cookie Information</h2>
            <p>This page demonstrates how to set, read, and use cookies in Expressify.</p>
            <p>You have visited this page <span class="cookie-info">{visit_count}</span> time(s).</p>
            <p>Your last visit was: <span class="cookie-info">{last_visit}</span></p>
            <a href="/cookies/clear" class="button">Clear Cookies</a>
        </div>
        
        <div class="card">
            <h2>How It Works</h2>
            <p>Each time you visit this page, the server:</p>
            <ol>
                <li>Reads your visit count from the 'visit_count' cookie</li>
                <li>Increments the count by 1</li>
                <li>Sets the updated count in a new cookie</li>
                <li>Records your visit time in the 'last_visit' cookie</li>
            </ol>
            <p>These cookies are set to expire in 30 days. You can clear them by clicking the button above.</p>
        </div>
        
        <div class="card">
            <h2>All Cookies</h2>
            <pre>{json.dumps(dict(req.cookies), indent=2)}</pre>
        </div>
    </body>
    </html>
    ''')

@app.get('/cookies/clear')
def clear_cookies(req, res):
    """Clear the demo cookies"""
    # Clear the visit count cookie
    res.set_cookie('visit_count', '', max_age=0)
    
    # Clear the last visit cookie
    res.set_cookie('last_visit', '', max_age=0)
    
    # Redirect back to the cookies demo page
    res.redirect('/cookies')

# ------------------------------------------------------------
# User Authentication
# ------------------------------------------------------------

@app.get('/login')
def login_page(req, res):
    """Login page"""
    # Check if the user is already logged in
    if req.user:
        return res.redirect('/')
    
    # Get the redirect URL from query parameter
    redirect_url = req.query.get('redirect', '/')
    
    # Get error message if any
    error = req.query.get('error', '')
    
    res.send(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2 {{
                color: #0066cc;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }}
            nav {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            nav a {{
                margin-right: 15px;
                text-decoration: none;
                color: #0066cc;
                font-weight: bold;
            }}
            form {{
                margin-top: 20px;
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }}
            input[type="text"],
            input[type="password"] {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            button {{
                background-color: #0066cc;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #0055aa;
            }}
            .error-message {{
                color: red;
                margin-bottom: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>Login</h1>
        
        <nav>
            <a href="/">Home</a>
            <a href="/cookies">Cookies Demo</a>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
        </nav>
        
        <div class="card">
            {f'<div class="error-message">{error}</div>' if error else ''}
            
            <form action="/login" method="post">
                <input type="hidden" name="redirect" value="{redirect_url}">
                
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit">Login</button>
            </form>
            
            <p>Don't have an account? <a href="/register">Register here</a></p>
        </div>
        
        <div class="card">
            <h2>Test Users</h2>
            <p>For testing purposes, the following users are available:</p>
            <pre>
Username: admin
Password: password

Username: user
Password: password
            </pre>
        </div>
    </body>
    </html>
    ''')

@app.post('/login')
def handle_login(req, res):
    """Handle login form submission"""
    username = req.body.get('username', '')
    password = req.body.get('password', '')
    redirect_url = req.body.get('redirect', '/')
    
    # Validate credentials
    user = get_user_by_credentials(username, password)
    
    if not user:
        # Invalid credentials, redirect back to login with an error
        return res.redirect('/login?error=Invalid+username+or+password&redirect=' + redirect_url)
    
    # Create a new session for the user
    session_id = create_session(user['id'])
    
    # Set the session cookie
    res.set_cookie('session_id', session_id, http_only=True, max_age=60*60*24)  # 1 day
    
    # Redirect to the requested page
    res.redirect(redirect_url)

@app.get('/register')
def register_page(req, res):
    """Registration page"""
    # Check if the user is already logged in
    if req.user:
        return res.redirect('/')
    
    # Get error message if any
    error = req.query.get('error', '')
    
    res.send(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2 {{
                color: #0066cc;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }}
            nav {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            nav a {{
                margin-right: 15px;
                text-decoration: none;
                color: #0066cc;
                font-weight: bold;
            }}
            form {{
                margin-top: 20px;
            }}
            .form-group {{
                margin-bottom: 15px;
            }}
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
            }}
            input[type="text"],
            input[type="password"],
            input[type="email"] {{
                width: 100%;
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                box-sizing: border-box;
            }}
            button {{
                background-color: #0066cc;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }}
            button:hover {{
                background-color: #0055aa;
            }}
            .error-message {{
                color: red;
                margin-bottom: 15px;
            }}
        </style>
    </head>
    <body>
        <h1>Register</h1>
        
        <nav>
            <a href="/">Home</a>
            <a href="/cookies">Cookies Demo</a>
            <a href="/login">Login</a>
            <a href="/register">Register</a>
        </nav>
        
        <div class="card">
            {f'<div class="error-message">{error}</div>' if error else ''}
            
            <form action="/register" method="post">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <div class="form-group">
                    <label for="name">Full Name</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <button type="submit">Register</button>
            </form>
            
            <p>Already have an account? <a href="/login">Login here</a></p>
        </div>
    </body>
    </html>
    ''')

@app.post('/register')
def handle_register(req, res):
    """Handle registration form submission"""
    username = req.body.get('username', '').strip()
    password = req.body.get('password', '')
    name = req.body.get('name', '').strip()
    email = req.body.get('email', '').strip()
    
    # Validate inputs
    if not username or not password or not name or not email:
        return res.redirect('/register?error=All+fields+are+required')
    
    # Check if username already exists
    users = load_users()
    if any(user['username'] == username for user in users):
        return res.redirect('/register?error=Username+already+exists')
    
    # Create new user
    new_user = {
        'id': str(len(users) + 1),
        'username': username,
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'name': name,
        'email': email,
        'created_at': datetime.now().isoformat()
    }
    
    # Add to users and save
    users.append(new_user)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    # Create a session for the new user
    session_id = create_session(new_user['id'])
    
    # Set the session cookie
    res.set_cookie('session_id', session_id, http_only=True, max_age=60*60*24)  # 1 day
    
    # Redirect to profile page
    res.redirect('/profile')

@app.get('/logout')
def logout(req, res):
    """Log out the user by clearing the session"""
    # Clear the session cookie
    res.set_cookie('session_id', '', max_age=0)
    
    # Redirect to home page
    res.redirect('/')

# ------------------------------------------------------------
# Protected Routes
# ------------------------------------------------------------

@app.get('/profile', [auth_required])
def profile(req, res):
    """User profile page (protected route)"""
    res.send(f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Profile</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }}
            h1, h2 {{
                color: #0066cc;
            }}
            .card {{
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #f9f9f9;
            }}
            nav {{
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
            }}
            nav a {{
                margin-right: 15px;
                text-decoration: none;
                color: #0066cc;
                font-weight: bold;
            }}
            .user-info {{
                display: grid;
                grid-template-columns: 150px 1fr;
                grid-gap: 10px;
            }}
            .user-info dt {{
                font-weight: bold;
                color: #666;
            }}
            .user-info dd {{
                margin-left: 0;
            }}
            .button {{
                display: inline-block;
                background-color: #0066cc;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                text-decoration: none;
                margin-top: 10px;
            }}
            .button:hover {{
                background-color: #0055aa;
            }}
        </style>
    </head>
    <body>
        <h1>Profile</h1>
        
        <nav>
            <a href="/">Home</a>
            <a href="/cookies">Cookies Demo</a>
            <a href="/profile">Profile</a>
            <a href="/logout">Logout</a>
        </nav>
        
        <div class="card">
            <h2>Welcome, {req.user['name']}!</h2>
            <p>This is a protected page that only authenticated users can access.</p>
            
            <h3>Your Profile Information</h3>
            <dl class="user-info">
                <dt>Username:</dt>
                <dd>{req.user['username']}</dd>
                
                <dt>Name:</dt>
                <dd>{req.user['name']}</dd>
                
                <dt>Email:</dt>
                <dd>{req.user['email']}</dd>
                
                <dt>User ID:</dt>
                <dd>{req.user['id']}</dd>
                
                <dt>Created:</dt>
                <dd>{req.user['created_at']}</dd>
            </dl>
            
            <a href="/logout" class="button">Logout</a>
        </div>
        
        <div class="card">
            <h2>How Authentication Works</h2>
            <p>This page is protected by the <code>auth_required</code> middleware. Here's how it works:</p>
            <ol>
                <li>When you log in, the server creates a session and sets a session cookie.</li>
                <li>On each request, the <code>session_middleware</code> checks for a valid session.</li>
                <li>If a valid session is found, the user is loaded and attached to the request.</li>
                <li>Protected routes use the <code>auth_required</code> middleware to ensure the user is authenticated.</li>
                <li>If not authenticated, you're redirected to the login page.</li>
            </ol>
        </div>
        
        <div class="card">
            <h2>Session Information</h2>
            <pre>{json.dumps(req.session, indent=2)}</pre>
        </div>
    </body>
    </html>
    ''')

# ------------------------------------------------------------
# Start the Server
# ------------------------------------------------------------

if __name__ == '__main__':
    print("Sessions and cookies example running on http://localhost:3000")
    print("Available test accounts:")
    print("  - Username: admin, Password: password")
    print("  - Username: user, Password: password")
    
    app.listen(port=3000, hostname='127.0.0.1') 