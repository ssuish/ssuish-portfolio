import unittest
from block import (
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
    BlockType,
)
from htmlnode import HTMLNode


class TestBlock(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

    def test_block_to_block_type_all_block_types(self):
        block = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        self.assertEqual(block_to_block_type("# Heading level 1"), BlockType.HEADING)
        self.assertEqual(
            block_to_block_type("###### Heading level 6"), BlockType.HEADING
        )

        code_block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

        quote_block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

        mixed_quote_block = "> quote line 1\nnot a quote line"
        self.assertEqual(block_to_block_type(mixed_quote_block), BlockType.PARAGRAPH)

        ul_block = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(ul_block), BlockType.UNORDERED_LIST)

        mixed_ul_block = "- item 1\nnot a list item"
        self.assertEqual(block_to_block_type(mixed_ul_block), BlockType.PARAGRAPH)

        ol_block = "1. item 1\n2. item 2\n3. item 3"
        self.assertEqual(block_to_block_type(ol_block), BlockType.ORDERED_LIST)

        misnumbered_block = "1. item 1\n3. item 3"
        self.assertEqual(block_to_block_type(misnumbered_block), BlockType.PARAGRAPH)

    def test_codeblock(self):
        md = """
        ```
            This is text that _should_ remain
            the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraphs(self):
        md = """
            This is **bolded** paragraph
            text in a p
            tag here

            This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
