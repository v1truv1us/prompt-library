#!/usr/bin/env python3
"""
Quick setup script to create Gmail labels and configure accounts.
"""
import json
import subprocess
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "gmail-config.json"

def main():
    print("🚀 Gmail Email Management Setup\n")
    
    # Check if config exists
    if not CONFIG_FILE.exists():
        print("❌ Config file not found!")
        print(f"Expected: {CONFIG_FILE}")
        return
    
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    
    print("📧 Accounts configured:")
    for email, settings in config['accounts'].items():
        print(f"  • {email}")
    
    print(f"\n🏷️  Labels to create ({len(config['labels'])}):")
    for label, settings in config['labels'].items():
        print(f"  • {label} ({settings.get('color', 'default')})")
    
    print(f"\n📋 Rules configured ({len(config['rules'])}):")
    for label, rule in config['rules'].items():
        print(f"  • {label}: {len(rule.get('domains', []))} domains, {len(rule.get('keywords', []))} keywords")
    
    print("\n" + "="*60)
    print("Setup Checklist:")
    print("="*60)
    
    print("\n1️⃣  Export credentials from gws:")
    print("   For each account:")
    print("   ```")
    print("   gws auth login -s gmail")
    print("   gws auth export --unmasked > ~/.config/gws/ACCOUNT.json")
    print("   ```")
    
    print("\n2️⃣  Create labels:")
    print("   python3 scripts/gmail-manage.py --setup-labels")
    
    print("\n3️⃣  Test dry run:")
    print("   python3 scripts/gmail-manage.py --dry-run")
    
    print("\n4️⃣  Run for real:")
    print("   python3 scripts/gmail-manage.py")
    
    print("\n5️⃣  Schedule daily (automated via heartbeat)")
    
    print("\n" + "="*60)
    print("Ready? Start with step 1! 🎯\n")

if __name__ == '__main__':
    main()
