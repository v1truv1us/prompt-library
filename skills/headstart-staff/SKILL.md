# Headstart Staff Skill

Update staff information for the Elko Head Start website.

## Usage

```
/headstart-staff [action] [arguments]
```

Actions:
- `add` - Add a new staff member
- `update` - Update existing staff member
- `remove` - Remove a staff member
- `list` - List all staff in a department

## Arguments

### add
```
/headstart-staff add [department] --name "Full Name" --title-en "English Title" --title-es "Spanish Title" --image "url-or-null"
```

### update
```
/headstart-staff update [department] --name "Full Name" --field [field] --value [new value]
```

### remove
```
/headstart-staff remove [department] --name "Full Name"
```

### list
```
/headstart-staff list [department]
```

## Departments

| Key | Display Name |
|-----|--------------|
| `director` | Executive Director |
| `familyServices` | Family Services |
| `healthAndNutrition` | Health and Nutrition |
| `earlyHeadStartTeachers` | Early Head Start Teachers |
| `headStartTeachers` | Head Start Teachers |
| `administration` | Administration |

## File Locations

- **Main team file**: `~/Github/headstart/src/content/data/team-members.json`
- **Teachers file**: `~/Github/headstart/src/content/data/head-start-teachers.json`

## Staff Entry Format

```json
{
  "name": "Full Name",
  "title": {
    "en": "English Title",
    "es": "Título en Español"
  },
  "cloudinaryImageUrl": "https://res.cloudinary.com/..." | null
}
```

## Workflow

### Add Staff
1. Validate department exists
2. Check for duplicate names (warn, don't block)
3. Add entry to appropriate array
4. Update both JSON files if needed
5. Commit: "Add [Name] to [Department]"
6. Ask to push/create PR

### Update Staff
1. Find staff member by name (fuzzy match if needed)
2. Update specified field
3. If updating image, validate URL format
4. Commit: "Update [Name]: [field] changed"

### Remove Staff
1. Confirm before deletion
2. Remove from array
3. Commit: "Remove [Name] from [Department]"

## Image Handling

- Images are stored in Cloudinary
- URL format: `https://res.cloudinary.com/unfergettabledesigns/image/upload/v[TIMESTAMP]/UnFergettableDesigns/Headstart-Elko/[Name]_[Number]_[ID].png`
- If `null`, placeholder will be shown on website
- To add new image: Upload to Cloudinary first, then provide URL

## Example Sessions

### Add new staff
```
User: /headstart-staff add familyServices --name "Maria Lopez" --title-en "Family Advocate" --title-es "Defensora Familiar" --image null

Assistant:
✓ Added Maria Lopez to Family Services
✓ Title: Family Advocate / Defensora Familiar
✓ Image: None (placeholder will show)

Commit: "Add Maria Lopez to Family Services"
Push to main or create PR?
```

### Update staff title
```
User: /headstart-staff update familyServices --name "Maria Lopez" --field title-en --value "Senior Family Advocate"

Assistant:
✓ Found Maria Lopez in Family Services
✓ Updated title-en: "Family Advocate" → "Senior Family Advocate"

Commit: "Update Maria Lopez: title changed"
```

### List department
```
User: /headstart-staff list familyServices

Assistant:
Family Services (4 members):
1. Anastacia Valdespino - Enrollment and Family Services Manager
2. Teresa Carlos - Family Advocate - Head Start Main
3. Yomaira Villegas - Family Advocate - Early Head Start
4. Yesenia Espitia Perez - Family Advocate - Head Start Silver Street
```

## Validation

- Name is required
- At least one title (en or es) is required
- Department must be valid
- Warn if cloudinaryImageUrl is null (no photo)
