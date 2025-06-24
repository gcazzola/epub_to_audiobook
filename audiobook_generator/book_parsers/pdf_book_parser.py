import logging
import re
from typing import List, Tuple

import fitz  # PyMuPDF

from audiobook_generator.book_parsers.base_book_parser import BaseBookParser
from audiobook_generator.config.general_config import GeneralConfig

logger = logging.getLogger(__name__)


class PdfBookParser(BaseBookParser):
    def __init__(self, config: GeneralConfig):
        super().__init__(config)
        self.doc = fitz.open(self.config.input_file)

    def __str__(self) -> str:
        return super().__str__()

    def validate_config(self):
        if self.config.input_file is None:
            raise ValueError("PDF Parser: Input file cannot be empty")
        if not self.config.input_file.endswith(".pdf"):
            raise ValueError(f"PDF Parser: Unsupported file format: {self.config.input_file}")

    def get_book(self):
        return self.doc

    def get_book_title(self) -> str:
        title = self.doc.metadata.get("title")
        if title:
            return title
        return "Untitled"

    def get_book_author(self) -> str:
        author = self.doc.metadata.get("author")
        if author:
            return author
        return "Unknown"

    def get_chapters(self, break_string) -> List[Tuple[str, str]]:
        text = ""
        for page in self.doc:
            text += page.get_text()
            text += "\n"

        # Normalize whitespaces similar to EPUB parser
        if self.config.newline_mode == "single":
            cleaned_text = re.sub(r"[\n]+", break_string, text.strip())
        elif self.config.newline_mode == "double":
            cleaned_text = re.sub(r"[\n]{2,}", break_string, text.strip())
        elif self.config.newline_mode == "none":
            cleaned_text = re.sub(r"[\n]+", " ", text.strip())
        else:
            raise ValueError(f"Invalid newline mode: {self.config.newline_mode}")

        cleaned_text = re.sub(r"\s+", " ", cleaned_text)

        if self.config.remove_endnotes:
            cleaned_text = re.sub(r'(?<=[a-zA-Z.,!?;”")])\d+', "", cleaned_text)

        if self.config.remove_reference_numbers:
            cleaned_text = re.sub(r'\[\d+(\.\d+)?\]', '', cleaned_text)

        search_and_replaces = self.get_search_and_replaces()
        for sr in search_and_replaces:
            cleaned_text = re.sub(sr['search'], sr['replace'], cleaned_text)

        # Single chapter titled "Document"
        return [("Document", cleaned_text)]

    def get_search_and_replaces(self):
        search_and_replaces = []
        if self.config.search_and_replace_file:
            with open(self.config.search_and_replace_file) as fp:
                for line in fp.readlines():
                    if '==' in line and not line.startswith('==') and not line.endswith('==') and not line.startswith('#'):
                        search_and_replaces.append({'search': r"{}".format(line.split('==')[0]),
                                                   'replace': r"{}".format(line.split('==')[1][:-1])})
        return search_and_replaces
