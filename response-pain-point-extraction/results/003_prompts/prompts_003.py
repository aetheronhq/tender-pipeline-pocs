"""
Shared prompts for the Pain Points POC - Version 3.

Changes from V2:
- Improved scoring rubric (no industry-specific examples)
- Source reference accuracy (document names in prompt)
- Description richness (WHAT/WHY/CONTEXT, 300 chars)
- Output validation checklist
- Duplicate detection guidance
- Verification step for Option 3

V2 prompts preserved in: prompts_002.py
"""

import json
from typing import List


def build_option1_prompt(file_labels: str, file_names: List[str]) -> str:
    """
    Option 1: Simple single-pass extraction.
    
    Args:
        file_labels: Formatted list of files for display
        file_names: Actual filenames for citation accuracy
    """
    file_names_list = "\n".join([f"  - {name}" for name in file_names])
    
    return f"""You are a strategic tender analyst identifying buyer pain points.

You are analyzing these tender documents:
{file_labels}

DOCUMENT NAMES FOR CITATIONS:
{file_names_list}

Extract UP TO 5 strategic buyer pain points. Only return pain points that are truly strategic.

For each pain point, provide:
1. title (max 50 chars)
2. description (max 300 chars - include WHAT the challenge is, WHY it matters, and CONTEXT/scale if mentioned)
3. strategic_importance_score (1-5, where 5 is critical)
4. source_references (use EXACT document names from list above, format: ["DocumentName.pdf page X-Y"])

SKIP:
- Administrative requirements ("Submit by Friday")
- Obvious compliance items ("Must have ABN")
- Formatting instructions ("PDF format")

SCORING GUIDE:

Score 5 - Critical transformational challenge:
  - Non-negotiable requirements
  - Significant scale/impact
  - High-stakes risk

Score 4 - Important strategic need:
  - Important but solvable
  - Risk mitigation
  - Strategic but not urgent

Score 3 or Below - DO NOT INCLUDE:
  - Nice-to-have preferences
  - Administrative tasks
  - Deadlines, not pain points

Only return pain points with strategic_importance_score >= 4.
Focus on QUALITY over quantity: 2-5 strategic pain points is acceptable.

IMPORTANT: Ensure pain points are DISTINCT and cover different strategic challenges.
Each pain point should address a separate buyer need.

DUPLICATE DETECTION:
Before returning, check for duplicates:
- If two pain points are about the SAME challenge with different wording → merge them
- If two pain points are RELATED but address different aspects → keep both

Examples:
- "Data security risk" + "Privacy compliance requirement" → KEEP BOTH (different aspects)
- "Manual workflows slow" + "Low productivity from manual tasks" → MERGE (same thing)

OUTPUT VALIDATION - Before returning, verify:
✓ Each pain point addresses a DIFFERENT strategic challenge
✓ Each pain point cites SPECIFIC page numbers using EXACT document names
✓ Descriptions are 200-300 chars with WHAT/WHY/CONTEXT
✓ All pain points scored 4-5 (nothing lower)
✓ Pain points are ACTIONABLE for a bid writer (not generic observations)

Output JSON:
{{
  "pain_points": [
    {{
      "title": "...",
      "description": "...",
      "strategic_importance_score": 4 or 5,
      "source_references": ["DocumentName.pdf page X-Y"]
    }}
  ]
}}"""


def build_option3_prompt(file_labels: str, file_names: List[str]) -> str:
    """
    Option 3: Structured extraction with validation and verification.
    
    Args:
        file_labels: Formatted list of files for display
        file_names: Actual filenames for citation accuracy
    """
    file_names_list = "\n".join([f"  - {name}" for name in file_names])
    
    return f"""You are a strategic tender analyst identifying buyer pain points.

You are analyzing these tender documents:
{file_labels}

DOCUMENT NAMES FOR CITATIONS:
{file_names_list}

Extract UP TO 10 strategic buyer pain points.

For EACH pain point you MUST provide:
1. title (max 50 chars)
2. description (max 300 chars - include WHAT the challenge is, WHY it matters, and CONTEXT/scale if mentioned)
3. strategic_importance_score (1-5, where 5 is critical to buyer's decision)
4. source_references (use EXACT document names from list above, format: ["DocumentName.pdf page X-Y"])

VALIDATION REQUIREMENTS:
- Only return pain points scored 4-5 (truly strategic)
- Do NOT merge semantically similar pain points before returning (let dedup handle it)
- Each pain point should address a DISTINCT strategic challenge
- Focus on QUALITY over quantity: extracting strategic pain points is more important than hitting 10

SCORING GUIDE:

Score 5 - Critical transformational challenge:
  - Non-negotiable requirements
  - Significant scale/impact
  - High-stakes risk

Score 4 - Important strategic need:
  - Important but solvable
  - Risk mitigation
  - Strategic but not urgent

Score 3 or Below - DO NOT INCLUDE:
  - Nice-to-have preferences
  - Administrative tasks
  - Deadlines, not pain points

IMPORTANT: Ensure pain points are DISTINCT and cover different strategic challenges.
Each pain point should address a separate buyer need.

DUPLICATE DETECTION:
Before returning, check for duplicates:
- If two pain points are about the SAME challenge with different wording → merge them
- If two pain points are RELATED but address different aspects → keep both

Examples:
- "Data security risk" + "Privacy compliance requirement" → KEEP BOTH (different aspects)
- "Manual workflows slow" + "Low productivity from manual tasks" → MERGE (same thing)

OUTPUT VALIDATION - Before returning, verify:
✓ Each pain point addresses a DIFFERENT strategic challenge
✓ Each pain point cites SPECIFIC page numbers using EXACT document names
✓ Descriptions are 200-300 chars with WHAT/WHY/CONTEXT
✓ All pain points scored 4-5 (nothing lower)
✓ Pain points are ACTIONABLE for a bid writer (not generic observations)

Output JSON:
{{
  "pain_points": [...],
  "extraction_confidence": "high|medium|low"
}}"""


