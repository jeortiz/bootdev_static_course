import sys
from htmlnode import HtmlNode
from textnode import TextNode, TextType

def main() -> int:
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(node)

    return 0

if __name__ == '__main__':
    sys.exit(main()) 
