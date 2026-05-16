#!/usr/bin/env python3
"""
ProtonMail Sender Discovery via IMAP Bridge
Scans inbox to find all unique senders (for setting up client list).
"""

import imaplib
import email
from email.header import decode_header
import json
import os
import re

CONFIG_PATH = os.path.expanduser("~/.openclaw/workspace/scripts/protonmail-config.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    return None

def decode_mime_words(s):
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
    if not from_header:
        return ""
    match = re.search(r'<([^>]+)>', from_header)
    if match:
        return match.group(1).lower()
    return from_header.strip().lower()

def connect_imap(config):
    imap_host = config.get('imap_host', '127.0.0.1')
    imap_port = config.get('imap_port', 1143)
    mail = imaplib.IMAP4(imap_host, imap_port)
    mail.login(config['username'], config['password'])
    return mail

def scan_all_senders(mail, limit=200):
    """Scan inbox for ALL senders."""
    results = {'senders': {}}
    
    mail.select('INBOX')
    status, messages = mail.search(None, 'ALL')
    
    if status != 'OK':
        return results
    
    message_ids = messages[0].split()[-limit:]
    
    for msg_id in message_ids:
        status, msg_data = mail.fetch(msg_id, '(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT)])')
        if status != 'OK':
            continue
        
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        
        from_addr = decode_mime_words(msg.get('From', ''))
        subject = decode_mime_words(msg.get('Subject', ''))
        email_addr = get_email_address(from_addr)
        
        if email_addr:
            domain = email_addr.split('@')[-1] if '@' in email_addr else email_addr
            
            if email_addr not in results['senders']:
                results['senders'][email_addr] = {
                    'from': from_addr,
                    'domain': domain,
                    'count': 0,
                    'subjects': []
                }
            results['senders'][email_addr]['count'] += 1
            if len(results['senders'][email_addr]['subjects']) < 3:
                results['senders'][email_addr]['subjects'].append(subject[:80])
    
    # Sort by frequency
    results['senders'] = dict(sorted(
        results['senders'].items(),
        key=lambda x: x[1]['count'],
        reverse=True
    ))
    
    return results

def main():
    config = load_config()
    if not config:
        print("❌ No config found")
        return
    
    mail = connect_imap(config)
    results = scan_all_senders(mail, limit=200)
    mail.logout()
    
    print("📧 **Recent Email Senders (Top 30 by frequency)**\n")
    print("_Use these to populate your client list_\n")
    
    count = 0
    for email_addr, data in list(results['senders'].items())[:30]:
        subjects_preview = data['subjects'][0][:50] if data['subjects'] else "N/A"
        print(f"**{data['from'][:55]}**")
        print(f"  `{email_addr}` ({data['count']} messages)")
        print(f"  Example: {subjects_preview}...")
        print()
        count += 1
    
    # Save full results
    output_path = os.path.expanduser("~/.openclaw/workspace/reports/email-senders.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📁 Full list saved to: reports/email-senders.json")

if __name__ == "__main__":
    main()
