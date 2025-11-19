import unittest
from inline_markdown import *

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_mardow_links(self):
        matches = extract_markdown_links(
            "this is a text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_mardow_links_with_an_image(self):
        matches = extract_markdown_links(
            "this text contains a link [to youtube](https://www.youtube.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com")], matches)

    def test_extract_mardow_images_with_a_link(self):
        matches = extract_markdown_images(
            "this text contains a link [to youtube](https://www.youtube.com) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_mardow_images_without_images(self):
        matches = extract_markdown_images(
            "this text contains a link [to youtube](https://www.youtube.com)"
        )
        self.assertListEqual([], matches)

    def test_extract_mardow_links_without_links(self):
        matches = extract_markdown_links(
            "this text contains an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_multiple_links(self):
        matches = extract_markdown_links(
            "This is a text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_extract_markdown_images_multiple_images(self):
        matches = extract_markdown_images(
            "This is a text with ![image](https://i.imgur.com/zjjcJKZ.png) and ![another image](https://i.imgur.com/drEHMuN.jpeg)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another image", "https://i.imgur.com/drEHMuN.jpeg"),
            ],
            matches,
        )


    def test_split_images(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is a text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev")
            ],
            new_nodes,
        )

    def test_split_images_without_images(self):
        node = TextNode(
            "This is a text",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_links_without_links(self):
        node = TextNode(
            "This is a text",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_link(self):
        node = TextNode(
            "This is a text with a [link](https://boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a [link](https://boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_image(self):
        node = TextNode(
             "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode( "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_with_image_and_link(self):
        node = TextNode(
            "This is a text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://blog.boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://blog.boot.dev)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links_with_image_and_link(self):
        node = TextNode(
            "This is a text with a [link](https://boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )



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

    def test_markdown_to_blocks_one_paragraph(self):
        md = """
This is a paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

    def test_markdown_to_blocks_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )


    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph \nThis is the same paragraph on a new line"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_heading(self):
        block = "### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.HEADING,
        )
    
    def test_block_to_block_type_not_heading(self):
        block = "###########This is not a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_type_multiple_line_heading(self):
        block = "### This is not a heading\nThis is the same paragraph on a new line"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_code(self):
        block = "```This is a code block\nThis is the same code block on a new line\nThis is the end of the code \n```"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.CODE,
        )

    def test_block_to_block_code_missing_backticks(self):
        block = "``` This is not a code block\nThis is the same none code block on a new line\nThis is the end of this none code block"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_quote(self):
        block = ">This is a quote block\n>This is the same quote block on a new line\n>This is the end of the quote block"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.QUOTE,
        )

    def test_block_to_block_not_quote(self):
        block = ">This is not a quote block\n>This is the same none quote block on a new line\nThis is the end of the none quote block"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_unordered_list(self):
        block = "- This is a unordered list block\n- This is the same unordered list block on a new line\n- This is the end of the unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.UNORDERED_LIST,
        )

    def test_block_to_block_not_unordered_list(self):
        block = "- This is a unordered list block\n-This is the same unordered list block on a new line\nThis is the end of the unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
        )

    def test_block_to_block_ordered_list(self):
        block = "1. This is a unordered list block\n2. This is the same unordered list block on a new line\n3. This is the end of the unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.ORDERED_LIST,
        )

    def test_block_to_block_not_ordered_list(self):
        block = "1. This is a unordered list block\n600. This is the same unordered list block on a new line\n3. This is the end of the unordered list"
        block_type = block_to_block_type(block)
        self.assertEqual(
            block_type,
            BlockType.PARAGRAPH,
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

    def test_heading(self):
        md = "### This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h3>This is a heading</h3></div>",
        )

    def test_ordered_list(self):
        md = """
1. This is an ordered list
2. another item
3. another item
4. another item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>This is an ordered list</li><li>another item</li><li>another item</li><li>another item</li></ol></div>",
        )

    
    def test_unordered_list(self):
        md = """
- This is an unordered list
- another item
- another item
- another item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>This is an unordered list</li><li>another item</li><li>another item</li><li>another item</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
>This is a quote
>another line
>another line
>another line
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>This is a quote another line another line another line</blockquote></div>",
        )
    
    
    


if __name__ == "__main__":
    unittest.main()
