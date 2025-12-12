"""
Option 3: Structured extraction with validation.
- Uses strategic_importance_score; only returns 4-5.
"""

import json
import sys
import time
from typing import List
from datetime import datetime

from google.genai import types

from shared_utils import get_gemini_client, upload_document, upload_documents, build_contents
from deduplication import deduplicate_pain_points, deduplicate_with_supporting_examples
import prompts


def main():
    if len(sys.argv) < 2:
        print("Usage: python option3_validated.py <pdf1> [pdf2 pdf3 ...]")
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

    # Extract with timing
    extraction_start = time.time()
    
    if not isinstance(files, list):
        files = [files]
    
    file_labels = "\n".join([f"File {i+1}: {f.display_name}" for i, f in enumerate(files)])
    file_names = [path.split('/')[-1] for path in paths]
    prompt = prompts.build_option3_prompt(file_labels, file_names)
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
    # Filter to scores 4-5
    pain_points_filtered = [pp for pp in pain_points_original if pp.get("strategic_importance_score", 0) >= 4]
    print(f"Extracted {len(pain_points_original)} pain points, {len(pain_points_filtered)} after score filter (4-5 only)")
    
    # Deduplicate with supporting examples (cluster to max 5 pain points)
    print(f"Clustering with supporting examples (max 5 final pain points)...")
    pain_points_final, merge_decisions = deduplicate_with_supporting_examples(
        client, 
        pain_points_filtered, 
        threshold=0.9,
        max_clusters=5
    )
    extraction_time = time.time() - extraction_start
    total_time = time.time() - start_time
    
    print(f"\n📊 Final count after dedup: {len(pain_points_final)}")
    print(f"⏱️  Total execution time: {total_time:.1f}s (upload: {upload_time:.1f}s, extraction+dedup: {extraction_time:.1f}s)")

    # Save with auto-incrementing filename
    import os
    os.makedirs("results", exist_ok=True)
    
    # Find next available number
    counter = 1
    while os.path.exists(f"results/option3_results_{counter:03d}.json"):
        counter += 1
    
    output_file = f"results/option3_results_{counter:03d}.json"
    
    # Build comprehensive output
    output_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "option": "option3_validated",
            "model": "gemini-3-pro-preview",
            "threshold": 0.9,
            "prompt_version": "v5",
            "max_final_pain_points": 5,
            "verification_step": False,
            "documents": doc_names,
            "timing": {
                "upload_seconds": round(upload_time, 2),
                "extraction_seconds": round(extraction_time, 2),
                "total_seconds": round(total_time, 2)
            },
            "tokens": token_usage
        },
        "pain_points_original": pain_points_original,
        "pain_points_after_score_filter": pain_points_filtered,
        "deduplication": {
            "before_count": len(pain_points_filtered),
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


