"""
Option 1: Single-pass extraction (quality over quantity).

Usage:
  python option1_simple.py tenders/tender1/RFT.pdf
  python option1_simple.py tenders/tender2/RFT_Main.pdf tenders/tender2/Technical_Specs.pdf
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


def main():
    if len(sys.argv) < 2:
        print("Usage: python option1_simple.py <pdf1> [pdf2 pdf3 ...]")
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

    # Extract (modified to capture original + dedup details)
    extraction_start = time.time()
    
    # Get original pain points before dedup
    if not isinstance(files, list):
        files = [files]
    
    file_labels = "\n".join([f"File {i+1}: {f.display_name}" for i, f in enumerate(files)])
    file_names = [path.split('/')[-1] for path in paths]
    prompt = prompts.build_option1_prompt(file_labels, file_names)
    contents = build_contents(prompt, files)
    
    response = client.models.generate_content(
        model="gemini-3-pro-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        ),
    )
    
    # Capture token usage
    token_usage = {
        "prompt_tokens": response.usage_metadata.prompt_token_count,
        "candidates_tokens": response.usage_metadata.candidates_token_count,
        "total_tokens": response.usage_metadata.total_token_count
    }
    
    try:
        result = json.loads(response.text)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON from model: {e}")
        sys.exit(1)
    
    pain_points_original = result.get("pain_points", [])
    print(f"Extracted {len(pain_points_original)} pain points (before dedup)")
    
    # Deduplicate
    pain_points_final, merge_decisions = deduplicate_pain_points(client, pain_points_original, threshold=0.9)
    extraction_time = time.time() - extraction_start
    total_time = time.time() - start_time
    
    print(f"\n📊 Final count after dedup: {len(pain_points_final)}")
    print(f"⏱️  Total execution time: {total_time:.1f}s (upload: {upload_time:.1f}s, extraction+dedup: {extraction_time:.1f}s)")

    # Save with auto-incrementing filename
    import os
    os.makedirs("results", exist_ok=True)
    
    # Find next available number
    counter = 1
    while os.path.exists(f"results/option1_results_{counter:03d}.json"):
        counter += 1
    
    output_file = f"results/option1_results_{counter:03d}.json"
    
    # Build comprehensive output
    output_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "option": "option1_simple",
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
        "pain_points_original": pain_points_original,
        "deduplication": {
            "before_count": len(pain_points_original),
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


