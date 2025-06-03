"""
📍 Path: backend/algorithms/llm/document_loaders/__init__.py

📌 Unified File Parser for Multi-format Uploads

This module provides a single entrypoint `file_parse(file_path)` that extracts text content from various document types. Useful for building clinical knowledge bases or extracting structured information from uploaded medical records.

Supported formats:
- PDF (via OCR or structured parsing)
- Word (.docx)
- Excel (.xls/.xlsx)
- PowerPoint (.pptx)
- Markdown / TXT / HTML / JSON
- CSV (row-based description)
- Image files (.png, .jpg, .tiff) via OCR
"""

import os
import pandas as pd

from algorithms.llm.document_loaders.loader.mypdfloader import RapidOCRPDFLoader
from algorithms.llm.document_loaders.loader.myimgloader import RapidOCRLoader
from algorithms.llm.document_loaders.loader.FilteredCSVloader import FilteredCSVLoader
from algorithms.llm.document_loaders.deepdoc.parser import (
    ExcelParser, DocxParser, PptParser, TxtParser,
    JsonParser, HtmlParser, MarkdownParser
)
from algorithms.llm.document_loaders.deepdoc.parser.markdown_parser2 import MarkdownDocument
from backend.algorithms.llm.document_loaders.parser_pdf import parse_pdf_with_mineru
from algorithms.llm.document_loaders.parser_office import parse_office_with_mineru


def file_parse(file_path: str) -> str:
    """Parse the given file into plain text for AI processing"""
    file_type = file_path.split('.')[-1].lower()

    if file_type == 'pdf':
        return parse_pdf_with_mineru(file_path)

    elif file_type in ['docx', 'doc']:
        try:
            parser = DocxParser()
            return '\n'.join(parser(file_path))
        except Exception:
            return parse_office_with_mineru(file_path)

    elif file_type in ['pptx', 'ppt']:
        parser = PptParser()
        return '\n'.join(parser(file_path))

    elif file_type in ['xls', 'xlsx']:
        parser = ExcelParser()
        return '\n'.join(parser(file_path))

    elif file_type == 'md':
        parser = MarkdownDocument(file_path=file_path)
        return parser.generate_document()

    elif file_type == 'txt':
        parser = TxtParser()
        return '\n'.join([res[0] for res in parser(file_path)])

    elif file_type == 'json':
        parser = JsonParser()
        return '\n'.join(parser(file_path, raw_text=True))

    elif file_type == 'html':
        parser = HtmlParser()
        return '\n'.join(parser(file_path))

    elif file_type == 'csv':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip().split(',') for line in f if line.strip()]
            if not lines:
                return 'Warning: empty file'

            max_cols = max(len(line) for line in lines)
            df = pd.read_csv(file_path, header=None, dtype=str, names=range(max_cols))
            df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
            if df_cleaned.empty:
                return 'Warning: no valid data'

            descriptions = []
            for _, row in df_cleaned.iterrows():
                desc = [f'{col}: {str(val).strip()}' for col, val in row.items() if str(val).strip() not in ['', 'None', 'nan']]
                if desc:
                    descriptions.append(', '.join(desc))
            return '\n'.join(descriptions)

        except Exception:
            parser = ExcelParser()
            return '\n'.join(parser(file_path))

    elif file_type in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif']:
        loader = RapidOCRLoader(file_path=file_path)
        docs = loader.load()
        return '\n'.join([doc.page_content for doc in docs])

    else:
        raise ValueError(f'Unsupported file type: {file_type}')
