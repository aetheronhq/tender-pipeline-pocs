"""
Deduplication helpers for pain points using Gemini embeddings.
"""

from typing import List, Dict, Optional

import numpy as np
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity


def deduplicate_pain_points(
    client: genai.Client,
    pain_points: List[Dict],
    threshold: float = 0.8,
) -> tuple[List[Dict], List[Dict]]:
    """
    Deduplicate pain points using Gemini embeddings.
    Merges by keeping the first occurrence and dropping later similar ones.
    
    Returns:
        tuple: (deduplicated_pain_points, merge_decisions)
    """
    if len(pain_points) <= 1:
        return pain_points, []

    descriptions = [pp["description"] for pp in pain_points]

    print(f"Generating embeddings for {len(descriptions)} pain points...")
    result = client.models.embed_content(
        model="text-embedding-004",  # Updated for Gemini 3 (gemini-embedding-001 is older)
        contents=descriptions,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY",
            output_dimensionality=768,
        ),
    )

    embeddings = []
    for e in result.embeddings:
        vec = np.array(e.values)
        embeddings.append(vec / np.linalg.norm(vec))

    sim = cosine_similarity(np.array(embeddings))

    keep = []
    skipped = set()
    merge_decisions = []
    
    for i in range(len(pain_points)):
        if i in skipped:
            continue
        keep.append(i)
        for j in range(i + 1, len(pain_points)):
            if sim[i][j] > threshold:
                print(f"  Merging similar items ({sim[i][j]:.2f}): keep '{pain_points[i]['title']}' skip '{pain_points[j]['title']}'")
                merge_decisions.append({
                    "kept": pain_points[i]['title'],
                    "merged": pain_points[j]['title'],
                    "similarity": float(sim[i][j])
                })
                skipped.add(j)

    deduped = [pain_points[i] for i in keep]
    print(f"Deduplication: {len(pain_points)} → {len(deduped)} (threshold={threshold})")
    return deduped, merge_decisions


def deduplicate_with_supporting_examples(
    client: genai.Client,
    pain_points: List[Dict],
    threshold: float = 0.9,
    max_clusters: int = 5
) -> tuple[List[Dict], List[Dict]]:
    """
    Deduplicate pain points using cluster-based approach with supporting examples.
    
    Creates up to max_clusters pain points, where similar items become supporting
    examples instead of being discarded.
    
    Returns:
        tuple: (clustered_pain_points, merge_decisions)
    """
    if len(pain_points) <= 1:
        return pain_points, []
    
    descriptions = [pp["description"] for pp in pain_points]
    
    print(f"Generating embeddings for {len(descriptions)} pain points...")
    result = client.models.embed_content(
        model="text-embedding-004",  # Updated for Gemini 3 (gemini-embedding-001 is older)
        contents=descriptions,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY",
            output_dimensionality=768,
        ),
    )
    
    embeddings = []
    for e in result.embeddings:
        vec = np.array(e.values)
        embeddings.append(vec / np.linalg.norm(vec))
    
    sim = cosine_similarity(np.array(embeddings))
    
    # Cluster similar items
    clusters = []
    assigned = set()
    merge_decisions = []
    
    for i in range(len(pain_points)):
        if i in assigned:
            continue
        
        # Start new cluster
        cluster = {
            "main_pain_point": pain_points[i],
            "supporting_examples": []
        }
        assigned.add(i)
        
        # Find similar items for this cluster
        for j in range(i + 1, len(pain_points)):
            if j in assigned:
                continue
            if sim[i][j] > threshold:
                print(f"  Adding supporting example (similarity {sim[i][j]:.2f}): '{pain_points[j]['title']}'")
                cluster["supporting_examples"].append(pain_points[j])
                merge_decisions.append({
                    "main": pain_points[i]['title'],
                    "supporting": pain_points[j]['title'],
                    "similarity": float(sim[i][j])
                })
                assigned.add(j)
        
        clusters.append(cluster)
        
        # Stop if we have enough clusters
        if len(clusters) >= max_clusters:
            # Add remaining unassigned as individual clusters if space
            break
    
    # Add any remaining unassigned items as individual clusters (if under max_clusters)
    for i in range(len(pain_points)):
        if i not in assigned and len(clusters) < max_clusters:
            clusters.append({
                "main_pain_point": pain_points[i],
                "supporting_examples": []
            })
            assigned.add(i)
    
    # Build final output with supporting examples
    result_pain_points = []
    for cluster in clusters:
        main = cluster["main_pain_point"].copy()
        if cluster["supporting_examples"]:
            main["supporting_examples"] = [
                {
                    "title": ex["title"],
                    "description": ex["description"],
                    "source_references": ex.get("source_references", [])
                }
                for ex in cluster["supporting_examples"]
            ]
        result_pain_points.append(main)
    
    print(f"Clustering: {len(pain_points)} → {len(result_pain_points)} pain points (with supporting examples)")
    
    return result_pain_points, merge_decisions


def test_thresholds(client: genai.Client, pain_points: List[Dict], thresholds=(0.7, 0.8, 0.9)) -> Dict[float, int]:
    """Return count of pain points after dedup for each threshold."""
    results = {}
    for t in thresholds:
        deduped, _ = deduplicate_pain_points(client, pain_points, threshold=t)
        results[t] = len(deduped)
    return results


