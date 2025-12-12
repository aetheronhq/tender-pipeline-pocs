"""
Option 2: Multi-pass (Read -> Extract -> Revise -> Refine).
Simple Python chaining; no frameworks. Basic error handling to avoid crashing.
Prompts centralized in prompts.py to keep wording consistent.
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


def step1_read(client, files) -> str:
    """Read & analyze: return context summary."""
    contents = build_contents(prompts.STEP1_READ_PROMPT, files)
    resp = client.models.generate_content(model="gemini-2.5-pro", contents=contents)
    return resp.text


def step2_extract(client, files, context_summary) -> List[dict]:
    """Extract initial (wide net) pain points."""
    prompt = prompts.build_step2_extract_prompt(context_summary)
    contents = build_contents(prompt, files)
    resp = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=contents,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return []
    if isinstance(data, list):
        return data
    return data.get("pain_points", data)


def step3_revise(client, initial_points) -> List[dict]:
    """Revise & filter to keep only strategic items."""
    prompt = prompts.build_step3_revise_prompt(initial_points)
    resp = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return []
    return data.get("pain_points", [])


def step4_refine(client, filtered_points) -> List[dict]:
    """Refine & finalize: merge similar, return final 3-5."""
    prompt = prompts.build_step4_refine_prompt(filtered_points)
    resp = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[prompt],
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    try:
        data = json.loads(resp.text)
    except json.JSONDecodeError:
        return []
    return data.get("pain_points", [])


def run_option2(client, files):
    """Returns: (deduped_pain_points, merge_decisions, step_results)"""
    try:
        print("[Option 2] Starting multi-pass extraction...")
        step_results = {}

        print("  Step 1/4: Reading and analyzing documents...")
        ctx = step1_read(client, files)
        step_results["step1_context"] = ctx
        print("  ✓ Context summary generated")

        print("  Step 2/4: Extracting initial pain points...")
        raw_points = step2_extract(client, files, ctx)
        step_results["step2_initial"] = raw_points
        print(f"  ✓ Extracted {len(raw_points)} initial pain points")
        if not raw_points:
            print("  ⚠️ No pain points extracted; stopping Option 2 for this tender")
            return [], [], step_results

        print("  Step 3/4: Revising and filtering...")
        filtered = step3_revise(client, raw_points)
        step_results["step3_filtered"] = filtered
        print(f"  ✓ Filtered to {len(filtered)} strategic pain points")

        print("  Step 4/4: Refining and merging similar items...")
        final_points = step4_refine(client, filtered)
        step_results["step4_refined"] = final_points
        print(f"  ✓ Final set: {len(final_points)} pain points")

        # Deduplicate
        deduped, merge_decisions = deduplicate_pain_points(client, final_points, threshold=0.9)
        return deduped, merge_decisions, step_results

    except Exception as e:
        print(f"[ERROR] Option 2 failed: {e}")
        return [], [], {}


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
    pain_points_final, merge_decisions, step_results = run_option2(client, files)
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
            "model": "gemini-2.5-pro",
            "threshold": 0.9,
            "documents": doc_names,
            "timing": {
                "upload_seconds": round(upload_time, 2),
                "extraction_seconds": round(extraction_time, 2),
                "total_seconds": round(total_time, 2)
            }
        },
        "step_results": {
            "step1_context_summary": step_results.get("context_summary", ""),
            "step2_initial_count": len(step_results.get("step2_initial", [])),
            "step2_initial_points": step_results.get("step2_initial", []),
            "step3_filtered_count": len(step_results.get("step3_filtered", [])),
            "step3_filtered_points": step_results.get("step3_filtered", []),
            "step4_refined_count": len(step_results.get("step4_refined", [])),
            "step4_refined_points": step_results.get("step4_refined", [])
        },
        "deduplication": {
            "before_count": len(step_results.get("step4_refined", [])),
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


