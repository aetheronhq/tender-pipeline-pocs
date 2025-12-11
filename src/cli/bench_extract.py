"""Benchmark extraction implementation against goldens (placeholder)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable, Dict

from src.eval.evaluate import evaluate, save_result
from src.extract import vision
from src.schema import ExtractionResult

IMPLEMENTATIONS: Dict[str, Callable[[str, Dict | None], ExtractionResult]] = {
    "vision": vision.run,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark extraction vs goldens")
    parser.add_argument("--impl", choices=IMPLEMENTATIONS.keys(), required=True)
    parser.add_argument("--docs", required=True, help="Path to directory of sample docs")
    parser.add_argument("--golden", required=True, help="Path to directory of golden JSONs")
    parser.add_argument("--out", required=True, help="Path to write predictions")
    args = parser.parse_args()

    docs_dir = Path(args.docs)
    golden_dir = Path(args.golden)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    runner = IMPLEMENTATIONS[args.impl]
    scores = {}

    for doc_path in sorted(docs_dir.iterdir()):
        if not doc_path.is_file():
            continue
        stem = doc_path.stem
        golden_path = golden_dir / f"{stem}.json"
        if not golden_path.exists():
            print(f"Skipping {doc_path} (no golden)")
            continue

        result = runner(str(doc_path), config=None)
        pred_path = out_dir / f"{stem}.json"
        save_result(result, pred_path)

        score = evaluate(pred_path, golden_path)
        scores[stem] = score
        metrics = score["metrics"]
        print(f"{stem}: pred={metrics['pred_count']} gold={metrics['gold_count']} acc={metrics['field_accuracy']} cost=${metrics['cost_usd']:.4f} time={metrics['latency_s']}s")

    (out_dir / "scores.json").write_text(json.dumps(scores, indent=2))
    print(f"Wrote scores to {out_dir / 'scores.json'}")


if __name__ == "__main__":
    main()
