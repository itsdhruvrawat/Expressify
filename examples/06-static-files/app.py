"""
Expressify Static Files Example

This example demonstrates how to:
- Set up static files middleware
- Serve CSS, JavaScript, and image files
- Organize static assets
"""

from expressify import expressify
from expressify.lib.middleware import Middleware
import os

# Create a new Expressify application
app = expressify()

# Set up static files middleware
# Method 1: Serve files from the 'public' directory at the root URL path
public_dir = os.path.join(os.path.dirname(__file__), 'public')
app.use(Middleware.static(public_dir))

# Method 2: Serve files from a directory at a specific URL path
# This mounts the 'public/assets' directory at the '/assets' URL path
assets_dir = os.path.join(os.path.dirname(__file__), 'public', 'assets')
app.use('/assets', Middleware.static(assets_dir))

# Home route
@app.get('/')
def home(req, res):
    """Home page that demonstrates static file usage"""
    res.type('html').send("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Expressify Static Files Example</title>
    <!-- Immediate dark mode application -->
    <script>
        // Apply dark mode immediately if saved in localStorage
        (function() {
            try {
                const savedTheme = localStorage.getItem('theme');
                console.log('Initial theme check:', savedTheme);
                if (savedTheme === 'dark') {
                    document.documentElement.classList.add('dark-mode');
                    document.documentElement.setAttribute('data-theme', 'dark');
                    document.write('<style>html, body { background-color: #222; color: #e0e0e0; }</style>');
                } else {
                    document.documentElement.setAttribute('data-theme', 'light');
                }
            } catch (e) {
                console.error('Theme initialization error:', e);
            }
        })();
    </script>
    <!-- CSS from root path -->
    <link rel="stylesheet" href="/css/styles.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>Static Files in Expressify</h1>
            <p>This example demonstrates how to serve static files such as CSS, JavaScript, and images.</p>
        </header>
        
        <main>
            <section class="card">
                <h2>How Static Files Work</h2>
                <p>There are two ways to serve static files in Expressify:</p>
                
                <h3>Method 1: Serve from root path</h3>
                <pre><code>app.use(Middleware.static(public_dir))</code></pre>
                <p>This serves files from the public directory at the root path:</p>
                <ul>
                    <li><code>public/css/styles.css</code> → <code>/css/styles.css</code></li>
                    <li><code>public/js/script.js</code> → <code>/js/script.js</code></li>
                    <li><code>public/images/logo.png</code> → <code>/images/logo.png</code></li>
                </ul>
                
                <h3>Method 2: Serve from a specific path</h3>
                <pre><code>app.use('/assets', Middleware.static(assets_dir))</code></pre>
                <p>This mounts the assets directory at the /assets URL path:</p>
                <ul>
                    <li><code>public/assets/icons/icon.svg</code> → <code>/assets/icons/icon.svg</code></li>
                </ul>
            </section>
            
            <section class="card">
                <h2>CSS Example</h2>
                <p>This page is styled using a CSS file served from <code>/css/styles.css</code>.</p>
                <div class="buttons">
                    <button class="btn primary">Primary Button</button>
                    <button class="btn secondary" id="themeToggle" onclick="window.toggleTheme && window.toggleTheme(); return false;">Toggle Dark Mode</button>
                </div>
                <div id="themeStatus" class="result" style="font-size: 0.8em;">
                    Current theme: <span id="currentTheme">light</span><br>
                    HTML data-theme: <span id="htmlTheme">light</span>
                </div>
            </section>
            
            <section class="card">
                <h2>Image Example</h2>
                <div class="image-container">
                    <img src="/images/logo.png" alt="Expressify Logo" class="logo">
                    <!-- Asset from mounted path -->
                    <img src="/assets/icons/icon.svg" alt="Icon" class="icon" width="50">
                </div>
            </section>
            
            <section class="card">
                <h2>JavaScript Example</h2>
                <p>Click the button below to trigger a JavaScript function:</p>
                <button id="clickMe" class="btn primary">Click Me</button>
                <div id="result" class="result"></div>
            </section>
            
            <section class="card">
                <h2>File Structure</h2>
                <pre>
public/
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── images/
│   └── logo.png
└── assets/
    └── icons/
        └── icon.svg
                </pre>
            </section>
        </main>
        
        <footer>
            <p>Expressify Static Files Example</p>
        </footer>
    </div>
    
    <!-- JavaScript from root path -->
    <script src="/js/script.js"></script>
    
    <!-- Direct toggle functionality as fallback -->
    <script>
        // Immediately define a global toggleTheme function as a fallback
        (function() {
            console.log('Setting up fallback toggle function');
            
            // Define global toggle function that will be overridden by script.js if it loads
            window.toggleTheme = function() {
                try {
                    console.log('Inline fallback toggle theme called');
                    const html = document.documentElement;
                    const isDark = html.getAttribute('data-theme') === 'dark';
                    const newTheme = isDark ? 'light' : 'dark';
                    
                    // Toggle attribute
                    html.setAttribute('data-theme', newTheme);
                    
                    // Toggle class
                    if (newTheme === 'dark') {
                        html.classList.add('dark-mode');
                    } else {
                        html.classList.remove('dark-mode');
                    }
                    
                    // Save theme
                    localStorage.setItem('theme', newTheme);
                    
                    // Update button text
                    const themeToggle = document.getElementById('themeToggle');
                    if (themeToggle) {
                        themeToggle.textContent = newTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode';
                    }
                    
                    // Update status display
                    const statusPanel = document.getElementById('themeStatus');
                    if (statusPanel) {
                        const currentTheme = document.getElementById('currentTheme');
                        const htmlTheme = document.getElementById('htmlTheme');
                        if (currentTheme) currentTheme.textContent = newTheme;
                        if (htmlTheme) htmlTheme.textContent = newTheme;
                    }
                    
                    console.log('Theme toggled to:', newTheme);
                    return false;
                } catch (e) {
                    console.error('Theme toggle error:', e);
                    return false;
                }
            };
            
            // Add a direct click handler for the theme toggle button
            document.addEventListener('DOMContentLoaded', function() {
                const themeToggle = document.getElementById('themeToggle');
                if (themeToggle) {
                    console.log('Adding click handler to theme toggle button');
                    themeToggle.addEventListener('click', function(e) {
                        console.log('Theme toggle button clicked');
                        e.preventDefault();
                        window.toggleTheme();
                        return false;
                    });
                } else {
                    console.warn('Theme toggle button not found during fallback setup');
                }
            });
        })();
    </script>
</body>
</html>
""")

# ------------------------------------------------------------
# Create static files if they don't exist
# ------------------------------------------------------------

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs(os.path.join(os.path.dirname(__file__), 'public', 'css'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'public', 'js'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'public', 'images'), exist_ok=True)
    os.makedirs(os.path.join(os.path.dirname(__file__), 'public', 'assets', 'icons'), exist_ok=True)
    
    # Create CSS file if it doesn't exist
    css_file = os.path.join(os.path.dirname(__file__), 'public', 'css', 'styles.css')
    if not os.path.exists(css_file):
        with open(css_file, 'w') as f:
            f.write("""/* styles.css */
:root {
    --primary-color: #0066cc;
    --primary-hover: #0055aa;
    --secondary-color: #f0f0f0;
    --secondary-hover: #e0e0e0;
    --text-color: #333;
    --background-color: #f5f5f5;
    --card-background: white;
    --card-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    --code-background: #f0f0f0;
    --footer-color: var(--primary-color);
    --footer-text: white;
    --transition-speed: 0.3s;
}

/* Dark mode styles */
[data-theme="dark"],
html.dark-mode {
    --primary-color: #3a86ff !important;
    --primary-hover: #4a94ff !important;
    --secondary-color: #444 !important;
    --secondary-hover: #555 !important;
    --text-color: #e0e0e0 !important;
    --background-color: #222 !important;
    --card-background: #333 !important;
    --card-shadow: 0 2px 4px rgba(0, 0, 0, 0.3) !important;
    --code-background: #444 !important;
    --footer-color: #1a1a1a !important;
    --footer-text: #e0e0e0 !important;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

/* Direct color application for dark mode to prevent FOUC */
[data-theme="dark"],
html.dark-mode {
    background-color: #222;
    color: #e0e0e0;
}

[data-theme="dark"] body,
html.dark-mode body {
    background-color: #222;
    color: #e0e0e0;
}

/* Transitions */
html, body, .card, pre, code, h1, h2, h3, .result, footer {
    transition: background-color 0.3s, color 0.3s, border-color 0.3s, box-shadow 0.3s;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    background: linear-gradient(135deg, var(--primary-color), #0088ff);
    color: white;
    padding: 30px;
    margin-bottom: 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

header h1 {
    margin-bottom: 15px;
    font-size: 2.5rem;
}

header p {
    font-size: 1.1rem;
    opacity: 0.9;
}

.card {
    background-color: var(--card-background);
    padding: 25px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: var(--card-shadow);
    transition: transform 0.2s, background-color var(--transition-speed);
}

.card:hover {
    transform: translateY(-3px);
}

h1, h2, h3 {
    margin-bottom: 15px;
}

h2 {
    color: var(--primary-color);
    border-bottom: 2px solid var(--primary-color);
    padding-bottom: 8px;
    margin-bottom: 20px;
}

h3 {
    margin-top: 20px;
    color: #444;
}

[data-theme="dark"] h3,
html.dark-mode h3 {
    color: #ccc !important;
}

ul {
    margin-left: 25px;
    margin-bottom: 20px;
}

li {
    margin-bottom: 8px;
}

code {
    background-color: var(--code-background);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', Courier, monospace;
    font-size: 0.9em;
}

pre {
    background-color: var(--code-background);
    padding: 15px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 15px 0;
    border-left: 4px solid var(--primary-color);
}

pre code {
    background-color: transparent;
    padding: 0;
}

.btn {
    display: inline-block;
    padding: 10px 18px;
    margin-right: 12px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.3s;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.primary {
    background-color: var(--primary-color);
    color: white;
    box-shadow: 0 2px 4px rgba(0, 102, 204, 0.3);
}

.primary:hover {
    background-color: var(--primary-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 102, 204, 0.4);
}

.secondary {
    background-color: var(--secondary-color);
    color: var(--text-color);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.secondary:hover {
    background-color: var(--secondary-hover);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.buttons {
    margin: 20px 0;
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.image-container {
    text-align: center;
    margin: 25px 0;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 30px;
    flex-wrap: wrap;
}

.logo {
    max-width: 200px;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    transition: transform 0.3s;
}

.logo:hover {
    transform: scale(1.05);
}

.icon {
    display: inline-block;
    transition: transform 0.3s;
}

.icon:hover {
    transform: rotate(15deg);
}

.result {
    margin-top: 15px;
    padding: 15px;
    background-color: var(--code-background);
    border-radius: 6px;
    min-height: 50px;
    border-left: 4px solid var(--primary-color);
}

footer {
    background-color: var(--footer-color);
    color: var(--footer-text);
    padding: 25px;
    text-align: center;
    border-radius: 8px;
    margin-top: 30px;
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

/* Responsive adjustments */
@media (max-width: 768px) {
    header {
        padding: 20px;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    .card {
        padding: 15px;
    }
    
    .buttons {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
        margin-bottom: 10px;
        margin-right: 0;
    }
}

/* Enhanced animation effects */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.card {
    animation: fadeIn 0.5s ease forwards;
}

.card:nth-child(1) { animation-delay: 0.1s; }
.card:nth-child(2) { animation-delay: 0.2s; }
.card:nth-child(3) { animation-delay: 0.3s; }
.card:nth-child(4) { animation-delay: 0.4s; }
.card:nth-child(5) { animation-delay: 0.5s; }

.clicked {
    transform: scale(0.95) !important;
}
""")
    
    # Create JavaScript file if it doesn't exist
    js_file = os.path.join(os.path.dirname(__file__), 'public', 'js', 'script.js')
    if not os.path.exists(js_file):
        with open(js_file, 'w') as f:
            f.write("""// script.js
// Update theme status panel
function updateThemeStatus() {
    const themeStatus = document.getElementById('themeStatus');
    if (!themeStatus) return;
    
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.getElementById('currentTheme').textContent = isDark ? 'dark' : 'light';
    document.getElementById('htmlTheme').textContent = 
        document.documentElement.getAttribute('data-theme') || 'none';
}

// Toggle theme function
function toggleTheme() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const newTheme = isDark ? 'light' : 'dark';
    
    // Update data attribute
    document.documentElement.setAttribute('data-theme', newTheme);
    
    // Update class for legacy support
    if (newTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
    } else {
        document.documentElement.classList.remove('dark-mode');
    }
    
    // Save preference
    localStorage.setItem('theme', newTheme);
    
    // Update button text
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.textContent = newTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode';
    }
    
    // Update status display
    updateThemeStatus();
    
    console.log('Theme toggled to:', newTheme);
}

document.addEventListener('DOMContentLoaded', function() {
    // Initial setup
    const savedTheme = localStorage.getItem('theme') || 'light';
    
    // Set theme on document
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
    }
    
    // Basic button functionality
    const button = document.getElementById('clickMe');
    const result = document.getElementById('result');
    const themeToggle = document.getElementById('themeToggle');
    
    // Click counter for the button demo
    let clickCount = 0;
    
    // Add click event listener to button
    if (button && result) {
        button.addEventListener('click', function() {
            // Increment click count
            clickCount++;
            
            // Update result text
            result.textContent = `Button clicked ${clickCount} time${clickCount !== 1 ? 's' : ''}!`;
            
            // Change result background color
            const colors = ['#ffcccb', '#ccffcc', '#cce5ff', '#ffffcc', '#e5ccff'];
            result.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
            
            // Add a little animation
            button.classList.add('clicked');
            setTimeout(() => {
                button.classList.remove('clicked');
            }, 200);
        });
    }
    
    // Theme toggle functionality
    if (themeToggle) {
        // Set toggle button text based on current theme
        themeToggle.textContent = savedTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode';
        
        // Handle theme toggle click
        themeToggle.addEventListener('click', function() {
            toggleTheme();
            
            // Add a little animation
            themeToggle.classList.add('clicked');
            setTimeout(() => {
                themeToggle.classList.remove('clicked');
            }, 200);
        });
    }
    
    // Add some dynamic effects
    const cards = document.querySelectorAll('.card');
    
    // Set initial opacity to 0 for fade-in effect
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        setTimeout(() => {
            card.style.opacity = '1';
        }, 100 * index);
    });
    
    // Initial theme status update
    updateThemeStatus();
});
""")
    
    # Create a simple logo if it doesn't exist
    logo_file = os.path.join(os.path.dirname(__file__), 'public', 'images', 'logo.png')
    if not os.path.exists(logo_file):
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create a simple logo image
            img = Image.new('RGB', (200, 200), color=(0, 102, 204))
            d = ImageDraw.Draw(img)
            
            # Try to use a font if available
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                # Fallback to default font
                try:
                    font = ImageFont.load_default()
                except:
                    font = None
            
            # Draw text on image
            if font:
                d.text((50, 80), "Expressify", fill=(255, 255, 255), font=font)
            else:
                d.text((50, 80), "Expressify", fill=(255, 255, 255))
            
            # Save the image
            img.save(logo_file)
            
        except Exception as e:
            print(f"Could not create logo image: {e}")
            print("Creating a placeholder file instead")
            
            # Create a placeholder text file
            with open(logo_file, 'w') as f:
                f.write("Expressify Logo Placeholder")
    
    # Create a simple SVG icon if it doesn't exist
    icon_file = os.path.join(os.path.dirname(__file__), 'public', 'assets', 'icons', 'icon.svg')
    if not os.path.exists(icon_file):
        with open(icon_file, 'w') as f:
            f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0066cc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="10"></circle>
  <line x1="12" y1="8" x2="12" y2="16"></line>
  <line x1="8" y1="12" x2="16" y2="12"></line>
</svg>""")
    
    print("Static files example running on http://localhost:3000")
    app.listen(port=3000, hostname='127.0.0.1')
