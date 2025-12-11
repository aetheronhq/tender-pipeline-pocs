"""Vision-first extraction using Gemini 1.5 Pro / 2.5 Flash Files API.

Strategy:
1. Normalize all inputs to PDF using LibreOffice Headless (DOCX -> PDF, XLSX -> PDF).
2. Upload the single PDF to Gemini Files API.
3. Send the file with strict extraction prompt.
"""
import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, Optional, List

import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from src.schema import ExtractionResult, Question, UsageStats, InteractionType, OutputSchema
from src.eval.pricing import calculate_cost

load_dotenv()


def _find_libreoffice() -> str:
    """Find the LibreOffice binary path."""
    # 1. Check environment variable
    if env_path := os.getenv("LIBREOFFICE_PATH"):
        if os.path.exists(env_path):
            return env_path

    # 2. Check system PATH (standard for Docker/Linux)
    if shutil.which("soffice"):
        return "soffice"

    # 3. Fallback for macOS local dev
    mac_path = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if os.path.exists(mac_path):
        return mac_path
        
    raise RuntimeError(
        "LibreOffice not found. Please install it or set LIBREOFFICE_PATH."
    )


def _convert_to_pdf_libreoffice(input_path: str, output_folder: str) -> Optional[Path]:
    """
    Converts DOCX or XLSX to PDF using LibreOffice Headless mode.
    No popups, no sandboxing issues.
    """
    libreoffice_path = _find_libreoffice()
    input_abs = os.path.abspath(input_path)
    output_abs = os.path.abspath(output_folder)
    
    # Command: soffice --headless --convert-to pdf --outdir <dir> <file>
    cmd = [
        libreoffice_path,
        "--headless",
        "--convert-to", "pdf",
        "--outdir", output_abs,
        input_abs
    ]
    
    try:
        # Run conversion silently
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        # Verify the PDF was created
        input_filename = Path(input_path).stem
        expected_pdf = Path(output_folder) / f"{input_filename}.pdf"
        
        if expected_pdf.exists():
            return expected_pdf
        else:
            print(f"   [Vision] Error: PDF not found at {expected_pdf}")
            print(f"   [Vision] LibreOffice Output: {result.stdout.strip()}")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"   [Vision] Conversion Failed: {e.stderr}")
        return None


def run(doc_path: str, config: Optional[Dict[str, Any]] = None) -> ExtractionResult:
    """Run vision-first extraction using Gemini Files API."""
    start_time = time.time()
    
    # Initialize usage stats with defaults
    model_name = "gemini-2.5-flash"
    input_tok = 0
    output_tok = 0
    total_tok = 0
    cost = 0.0

    path = Path(doc_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    # Use a temporary directory for the PDF conversion to ensure cleanup
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Normalize to PDF
        pdf_path: Path
        
        print(f"   [Vision] Processing {path.name}...")
        if path.suffix.lower() in [".docx", ".xlsx"]:
            print(f"   [Vision] Converting {path.suffix} to PDF via LibreOffice...")
            converted_path = _convert_to_pdf_libreoffice(str(path), temp_dir)
            if not converted_path:
                raise RuntimeError("File conversion failed.")
            pdf_path = converted_path
        elif path.suffix.lower() == ".pdf":
            pdf_path = path
        else:
            raise ValueError(f"Unsupported file type: {path.suffix}")

        # 2. Upload to Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in env")

        genai.configure(api_key=api_key)

        print(f"   [Vision] Uploading {pdf_path.name} to Gemini...")
        uploaded_file = genai.upload_file(path=pdf_path, mime_type="application/pdf")

        try:
            # 3. Wait for processing
            while uploaded_file.state.name == "PROCESSING":
                print("   [Vision] Waiting for processing...")
                time.sleep(2)
                uploaded_file = genai.get_file(uploaded_file.name)

            if uploaded_file.state.name == "FAILED":
                raise ValueError("Gemini failed to process the file.")

            print(f"   [Vision] File ready: {uploaded_file.uri}")

            # 4. Generate Content
            # Use Flash 2.5 (or Pro 1.5) for vision.
            
            # Use strict explicit schema from src.schema
            model = genai.GenerativeModel(
                model_name,
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": OutputSchema,
                }
            )

            # Strict Prompt
            prompt = """
            You are an Expert Tender Response Analyst specializing in parsing complex RFP documents for bid teams.
            Your objective is to extract a strictly structured Response Schedule from the document provided.

            ### CRITICAL RULES
            1. **Questions vs Headings**: 
               - Create a `question` record ONLY for items that require a user response (text, check).
               - Do NOT create records for pure headings, titles, or instructional text. Instead, use them to build the `section_path`.
               - If a row is purely informational (background context), do not create a question unless it explicitly asks for acknowledgement.
               - **Text Content**: Include the FULL question text including any immediate instructions (e.g., "If yes, attach certificate").

            2. **Interaction Types & Options (STRICT)**:
               - `open_text`: Standard questions asking for description/details. `options` must be [].
               - `yes_no`: Simple Yes/No or Pass/Fail confirmation. **MUST use `yes_no` type, NOT `dropdown`. `options` must be [].**
               - `checkbox`: Checkbox items. `options` must be [].
               - `date`/`numeric`: Specific types. `options` must be [].
               - `dropdown`: Selection from a list of 3+ specific choices (e.g. State, Category). ONLY then populate `options`.

            3. **Numbering & Hierarchy**:
               - Extract the EXACT official numbering from the document (e.g., "1.1", "C.2.iv", "Q5").
               - If NO number exists, synthesize one (e.g., "auto-001", "auto-002") maintaining strict document order.
               - `section_path` must include the full hierarchy of headings above the question. format: "Number Title" (e.g. "2. Technical Methodology").

            4. **Limits**:
               - `limit`: Extract explicit constraints as a string (e.g., "500 words", "1 page").
            """

            response = model.generate_content([uploaded_file, prompt])

            # 5. Parse Result
            usage_meta = response.usage_metadata
            input_tok = usage_meta.prompt_token_count
            output_tok = usage_meta.candidates_token_count
            total_tok = usage_meta.total_token_count
            
            cost = calculate_cost(input_tok, output_tok, model_name)
            
            # Manual parsing since we used TypedDict for schema
            data = json.loads(response.text)
            questions_data = data.get("questions", [])
            questions = [Question(**q) for q in questions_data]

            latency = time.time() - start_time
            usage = UsageStats(
                input_tokens=input_tok,
                output_tokens=output_tok,
                total_tokens=total_tok,
                model_name=model_name,
                cost_usd=cost,
                latency_s=latency
            )
            
            return ExtractionResult(questions=questions, usage=usage)

        except Exception as e:
            print(f"Gemini processing error: {e}")
            latency = time.time() - start_time
            usage = UsageStats(
                input_tokens=input_tok,
                output_tokens=output_tok,
                total_tokens=total_tok,
                model_name=model_name,
                cost_usd=cost,
                latency_s=latency
            )
            # Try to print raw response text if available for debugging
            try:
                print(f"Raw response: {response.text}")
            except:
                pass
                
            return ExtractionResult(questions=[], usage=usage)
        finally:
            # Cleanup Gemini file
            try:
                genai.delete_file(uploaded_file.name)
                print(f"   [Vision] Deleted remote file {uploaded_file.name}")
            except Exception:
                pass
