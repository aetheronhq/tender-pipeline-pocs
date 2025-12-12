"""
Quick smoke test:
- Upload the largest tender file(s)
- Ensure they become ACTIVE within timeout
Usage:
  python run_smoke_test_upload.py tenders/big/RFT_Main.pdf [tenders/big/Technical_Specs.pdf ...]
"""

import sys
from shared_utils import get_gemini_client, upload_document, upload_documents


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_smoke_test_upload.py <pdf1> [pdf2 ...]")
        sys.exit(1)

    paths = sys.argv[1:]
    client = get_gemini_client()

    if len(paths) == 1:
        file = upload_document(client, paths[0])
        if file:
            print("✅ Single-file upload ACTIVE")
        else:
            print("❌ Upload failed or timed out")
    else:
        files = upload_documents(client, paths)
        if files:
            print("✅ Multi-file upload ACTIVE for all files")
        else:
            print("❌ Upload failed or timed out for one or more files")


if __name__ == "__main__":
    main()


