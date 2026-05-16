# HEARTBEAT.md

## Daily Tasks

### Gmail Email Management
- Run: `python3 scripts/gmail-manage.py`
- Purpose: Automatically label and sort emails based on rules
- Report: Summary of labeled messages to #personal
- Accounts: johncferguson90@gmail.com, snobord4life@gmail.com
- Config: `scripts/gmail-config.json`

### Gmail Account Check
- Run: `python3 scripts/gmail-check.py --recent`
- Report: Post results to #unfergettable-designs (client-related) or #personal (personal)
- Look for: Unread messages requiring attention
- Accounts: johncferguson90@gmail.com, snobord4life@gmail.com

### ProtonMail Client Email Check
- Run: `python3 scripts/protonmail-review.py --recent`
- Report: Post results to #unfergettable-designs
- Look for: Client emails requiring attention

### ProtonMail Sender Discovery (Weekly)
- Run: `python3 scripts/protonmail-discover.py`
- Check: Look for new frequent senders that might be clients
- Update: Add new clients to `scripts/protonmail-config.json`

### Cost Tracker (Weekly)
- Run: `python3 scripts/cost-tracker.py --days 7`
- Purpose: TailClaude-style cost visibility for all coding harnesses
- Tracks: OpenClaw sessions, Claude Code, Codex, OpenCode
- Shows: Per-message cost, 7-day trends, by-source breakdown
- Report: Post summary to #oss

## Setup
- Gmail: See GMAIL_SETUP.md for OAuth setup (uses gws CLI)
- ProtonMail: Bridge must be running on 127.0.0.1:1143

## Notes
- Gmail uses Google Workspace CLI (gws) with OAuth credentials
- ProtonMail Bridge must be running for scripts to work
- Email management rules are in `scripts/gmail-config.json`
