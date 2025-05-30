"""
document_loaders/__init__.py

This module serves as the unified document ingestion entry point.
It supports multiple file types including PDF, DOCX, PPTX, XLSX, TXT, JSON, HTML, Markdown, CSV, and image OCR.

Output: All parsed content is returned as plain text string.
"""

import os
from config.path_conf import BASE_PATH
from algorithms.llm.document_loaders.loader.mypdfloader import RapidOCRPDFLoader
from algorithms.llm.document_loaders.loader.myimgloader import RapidOCRLoader
from algorithms.llm.document_loaders.loader.FilteredCSVloader import FilteredCSVLoader
from langchain_community.document_loaders import CSVLoader
from algorithms.llm.document_loaders.deepdoc.parser import (
    ExcelParser, DocxParser, PptParser, TxtParser,
    JsonParser, HtmlParser, MarkdownParser
)
from algorithms.llm.document_loaders.deepdoc.parser.markdown_parser2 import MarkdownDocument
from algorithms.llm.document_loaders.parser_utils import parse_pdf_with_mineru
import pandas as pd

output_dir = os.path.join(BASE_PATH, 'data', 'llm_file', 'mineru_output')

def file_parse(file_path: str) -> str:
    """
    Auto-detect file type and parse its content into a plain text string.
    """
    file_type = file_path.split('.')[-1].lower()

    if file_type == 'pdf':
        result = parse_pdf_with_mineru(file_path, output_dir=output_dir)

    elif file_type in ["docx", "doc"]:
        try:
            docx_parser = DocxParser()
            result = "\n".join(docx_parser(file_path))
        except:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

    elif file_type in ["pptx", "ppt"]:
        result = "\n".join(PptParser()(file_path))

    elif file_type in ['xls', 'xlsx']:
        result = "\n".join(ExcelParser()(file_path))

    elif file_type == 'md':
        result = MarkdownDocument(file_path=file_path).generate_document()

    elif file_type == 'txt':
        result = "\n".join([r[0] for r in TxtParser()(file_path)])

    elif file_type == 'json':
        result = "\n".join(JsonParser()(file_path, raw_text=True))

    elif file_type == 'html':
        result = "\n".join(HtmlParser()(file_path))

    elif file_type == 'csv':
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = [line.strip().split(',') for line in f if line.strip()]
            if not lines:
                return "Warning: File is empty"

            max_cols = max(len(line) for line in lines)
            df = pd.read_csv(file_path, header=None, names=range(max_cols), dtype=str)
            df_cleaned = df.dropna(how='all').dropna(axis=1, how='all')
            if df_cleaned.empty:
                return "Warning: No valid content"

            descriptions = []
            for _, row in df_cleaned.iterrows():
                filtered = [f"{col}: {val.strip()}" for col, val in row.items()
                            if str(val).strip() not in ['', 'None', 'nan']]
                if filtered:
                    descriptions.append(",".join(filtered))

            return "\n".join(descriptions)
        except:
            result = "\n".join(ExcelParser()(file_path))

    elif file_type in ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'tif']:
        docs = RapidOCRLoader(file_path).load()
        result = '\n'.join([doc.page_content for doc in docs])

    else:
        raise ValueError(f'Unsupported file type: {file_type}')

    return result
