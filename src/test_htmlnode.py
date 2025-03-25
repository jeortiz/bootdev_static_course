import unittest
from htmlnode import HtmlNode

class TestHtmlNode(unittest.TestCase):
    def test_eq(self):
        node = HtmlNode('<p>','Hi again')
        node2 = HtmlNode('<p>','Hi again')
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HtmlNode('<p>','Hi again', props={'id': 'unique', 'class': 'red,big'})
        html = node.props_to_html()
        expected = ' id="unique" class="red,big"'
        self.assertEqual(html, expected)

    def test_children_is_none(self):
        node = HtmlNode('<p>','Hi again', props={'id': 'unique', 'class': 'red,big'})
        self.assertIsNone(node.children)
