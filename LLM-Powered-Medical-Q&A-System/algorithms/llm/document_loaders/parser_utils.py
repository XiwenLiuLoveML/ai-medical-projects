"""
parser_utils.py

This module provides a PDF parsing utility using the MagicPDF (MinerU) framework.
It converts PDF files into structured Markdown, then parses the markdown content into plain text.

Used in: document_loaders/__init__.py for PDF parsing fallback
"""

import os
import tempfile
from magic_pdf.data.data_reader_writer import FileBasedDataWriter, FileBasedDataReader
from magic_pdf.data.dataset import PymuDocDataset
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from magic_pdf.data.dataset import SupportedPdfParseMethod
from algorithms.llm.document_loaders.deepdoc.parser.markdown_parser2 import MarkdownDocument

def parse_pdf_with_mineru(pdf_file_path: str, output_dir: str = 'output'):
    """
    Parse a PDF file using MagicPDF framework and extract structured content.

    Args:
        pdf_file_path (str): Path to the input PDF file.
        output_dir (str): Directory to store temporary markdown and images.

    Returns:
        str: Parsed document content in plain text.
    """

    # Prepare temporary image output directory
    local_image_dir = os.path.join(output_dir, 'images')
    os.makedirs(local_image_dir, exist_ok=True)
    image_writer = FileBasedDataWriter(local_image_dir)

    # Read the PDF as bytes
    pdf_bytes = FileBasedDataReader('').read(pdf_file_path)

    # Use temp markdown file for intermediate output
    with tempfile.NamedTemporaryFile(suffix='.md', delete=True) as temp_file:
        temp_path = temp_file.name
        md_writer = FileBasedDataWriter(os.path.dirname(temp_path))

        # Load dataset and choose parsing mode (OCR vs. text)
        ds = PymuDocDataset(pdf_bytes)
        if ds.classify() == SupportedPdfParseMethod.OCR:
            ds.apply(doc_analyze, ocr=True).pipe_ocr_mode(image_writer).dump_md(
                md_writer, temp_path, os.path.basename(local_image_dir)
            )
        else:
            ds.apply(doc_analyze, ocr=False).pipe_txt_mode(image_writer).dump_md(
                md_writer, temp_path, os.path.basename(local_image_dir)
            )

        # Parse the markdown to plain text
        md_parser = MarkdownDocument(file_path=temp_path)
        return md_parser.generate_document()
