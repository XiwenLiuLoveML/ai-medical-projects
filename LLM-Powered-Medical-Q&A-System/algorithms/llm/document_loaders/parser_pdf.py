"""
📍 Path: document_loaders/parser_pdf.py

📌 PDF Parser using MinerU + Markdown Pipeline

This function extracts clean text from PDF files using the `magic_pdf` library and a custom Markdown conversion pipeline. It supports both OCR-based and structured text extraction modes.

🔧 Pipeline:
1. Read PDF bytes
2. Detect parsing strategy (OCR or structured)
3. Use `doc_analyze()` to convert PDF to intermediate Markdown
4. Parse Markdown into final plain text for use in LLMs or Q&A systems

✅ Use Cases:
- Extracting clinical content from scanned forms or procedural PDFs
- Uploading PDF reports into medical knowledge base
- Removing manual effort in document reading

"""

import os
import tempfile
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset, SupportedPdfParseMethod
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from algorithms.llm.document_loaders.deepdoc.parser.markdown_parser2 import MarkdownDocument

def parse_pdf_with_mineru(pdf_file_path: str, output_dir: str = 'output') -> str:
    """Extract plain text from PDF using MinerU's Markdown pipeline

    Args:
        pdf_file_path: Path to the PDF file
        output_dir: Output directory (for temp files & images)

    Returns:
        Clean plain text extracted from the PDF content
    """
    local_image_dir = os.path.join(output_dir, 'images')
    os.makedirs(local_image_dir, exist_ok=True)

    image_writer = FileBasedDataWriter(local_image_dir)
    pdf_bytes = FileBasedDataReader('').read(pdf_file_path)

    with tempfile.NamedTemporaryFile(suffix='.md', delete=True) as temp_file:
        temp_path = temp_file.name
        md_writer = FileBasedDataWriter(os.path.dirname(temp_path))

        dataset = PymuDocDataset(pdf_bytes)
        if dataset.classify() == SupportedPdfParseMethod.OCR:
            dataset.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer).dump_md(
                md_writer, temp_path, os.path.basename(local_image_dir)
            )
        else:
            dataset.apply(doc_analyze, ocr=False).pipe_txt_mode(image_writer).dump_md(
                md_writer, temp_path, os.path.basename(local_image_dir)
            )

        md_parser = MarkdownDocument(file_path=temp_path)
        return md_parser.generate_document()
