# UnFergettable Designs Monthly Updates

Perform monthly maintenance and updates across UnFergettable Designs client websites.

## Usage

```
/ud-monthly-updates [site] [action]
```

## Sites

| Short Name | Full Name | Repo Path |
|------------|-----------|-----------|
| `headstart` | Elko Head Start | `~/Github/headstart` |
| `ud` | UnFergettable Designs (agency site) | `~/Github/unfergettable-designs` |
| `carrie-on` | Carrie On Pens & Needles | `~/Github/carrie-on-pens-and-needles` |
| `spring-creek` | Spring Creek Baptist | `~/Github/spring-creek-baptist` |
| `valkyrie` | Valkyrie Fitness | `~/Github/valkyrie-fitness` |
| `jferguson` | jferguson.info (personal) | `~/Github/jferguson.info` |
| `all` | Run on all sites | - |

## Actions

| Action | Description |
|--------|-------------|
| `seo` | SEO health check |
| `deps` | Dependency audit & updates |
| `lighthouse` | Run Lighthouse reports |
| `content` | Content freshness review |
| `full` | Complete monthly checkup |

## SEO Health Check (`seo`)

### Checks
1. **Meta tags** - Title, description, OG tags present
2. **Headings hierarchy** - H1-H6 properly nested
3. **Image alt text** - All images have alt attributes
4. **Internal links** - No broken links
5. **Sitemap** - Valid sitemap.xml exists
6. **robots.txt** - Properly configured
7. **Canonical URLs** - Set correctly

### Output
```
SEO Report: [site]
═══════════════════════════════════════
✓ Meta tags: All pages have title & description
✓ Headings: Proper hierarchy
⚠ Images: 3 missing alt text
  - /images/team/photo1.jpg
  - /images/gallery/img2.png
✓ Links: 47 internal, 0 broken
✓ Sitemap: Found at /sitemap-index.xml
✓ robots.txt: Configured

Issues to fix:
1. Add alt text to 3 images
```

## Dependency Audit (`deps`)

### Checks
1. **Outdated packages** - List major/minor updates available
2. **Security vulnerabilities** - Run `bun audit` or `npm audit`
3. **Unused dependencies** - Identify candidates for removal
4. **Peer dependency warnings** - Check for conflicts

### Output
```
Dependency Report: [site]
═══════════════════════════════════════
Total dependencies: 87

Security: ✓ No vulnerabilities

Outdated (major):
- astro: 4.16 → 5.0 (breaking changes, check migration guide)
- tailwindcss: 3.4 → 4.0 (new syntax)

Outdated (minor):
- @astrojs/sitemap: 3.1 → 3.2
- prettier: 3.2 → 3.3

Recommendations:
1. Review Astro 5 migration: https://docs.astro.build/en/guides/upgrade-to/v5/
2. Update minor versions: bun update
```

## Lighthouse Reports (`lighthouse`)

### Categories
- Performance
- Accessibility
- Best Practices
- SEO

### Output
```
Lighthouse Report: [site]
═══════════════════════════════════════
                    Desktop    Mobile
Performance          95         78
Accessibility        100        100
Best Practices       100        100
SEO                  92         90

Mobile Performance Issues:
- LCP: 3.2s (target: <2.5s)
- CLS: 0.15 (target: <0.1)
  - Caused by: hero image loading

Recommendations:
1. Add width/height to hero image
2. Preload critical fonts
```

## Content Freshness (`content`)

### Checks
1. **Blog/news** - Last post date, stale content
2. **Team/staff** - Outdated info, missing photos
3. **Services/pricing** - Accurate and current
4. **Contact info** - Valid phone, email, address
5. **External links** - All still working
6. **Copyright year** - Updated in footer

### Output
```
Content Report: [site]
═══════════════════════════════════════
Blog: Last post 45 days ago (Feb 22, 2026)
⚠ Consider adding new content

Team: 2 members with placeholder images
- Maria Lopez (added Jan 2026)
- New hire pending

Services: ✓ All current
Contact: ✓ Verified
Copyright: ✓ Shows 2026

Action Items:
1. Add Q1 blog post
2. Get photos for 2 team members
```

## Full Checkup (`full`)

Runs all checks in sequence:
1. SEO
2. Dependencies
3. Lighthouse
4. Content

Generates summary report and prioritized action items.

## Example Session

```
User: /ud-monthly-updates all full

Assistant:
Running full monthly checkup on 6 sites...

━━━ headstart ━━━
SEO: 3 issues
Deps: 2 outdated (minor)
Lighthouse: 89/92/100/94
Content: 1 stale newsletter

━━━ ud ━━━
SEO: ✓ No issues
Deps: 1 vulnerability (CVE-2026-XXXX)
Lighthouse: 95/100/100/100
Content: ✓ Current

[... continues for all sites ...]

═══════════════════════════════════════
PRIORITY ACTION ITEMS
═══════════════════════════════════════
🔴 CRITICAL (fix today)
- ud: Update lodash (CVE-2026-XXXX)

🟡 IMPORTANT (fix this week)
- headstart: Add April newsletter
- carrie-on: 2 missing alt texts

🟢 ROUTINE (fix this month)
- Update Astro on 2 sites
- Add new blog post to ud

Generate detailed reports? [yes/no]
```

## Configuration

Per-site config stored in `~/.openclaw/skills/ud-monthly-updates/config.json`:

```json
{
  "sites": {
    "headstart": {
      "repo": "~/Github/headstart",
      "productionUrl": "https://elkoheadstart.com",
      "alerts": ["v1truv1us"],
      "schedule": "1st of month"
    },
    "ud": {
      "repo": "~/Github/unfergettable-designs",
      "productionUrl": "https://unfergettabledesigns.com",
      "alerts": ["v1truv1us"],
      "schedule": "1st of month"
    }
  }
}
```

## Integration

Can be triggered via:
- Manual command: `/ud-monthly-updates`
- Heartbeat: Add to HEARTBEAT.md
- Cron: Schedule via OpenClaw cron

## Notifications

Reports can be sent to:
- Discord: #unfergettable-designs channel
- Email: Summary to configured address
- File: Save to `~/Github/reports/`
