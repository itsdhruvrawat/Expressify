#!/usr/bin/env python3
"""
Expressify Development Server with Hot Reloading

This script provides a development server with automatic reloading
when source files change. It monitors the current directory and restarts
the application when any Python file changes.

Usage:
    python dev.py app.py
    python dev.py examples/01-hello-world/app.py
"""

import argparse
import importlib.util
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from types import ModuleType
from typing import Any, List, Optional

try:
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
except ImportError:
    print("watchdog package is required for dev server. Install it with:")
    print("pip install watchdog")
    sys.exit(1)

class AppReloader(FileSystemEventHandler):
    """Watches for file changes and reloads the application."""
    
    def __init__(self, app_path: str, watch_dirs: List[str] = None):
        self.app_path = app_path
        self.watch_dirs = watch_dirs or ['.']
        self.process: Optional[subprocess.Popen] = None
        self.observer = Observer()
        self.module_name = os.path.basename(app_path).replace('.py', '')
        self.module: Optional[ModuleType] = None
        self.last_reload = 0
        self.reloading = False
        
        # Handle SIGINT (Ctrl+C) gracefully
        signal.signal(signal.SIGINT, self.handle_sigint)
            
    def start(self):
        """Start the development server with hot reloading."""
        print(f"🔥 Expressify development server starting...")
        print(f"📁 Application: {self.app_path}")
        
        # Start watching for file changes
        for watch_dir in self.watch_dirs:
            self.observer.schedule(self, watch_dir, recursive=True)
        self.observer.start()
        
        try:
            self.load_app()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the reloader and clean up resources."""
        print("\n🛑 Shutting down development server...")
        if self.process:
            self.kill_process()
        self.observer.stop()
        self.observer.join()
        print("👋 Server stopped")
        
    def handle_sigint(self, sig, frame):
        """Handle SIGINT (Ctrl+C) signal."""
        self.stop()
        sys.exit(0)
        
    def on_modified(self, event):
        """Called when a file is modified."""
        if event.is_directory:
            return
            
        # Only reload on Python file changes
        if not event.src_path.endswith('.py'):
            return
            
        # Avoid multiple simultaneous reloads
        current_time = time.time()
        if current_time - self.last_reload < 1 or self.reloading:
            return
            
        self.last_reload = current_time
        self.reloading = True
        print(f"\n🔄 File changed: {os.path.basename(event.src_path)}")
        self.reload_app()
        self.reloading = False
    
    def load_app(self):
        """Load or reload the application."""
        if self.process:
            self.kill_process()
        
        print(f"🚀 Starting application: {self.app_path}")
        
        # Start the application as a subprocess
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.app_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1  # Line buffered
            )
            
            # Start threads to read stdout and stderr
            self.start_output_reader(self.process.stdout, "📤")
            self.start_output_reader(self.process.stderr, "⚠️")
            
        except Exception as e:
            print(f"❌ Failed to start application: {e}")
            self.process = None
    
    def reload_app(self):
        """Reload the application after changes."""
        print("🔄 Reloading application...")
        self.load_app()
    
    def kill_process(self):
        """Kill the current process if it exists."""
        if self.process:
            print("🛑 Stopping current process...")
            try:
                # Try to terminate gracefully first
                self.process.terminate()
                # Give it some time to terminate
                for _ in range(5):
                    if self.process.poll() is not None:
                        break
                    time.sleep(0.1)
                    
                # If still running, force kill
                if self.process.poll() is None:
                    self.process.kill()
                    self.process.wait()
            except Exception as e:
                print(f"❌ Error stopping process: {e}")
            
            self.process = None
    
    def start_output_reader(self, pipe, prefix):
        """Start a thread to read output from the subprocess."""
        def reader():
            for line in iter(pipe.readline, ''):
                if line.strip():
                    print(f"{prefix} {line.rstrip()}")
            
        import threading
        thread = threading.Thread(target=reader)
        thread.daemon = True
        thread.start()

def find_watch_dirs(app_path: str) -> List[str]:
    """Find directories to watch for changes."""
    app_dir = os.path.dirname(os.path.abspath(app_path))
    
    # Always watch the directory of the app
    watch_dirs = [app_dir]
    
    # If it's an examples subdirectory, also watch the core expressify package
    if app_dir.startswith(os.path.join(os.getcwd(), 'examples')):
        expressify_dir = os.path.join(os.getcwd(), 'expressify')
        if os.path.exists(expressify_dir):
            watch_dirs.append(expressify_dir)
    
    return watch_dirs

def main():
    """Main entry point for the development server."""
    parser = argparse.ArgumentParser(description="Expressify Development Server with Hot Reloading")
    parser.add_argument('app_path', help="Path to the main application file")
    args = parser.parse_args()
    
    # Ensure the app file exists
    if not os.path.exists(args.app_path):
        print(f"❌ Error: App file not found: {args.app_path}")
        sys.exit(1)
    
    # Find directories to watch
    watch_dirs = find_watch_dirs(args.app_path)
    
    # Start the reloader
    reloader = AppReloader(args.app_path, watch_dirs)
    reloader.start()

if __name__ == "__main__":
    main() 