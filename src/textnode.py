from enum import Enum

class TextType(Enum):
    TEXT = "text"
    ITALIC = "italic"
    BOLD = "bold"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextDelimeter(Enum):
    ITALIC = "_"
    BOLD = "**"
    CODE = "`"

class TextNode():
    def __init__(self, text, text_type: TextType, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        if self.text == value.text and self.text_type == value.text_type and self.url == value.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"