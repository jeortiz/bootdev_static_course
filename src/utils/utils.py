from htmlnode import HtmlNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
        if not text_node:
            raise ValueError('No text node given.')
        
        match text_node.text_type:
            case TextType.TEXT:
                return HtmlNode(value=text_node.text)
            case TextType.BOLD:
                return HtmlNode('b', value=text_node.text)
            case TextType.ITALIC:
                return HtmlNode('i', value=text_node.text)
            case TextType.CODE:
                return HtmlNode('code', value=text_node.text)
            case TextType.LINK:
                return HtmlNode('a', value=text_node.text, props={'href': text_node.url})
            case TextType.IMAGE:
                return HtmlNode('img', props={'src': text_node.url, 'alt': text_node.url})
            case _:
                raise ValueError('Not a known text type format.')