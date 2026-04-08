# Prompt Templates Library

Battle-tested prompts for recurring tasks. Version controlled like code.

**Usage:**
1. Pick a prompt from the library
2. Add context for your specific task
3. Run the model
4. If it performs better, update the template → v2, v3, etc.

---

## Table of Contents

1. [Coding & Debugging](#coding--debugging)
2. [Specs & PRDs](#specs--prds)
3. [Documentation](#documentation)
4. [Research & Analysis](#research--analysis)
5. [Content Creation](#content-creation)
6. [Code Review](#code-review)
7. [Client Work & Recurring Updates](#client-work--recurring-updates)

---

## Coding & Debugging

### `debug-issue` v1
**Purpose:** Diagnose and fix bugs systematically

```
You are debugging a codebase. Follow this structured approach:

## Context
- Language/Framework: [INSERT]
- Error message: [INSERT]
- Expected behavior: [INSERT]
- Actual behavior: [INSERT]

## Steps
1. **Reproduce** - Confirm you understand the exact steps to trigger the issue
2. **Isolate** - Identify the minimal code path that causes the problem
3. **Root cause** - Explain WHY it's happening, not just WHAT
4. **Fix** - Provide the minimal change that solves it
5. **Prevent** - Suggest a test or guard to prevent regression

## Output format
- **Root cause**: [one sentence]
- **Fix location**: [file:line]
- **Code change**:
```[language]
[the fix]
```
- **Why this works**: [brief explanation]
- **Test to add**: [if applicable]
```

---

### `implement-feature` v1
**Purpose:** Build new features with clear specs

```
Implement a new feature following this structure:

## Feature Spec
- **Name**: [feature name]
- **Goal**: [what it accomplishes]
- **Acceptance criteria**:
  - [ ] [criterion 1]
  - [ ] [criterion 2]
  - [ ] [criterion 3]

## Context
- Tech stack: [INSERT]
- Related files: [INSERT]
- Constraints: [INSERT - performance, compatibility, etc.]

## Implementation steps
1. Create a brief implementation plan (2-3 sentences)
2. Write the code with clear comments explaining decisions
3. Add/update tests
4. Note any trade-offs or future improvements

## Output
Provide:
- Implementation plan
- Code changes (with file paths)
- Test coverage
- Trade-offs/notes
```

---

### `refactor-code` v1
**Purpose:** Clean up code without changing behavior

```
Refactor the following code while preserving exact behavior:

## Goals
- [ ] Improve readability
- [ ] Reduce complexity
- [ ] Follow [language] best practices
- [ ] Maintain 100% behavioral parity

## Code to refactor
```
[INSERT CODE]
```

## Constraints
- Do NOT change function signatures
- Do NOT change external behavior
- MUST pass existing tests

## Output
- **Refactored code**:
- **Changes made**: [bullet list of improvements]
- **Why each change**: [brief rationale]
```

---

## Specs & PRDs

### `create-prd` v1
**Purpose:** Write comprehensive product requirements documents

```
Create a Product Requirements Document (PRD) for:

## Product/Feature
[INSERT FEATURE NAME]

## Context
- Target users: [INSERT]
- Problem it solves: [INSERT]
- Business goal: [INSERT]

## PRD Structure

### 1. Overview
- **Summary**: [one paragraph description]
- **Success metrics**: [how we measure success]
- **Timeline**: [rough estimate]

### 2. User Stories
As a [user type], I want to [action] so that [benefit].

- [ ] Story 1
- [ ] Story 2
- [ ] Story 3

### 3. Functional Requirements
| Requirement | Priority | Notes |
|------------|----------|-------|
| [req 1] | P0/P1/P2 | [context] |

### 4. Non-Functional Requirements
- Performance: [targets]
- Security: [considerations]
- Accessibility: [standards]

### 5. Technical Considerations
- Dependencies: [external systems/libraries]
- Risks: [technical risks and mitigations]
- Alternatives considered: [what we didn't choose and why]

### 6. Open Questions
- [ ] [question 1]
- [ ] [question 2]

### 7. Milestones
- **M1**: [description] - [date]
- **M2**: [description] - [date]
```

---

### `create-spec` v1
**Purpose:** Write technical specifications for implementation

```
Create a technical specification for:

## Feature/Component
[INSERT NAME]

## Requirements
- Functional: [INSERT]
- Non-functional: [INSERT performance, security, etc.]
- Constraints: [INSERT]

## Specification Structure

### 1. System Design
- **Architecture diagram**: [describe or provide mermaid]
- **Data flow**: [how data moves through the system]
- **Key components**: [list with responsibilities]

### 2. API Design
```
[endpoint/method signatures with types]
```

### 3. Data Model
```
[schema/struct definitions]
```

### 4. Implementation Notes
- **Critical paths**: [code that must be correct]
- **Edge cases**: [unusual situations to handle]
- **Error handling**: [how failures are managed]

### 5. Testing Strategy
- **Unit tests**: [what to test in isolation]
- **Integration tests**: [what to test together]
- **Performance tests**: [benchmarks if applicable]

### 6. Security Considerations
- [security requirements and how they're met]

### 7. Migration Plan (if applicable)
- [how to roll out without breaking existing functionality]
```

---

## Documentation

### `document-codebase` v1
**Purpose:** Generate comprehensive documentation for a project

```
Create documentation for this codebase:

## Project Context
- Name: [INSERT]
- Tech stack: [INSERT]
- Primary purpose: [INSERT]
- Target audience: [who will read this docs]

## Documentation Structure

### 1. README.md (if missing or outdated)
- Project name & one-line description
- Quick start (install + run in < 5 commands)
- Prerequisites
- Basic usage examples
- Link to full docs

### 2. Architecture Overview
- High-level system design
- Key directories and their purposes
- Important files and what they do
- Data flow diagram (mermaid or description)

### 3. API Documentation
For each public API:
- Purpose
- Parameters (with types)
- Return value
- Example usage
- Edge cases/errors

### 4. Development Guide
- Local setup
- Running tests
- Common development tasks
- Debugging tips

### 5. Deployment Guide
- Environment variables
- Build process
- Deployment steps
- Rollback procedure

## Output
Generate each section with:
- Clear, concise language
- Code examples where helpful
- Links to related sections
```

---

### `document-api` v1
**Purpose:** Document API endpoints comprehensively

```
Document this API:

## API Overview
- Base URL: [INSERT]
- Authentication: [INSERT]
- Rate limits: [INSERT]

## For each endpoint:

### [METHOD] /path
**Purpose**: [one sentence]

**Authentication**: [required/optional]

**Request**:
```
{
  "field": "type - description"
}
```

**Response** (200):
```
{
  "field": "type - description"
}
```

**Errors**:
- `400`: [when this happens]
- `401`: [when this happens]
- `500`: [when this happens]

**Example**:
```
[full request/response example]
```

**Notes**: [edge cases, gotchas, performance tips]
```

---

## Research & Analysis

### `analyze-codebase` v1
**Purpose:** Deep analysis of a codebase's structure, patterns, and health

```
Analyze this codebase comprehensively:

## Codebase
[INSERT PATH or describe structure]

## Analysis Dimensions

### 1. Architecture
- **Pattern**: [MVC, microservices, monolith, etc.]
- **Modularity**: [how well-separated are concerns]
- **Dependencies**: [external libs, their purposes, any concerns]
- **Strengths**: [what's done well]
- **Weaknesses**: [technical debt, areas for improvement]

### 2. Code Quality
- **Consistency**: [naming, formatting, patterns]
- **Test coverage**: [estimated, areas missing]
- **Documentation**: [what's documented, what's not]
- **Error handling**: [robust, missing, patterns used]

### 3. Performance
- **Bottlenecks**: [obvious slow points]
- **Optimization opportunities**: [low-hanging fruit]
- **Scalability concerns**: [what breaks at scale]

### 4. Security
- **Auth/authz patterns**: [how security is handled]
- **Input validation**: [where it's done, where it's missing]
- **Sensitive data**: [how secrets/PII are handled]
- **Vulnerabilities**: [obvious issues]

### 5. Maintainability
- **Onboarding difficulty**: [how hard for new devs]
- **Change frequency**: [what changes often]
- **Refactoring candidates**: [what should be cleaned up]

## Output Format
Provide a structured report with:
- Executive summary (3-5 sentences)
- Detailed findings per dimension
- Prioritized recommendations (P0/P1/P2)
- Quick wins (improvements that take < 1 hour)
```

---

### `research-topic` v1
**Purpose:** Deep research on a technical topic

```
Conduct comprehensive research on:

## Topic
[INSERT TOPIC]

## Research Questions
1. [question 1]
2. [question 2]
3. [question 3]

## Research Structure

### 1. Summary
[2-3 paragraph overview answering the core questions]

### 2. Key Findings
- **Finding 1**: [explanation]
  - Source: [link/reference]
  - Confidence: [high/medium/low]
  
- **Finding 2**: [explanation]
  - Source: [link/reference]
  - Confidence: [high/medium/low]

### 3. Comparison (if applicable)
| Option | Pros | Cons | Best for |
|--------|------|------|----------|
| [A] | [pros] | [cons] | [use case] |

### 4. Recommendations
Based on the research, I recommend [conclusion] because [reasoning].

### 5. Open Questions
- [ ] [what's still unclear]
- [ ] [what needs further investigation]

### 6. Sources
- [list of references with links]
```

---

### `analyze-dependencies` v1
**Purpose:** Audit and analyze project dependencies

```
Analyze the dependencies for this project:

## Project
[INSERT - package.json, go.mod, requirements.txt, etc.]

## Analysis Tasks

### 1. Dependency Inventory
List all direct dependencies with:
- Name & version
- Purpose in this project
- License
- Last updated

### 2. Risk Assessment
For each dependency, note:
- **Security**: Any known vulnerabilities?
- **Maintenance**: Is it actively maintained?
- **Alternatives**: Are there better options?
- **Necessity**: Is it actually needed?

### 3. Recommendations
- **Update**: [deps that should be updated]
- **Replace**: [deps that should be swapped]
- **Remove**: [deps that can be removed]
- **Pin**: [deps that should be pinned to specific versions]

### 4. Dependency Health Score
Give the overall dependency health a score (1-10) with reasoning.

## Output
Provide a structured report with actionable recommendations.
```

---

## Content Creation

### `write-blog-post` v1
**Purpose:** Create technical blog posts

```
Write a blog post on:

## Topic
[INSERT TOPIC]

## Audience
- Technical level: [beginner/intermediate/advanced]
- Background: [what they already know]

## Requirements
- Word count: [target]
- Tone: [tutorial/explanatory/opinion/case-study]
- Include code examples: [yes/no]

## Structure

### Title
[Compelling, specific title]

### Introduction (2-3 paragraphs)
- Hook the reader
- State the problem
- Preview the solution

### Body
[Logical sections with headers]

- Use code examples
- Explain the "why" not just the "how"
- Include diagrams if helpful

### Conclusion
- Summarize key takeaways
- Suggest next steps
- Invite discussion

### Call to Action
[What should readers do next?]

## Output
Write in a clear, conversational tone. Use active voice. Avoid jargon unless necessary (then explain it).
```

---

### `write-readme` v1
**Purpose:** Create or improve README files

```
Create a README for:

## Project
[INSERT - describe project or provide codebase]

## Requirements

### Must Have
- Project name (clear, memorable)
- One-line description (what it does)
- Installation instructions (copy-pasteable)
- Basic usage example (minimal working example)
- License

### Should Have
- Badges (build status, version, license)
- Screenshots/demos (if visual)
- Contributing guidelines link
- Roadmap or changelog link

### Nice to Have
- Architecture overview
- Comparison to alternatives
- FAQ section

## README Structure

```
# Project Name
[badges]

Brief description of what this project does.

## Features
- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Prerequisites
- [requirement 1]
- [requirement 2]

### Installation
```bash
[install commands]
```

### Usage
```bash
[usage example]
```

## Documentation
[Link to full docs or expand here]

## Contributing
[How to contribute]

## License
[License name]

## Acknowledgments
[If applicable]
```

## Output
Generate the README with clear, concise language. Every command should be copy-pasteable.
```

---

### `write-changelog` v1
**Purpose:** Generate changelog entries from commits/changes

```
Create a changelog entry for:

## Version
[INSERT VERSION NUMBER]

## Changes
[INSERT - git log, PR descriptions, or list of changes]

## Changelog Format

### [version] - YYYY-MM-DD

#### Added
- [new features]

#### Changed
- [changes to existing features]

#### Deprecated
- [features being phased out]

#### Removed
- [features removed in this version]

#### Fixed
- [bug fixes]

#### Security
- [security improvements]

## Guidelines
- Write for users, not developers
- Be specific but concise
- Include breaking changes prominently
- Link to issues/PRs where helpful
- Use present tense ("Add feature" not "Added feature")

## Output
Generate a changelog entry following [Keep a Changelog](https://keepachangelog.com/) format.
```

---

## Code Review

### `review-pr` v1
**Purpose:** Comprehensive PR review

```
Review this pull request:

## PR Context
- Title: [INSERT]
- Description: [INSERT]
- Files changed: [INSERT or let me analyze]

## Review Checklist

### 1. Correctness
- [ ] Does it do what it claims?
- [ ] Are edge cases handled?
- [ ] Are errors handled properly?

### 2. Code Quality
- [ ] Is it readable?
- [ ] Is it well-structured?
- [ ] Are names clear and consistent?
- [ ] Is there unnecessary complexity?

### 3. Testing
- [ ] Are there tests?
- [ ] Do tests cover the important cases?
- [ ] Would you trust these tests to catch regressions?

### 4. Performance
- [ ] Are there obvious performance issues?
- [ ] Are expensive operations optimized?
- [ ] Is there unnecessary work being done?

### 5. Security
- [ ] Is input validated?
- [ ] Are secrets handled properly?
- [ ] Are there obvious vulnerabilities?

### 6. Documentation
- [ ] Is new code documented?
- [ ] Are public APIs documented?
- [ ] Is the README updated if needed?

## Output Format

### Summary
[1-2 sentences: should this merge?]

### Must Fix (blocking)
- [ ] **[file:line]**: [issue + how to fix]

### Should Fix (non-blocking)
- [ ] **[file:line]**: [suggestion]

### Nits (optional)
- [ ] **[file:line]**: [minor improvement]

### Questions
- [ ] [clarifying question]

### What's Good
- [positive feedback on what's done well]
```

---

### `review-security` v1
**Purpose:** Security-focused code review

```
Perform a security review of:

## Code/Project
[INSERT - code snippet, file, or describe the system]

## Security Review

### 1. Authentication & Authorization
- How is identity verified?
- How are permissions checked?
- Are there privilege escalation risks?

### 2. Input Handling
- Is all input validated?
- Is input sanitized before use?
- Are there injection vulnerabilities?

### 3. Data Protection
- How is sensitive data stored?
- How is data transmitted?
- Are secrets properly managed?

### 4. Dependencies
- Are there known vulnerabilities in deps?
- Are deps from trusted sources?
- Is dependency pinning used?

### 5. Error Handling
- Do errors leak sensitive info?
- Are errors handled gracefully?
- Is logging secure?

### 6. Common Vulnerabilities
Check for:
- [ ] SQL injection
- [ ] XSS
- [ ] CSRF
- [ ] Path traversal
- [ ] Command injection
- [ ] Insecure deserialization
- [ ] Hardcoded secrets
- [ ] Weak crypto

## Output

### Risk Level: [Critical/High/Medium/Low]

### Findings
| Severity | Issue | Location | Remediation |
|----------|-------|----------|-------------|
| [Critical/High/Medium/Low] | [description] | [file:line] | [how to fix] |

### Recommendations
[Prioritized list of security improvements]
```

---

## Client Work & Recurring Updates

### `headstart-newsletter` v1
**Purpose:** Create monthly newsletter content for Head Start program website

```
Create the monthly newsletter for Elko Head Start:

## Month/Year
[INSERT - e.g., "April 2026"]

## Content to Include
[INSERT - events, announcements, dates, etc.]

## Newsletter Structure

### File Locations
- English: `src/content/docs/en/newsletter-[month]-[year].mdx`
- Spanish: `src/content/docs/es/newsletter-[month]-[year].mdx`

### Required Sections

1. **Header/Title**
   - "Head Start News - [Month Year]" (EN)
   - "Noticias de Head Start - [Mes Año]" (ES)

2. **Upcoming Events**
   - Date, time, location
   - Brief description
   - Who should attend

3. **Important Dates**
   - School closures
   - Registration deadlines
   - Parent meetings

4. **Highlights**
   - Student achievements
   - Classroom activities
   - Community partnerships

5. **Reminders**
   - What parents need to do
   - Documents needed
   - Deadlines

6. **Contact Information**
   - Phone, email, address
   - Office hours

## Localization Guidelines
- Translate meaning, not word-for-word
- Use culturally appropriate language for Spanish version
- Keep dates in consistent format
- Ensure all names/places are accurate in both versions

## Output
Generate:
1. English newsletter (newsletter-[month]-[year].mdx)
2. Spanish newsletter (newsletter-[month]-[year].mdx)
3. Summary of key dates for calendar update
4. Social media snippet (optional)
```

---

### `headstart-calendar-update` v1
**Purpose:** Update Head Start calendar with new events

```
Update the Elko Head Start calendar with new events:

## New Events to Add
[INSERT - list of events with dates, times, descriptions]

## Events to Remove/Update
[INSERT - any changes to existing events]

## File Location
`src/content/calendar/` or appropriate calendar data file

## Calendar Entry Format
```yaml
- title: "[Event Name]"
  titleEs: "[Nombre del Evento]"
  date: YYYY-MM-DD
  time: "HH:MM AM/PM"
  location: "[Location]"
  locationEs: "[Ubicación]"
  description: "[Brief description]"
  descriptionEs: "[Breve descripción]"
  audience: "[Who should attend]"
  audienceEs: "[Quién debe asistir]"
```

## Output
1. Updated calendar data file
2. List of new events added
3. List of events removed/modified
4. iCal feed update (if applicable)
```

---

### `unfergettable-monthly-update` v1
**Purpose:** Monthly content and portfolio updates for UnFergettable Designs

```
Perform monthly updates for UnFergettable Designs website:

## Update Type
[ ] Portfolio additions
[ ] Testimonials
[ ] Services/pricing
[ ] Blog content
[ ] Team updates
[ ] Other: [specify]

## New Content to Add
[INSERT - describe what needs to be added/updated]

## Update Checklist

### Portfolio Projects
For each new project:
- Project name & client (if public)
- Services provided
- Technologies used
- Project description (2-3 sentences)
- Outcomes/results (metrics if available)
- Images/screenshots (specify what's needed)
- Testimonial (if available)

File location: `src/content/work/` or portfolio collection

### Testimonials
- Client name (or anonymous)
- Project type
- Quote
- Rating (if applicable)

File location: `src/content/testimonials/`

### Services/Pricing
- Service name
- Description
- Starting price (if public)
- Package options

File location: Check `src/pages/services` or content config

### Blog Posts
- Title
- Topic/category
- Target keywords
- Call to action

File location: `src/content/blog/`

## SEO Considerations
- Include relevant keywords naturally
- Add alt text for new images
- Update meta descriptions if pages change
- Check internal links

## Output
1. List of files created/updated
2. Summary of changes
3. Preview URLs to check
4. Any missing assets (images, client approval, etc.)
5. Deploy command or PR ready
```

---

### `client-site-checkup` v1
**Purpose:** Monthly health check for client websites

```
Perform monthly checkup for client website:

## Client
[INSERT - client name/site]

## Site URL
[INSERT - production URL]

## Checkup Tasks

### 1. Functionality
- [ ] Homepage loads correctly
- [ ] Contact form works
- [ ] All links work (no 404s)
- [ ] Images load
- [ ] Mobile responsive

### 2. Performance
- [ ] Run Lighthouse audit
- [ ] Check Core Web Vitals
- [ ] Note any slowdowns

### 3. Content Freshness
- [ ] Is content up to date?
- [ ] Any outdated information?
- [ ] Blog/news needs update?

### 4. Security
- [ ] SSL certificate valid
- [ ] Dependencies up to date
- [ ] No known vulnerabilities

### 5. SEO
- [ ] Check Google Search Console
- [ ] Any crawl errors?
- [ ] Rankings stable?

### 6. Analytics
- [ ] Traffic trends (up/down/stable)
- [ ] Any anomalies?
- [ ] Conversion rates

## Output Format

### Summary
[Overall health: Good/Needs Attention/Critical]

### Issues Found
| Priority | Issue | Recommended Action |
|----------|-------|-------------------|
| [High/Medium/Low] | [description] | [what to do] |

### Metrics
- Performance score: [X/100]
- Accessibility score: [X/100]
- SEO score: [X/100]
- Best practices: [X/100]

### Action Items
1. [ ] [immediate fix needed]
2. [ ] [schedule for next update]
3. [ ] [monitor but not urgent]

### Client Communication
[Draft brief update for client if notable issues or improvements]
```

---

## OpenClaw Skills (Automated)

These prompts have been converted to OpenClaw Skills with tool access:

| Skill | Purpose | Usage |
|------|--------|-------|
| `headstart-newsletter` | Add newsletter PDFs to site | `/headstart-newsletter April 2026` |
| `headstart-staff` | Update staff directory | `/headstart-staff add director --name "..."` |
| `ud-monthly-updates` | SEO, deps, lighthouse, content audits | `/ud-monthly-updates all full` |

Skills live in `~/.openclaw/skills/` and can:
- Read/write files directly
- Run commands (lighthouse, git, etc.)
- Send reports to Discord

**When to use Skills vs Prompts:**
- **Skills**: Recurring tasks that need file/tool access (newsletters, staff, monthly audits)
- **Prompts**: One-off tasks, sharing with others, using outside OpenClaw

---

## Usage Tips

1. **Copy the prompt** that matches your task
2. **Fill in the [INSERT]** placeholders with your context
3. **Run with your model** of choice
4. **Iterate**: if the output isn't great, refine the prompt and save as v2

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2026-04-07 | Initial prompt library |
| v1.1 | 2026-04-08 | Added OpenClaw skills section, converted to skills |

---

## Contributing

Found a better version of a prompt? 

1. Test it thoroughly
2. Update the prompt with v2, v3, etc.
3. Add a note in version history
4. Commit with message: "Improve [prompt-name] to v2"

---

*Inspired by Anthropic's internal prompt template practices. Treat prompts like code: version, test, iterate.*
