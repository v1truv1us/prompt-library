#!/usr/bin/env python3
"""
Watch for new Gmail messages using gws +watch.
Streams new messages as they arrive.
"""
import subprocess
import sys
import json
from datetime import datetime

def watch_gmail():
    """Watch for new Gmail messages"""
    print(f"👀 Watching for new Gmail messages... (Ctrl+C to stop)")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    try:
        # Use gws gmail +watch to stream new messages
        process = subprocess.Popen(
            ["gws", "gmail", "+watch"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        for line in process.stdout:
            if line.strip():
                try:
                    msg = json.loads(line)
                    # Format and display new message
                    print(f"\n📧 New message at {datetime.now().strftime('%H:%M:%S')}")
                    print(f"  From: {msg.get('from', 'Unknown')}")
                    print(f"  Subject: {msg.get('subject', 'No Subject')[:70]}")
                    print(f"  ID: {msg.get('id', 'Unknown')}")
                except json.JSONDecodeError:
                    print(f"  Raw: {line.strip()}")
    
    except KeyboardInterrupt:
        print("\n\n👋 Stopped watching")
        process.terminate()
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    watch_gmail()
