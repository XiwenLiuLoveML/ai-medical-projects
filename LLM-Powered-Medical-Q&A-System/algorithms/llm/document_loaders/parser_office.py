"""
📍 Path: document_loaders/parser_office.py

📌 Office File Parser using MinerU (Word / PPT)

This module processes MS Office documents using the MinerU parsing engine.  
It extracts clean text content from `.doc`, `.docx`, `.ppt`, `.pptx` files through a Markdown pipeline.

🔧 Pipeline:
1. Read file via `read_local_office()`
2. Detect parsing strategy: OCR or text mode
3. Extract content using `doc_analyze()`
4. Convert to Markdown and parse it into plain text

✅ Use Cases:
- Ingesting clinical notes in Word format
- Processing educational slides for medical knowledge base
- Extracting text from scanned or structured .doc/.ppt files
"""

import os
import tempfile
from magic_pdf.data.data_reader_writer import FileBasedDataWriter
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.data.read_api import read_local_office
from magic_pdf.config.enums import SupportedPdfParseMethod
from algorithms.llm.document_loaders.deepdoc.parser.markdown_parser2 import MarkdownDocument

def parse_office_with_mineru(input_file: str, output_dir: str = 'output'):
    """Extract plain text from MS Word / PowerPoint using MinerU Markdown pipeline

    Args:
        input_file: Path to the Office file (.doc/.docx/.ppt/.pptx)
        output_dir: Output directory for images and markdown

    Returns:
        Extracted plain text content
    """
    local_image_dir = os.path.join(output_dir, 'images')
    os.makedirs(local_image_dir, exist_ok=True)
    image_writer = FileBasedDataWriter(local_image_dir)

    with tempfile.NamedTemporaryFile(suffix='.md', delete=True) as temp_file:
        temp_path = temp_file.name
        md_writer = FileBasedDataWriter(os.path.dirname(temp_path))

        dataset = read_local_office(input_file)[0]
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
