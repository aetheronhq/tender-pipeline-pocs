# Response Schedule Extraction POC (Gemini)

Purpose: rapid experiments to extract tender response schedule structure (numbering, questions, limits, compliance items) from DOCX/XLSX/PDF using multiple Gemini-based approaches. This repo is intentionally isolated from the main tender-creator-ai codebase to iterate quickly and choose the best architecture for production.

## Goals
- Preserve exact question numbering and order from response schedules.
- Capture question text, word/character limits, and classify rows (question vs compliance vs background).
- Support multiple formats (DOCX first, then XLSX, then PDF/scanned) with measurable fidelity.
- Compare multiple extraction strategies for accuracy, latency, and cost.

## Planned options to prototype
1. Vision-first (Gemini 1.5 Pro Vision): page images or PDF to structured JSON.
2. Parse-first + schema-constrained (Gemini 1.5 Flash): docx/xlsx parsed to tables, LLM classifies.
3. Hybrid validator: parse-first output cross-checked with selective vision page crops.
4. Office-API-assisted (DOCX/XLSX): use structured table extraction, then LLM classification.

## Repo layout (initial)
- `docs/` – ADRs and research notes.
- `data/` – sample/redacted schedules for benchmarking (not committed yet).
- `src/` – extraction drivers and evaluation harness (to be added).
- `scripts/` – convenience CLIs (to be added).

## Next steps
- Add sample documents and golden JSON for evaluation.
- Implement Option 2 (parse-first) and Option 1 (vision-first) runners for comparison.
- Capture results in ADR and select preferred approach for productionization.
