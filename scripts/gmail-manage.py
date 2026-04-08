#!/usr/bin/env python3
"""
Gmail email management system.
Automatically labels and sorts emails based on configurable rules.
"""
import subprocess
import json
import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

CONFIG_FILE = Path(__file__).parent / "gmail-config.json"

def load_config() -> dict:
    """Load email management configuration"""
    if not CONFIG_FILE.exists():
        print(f"❌ Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    with open(CONFIG_FILE) as f:
        return json.load(f)

def run_gws(args: List[str], credentials_file: Optional[str] = None) -> dict:
    """Run gws command with optional credentials file"""
    env = os.environ.copy()
    if credentials_file:
        env['GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE'] = os.path.expanduser(credentials_file)
    
    cmd = ['gws'] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=env,
        timeout=30
    )
    
    if result.returncode != 0:
        return {"error": result.stderr, "code": result.returncode}
    
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        return {"raw": result.stdout}

def get_labels(credentials_file: str) -> Dict[str, str]:
    """Get all labels, returns {name: id} mapping"""
    result = run_gws(['gmail', 'users', 'labels', 'list', '--params', '{"userId": "me"}'], credentials_file)
    
    labels = {}
    if 'labels' in result:
        for label in result['labels']:
            labels[label['name']] = label['id']
    
    return labels

def create_label(credentials_file: str, name: str, color: str = None) -> Optional[str]:
    """Create a new label and return its ID"""
    label_data = {
        "name": name,
        "labelListVisibility": "labelShow",
        "messageListVisibility": "show"
    }
    
    if color:
        # Map simple color names to Gmail color codes
        color_map = {
            "bg_yellow": {"backgroundColor": "#fb4c2f", "textColor": "#ffffff"},
            "bg_green": {"backgroundColor": "#076231", "textColor": "#ffffff"},
            "bg_red": {"backgroundColor": "#cc3d21", "textColor": "#ffffff"},
            "bg_blue": {"backgroundColor": "#4285f4", "textColor": "#ffffff"},
            "bg_teal": {"backgroundColor": "#20b2aa", "textColor": "#ffffff"},
            "bg_purple": {"backgroundColor": "#8e63ce", "textColor": "#ffffff"},
            "bg_orange": {"backgroundColor": "#ff6d01", "textColor": "#ffffff"},
            "bg_pink": {"backgroundColor": "#cf62b0", "textColor": "#ffffff"},
            "bg_gray": {"backgroundColor": "#414141", "textColor": "#ffffff"},
            "bg_cyan": {"backgroundColor": "#00b8d9", "textColor": "#ffffff"}
        }
        if color in color_map:
            label_data["color"] = color_map[color]
    
    result = run_gws(
        ['gmail', 'users', 'labels', 'create', '--params', '{"userId": "me"}', '--json', json.dumps(label_data)],
        credentials_file
    )
    
    if 'error' in result:
        print(f"  ⚠️  Could not create label {name}: {result['error']}")
        return None
    
    return result.get('id')

def ensure_labels(credentials_file: str, config: dict) -> Dict[str, str]:
    """Ensure all configured labels exist, return {name: id} mapping"""
    existing = get_labels(credentials_file)
    created = []
    
    for label_name, label_config in config.get('labels', {}).items():
        if label_name not in existing:
            print(f"  Creating label: {label_name}")
            label_id = create_label(credentials_file, label_name, label_config.get('color'))
            if label_id:
                existing[label_name] = label_id
                created.append(label_name)
    
    if created:
        print(f"  ✅ Created {len(created)} labels")
    
    return existing

def get_unlabeled_messages(credentials_file: str, max_messages: int = 100) -> List[dict]:
    """Get messages without user labels (only INBOX, CATEGORY_*, etc)"""
    # Get messages from inbox that aren't starred or labeled
    result = run_gws(
        ['gmail', 'users', 'messages', 'list',
         '--params', json.dumps({"userId": "me", "maxResults": max_messages, "q": "in:inbox -has:userlabels"})],
        credentials_file
    )
    
    return result.get('messages', [])

