import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_url_non(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_url_is_set(self):
        node = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node.url, "https://www.boot.dev")

if __name__ == "__main__":
    unittest.main()