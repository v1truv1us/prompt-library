#!/usr/bin/env python3
"""
Gmail monitoring using Google Workspace CLI (gws).
Monitors multiple Gmail accounts for unread messages.
"""
import subprocess
import sys
import json
from pathlib import Path

# Gmail addresses to monitor
GMAIL_ACCOUNTS = [
    "johncferguson90@gmail.com",
    "snobord4life@gmail.com"
]

def check_gws_installed():
    """Check if gws is installed"""
    try:
        result = subprocess.run(
            ["gws", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def get_gmail_profile():
    """Get current Gmail profile"""
    try:
        result = subprocess.run(
            ["gws", "gmail", "users", "getProfile", "--params", '{"userId": "me"}'],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        return None
    except Exception as e:
        print(f"Error getting profile: {e}", file=sys.stderr)
        return None

def get_unread_messages(max_results=10):
    """Get unread messages using gws gmail +triage helper"""
    try:
        result = subprocess.run(
            ["gws", "gmail", "+triage", "--limit", str(max_results)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            # +triage returns NDJSON (one JSON object per line)
            messages = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        messages.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
            return messages
        return []
    except Exception as e:
        print(f"Error getting messages: {e}", file=sys.stderr)
        return []

def check_gmail_accounts():
    """Check all configured Gmail accounts"""
    if not check_gws_installed():
        print("❌ gws not installed!")
        print("\nInstall with:")
        print("  brew install googleworkspace-cli")
        print("  # or")
        print("  npm install -g @googleworkspace/cli")
        sys.exit(1)
    
    # Get current profile
    profile = get_gmail_profile()
    if not profile:
        print("❌ Not authenticated with gws!")
        print("\nRun: gws auth setup")
        print("Then: gws auth login -s gmail")
        sys.exit(1)
    
    email_address = profile.get('emailAddress', 'Unknown')
    
    # Check if this account is in our list
    if email_address not in GMAIL_ACCOUNTS:
        print(f"⚠️  Logged in as {email_address}, but monitoring:")
        for acc in GMAIL_ACCOUNTS:
            print(f"  - {acc}")
        print("\nTo switch accounts, run: gws auth login")
    
    # Get unread messages
    messages = get_unread_messages(max_results=10)
    
    result = {
        'email': email_address,
        'unread_count': len(messages),
        'messages': []
    }
    
    # Format messages
    for msg in messages[:5]:  # Limit to 5
        result['messages'].append({
            'from': msg.get('from', 'Unknown'),
            'subject': msg.get('subject', 'No Subject'),
            'date': msg.get('date', 'Unknown')
        })
    
    return [result]

def main():
    """Main entry point"""
    import argparse
    parser = argparse.ArgumentParser(description='Check Gmail accounts via gws')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--recent', action='store_true', help='Show recent unread messages')
    args = parser.parse_args()
    
    results = check_gmail_accounts()
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for account in results:
            email = account['email']
            count = account['unread_count']
            print(f"\n📧 {email}: {count} unread")
            
            if count > 0:
                for msg in account['messages']:
                    subject = msg['subject'][:60]
                    print(f"  • {subject}")
                    print(f"    From: {msg['from'][:50]}")

if __name__ == '__main__':
    main()