# Option 2 (multi-pass) prompts - 3 steps

def build_step1_extract_prompt(file_labels: str, file_names: List[str]) -> str:
    """Step 1: Extract 8-10 initial pain points (broad net)"""
    file_names_list = "\n".join([f"  - {name}" for name in file_names])
    
    return f"""You are a strategic tender analyst identifying buyer pain points.

You are analyzing these tender documents:
{file_labels}

DOCUMENT NAMES FOR CITATIONS:
{file_names_list}

Extract UP TO 10 potential buyer pain points. We'll refine in the next steps.

For each pain point, provide:
1. title (max 50 chars)
2. description (max 300 chars - include WHAT the challenge is, WHY it matters, CONTEXT if mentioned)
3. source_references (use EXACT document names from list above, format: ["DocumentName.pdf page X-Y"])

IMPORTANT: Ensure pain points are DISTINCT and cover different strategic challenges.
Each pain point should address a separate buyer need.

Return JSON with 'pain_points' list."""


def build_step2_filter_prompt(initial_points: List[dict]) -> str:
    """Step 2: Filter and score"""
    return f"""Review these extracted pain points:
{json.dumps(initial_points, indent=2)}

Remove:
- Generic/obvious items
- Administrative requirements
- Low strategic value items

Score remaining items 1-5 for strategic importance.

SCORING GUIDE:

Score 5 - Critical transformational challenge:
  - Non-negotiable requirements
  - Significant scale/impact
  - High-stakes risk

Score 4 - Important strategic need:
  - Important but solvable
  - Risk mitigation
  - Strategic but not urgent

Score 3 or Below - Remove:
  - Nice-to-have preferences
  - Administrative tasks
  - Deadlines, not pain points

Keep only items scored 4-5.

Return JSON with 'pain_points' list."""


def build_step3_refine_prompt(filtered_points: List[dict]) -> str:
    """Step 3: Refine and merge"""
    return f"""Consolidate these strategic pain points:
{json.dumps(filtered_points, indent=2)}

ONLY merge if pain points are saying the SAME thing with different wording.
KEEP SEPARATE if pain points address different strategic challenges, even if related.

Examples:
- "Low productivity" + "Manual workflows" → MERGE (same challenge)
- "Security compliance" + "Explainability requirements" → KEEP SEPARATE (different compliance aspects)
- "Budget uncertainty" + "Strategic planning gap" → KEEP SEPARATE (different concerns)

DUPLICATE DETECTION:
- If two pain points are about the SAME challenge with different wording → merge them
- If two pain points are RELATED but address different aspects → keep both

OUTPUT VALIDATION - Before returning, verify:
✓ Each pain point addresses a DIFFERENT strategic challenge
✓ Descriptions are 200-300 chars with WHAT/WHY/CONTEXT
✓ All pain points scored 4-5
✓ Pain points are ACTIONABLE for a bid writer

Return final 3-5 pain points with:
- title (max 50 chars)
- description (max 300 chars)
- strategic_importance_score
- source_references

Output JSON with 'pain_points' list."""


def build_verification_prompt(pain_points: List[dict]) -> str:
    """Verification step for Option 3: Final quality check before clustering"""
    return f"""Review these pain points for final verification:
{json.dumps(pain_points, indent=2)}

For EACH pain point, verify:
1. Is it truly STRATEGIC (not administrative/generic)?
2. Does it cite SPECIFIC evidence from the tender?
3. Is it DISTINCT from the others (different buyer need)?
4. Is the description informative (includes WHAT/WHY/CONTEXT)?

Remove any that fail verification.

Keep only pain points that pass all checks.

Return JSON with verified 'pain_points' list."""



