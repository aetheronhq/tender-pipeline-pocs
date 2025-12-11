#!/usr/bin/env python3
"""
Run extraction on all documents in data/samples/ using a specified implementation.
Usage: python scripts/run_all.py --impl vision
"""
import argparse
import sys
import time
from pathlib import Path
from typing import List

# Add src to path so we can import modules
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from src.extract import vision
from src.eval.evaluate import save_result
from src.schema import ExtractionResult

IMPLEMENTATIONS = {
    "vision": vision.run,
}

def main():
    parser = argparse.ArgumentParser(description="Run extraction on all sample documents.")
    parser.add_argument("--impl", choices=IMPLEMENTATIONS.keys(), required=True, help="Implementation to use")
    parser.add_argument("--samples", default="data/samples", help="Path to samples directory")
    parser.add_argument("--out-dir", default="output", help="Base output directory")
    
    args = parser.parse_args()

    samples_dir = Path(args.samples)
    if not samples_dir.exists():
        print(f"Samples directory not found: {samples_dir}")
        return

    # Create timestamped output directory
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_dir = Path(args.out_dir) / args.impl / timestamp
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Output directory: {out_dir}")
    
    files = list(samples_dir.glob("*.docx")) + \
            list(samples_dir.glob("*.xlsx")) + \
            list(samples_dir.glob("*.pdf"))
    
    if not files:
        print("No documents found in samples directory.")
        return

    runner = IMPLEMENTATIONS[args.impl]
    
    for doc_path in files:
        print(f"\nProcessing {doc_path.name}...")
        try:
            result = runner(str(doc_path), None)
            
            out_file = out_dir / f"{doc_path.stem}.json"
            save_result(result, out_file)
            print(f"Success! Saved to {out_file.name}")
            
        except Exception as e:
            print(f"Error processing {doc_path.name}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\nDone! Results saved in {out_dir}")

if __name__ == "__main__":
    main()
