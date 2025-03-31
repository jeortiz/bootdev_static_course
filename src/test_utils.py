import unittest

from block_markdown import BlockType
from htmlnode import HtmlNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from utils.utils import block_to_block_type, block_to_node, extract_markdown_images, extract_markdown_links, extract_title, get_heading_tag, get_paragraph_html, heading_type_block_to_html_node, markdown_to_blocks, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_node_to_html_node, text_to_textnodes


class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, '')
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is text")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is code")
    
    def test_link(self):
        node = TextNode(None, TextType.LINK, 'https://www.boot.dev/')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.props['href'], node.url)
    
    def test_image(self):
        node = TextNode(None, TextType.IMAGE, 'https://www.boot.dev/img/bootdev-logo-full-small.webp')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.props['src'], node.url)

    def test_split_delimeter_not_text(self):
        node = TextNode("Test", TextType.IMAGE,'https://www.boot.dev/img/bootdev-logo-full-small.webp' )
        expected = [node]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, expected)

    def test_split_delimeter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(new_nodes, expected)
    
    def test_split_delimeter_bold(self):
        node = TextNode("This is text with a **bold statement**", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold statement", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(new_nodes, expected)

    def test_split_delimeter_list(self):
        nodeText = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodeImg = TextNode("Test", TextType.IMAGE,'https://www.boot.dev/img/bootdev-logo-full-small.webp' )
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            nodeImg
        ]
        new_nodes = split_nodes_delimiter([nodeText, nodeImg], "`", TextType.CODE)

        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image2](https://i.imgur.com/zjjcJKY.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKY.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
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
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_with_img(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an image ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an image ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        node = text_to_textnodes(text)
        
        self.assertEqual(
            node,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_textnode_no_nodes(self):
        text = "This is a regular, ol' texty text!!! Right?"
        node = text_to_textnodes(text)
        
        self.assertEqual(
            node,
            [TextNode("This is a regular, ol' texty text!!! Right?", TextType.TEXT)]
        )
    
    def test_text_to_textnode_empty(self):
        text = ""
        node = text_to_textnodes(text)
        
        self.assertEqual(node, [])

    def test_text_to_textnode_empty(self):
        text = None
        node = text_to_textnodes(text)
        
        self.assertEqual(node, [])

    def test_text_to_textnode_not_string(self):
        with self.assertRaises(ValueError):
             text_to_textnodes(2)

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

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,[])
    
    def test_markdown_to_blocks_non_str(self):
        md = 5
        with self.assertRaises(ValueError):
             markdown_to_blocks(md)

    def test_block_to_block_type_paragraph(self):
        block = "Hi all, this is a normal paragraph.\nWith a line change!"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is\n2. A list\n3. For sure"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_type_ordered_list_not(self):
        block = "1. This is not\n3. A continuos list\n7. For sure"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is\n- An unordered list\n- For sure"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_type_unordered_quote(self):
        block = ">This is a quote\n>For sure"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_code(self):
        block = "```This is code\nand more code```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_heading(self):
        block_h2 = "## This is an H2"
        block_type = block_to_block_type(block_h2)
        self.assertEqual(block_type, BlockType.HEADING)

        block_h1 = "# This is an H1"
        block_type = block_to_block_type(block_h1)
        self.assertEqual(block_type, BlockType.HEADING)

        block_h6 = "###### This is an H6"
        block_type = block_to_block_type(block_h6)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_wrong_heading(self):
        block_not_h2 = "##This is not an H2"
        block_type = block_to_block_type(block_not_h2)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

        block_not_heading = "############ This is not an heading"
        block_type = block_to_block_type(block_not_heading)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_get_heading_tag(self):
        pre = "## "
        tag = get_heading_tag(pre)
        self.assertEqual(tag, 'h2')

        pre = "#### "
        tag = get_heading_tag(pre)
        self.assertEqual(tag, 'h4')

        pre = "# "
        tag = get_heading_tag(pre)
        self.assertEqual(tag, 'h1')

    def test_heading_type_block_to_html_node(self):
        block = "###### This is an H6"
        node = heading_type_block_to_html_node(block)
        self.assertEqual(node, HtmlNode('h6', 'This is an H6'))

    def test_get_paragraph_html(self):
        text = "This is another paragraph with _italic_ text and `code` here\nThis is a paragraph on a new line"
        html = get_paragraph_html(text).to_html()
        
        self.assertEqual(html,'<div>This is another paragraph with <i>italic</i> text and <code>code</code> here\nThis is a paragraph on a new line</div>')

    def test_block_to_node_quote(self):
        block = ">This is a quote.\n>\n>This is still quote."
        node = block_to_node(block, BlockType.QUOTE)
        self.assertEqual(node.to_html(), "<div><blockquote>This is a quote.\n\nThis is still quote.</blockquote></div>")

    def test_block_to_node_ul(self):
        block = "- This is a list.\n- This is still list."
        node = block_to_node(block, BlockType.UNORDERED_LIST).to_html()
        self.assertEqual(node, "<div><ul><li>This is a list.</li><li>This is still list.</li></ul></div>")

    def test_block_to_node_ol(self):
        block = "1. This is a list.\n2. This is still list."
        node = block_to_node(block, BlockType.ORDERED_LIST)
        self.assertEqual(node.to_html(), "<div><ol><li>This is a list.</li><li>This is still list.</li></ol></div>")

    def test_extract_title(self):
        markdown = "# Hello!"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello!")

        markdown = "# Hello!\n This is Markdown\nlol"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello!")

    def test_extract_title(self):
        markdown = " Hello! This is Markdown\nlol"
        with self.assertRaises(Exception):
            extract_title(markdown)

        markdown = "# \n Hello! This is Markdown\nlol"
        with self.assertRaises(Exception):
            extract_title(markdown)