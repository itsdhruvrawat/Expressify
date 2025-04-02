// script.js
console.log('Script.js loaded');

// Update theme status panel
function updateThemeStatus() {
    try {
        const themeStatus = document.getElementById('themeStatus');
        if (!themeStatus) {
            console.log('Theme status panel not found');
            return;
        }
        
        const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
        console.log('Updating theme status. Current theme:', isDark ? 'dark' : 'light');
        
        document.getElementById('currentTheme').textContent = isDark ? 'dark' : 'light';
        document.getElementById('htmlTheme').textContent = 
            document.documentElement.getAttribute('data-theme') || 'none';
    } catch (e) {
        console.error('Error in updateThemeStatus:', e);
    }
}

// Toggle theme function
function toggleTheme() {
    try {
        console.log('Main toggle theme called');
        const html = document.documentElement;
        const isDark = html.getAttribute('data-theme') === 'dark';
        const newTheme = isDark ? 'light' : 'dark';
        
        console.log('Current theme:', isDark ? 'dark' : 'light');
        console.log('Setting new theme to:', newTheme);
        
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
        console.log('Theme saved to localStorage');
        
        // Update button text
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.textContent = newTheme === 'dark' ? 'Toggle Light Mode' : 'Toggle Dark Mode';
            console.log('Button text updated');
        } else {
            console.warn('Theme toggle button not found');
        }
        
        // Update status display
        updateThemeStatus();
        
        console.log('Theme toggle complete. New theme:', newTheme);
        return false;
    } catch (e) {
        console.error('Theme toggle error:', e);
        return false;
    }
}

// Make toggleTheme available globally
window.toggleTheme = toggleTheme;
console.log('Toggle theme function attached to window object');

document.addEventListener('DOMContentLoaded', function() {
    // Initial setup
    try {
        const savedTheme = localStorage.getItem('theme') || 'light';
        console.log("DOM content loaded, applying theme:", savedTheme);
        
        // Set theme on document
        document.documentElement.setAttribute('data-theme', savedTheme);
        if (savedTheme === 'dark') {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
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
            themeToggle.addEventListener('click', function(e) {
                e.preventDefault();
                toggleTheme();
                
                // Add a little animation
                themeToggle.classList.add('clicked');
                setTimeout(() => {
                    themeToggle.classList.remove('clicked');
                }, 200);
                
                return false;
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
    } catch (e) {
        console.error('Error in DOM ready handler:', e);
    }
}); 