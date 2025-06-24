import unittest

from audiobook_generator.book_parsers.base_book_parser import get_book_parser
from audiobook_generator.book_parsers.pdf_book_parser import PdfBookParser
from tests.test_utils import get_pdf_config


class TestPdfBookParser(unittest.TestCase):
    def test_get_pdf_book_parser(self):
        config = get_pdf_config()
        parser = get_book_parser(config)
        self.assertIsInstance(parser, PdfBookParser)
        self.assertEqual(len(parser.get_chapters("   ")), 1)


if __name__ == '__main__':
    unittest.main()
