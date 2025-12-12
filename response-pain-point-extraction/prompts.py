"""
Shared prompts for the Pain Points POC - Version 5.

Changes from V4:
- Threshold: 0.85 → 0.9 (proven optimal from V2)
- Reframed pain points: Emphasize "problems the company is trying to solve"
- WHY framing: Why it's important to the company and tender
- CONTEXT: Include specific examples from the documents

V4 prompts preserved in: prompts_004.py
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

PAIN POINTS are the PROBLEMS the company is trying to solve in this tender.

You are analyzing these tender documents:
{file_labels}

DOCUMENT NAMES FOR CITATIONS:
{file_names_list}

Extract UP TO 5 strategic buyer pain points - the problems they need to solve.

For each pain point, provide:
1. title (max 50 chars) - The problem they're trying to solve
2. description (max 300 chars) - Include:
   - WHAT is the problem they're trying to solve
   - WHY it's important to the company and this tender
   - CONTEXT with specific examples from the documents (e.g., "570 lawyers", "IRAP PROTECTED")
3. strategic_importance_score (1-5, where 5 is critical)
4. source_references (use EXACT document names: ["DocumentName.pdf"])

SKIP - These are NOT pain points:
- Administrative requirements ("Submit by Friday")
- Obvious compliance items ("Must have ABN")
- Formatting instructions ("PDF format")

SCORING GUIDE:

Score 5 - Critical problem to solve:
  - Non-negotiable requirements
  - Significant scale/impact on their operations
  - High-stakes risk if not addressed

Score 4 - Important problem to solve:
  - Important but solvable challenge
  - Risk they want to mitigate
  - Strategic need for their organization

Score 3 or Below - DO NOT INCLUDE:
  - Nice-to-have preferences
  - Administrative tasks
  - Not actual problems to solve

Only return pain points with strategic_importance_score >= 4.
Focus on QUALITY: Identify the real problems they need to solve, not just requirements.

IMPORTANT: Ensure pain points are DISTINCT problems covering different strategic challenges.
Each pain point should be a separate problem the buyer needs to solve.

Before returning, verify:
✓ Each pain point is a REAL PROBLEM the company needs to solve
✓ Descriptions explain WHY it's important to this company and tender
✓ CONTEXT includes specific examples from documents
✓ Pain points are DISTINCT (different problems, not aspects of same problem)
✓ All scored 4-5 (truly strategic problems)

Output JSON:
{{
  "pain_points": [
    {{
      "title": "...",
      "description": "...",
      "strategic_importance_score": 4 or 5,
      "source_references": ["DocumentName.pdf"]
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

PAIN POINTS are the PROBLEMS the company is trying to solve in this tender.

You are analyzing these tender documents:
{file_labels}

DOCUMENT NAMES FOR CITATIONS:
{file_names_list}

Extract UP TO 10 strategic buyer pain points - the problems they need to solve.

For EACH pain point you MUST provide:
1. title (max 50 chars) - The problem they're trying to solve
2. description (max 300 chars) - Include:
   - WHAT is the problem they're trying to solve
   - WHY it's important to the company and this tender
   - CONTEXT with specific examples from the documents (e.g., "570 lawyers", "IRAP PROTECTED")
3. strategic_importance_score (1-5, where 5 is critical)
4. source_references (use EXACT document names: ["DocumentName.pdf"])

SCORING GUIDE:

Score 5 - Critical problem to solve:
  - Non-negotiable requirements
  - Significant scale/impact on their operations
  - High-stakes risk if not addressed

Score 4 - Important problem to solve:
  - Important but solvable challenge
  - Risk they want to mitigate
  - Strategic need for their organization

Score 3 or Below - DO NOT INCLUDE:
  - Nice-to-have preferences
  - Administrative tasks
  - Not actual problems to solve

IMPORTANT: Ensure pain points are DISTINCT problems covering different strategic challenges.
Each pain point should be a separate problem the buyer needs to solve.

Before returning, verify:
✓ Each pain point is a REAL PROBLEM the company needs to solve
✓ Descriptions explain WHY it's important to this company and tender
✓ CONTEXT includes specific examples from documents
✓ Pain points are DISTINCT (different problems, not aspects of same problem)
✓ All scored 4-5 (truly strategic problems)
✓ Do NOT merge similar pain points before returning (let dedup handle it)

Output JSON:
{{
  "pain_points": [...],
  "extraction_confidence": "high|medium|low"
}}"""


