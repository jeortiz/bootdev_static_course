import unittest

from textnode import TextNode, TextType
from utils.utils import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
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