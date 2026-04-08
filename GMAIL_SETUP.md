# Gmail Setup Guide (Google Workspace CLI)

Using the official Google Workspace CLI (`gws`) instead of third-party services.

## Step 1: Install gws

```bash
# macOS (recommended)
brew install googleworkspace-cli

# Or via npm
npm install -g @googleworkspace/cli

# Or download binary from GitHub
# https://github.com/googleworkspace/cli/releases
```

## Step 2: Authenticate

```bash
# One-time setup (creates GCP project, enables APIs)
gws auth setup

# Login with Gmail scopes only (avoids testing mode scope limits)
gws auth login -s gmail

# Or login with multiple services
gws auth login -s gmail,drive,calendar
```

### If Testing Mode Limits Hit

If you get "scope limit" errors with `@gmail.com` accounts:

1. Go to [OAuth Consent Screen](https://console.cloud.google.com/apis/credentials/consent)
2. Add yourself as a **Test User**
3. Use selective scopes: `gws auth login -s gmail`

## Step 3: Test It Works

```bash
# Check your profile
gws gmail users getProfile --params '{"userId": "me"}'

# Triage unread emails (helper command)
gws gmail +triage

# List recent messages
gws gmail users messages list --params '{"userId": "me", "maxResults": 10}'
```

## Step 4: Multiple Accounts

To switch between Gmail accounts:

```bash
# Login to different account
gws auth login -s gmail

# Export credentials for automation
gws auth export --unmasked > ~/.config/gws/account1.json
```

Then in scripts, use:
```bash
export GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE=~/.config/gws/account1.json
```

## Gmail Addresses Configured

- johncferguson90@gmail.com
- snobord4life@gmail.com

## Useful Commands

```bash
# Show unread inbox summary (sender, subject, date)
gws gmail +triage

# Watch for new emails (stream as NDJSON)
gws gmail +watch

# Send email
gws gmail +send --to recipient@example.com --subject "Hello" --body "Hi there"

# Reply to message
gws gmail +reply --message-id MSG_ID --body "Thanks!"

# Get full message
gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'
```

## Automatic Monitoring

The Gmail check is integrated into heartbeat monitoring. It will check for unread messages periodically.

Manual check:
```bash
python3 scripts/gmail-check.py --recent
```

JSON output:
```bash
python3 scripts/gmail-check.py --json
```

## Resources

- [GitHub Repo](https://github.com/googleworkspace/cli)
- [Skills Index](https://github.com/googleworkspace/cli/blob/main/docs/skills.md)
- [NPM Package](https://www.npmjs.com/package/@googleworkspace/cli)
