# Gmail Management Quick Start

## First-Time Setup

### 1. Export Gmail Credentials

For each Gmail account:

```bash
# Login to account
gws auth login -s gmail

# Export credentials to file
gws auth export --unmasked > ~/.config/gws/johncferguson90.json
```

Repeat for second account:
```bash
# Login to second account
gws auth login -s gmail

# Export to different file
gws auth export --unmasked > ~/.config/gws/snobord4life.json
```

### 2. Update Config File

Edit `scripts/gmail-config.json` and ensure the `credentials_file` paths are correct:

```json
{
  "accounts": {
    "johncferguson90@gmail.com": {
      "credentials_file": "~/.config/gws/johncferguson90.json"
    },
    "snobord4life@gmail.com": {
      "credentials_file": "~/.config/gws/snobord4life.json"
    }
  }
}
```

### 3. Test It

```bash
# See what would be labeled (dry run)
python3 scripts/gmail-manage.py --dry-run

# Run for real
python3 scripts/gmail-manage.py
```

### 4. View Results

```bash
# JSON output
python3 scripts/gmail-manage.py --json

# Specific account only
python3 scripts/gmail-manage.py --account johncferguson90@gmail.com
```

## Customizing Rules

Edit `scripts/gmail-config.json` to:

### Add New Labels

```json
"labels": {
  "VIP": {
    "color": "bg_red",
    "description": "High priority emails"
  }
}
```

### Add Labeling Rules

```json
"rules": {
  "VIP": {
    "domains": ["@important-client.com"],
    "senders": ["boss@company.com"],
    "keywords": ["urgent", "asap", "critical"]
  }
}
```

### Color Options

- bg_yellow, bg_green, bg_red, bg_blue
- bg_teal, bg_purple, bg_orange, bg_pink
- bg_gray, bg_cyan

## Automation

The management script runs automatically during heartbeats (see `HEARTBEAT.md`).

Manual schedule via cron:
```bash
# Daily at 9 AM
0 9 * * * python3 /path/to/scripts/gmail-manage.py
```

## Commands

```bash
# Daily management (labeling)
python3 scripts/gmail-manage.py

# Check for unread
python3 scripts/gmail-check.py --recent

# Watch for new emails (live)
python3 scripts/gmail-watch.py

# Setup helper
python3 scripts/gmail-setup-labels.py
```
