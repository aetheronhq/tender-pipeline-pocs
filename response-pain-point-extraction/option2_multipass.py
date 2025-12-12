"""
Option 2: Deep Extract & Select (3 steps).
1. Deep Extraction: Extract 15 pain points (wide net).
2. Smart Merge: LLM-based deduplication (merge similar, keep unique).
3. Strategic Selection: Select Top 5 most critical & diverse.
Replaces embeddings-based dedup with intelligent LLM reasoning.
"""

import json
import sys
import time
from typing import List
from datetime import datetime

from google.genai import types

from shared_utils import get_gemini_client, upload_document, upload_documents, build_contents
from deduplication import deduplicate_pain_points
import prompts


def step1_extract(client, files, file_names):
    """Step 1: Extract 8-10 initial pain points. Returns (pain_points, tokens)."""
    if not isinstance(files, list):
        files = [files]
    
    file_labels = "\n".join([f"File {i+1}: {f.display_name}" for i, f in enumerate(files)])
    prompt = prompts.build_step1_extract_prompt(file_labels, file_names)
    contents = build_contents(prompt, files)
    
    resp = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=contents,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    
    tokens = {
        "prompt_tokens": resp.usage_metadata.prompt_token_count,
        "candidates_tokens": resp.usage_metadata.candidates_token_count,
        "total_tokens": resp.usage_metadata.total_token_count
    }
    
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return [], tokens
    return data.get("pain_points", []), tokens


def step2_smart_merge(client, initial_points):
    """Step 2: LLM-based Smart Merge (Deduplicate & Consolidate)."""
    prompt = prompts.build_step2_smart_merge_prompt(initial_points)
    
    # Increase tokens for processing larger context
    resp = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=4000
        ),
    )
    
    tokens = {
        "prompt_tokens": resp.usage_metadata.prompt_token_count,
        "candidates_tokens": resp.usage_metadata.candidates_token_count,
        "total_tokens": resp.usage_metadata.total_token_count
    }
    
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return [], tokens
    return data.get("pain_points", []), tokens


def step3_select_top5(client, consolidated_points):
    """Step 3: Strategic Selection (Top 5)."""
    prompt = prompts.build_step3_select_top5_prompt(consolidated_points)
    resp = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    
    tokens = {
        "prompt_tokens": resp.usage_metadata.prompt_token_count,
        "candidates_tokens": resp.usage_metadata.candidates_token_count,
        "total_tokens": resp.usage_metadata.total_token_count
    }
    
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return [], tokens
    return data.get("pain_points", []), tokens


def run_option2(client, files, file_names):
    """Returns: (final_points, merge_decisions_dummy, step_results, token_usage)"""
    try:
        print("[Option 2] Starting Deep Extract & Select (3 steps)...")
        step_results = {}
        all_tokens = []

        # Step 1: Deep Extraction (Wide Net)
        print("  Step 1/3: Deep Extraction (up to 15 points)...")
        initial_points, tokens1 = step1_extract(client, files, file_names)
        all_tokens.append(tokens1)
        step_results["step1_initial"] = initial_points
        print(f"  ✓ Extracted {len(initial_points)} initial pain points")
        if not initial_points:
            print("  ⚠️ No pain points extracted; stopping Option 2")
            return [], [], step_results, {"note": "Failed at step 1"}

        # Step 2: Smart Merge (LLM Dedup)
        print("  Step 2/3: Smart Merge (LLM-based deduplication)...")
        consolidated_points, tokens2 = step2_smart_merge(client, initial_points)
        all_tokens.append(tokens2)
        step_results["step2_consolidated"] = consolidated_points
        print(f"  ✓ Consolidated to {len(consolidated_points)} unique strategic points")

        # Step 3: Strategic Selection (Top 5)
        print("  Step 3/3: Strategic Selection (picking Top 5)...")
        final_points, tokens3 = step3_select_top5(client, consolidated_points)
        all_tokens.append(tokens3)
        step_results["step3_selected"] = final_points
        print(f"  ✓ Selected {len(final_points)} final pain points")

        # No python deduplication needed - LLM did it in Step 2!
        merge_decisions = [{"note": "LLM handled merging in Step 2"}]
        
        # Sum all token usage
        total_token_usage = {
            "step1_tokens": tokens1,
            "step2_tokens": tokens2,
            "step3_tokens": tokens3,
            "total_prompt_tokens": sum(t["prompt_tokens"] for t in all_tokens),
            "total_candidates_tokens": sum(t["candidates_tokens"] for t in all_tokens),
            "total_tokens": sum(t["total_tokens"] for t in all_tokens)
        }
        
        return final_points, merge_decisions, step_results, total_token_usage

    except Exception as e:
        print(f"[ERROR] Option 2 failed: {e}")
        return [], [], {}, {"error": str(e)}


def main():
    if len(sys.argv) < 2:
        print("Usage: python option2_multipass.py <pdf1> [pdf2 pdf3 ...]")
        sys.exit(1)

    start_time = time.time()
    paths = sys.argv[1:]
    client = get_gemini_client()

    # Upload
    upload_start = time.time()
    if len(paths) == 1:
        files = upload_document(client, paths[0])
        if files is None:
            sys.exit(1)
        files = [files]
    else:
        files = upload_documents(client, paths)
        if files is None:
            sys.exit(1)
    upload_time = time.time() - upload_start
    
    # Store document names from paths for metadata
    doc_names = [path.split('/')[-1] for path in paths]

    # Run multi-pass extraction
    extraction_start = time.time()
    pain_points_final, merge_decisions, step_results, token_usage = run_option2(client, files, doc_names)
    extraction_time = time.time() - extraction_start
    total_time = time.time() - start_time
    
    print(f"\n📊 Final count after dedup: {len(pain_points_final)}")
    print(f"⏱️  Total execution time: {total_time:.1f}s (upload: {upload_time:.1f}s, extraction+dedup: {extraction_time:.1f}s)")

    # Save with auto-incrementing filename
    import os
    os.makedirs("results", exist_ok=True)
    
    # Find next available number
    counter = 1
    while os.path.exists(f"results/option2_results_{counter:03d}.json"):
        counter += 1
    
    output_file = f"results/option2_results_{counter:03d}.json"
    
    # Build comprehensive output
    output_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "option": "option2_multipass",
            "model": "gemini-3-pro-preview",
            "threshold": 0.9,
            "prompt_version": "v5",
            "documents": doc_names,
            "timing": {
                "upload_seconds": round(upload_time, 2),
                "extraction_seconds": round(extraction_time, 2),
                "total_seconds": round(total_time, 2)
            },
            "tokens": token_usage
        },
        "step_results": {
            "step1_initial_count": len(step_results.get("step1_initial", [])),
            "step1_initial_points": step_results.get("step1_initial", []),
            "step2_filtered_count": len(step_results.get("step2_consolidated", [])),
            "step2_filtered_points": step_results.get("step2_consolidated", []),
            "step3_refined_count": len(step_results.get("step3_selected", [])),
            "step3_refined_points": step_results.get("step3_selected", [])
        },
        "deduplication": {
            "before_count": len(step_results.get("step3_selected", [])),
            "after_count": len(pain_points_final),
            "merge_decisions": merge_decisions
        },
        "pain_points_final": pain_points_final
    }
    
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2)
    print(f"✅ Saved to {output_file}")


if __name__ == "__main__":
    main()

