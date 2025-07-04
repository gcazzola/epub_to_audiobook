from typing import List, Tuple

from audiobook_generator.config.general_config import GeneralConfig

EPUB = "epub"
PDF = "pdf"


class BaseBookParser:  # Base interface for books parsers
    # Base Book Parser interface
    def __init__(self, config: GeneralConfig):
        self.config = config
        self.validate_config()

    def __str__(self) -> str:
        return f"{self.config}"

    def validate_config(self):
        raise NotImplementedError

    def get_book(self):
        raise NotImplementedError

    def get_book_title(self) -> str:
        raise NotImplementedError

    def get_book_author(self) -> str:
        raise NotImplementedError

    def get_chapters(self, break_string) -> List[Tuple[str, str]]:
        raise NotImplementedError


# Common support methods for all book parsers

def get_supported_book_parsers() -> List[str]:
    return [EPUB, PDF]


def get_book_parser(config) -> BaseBookParser:
    if config.input_file.endswith(EPUB):
        from audiobook_generator.book_parsers.epub_book_parser import EpubBookParser
        return EpubBookParser(config)
    elif config.input_file.endswith(PDF):
        from audiobook_generator.book_parsers.pdf_book_parser import PdfBookParser
        return PdfBookParser(config)
    # elif <- new book parser goes here
    else:
        raise NotImplementedError(f"Unsupported file format: {config.input_file}")
