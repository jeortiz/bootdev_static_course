import re
from block_markdown import BlockType
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
            
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        img_alt, img_url = images[0]

        segments = node.text.split(f"![{img_alt}]({img_url})", 1)
        
        split_nodes = []

        if segments[0] != '':
            split_nodes.append(TextNode(segments[0], TextType.TEXT))

        split_nodes.append(TextNode(img_alt, TextType.IMAGE, img_url))

        if segments[1] != '':
            split_nodes.append(TextNode(segments[1], TextType.TEXT))
        
        new_nodes.extend(split_nodes_image(split_nodes))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        link_text, link_url = links[0]

        segments = node.text.split(f"[{link_text}]({link_url})", 1)
        
        split_nodes = []

        if segments[0] != '':
            split_nodes.append(TextNode(segments[0], TextType.TEXT))

        split_nodes.append(TextNode(link_text, TextType.LINK, link_url))

        if segments[1] != '':
            split_nodes.append(TextNode(segments[1], TextType.TEXT))
        
        new_nodes.extend(split_nodes_link(split_nodes))

    return new_nodes

def text_to_textnodes(text):
    nodes = []
    if not text:
        return nodes
    
    if not isinstance(text, str):
        raise ValueError('text is not a string')
    
    text_node = TextNode(text,TextType.TEXT)
    
    nodes = split_nodes_delimiter([text_node], '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown: str):
    if not markdown:
        return []
    
    if not isinstance(markdown, str):
        raise ValueError('text is not a string')
    
    blocks = markdown.split('\n\n')
    blocks = map(lambda s: s.strip(), blocks)
    blocks = filter(lambda s: s != '', blocks)

    return list(blocks)

def check_every_line_start_with(lines: list[str], pattern):
    for line in lines:
        if not line.startswith(pattern):
            return False
    return True

def check_ordered_list_block(lines: list[str]):
    for n in range(len(lines)):
        if not lines[n].startswith(f'{n+1}. '):
            return False
    return True

def block_to_block_type(block: str):

    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("``") and block.endswith("```"):
        return BlockType.CODE
    if check_every_line_start_with(block.split('\n'), '>'):
        return BlockType.QUOTE
    if check_every_line_start_with(block.split('\n'), '- '):
        return BlockType.UNORDERED_LIST
    if check_ordered_list_block(block.split('\n')):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    
    