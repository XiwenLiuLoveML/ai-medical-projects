
# 📄 Document Loaders for Multi-format Medical File Parsing

This module provides a unified interface for parsing documents of various formats into clean plain text, ready for AI processing such as:

- Knowledge base construction
- Document question answering (RAG)
- Patient data ingestion and summarization

---

## ✅ Supported File Formats

| File Type     | Description                           |
|---------------|---------------------------------------|
| `.pdf`        | Extracted using `mineru` or OCR       |
| `.docx`/`.doc`| Extracted using `python-docx` or fallback to `mineru` |
| `.pptx`/`.ppt`| Slide content flattened to text       |
| `.xlsx`/`.xls`| Excel rows transformed to readable text |
| `.csv`        | Cleaned and converted into row-level descriptions |
| `.md`         | Parsed into text + table segments     |
| `.txt`        | Basic text files                      |
| `.json`       | Flattened into key-value format       |
| `.html`       | Body text and tags stripped out       |
| `.png`/`.jpg`/`.tiff` | OCR-based image-to-text extraction |

---

## 🏥 Use Cases in Healthcare

- Upload **lab reports**, **referral letters**, or **EHR exports** for summarization
- Pre-process **discharge forms** or **TAVI procedure notes** into a searchable knowledge base
- Extract clinical content from **scanned documents or screenshots**

---

## 🚀 How It Works

```python
from document_loaders import file_parse

text = file_parse("/path/to/uploaded_file.pdf")
# Pass `text` to your LLM pipeline
```

The `file_parse()` function:
- Automatically detects file type
- Uses the appropriate parser or OCR engine
- Returns a plain string containing readable content

---

## 📁 File Structure

```
document_loaders/
├── __init__.py          ← Unified `file_parse()` entrypoint
├── loader/              ← Custom OCR and CSV loaders
├── deepdoc/parser/      ← Parsers for DOCX, PPTX, Excel, HTML, etc.
├── parser_pdf.py        ← PDF parser using `mineru`
├── parser_office.py     ← Office file parser fallback via `mineru`
```

---

Let your AI system understand medical documents without manual formatting.  
**One line input, universal understanding.**
