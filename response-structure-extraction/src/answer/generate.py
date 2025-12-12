"""Placeholder answer-generation runner (Gemini-only, to be implemented)."""
from typing import Any, Dict, Optional

from src.schema import AnswerResult, ExtractionResult


def run(
    extraction: ExtractionResult,
    retrieval_context: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None,
) -> AnswerResult:
    """Generate answers for extracted questions (placeholder).

    Args:
        extraction: Extracted schedule structure.
        retrieval_context: Optional retrieval results (docs, snippets, citations).
        config: Optional model/settings.

    Returns:
        AnswerResult with answers (empty placeholder).
    """

    # TODO: implement Gemini-based answer generation using extraction + retrieval_context
    return AnswerResult()
