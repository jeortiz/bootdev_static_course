
import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_a_to_html_(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_to_html__no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")