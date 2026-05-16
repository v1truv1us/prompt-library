#!/usr/bin/env python3
"""
Cost Dashboard Server - Serves the TailClaude-style cost visibility dashboard
"""

import http.server
import socketserver
import json
import subprocess
import os
from pathlib import Path
from urllib.parse import urlparse

WORKSPACE = Path(__file__).parent.parent
SCRIPTS_DIR = WORKSPACE / "scripts"
REPORTS_DIR = WORKSPACE / "reports"

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SCRIPTS_DIR), **kwargs)
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == "/" or parsed.path == "/index.html":
            # Serve the dashboard HTML
            self.path = "/cost-dashboard.html"
            return super().do_GET()
        
        elif parsed.path == "/reports/cost-tracker.json":
            # Generate fresh data on request
            self.generate_data()
            self.path = parsed.path
            return super().do_GET()
        
        elif parsed.path == "/api/refresh":
            # Force refresh endpoint
            self.generate_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "message": "Data refreshed"}).encode())
            return
        
        elif parsed.path == "/api/data":
            # JSON API endpoint
            self.generate_data()
            data = self.read_data()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
            return
        
        return super().do_GET()
    
    def generate_data(self):
        """Run the cost tracker to generate fresh JSON data"""
        try:
            subprocess.run(
                ["python3", str(SCRIPTS_DIR / "cost-tracker.py"), "--json"],
                capture_output=True,
                cwd=str(WORKSPACE),
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error generating data: {e.stderr.decode()}")
    
    def read_data(self):
        """Read the generated JSON data"""
        data_path = REPORTS_DIR / "cost-tracker.json"
        if data_path.exists():
            with open(data_path) as f:
                return json.load(f)
        return {"error": "No data available", "sessions": [], "daily": {}}
    
    def log_message(self, format, *args):
        print(f"[Dashboard] {args[0]}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Cost Dashboard Server")
    parser.add_argument("--port", type=int, default=8765, help="Port to serve on")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    args = parser.parse_args()
    
    # Ensure reports directory exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate initial data
    print("📊 Generating initial cost data...")
    subprocess.run(
        ["python3", str(SCRIPTS_DIR / "cost-tracker.py")],
        cwd=str(WORKSPACE),
        capture_output=True
    )
    
    # Start server
    with socketserver.TCPServer((args.host, args.port), DashboardHandler) as httpd:
        url = f"http://{args.host}:{args.port}"
        print(f"\n💰 Cost Dashboard running at {url}")
        print(f"   Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Dashboard stopped")


if __name__ == "__main__":
    main()
