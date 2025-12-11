"""Evaluation harness with metrics and reporting."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from src.schema import ExtractionResult, UsageStats


def load_result(path: Path) -> ExtractionResult:
    """Load an ExtractionResult from a JSON file."""
    # Pydantic handles the parsing automatically
    return ExtractionResult.model_validate_json(path.read_text())


def evaluate(pred_path: Path, golden_path: Path) -> Dict[str, Any]:
    """Compare prediction and golden files and return metrics."""
    # Load as simple dicts for flexible comparison, or use models
    # Using dicts is often easier for flexible field access without strict validation errors on golden data
    pred_data = json.loads(pred_path.read_text())
    gold_data = json.loads(golden_path.read_text())
    
    pred_questions = pred_data.get("questions", [])
    gold_questions = gold_data.get("questions", [])
    usage = pred_data.get("usage", {})

    # 1. Exact Count Match
    count_match = len(pred_questions) == len(gold_questions)
    
    # 2. Numbering Match (Set comparison)
    pred_nums = set(q.get("number") for q in pred_questions)
    gold_nums = set(q.get("number") for q in gold_questions)
    
    missing_nums = list(gold_nums - pred_nums)
    extra_nums = list(pred_nums - gold_nums)
    numbering_accuracy = len(pred_nums.intersection(gold_nums)) / len(gold_nums) if gold_nums else 0.0

    # 3. Field-Level Accuracy (for matching numbers)
    field_matches = 0
    total_fields = 0
    
    # Create map for fast lookup
    pred_map = {q.get("number"): q for q in pred_questions}
    
    fields_to_check = ["text", "interaction_type", "limit"]
    
    for gold_q in gold_questions:
        num = gold_q.get("number")
        if num in pred_map:
            pred_q = pred_map[num]
            for field in fields_to_check:
                total_fields += 1
                # Simple exact match (case-insensitive for text)
                g_val = gold_q.get(field)
                p_val = pred_q.get(field)
                
                if field == "text" and isinstance(g_val, str) and isinstance(p_val, str):
                    if g_val.lower().strip() == p_val.lower().strip():
                        field_matches += 1
                elif g_val == p_val:
                    field_matches += 1

    field_accuracy = field_matches / total_fields if total_fields > 0 else 0.0

    return {
        "metrics": {
            "count_match": count_match,
            "pred_count": len(pred_questions),
            "gold_count": len(gold_questions),
            "numbering_accuracy": round(numbering_accuracy, 4),
            "field_accuracy": round(field_accuracy, 4),
            "cost_usd": usage.get("cost_usd", 0.0),
            "latency_s": round(usage.get("latency_s", 0.0), 2),
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0)
        },
        "details": {
            "missing_numbers": missing_nums,
            "extra_numbers": extra_nums
        }
    }


def save_result(result: ExtractionResult, out_path: Path) -> None:
    """Save ExtractionResult to JSON."""
    out_path.write_text(result.model_dump_json(indent=2))
