#!/usr/bin/env python3
"""
ProtonMail Daily Client Review via IMAP Bridge
Connects to ProtonMail Bridge and scans for client emails.
"""

import imaplib
import email
from email.header import decode_header
import json
import os
from datetime import datetime, timedelta
import re

# Config path
CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/scripts/protonmail-config.json")

def load_config():
    """Load configuration from JSON file."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return None

def decode_mime_words(s):
    """Decode MIME encoded words in email headers."""
    if s is None:
        return ""
    decoded_parts = decode_header(s)
    result = []
    for part, charset in decoded_parts:
        if isinstance(part, bytes):
            result.append(part.decode(charset or 'utf-8', errors='replace'))
        else:
            result.append(part)
    return ''.join(result)

def get_email_address(from_header):
    """Extract email address from From header."""
    if not from_header:
        return ""
    # Try to extract email from "Name <email@domain.com>" format
    match = re.search(r'<([^>]+)>', from_header)
    if match:
        return match.group(1).lower()
    # Otherwise return the whole thing cleaned up
    return from_header.strip().lower()

def connect_imap(config):
    """Connect to ProtonMail Bridge IMAP server."""
    imap_host = config.get('imap_host', '127.0.0.1')
    imap_port = config.get('imap_port', 1143)
    
    mail = imaplib.IMAP4(imap_host, imap_port)
    mail.login(config['username'], config['password'])
    return mail

def scan_for_client_emails(mail, client_emails, days_back=1):
    """Scan inbox for emails from client addresses."""
    results = {
        'scanned_at': datetime.now().isoformat(),
        'clients_found': {},
        'uncategorized': [],
        'total_unread': 0
    }
    
    # Select inbox
    mail.select('INBOX')
    
    # Search for unread messages from last N days
    since_date = (datetime.now() - timedelta(days=days_back)).strftime("%d-%b-%Y")
    
    # Get all unread messages
    status, messages = mail.search(None, 'UNSEEN')
    
    if status != 'OK':
        return results
    
    message_ids = messages[0].split()
    results['total_unread'] = len(message_ids)
    
    for msg_id in message_ids:
        status, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
        
        if status != 'OK':
            continue
        
        # Parse email headers
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        from_addr = decode_mime_words(msg.get('From', ''))
        subject = decode_mime_words(msg.get('Subject', ''))
        date = msg.get('Date', '')
        
        email_addr = get_email_address(from_addr)
        
        # Check if from a client
        found_client = False
        for client_name, client_data in client_emails.items():
            client_email_list = client_data if isinstance(client_data, list) else client_data.get('emails', [])
            if any(client_email.lower() in email_addr for client_email in client_email_list):
                if client_name not in results['clients_found']:
                    results['clients_found'][client_name] = []
                results['clients_found'][client_name].append({
                    'from': from_addr,
                    'email': email_addr,
                    'subject': subject,
                    'date': date
                })
                found_client = True
                break
        
        if not found_client and email_addr:
            results['uncategorized'].append({
                'from': from_addr,
                'email': email_addr,
                'subject': subject,
                'date': date
            })
    
    return results

def format_report(results):
    """Format results as a readable report."""
    lines = ["📬 **ProtonMail Client Review**", ""]
    
    if 'total_unread' in results:
        lines.append(f"**Unread emails:** {results['total_unread']}")
    if 'total_scanned' in results:
        lines.append(f"**Messages scanned:** {results['total_scanned']}")
    
    lines.append(f"**Scanned:** {results['scanned_at']}")
    lines.append("")
    
    if results['clients_found']:
        lines.append("## ✉️ Client Emails Found")
        for client, emails in results['clients_found'].items():
            lines.append(f"\n**{client}:**")
            for e in emails:
                lines.append(f"  • {e['subject'][:60]}{'...' if len(e['subject']) > 60 else ''}")
                lines.append(f"    _From: {e['from'][:50]}_")
    
    if results.get('uncategorized'):
        lines.append("\n## ❓ Uncategorized (Potential Clients/Leads)")
        for e in results['uncategorized'][:10]:  # Limit to 10
            lines.append(f"  • **{e['subject'][:50]}{'...' if len(e['subject']) > 50 else ''}**")
            lines.append(f"    _{e['email']}_")
        
        if len(results['uncategorized']) > 10:
            lines.append(f"  _...and {len(results['uncategorized']) - 10} more_")
    
    if not results['clients_found'] and not results.get('uncategorized'):
        lines.append("✅ No client emails in this scan.")
    
    return '\n'.join(lines)

def scan_recent_for_clients(mail, client_emails, days_back=7):
    """Scan recent messages (read or unread) for client emails."""
    results = {
        'scanned_at': datetime.now().isoformat(),
        'clients_found': {},
        'total_scanned': 0
    }
    
    mail.select('INBOX')
    status, messages = mail.search(None, 'ALL')
    
    if status != 'OK':
        return results
    
    message_ids = messages[0].split()[-50:]  # Last 50 messages
    results['total_scanned'] = len(message_ids)
    
    for msg_id in message_ids:
        status, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])')
        if status != 'OK':
            continue
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        from_addr = decode_mime_words(msg.get('From', ''))
        subject = decode_mime_words(msg.get('Subject', ''))
        date = msg.get('Date', '')
        
        email_addr = get_email_address(from_addr)
        
        for client_name, client_data in client_emails.items():
            client_email_list = client_data if isinstance(client_data, list) else client_data.get('emails', [])
            if any(client_email.lower() in email_addr for client_email in client_email_list):
                if client_name not in results['clients_found']:
                    results['clients_found'][client_name] = []
                results['clients_found'][client_name].append({
                    'from': from_addr,
                    'email': email_addr,
                    'subject': subject,
                    'date': date
                })
                break
    
    return results

def main():
    import sys
    
    config = load_config()
    
    if not config:
        print("❌ No configuration found. Run setup first.")
        print(f"Create {CONFIG_PATH} with your ProtonMail Bridge credentials.")
        return
    
    try:
        mail = connect_imap(config)
        
        # Check if --recent flag to show recent client activity
        if '--recent' in sys.argv:
            results = scan_recent_for_clients(
                mail,
                config.get('clients', {}),
                config.get('days_back', 7)
            )
            report = format_report(results)
        else:
            # Default: check unread only
            results = scan_for_client_emails(
                mail,
                config.get('clients', {}),
                config.get('days_back', 1)
            )
            report = format_report(results)
        
        mail.logout()
        
        print(report)
        
        # Also save results to JSON for further processing
        output_path = os.path.expanduser("~/.openclaw/workspace/reports/email-review.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