def get_message_details(message_id: str, credentials_file: str) -> Optional[dict]:
    """Get full message details"""
    result = run_gws(
        ['gmail', 'users', 'messages', 'get',
         '--params', json.dumps({"userId": "me", "id": message_id, "format": "metadata",
                                 "metadataHeaders": ["From", "Subject", "To"]})],
        credentials_file
    )
    
    if 'error' in result:
        return None
    
    headers = {h['name']: h['value'] for h in result.get('payload', {}).get('headers', [])}
    
    return {
        'id': message_id,
        'from': headers.get('From', ''),
        'subject': headers.get('Subject', ''),
        'to': headers.get('To', ''),
        'snippet': result.get('snippet', '')
    }

def match_rule(message: dict, rule: dict) -> bool:
    """Check if message matches a labeling rule"""
    from_addr = message.get('from', '').lower()
    subject = message.get('subject', '').lower()
    snippet = message.get('snippet', '').lower()
    
    # Check domains
    for domain in rule.get('domains', []):
        if domain.lower() in from_addr:
            return True
    
    # Check sender patterns
    for sender in rule.get('senders', []):
        if sender.lower() in from_addr:
            return True
    
    # Check keywords in subject or snippet
    combined_text = f"{subject} {snippet}"
    for keyword in rule.get('keywords', []):
        if keyword.lower() in combined_text:
            return True
    
    return False

def apply_label(message_id: str, label_id: str, credentials_file: str) -> bool:
    """Apply label to message"""
    result = run_gws(
        ['gmail', 'users', 'messages', 'modify',
         '--params', json.dumps({"userId": "me", "id": message_id}),
         '--json', json.dumps({"addLabelIds": [label_id]})],
        credentials_file
    )
    
    return 'error' not in result

def process_account(email: str, config: dict, dry_run: bool = False) -> dict:
    """Process a single Gmail account"""
    account_config = config['accounts'].get(email)
    if not account_config:
        return {"error": f"Account {email} not in config"}
    
    print(f"\n📧 Processing {email}...")
    
    creds_file = account_config['credentials_file']
    
    # Ensure labels exist
    labels = ensure_labels(creds_file, config)
    
    # Get unlabeled messages
    print(f"  Fetching unlabeled messages...")
    messages = get_unlabeled_messages(creds_file, max_messages=50)
    
    results = {
        'email': email,
        'processed': 0,
        'labeled': {},
        'errors': 0
    }
    
    if not messages:
        print(f"  ✅ No unlabeled messages found")
        return results
    
    print(f"  Found {len(messages)} unlabeled messages")
    
    # Process each message
    for msg_ref in messages[:20]:  # Limit to 20 per run
        msg_id = msg_ref['id']
        msg = get_message_details(msg_id, creds_file)
        
        if not msg:
            results['errors'] += 1
            continue
        
        results['processed'] += 1
        
        # Check each rule
        for label_name, rule in config.get('rules', {}).items():
            if match_rule(msg, rule):
                label_id = labels.get(label_name)
                if label_id:
                    if dry_run:
                        print(f"  📌 Would label: '{msg['subject'][:40]}...' → {label_name}")
                    else:
                        if apply_label(msg_id, label_id, creds_file):
                            results['labeled'][label_name] = results['labeled'].get(label_name, 0) + 1
    
    # Summary
    if results['labeled']:
        print(f"  ✅ Labeled {sum(results['labeled'].values())} messages:")
        for label, count in results['labeled'].items():
            print(f"     • {label}: {count}")
    else:
        print(f"  ℹ️  No matching rules found for {results['processed']} messages")
    
    return results

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Gmail email management')
    parser.add_argument('--account', help='Process specific account only')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')
    parser.add_argument('--setup-labels', action='store_true', help='Only create labels, don\'t process emails')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()
    
    config = load_config()
    
    if args.setup_labels:
        # Just create labels for all accounts
        for email in config['accounts']:
            ensure_labels(config['accounts'][email]['credentials_file'], config)
        return
    
    results = []
    
    if args.account:
        if args.account not in config['accounts']:
            print(f"❌ Account {args.account} not found in config")
            sys.exit(1)
        results.append(process_account(args.account, config, args.dry_run))
    else:
        for email in config['accounts']:
            results.append(process_account(email, config, args.dry_run))
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"📊 Summary: {len(results)} account(s) processed")
        total_labeled = sum(sum(r.get('labeled', {}).values()) for r in results)
        print(f"   Total messages labeled: {total_labeled}")

if __name__ == '__main__':
    main()
