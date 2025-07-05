from blocktype import BlockType
from convert_block import block_to_block_type, markdown_to_blocks

import unittest

class TestConvertBlock(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_heading(self):
        self.assertEqual(block_to_block_type("# Header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Header"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Header"), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type("A heade#r"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(block_to_block_type("``` int main(); ```"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("`` int main(); ``"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(" int main(); ```"), BlockType.CODE)
        self.assertNotEqual(block_to_block_type("``` int main();"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        self.assertEqual(block_to_block_type("> A quote"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("A quote"), BlockType.QUOTE)
        self.assertNotEqual(block_to_block_type("A > quote"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type("- list 1"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("no - list"), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type("-notquite"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type("1. A list item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is an `ordered` list\n2. with items\n3. and more items"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("1.Not"), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type("Item 1. on the agenda"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(block_to_block_type("A paragraph of text here"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("1.Not"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("Item 1. on the agenda"), BlockType.PARAGRAPH)