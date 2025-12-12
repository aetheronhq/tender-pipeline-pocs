"""
Shared prompts for the Pain Points POC.

Goal: keep core wording consistent across options; only change workflow,
not the prompt content, when comparing approaches.
"""

import json
from typing import List


def build_option1_prompt(file_labels: str) -> str:
    return f"""You are a strategic tender analyst identifying buyer pain points.

You are analyzing these tender documents:
{file_labels}

Extract UP TO 5 strategic buyer pain points. Only return pain points that are truly strategic.

For each pain point, provide:
1. title (max 50 chars)
2. description (max 250 chars)
3. strategic_importance_score (1-5, where 5 is critical)
4. source_references (page numbers in format ["DocumentName.pdf page X-Y"])

SKIP:
- Administrative requirements ("Submit by Friday")
- Obvious compliance items ("Must have ABN")
- Formatting instructions ("PDF format")

Score 5: Critical transformational challenge
Score 4: Important strategic need
Score 3 or below: DO NOT INCLUDE

Only return pain points with strategic_importance_score >= 4.
Focus on QUALITY over quantity: 2-5 strategic pain points is acceptable.

IMPORTANT: Ensure pain points are DISTINCT and cover different strategic challenges.
Each pain point should address a separate buyer need.

ONLY merge if pain points are saying the SAME thing with different wording.
KEEP SEPARATE if pain points address different strategic challenges, even if related.

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


def build_option3_prompt(file_labels: str) -> str:
    return f"""You are a strategic tender analyst identifying buyer pain points.

You are analyzing these tender documents:
{file_labels}

Extract UP TO 10 strategic buyer pain points.

For EACH pain point you MUST provide:
1. title (max 50 chars)
2. description (max 250 chars)
3. strategic_importance_score (1-5, where 5 is critical to buyer's decision)
4. source_references (specific page numbers in format ["DocumentName.pdf page X-Y"])

VALIDATION REQUIREMENTS:
- Only return pain points scored 4-5 (truly strategic)
- Do NOT merge semantically similar pain points before returning (let dedup handle it)
- Each pain point should address a DISTINCT strategic challenge
- Focus on QUALITY over quantity: extracting strategic pain points is more important than hitting 10

IMPORTANT: Ensure pain points are DISTINCT and cover different strategic challenges.
Each pain point should address a separate buyer need.

ONLY merge if pain points are saying the SAME thing with different wording.
KEEP SEPARATE if pain points address different strategic challenges, even if related.

Output JSON:
{{
  "pain_points": [...],
  "extraction_confidence": "high|medium|low"
}}"""


# Option 2 (multi-pass) prompts - 3 steps (removed broken Step 1)

def build_step1_extract_prompt(file_labels: str) -> str:
    """Step 1: Extract 8-10 initial pain points (broad net)"""
    return f"""You are a strategic tender analyst identifying buyer pain points.

You are analyzing these tender documents:
{file_labels}

Extract 8-10 potential buyer pain points. We'll refine in the next steps.

For each pain point, provide:
1. title (max 50 chars)
2. description (max 250 chars)
3. source_references (page numbers in format ["DocumentName.pdf page X-Y"])

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

Return final 3-5 pain points with:
- title (max 50 chars)
- description (max 250 chars)
- strategic_importance_score
- source_references

Output JSON with 'pain_points' list."""


