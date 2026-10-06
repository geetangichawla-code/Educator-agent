import io
from pypdf import PdfReader
from docx import Document

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt"}


def extension_of(filename: str) -> str:
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def extract_text(filename: str, data: bytes) -> str:
    """Return the plain text of an uploaded file. Works from memory, nothing is saved to disk."""
    ext = extension_of(filename)

    if ext == "pdf":
        reader = PdfReader(io.BytesIO(data))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages).strip()

    if ext == "docx":
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs).strip()

    if ext == "txt":
        return data.decode("utf-8", errors="ignore").strip()

    raise ValueError("Unsupported file type")