#!/usr/bin/env python3
"""
Evaluate ALL existing extraction results against golden files.
Usage: python scripts/eval_only.py [--base-dir output]
"""
import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict

# Add src to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.eval.evaluate import evaluate

def main():
    parser = argparse.ArgumentParser(description="Evaluate all existing predictions against goldens")
    parser.add_argument("--base-dir", default="output", help="Base output directory containing implementation folders")
    parser.add_argument("--golden", default="data/golden", help="Path to directory of golden JSONs")
    args = parser.parse_args()

    base_dir = Path(args.base_dir)
    golden_dir = Path(args.golden)
    
    if not base_dir.exists():
        print(f"Base directory not found: {base_dir}")
        return

    print(f"\nEvaluating ALL results in: {base_dir}")
    print("=" * 100)
    print(f"{'Run (Impl/Time)':<40} | {'Doc':<20} | {'Count':<8} | {'Acc':<8} | {'Cost':<8} | {'Time':<8}")
    print("-" * 100)

    # Walk through: output/{impl}/{timestamp}/{file}.json
    results_summary = []

    # Find all implementation directories
    impl_dirs = [d for d in base_dir.iterdir() if d.is_dir() and d.name not in ["temp_vision"]]
    
    for impl_dir in sorted(impl_dirs):
        impl_name = impl_dir.name
        
        # Find all timestamp runs
        run_dirs = [d for d in impl_dir.iterdir() if d.is_dir()]
        
        for run_dir in sorted(run_dirs, reverse=True): # Latest first
            run_id = f"{impl_name}/{run_dir.name}"
            
            # Find all JSON predictions in this run
            pred_files = list(run_dir.glob("*.json"))
            valid_preds = [p for p in pred_files if p.name not in ["scores.json", "eval_scores.json"]]
            
            if not valid_preds:
                continue

            for pred_path in valid_preds:
                stem = pred_path.stem
                golden_path = golden_dir / f"{stem}.json"
                
                if not golden_path.exists():
                    continue

                try:
                    score = evaluate(pred_path, golden_path)
                    m = score["metrics"]
                    
                    count_str = f"{m['pred_count']}/{m['gold_count']}"
                    acc_str = f"{m['field_accuracy']:.0%}"
                    cost_str = f"${m['cost_usd']:.4f}"
                    time_str = f"{m['latency_s']}s"
                    
                    print(f"{run_id:<40} | {stem:<20} | {count_str:<8} | {acc_str:<8} | {cost_str:<8} | {time_str:<8}")
                    
                    results_summary.append({
                        "run_id": run_id,
                        "doc": stem,
                        "metrics": m
                    })
                    
                except Exception as e:
                    # print(f"Error evaluating {pred_path}: {e}")
                    pass

    # Save master report
    report_path = base_dir / "master_eval_report.json"
    report_path.write_text(json.dumps(results_summary, indent=2))
    print("=" * 100)
    print(f"Master evaluation report saved to {report_path}")

if __name__ == "__main__":
    main()
