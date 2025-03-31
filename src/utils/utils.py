from functools import reduce
import os
import re
import shutil
from block_markdown import BlockType
from htmlnode import HtmlNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
        if not text_node:
            raise ValueError('No text node given.')
        
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode('',value=text_node.text)
            case TextType.BOLD:
                return LeafNode('b', value=text_node.text)
            case TextType.ITALIC:
                return LeafNode('i', value=text_node.text)
            case TextType.CODE:
                return LeafNode('code', value=text_node.text)
            case TextType.LINK:
                return LeafNode('a', value=text_node.text, props={'href': text_node.url})
            case TextType.IMAGE:
                return LeafNode('img', value='', props={'src': text_node.url, 'alt': text_node.url})
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
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if check_every_line_start_with(block.split('\n'), '>'):
        return BlockType.QUOTE
    if check_every_line_start_with(block.split('\n'), '- '):
        return BlockType.UNORDERED_LIST
    if check_ordered_list_block(block.split('\n')):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

def handle_block_by_type(block):
    match(block_to_block_type(block)):
        case BlockType.HEADING:
            return 
        
def get_heading_tag(matched_markdown_pre):
    num = reduce(lambda a, c: a+1 if c=="#" else a, matched_markdown_pre, 0)
    return f"h{num}"
    
def heading_type_block_to_html_node(block):
    matched = re.findall(r"(^#{1,6} )", block)
    heading_tag = get_heading_tag(matched[0])
    stripped = block.replace(matched[0], '')

    return LeafNode(heading_tag, stripped)

def get_paragraph_html(text):
    nodes = text_to_textnodes(text)
    html_nodes = map(text_node_to_html_node, nodes)

    return ParentNode('p', children=html_nodes)

def block_to_node(block: str, block_type: BlockType):
    match(block_type):
        case BlockType.PARAGRAPH:
            return get_paragraph_html(block)
        case BlockType.HEADING:
            return heading_type_block_to_html_node(block)
        case BlockType.CODE:
            return LeafNode('code', block.strip('`'))
        case BlockType.QUOTE:
            return LeafNode('blockquote', re.sub(r"^>", '', block, flags=re.MULTILINE))
        case BlockType.UNORDERED_LIST:
            stripped_block = re.sub(r"^- ", '', block, flags=re.MULTILINE)
            children = map(lambda ln: LeafNode('li',ln), stripped_block.split('\n'))
            return ParentNode('ul', children)
        case BlockType.ORDERED_LIST:
            stripped_block = re.sub(r"^\d\. ", '', block, flags=re.MULTILINE)
            children = map(lambda ln: LeafNode('li',ln), stripped_block.split('\n'))
            return ParentNode('ol', children)
        case _:
            raise Exception('Unknown type')
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    nodes = map(handle_block_by_type, blocks)

    return ParentNode('div',list(nodes))

def publish_static_files():
    static_folder = '../static'
    public_folder = '../public'

    try:
        if os.path.isdir(public_folder):
            shutil.rmtree(public_folder)
            os.mkdir(public_folder)
            copy_dir_files(static_folder, public_folder)

    except OSError as e:
        print(f"Failed - error: {e}")
    
    return

def copy_dir_files(src, dest):
    files = os.listdir(src)

    for f in files:
        f_path = os.path.join(src,f)

        if os.path.isfile(f_path):
            shutil.copy(f_path, dest)
        elif os.path.isdir(f_path):
            dest_dir = os.path.join(dest,f)
            os.mkdir(dest_dir)
            copy_dir_files(f_path, dest_dir)
    
    return

def extract_title(markdown):
    title_matches = re.findall(r"^#{1} (.+)", markdown)

    if len(title_matches) == 0 or title_matches[0] == '':
        raise Exception("No title specified!")
    
    return title_matches[0].strip()
    
