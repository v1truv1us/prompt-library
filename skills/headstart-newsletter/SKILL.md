# Headstart Newsletter Skill

Add monthly newsletters to the Elko Head Start website.

## Usage

```
/headstart-newsletter [month] [year]
```

Example: `/headstart-newsletter April 2026`

## What This Skill Does

1. **Validates the PDF exists** in `~/Github/headstart/public/pdfs/`
2. **Updates the calendar collection** at `src/content/calendar/_index.json`
3. **Adds newsletter entry** to the newsletters array
4. **Commits the change** with descriptive message
5. **Optionally opens a PR** or pushes to main

## Prerequisites

- Newsletter PDF must already be placed in `public/pdfs/`
- Naming convention: `{Month} Newsletter {Year}.pdf` (e.g., `April Newsletter 2026.pdf`)
- Git repo must be clean or you must approve dirty state

## Arguments

- `month` (required): Month name (e.g., "April", "November")
- `year` (required): 4-digit year (e.g., "2026")

## Workflow

1. Check if PDF exists at expected path
2. Read current calendar JSON
3. Add new newsletter entry to array (prepend - newest first)
4. Write updated JSON
5. Commit with message: "Add {Month} {Year} newsletter"
6. Ask user: push to main or create PR?

## File Locations

- **PDF storage**: `~/Github/headstart/public/pdfs/{Month} Newsletter {Year}.pdf`
- **Calendar data**: `~/Github/headstart/src/content/calendar/_index.json`

## JSON Entry Format

```json
{
  "url": "/pdfs/{Month} Newsletter {Year}.pdf",
  "name": "{Month} {Year} Newsletter"
}
```

## Error Handling

- **PDF not found**: Tell user exact path to place the file
- **Duplicate entry**: Warn if newsletter already exists, ask to proceed anyway
- **Invalid JSON**: Abort and show parse error

## Example Session

```
User: /headstart-newsletter April 2026

Assistant: 
✓ Found PDF: public/pdfs/April Newsletter 2026.pdf
✓ Current newsletters: 9 entries (last: March 2026)
✓ Added April 2026 to top of list
✓ Committed: "Add April 2026 newsletter"

Push to main or create PR? [main/PR/cancel]
```