# Option 2 (multi-pass) prompts - 3 steps

def build_step1_extract_prompt(file_labels: str, file_names: List[str]) -> str:
    """Step 1: Extract UP TO 15 initial pain points (wider net)"""
    file_names_list = "\n".join([f"  - {name}" for name in file_names])
    
    return f"""You are a strategic tender analyst identifying buyer pain points.

PAIN POINTS are the PROBLEMS the company is trying to solve in this tender.

You are analyzing these tender documents:
{file_labels}

DOCUMENT NAMES FOR CITATIONS:
{file_names_list}

Extract UP TO 15 potential buyer pain points - the problems they need to solve. We'll refine in the next steps.

Cast a wide net to capture all potential problems. Quality filtering happens in Step 2.

For each pain point, provide:
1. title (max 50 chars) - The problem they're trying to solve
2. description (max 300 chars) - WHAT the problem is, WHY it matters to the company, CONTEXT from documents
3. source_references (use EXACT document names: ["DocumentName.pdf"])

IMPORTANT: Ensure pain points are DISTINCT problems covering different strategic challenges.

Return JSON with 'pain_points' list."""


def build_step2_smart_merge_prompt(initial_points: List[dict]) -> str:
    """Step 2: Smart Merge (LLM-based dedup)"""
    return f"""Review these extracted pain points:
{json.dumps(initial_points, indent=2)}

Your task is to DEDUPLICATE and CONSOLIDATE this list.

Instructions:
1. Identify pain points that are discussing the SAME underlying problem
2. MERGE them into a single, comprehensive pain point
   - Combine their descriptions to capture all nuances
   - Combine their source references
3. KEEP unique pain points as they are
4. DO NOT delete distinct strategic problems

Example:
- "Security compliance" + "Data privacy risk" → MERGE into "Comprehensive Security & Privacy Mandate"
- "Budget uncertainty" + "Lack of market knowledge" → KEEP SEPARATE (different problems)

Return JSON with 'pain_points' list containing the consolidated set."""


def build_step3_select_top5_prompt(consolidated_points: List[dict]) -> str:
    """Step 3: Strategic Selection (Pick Best 5)"""
    return f"""Review these consolidated pain points:
{json.dumps(consolidated_points, indent=2)}

Select the TOP 5 most critical pain points for a winning tender response.

Selection Criteria:
1. Highest strategic impact (transformational, high-stakes, large scale)
2. Non-negotiable requirements (security, compliance)
3. Must cover DIVERSE strategic themes (e.g. don't pick 5 security points; pick Security, Productivity, Integration, Innovation, etc.)

Discard the rest.

Return final 5 pain points with:
- title (max 50 chars)
- description (max 300 chars - rich, problem-focused)
- strategic_importance_score
- source_references

Output JSON with 'pain_points' list."""


def build_verification_prompt(pain_points: List[dict]) -> str:
    """Verification step for Option 3: Final quality check before clustering"""
    return f"""Review these pain points for final verification:
{json.dumps(pain_points, indent=2)}

For EACH pain point, verify it's a REAL PROBLEM the company needs to solve:
1. Is it truly a STRATEGIC PROBLEM (not just an administrative task)?
2. Does the description explain WHY it's important to the company?
3. Is it DISTINCT from the others (a different problem)?
4. Does CONTEXT include specific examples from the tender?

Remove any that fail verification.

Keep only pain points that are real strategic problems the company needs to solve.

Return JSON with verified 'pain_points' list."""


