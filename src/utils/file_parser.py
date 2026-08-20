import os
import PyPDF2
from typing import Optional

def parse_file(file_path: str) -> Optional[str]:
    """
    Parses a file and extracts its text content.
    Returns None if the file is an image or unsupported format.
    """
    if not os.path.exists(file_path):
        return None

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Images (handled separately by base64 encoding later)
    if ext in ['.png', '.jpg', '.jpeg', '.webp']:
        return None

    try:
        # PDF Parsing
        if ext == '.pdf':
            text = ""
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
            return text.strip()
        
        # Fallback for text/code files
        # We try utf-8, if fails, we try other encodings or return None
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                return f.read()
        except Exception:
            return None
    except Exception as e:
        print(f"Error parsing file {file_path}: {e}")
        return None
