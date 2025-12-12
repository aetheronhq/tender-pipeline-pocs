"""
Shared utilities for the Pain Points POC.

Includes:
- Gemini client initialization
- File upload helpers (single + multi-doc) with ACTIVE polling
"""

import os
import time
from typing import List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env file
load_dotenv()


def get_gemini_client():
    """Initialize Gemini client from GEMINI_API_KEY in environment."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set in environment")
    return genai.Client(api_key=api_key)


def wait_for_active(client, file, max_wait: int = 120) -> Optional[types.File]:
    """
    Poll Gemini Files until the file becomes ACTIVE or times out.
    Logs state transitions; returns None on failure/timeout.
    """
    start = time.time()
    while time.time() - start < max_wait:
        status = client.files.get(name=file.name)
        state = status.state.name
        print(f"  File {file.name}: {state}")

        if state == "ACTIVE":
            print(f"  ✓ File ready in {time.time() - start:.1f}s")
            return status

        if state == "FAILED":
            print(f"  ❌ File upload FAILED: {file.name}")
            return None

        time.sleep(2)

    print(f"  ⚠️ File upload TIMEOUT after {max_wait}s: {file.name}")
    return None


def upload_document(client, path: str, max_wait: int = 120) -> Optional[types.File]:
    """Upload a single document and wait for ACTIVE."""
    print(f"Uploading {path} ...")
    # google-genai expects a keyword arg `file` for upload
    file = client.files.upload(file=path)
    return wait_for_active(client, file, max_wait=max_wait)


def upload_documents(client, paths: List[str], max_wait: int = 120) -> Optional[List[types.File]]:
    """Upload multiple documents (for multi-doc tenders)."""
    uploaded = []
    for p in paths:
        f = upload_document(client, p, max_wait=max_wait)
        if f is None:
            print(f"  ⚠️ Skipping tender due to upload failure: {p}")
            return None
        uploaded.append(f)
    print(f"  ✓ All {len(uploaded)} files ready")
    return uploaded


def build_contents(prompt: str, files: List[types.File]):
    """
    Build contents list for generate_content with prompt + all files.
    """
    return [prompt] + files


