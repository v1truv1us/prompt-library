#!/usr/bin/env python3
"""
Helper script to set up Gmail connections via Maton API.
"""
import os
import sys
import json
import urllib.request

def create_connection():
    """Create a new Gmail connection and return OAuth URL"""
    if 'MATON_API_KEY' not in os.environ:
        print("❌ MATON_API_KEY not set!")
        print("\n1. Get your API key at: https://maton.ai/settings")
        print("2. Add to ~/.zshrc: export MATON_API_KEY=\"your-key-here\"")
        print("3. Run: source ~/.zshrc")
        print("4. Run this script again")
        sys.exit(1)
    
    print("Creating Gmail connection...")
    
    data = json.dumps({'app': 'google-mail'}).encode()
    req = urllib.request.Request(
        'https://ctrl.maton.ai/connections',
        data=data,
        method='POST'
    )
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        response = urllib.request.urlopen(req)
        result = json.load(response)
        conn = result.get('connection', {})
        
        print("\n✅ Connection created!")
        print(f"\nConnection ID: {conn.get('connection_id')}")
        print(f"\n🔗 Open this URL to authorize Gmail access:")
        print(f"\n{conn.get('url')}\n")
        print("After authorizing, the connection will be active.")
        
        return conn
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ Error creating connection: {e.code}")
        print(error_body)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def list_connections():
    """List all active Gmail connections"""
    if 'MATON_API_KEY' not in os.environ:
        print("❌ MATON_API_KEY not set!")
        return
    
    print("Checking Gmail connections...\n")
    
    req = urllib.request.Request(
        'https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE'
    )
    req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
    
    try:
        response = urllib.request.urlopen(req)
        result = json.load(response)
        connections = result.get('connections', [])
        
        if not connections:
            print("No active Gmail connections found.")
            print("Run: python3 scripts/gmail-setup.py --create")
            return
        
        print(f"Found {len(connections)} active connection(s):\n")
        
        # Get profile for each connection to show email address
        for conn in connections:
            conn_id = conn.get('connection_id')
            profile_req = urllib.request.Request(
                'https://gateway.maton.ai/google-mail/gmail/v1/users/me/profile'
            )
            profile_req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
            profile_req.add_header('Maton-Connection', conn_id)
            
            try:
                profile_response = urllib.request.urlopen(profile_req)
                profile = json.load(profile_response)
                email = profile.get('emailAddress', 'Unknown')
                print(f"  • {email}")
                print(f"    ID: {conn_id}")
                print(f"    Created: {conn.get('creation_time', 'Unknown')}")
            except:
                print(f"  • Connection {conn_id} (unable to get profile)")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Gmail connection setup')
    parser.add_argument('--create', action='store_true', help='Create new connection')
    parser.add_argument('--list', action='store_true', help='List existing connections')
    args = parser.parse_args()
    
    if args.create:
        create_connection()
    elif args.list:
        list_connections()
    else:
        print("Gmail Setup Helper\n")
        print("Usage:")
        print("  python3 scripts/gmail-setup.py --create   # Create new connection")
        print("  python3 scripts/gmail-setup.py --list     # List connections")

if __name__ == '__main__':
    main()
