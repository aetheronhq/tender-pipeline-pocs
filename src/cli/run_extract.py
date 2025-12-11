"""Run a single extraction implementation on one document and save prediction."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, Dict

from src.eval.evaluate import save_result
from src.extract import parse, vision, smart_parse
from src.schema import ExtractionResult

IMPLEMENTATIONS: Dict[str, Callable[[str, Dict | None], ExtractionResult]] = {
    "parse": parse.run,
    "vision": vision.run,
    "smart": smart_parse.run,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run extraction implementation")
    parser.add_argument("--impl", choices=IMPLEMENTATIONS.keys(), required=True)
    parser.add_argument("--doc", required=True, help="Path to schedule document")
    parser.add_argument("--out", required=True, help="Path to write prediction JSON")
    args = parser.parse_args()

    runner = IMPLEMENTATIONS[args.impl]
    print(f"Running {args.impl} extraction on {args.doc}...")
    
    result = runner(args.doc, None)
    
    save_result(result, Path(args.out))
    print(f"Saved prediction to {args.out}")


if __name__ == "__main__":
    main()
