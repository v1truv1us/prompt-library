#!/bin/bash

# Test script for prompt validation
# Shows how each prompt would be executed via API

echo "=== PROMPT VALIDATION TEST ==="
echo ""

# Sample inputs
TOPIC="AI Automation Consulting"
DEMOGRAPHIC="Small business owners"
SKILLS="Python, ChatGPT, Data Analysis"
HOURS="10"
BUDGET="$500"
AUDIENCE="500"

echo "Sample inputs:"
echo "  Topic: $TOPIC"
echo "  Demographic: $DEMOGRAPHIC"
echo "  Skills: $SKILLS"
echo "  Hours: $HOURS"
echo "  Budget: $BUDGET"
echo "  Audience: $AUDIENCE"
echo ""

# Prompt 1: Offer Creation Engine
echo "=== Prompt 1: Offer Creation Engine ==="
PROMPT1="Build a 3-tier offer ladder for my expertise using proven revenue models. Include starter offer (\$27-\$297), core offer (\$497-\$1,997), and premium offer (\$5K-\$25K+) with specific deliverables, pricing justifications, and upsell sequences. Provide a complete value ladder diagram and launch timeline. Consider my niche of $TOPIC and target audience of $DEMOGRAPHIC."

echo "$PROMPT1"
echo ""

# Prompt 2: Income Opportunity Scanner
echo "=== Prompt 2: Income Opportunity Scanner ==="
PROMPT2="Scan current market trends to find 3 profitable side income opportunities aligned with my skills and interests. Include market size (online education \$450B by 2026), growth rate, and demand signals. Provide entry barriers, startup costs, and monetization timelines with specific action steps for each opportunity. Consider my current skills of $SKILLS and available hours of $HOURS weekly."

echo "$PROMPT2"
echo ""

# Prompt 3: Skill Monetization Mapper
echo "=== Prompt 3: Skill Monetization Mapper ==="
PROMPT3="Map my skills to revenue using the implementation expert framework. Identify which skills can package into digital products, which into services, and which into hybrid offers. Provide the three-pillar monetization structure (content authority, scalable products, optimized distribution) with specific packaging templates for each revenue stream. Consider my top skills of $SKILLS and audience size of $AUDIENCE."

echo "$PROMPT3"
echo ""

# Prompt 4: Pricing Strategy Framework
echo "=== Prompt 4: Pricing Strategy Framework ==="
PROMPT4="Design a multi-tier pricing structure for my product/service using value-based pricing models. Include starter, core, and premium tiers with specific features, payment terms, and positioning scripts. Provide competitor pricing analysis, anchor pricing tactics, and psychological pricing triggers that maximize conversion. Consider my market of $TOPIC and cost structure of $BUDGET."

echo "$PROMPT4"
echo ""

# Prompt 5: Client Acquisition Protocol
echo "=== Prompt 5: Client Acquisition Protocol ==="
PROMPT5="Create a multi-channel client acquisition system using cold outreach, LinkedIn, and referral prospecting. Include timing rules (call 5-min before hour), permission-based openers, objection handlers, and 3-5 touchpoint follow-up sequences. Provide email templates, call scripts, and a weekly outreach calendar with specific metrics to track. Consider my target clients of $DEMOGRAPHIC and industry of $TOPIC."

echo "$PROMPT5"
echo ""

echo "=== TEST COMPLETE ==="
echo ""
echo "Next steps:"
echo "1. Review prompt outputs for clarity"
echo "2. Test variable replacement"
echo "3. Validate format specifications"