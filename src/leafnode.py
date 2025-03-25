from htmlnode import HtmlNode


class LeafNode(HtmlNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError()
        
        tag_open = f"<{self.tag}>" if self.tag else ''
        tag_close = f"</{self.tag}>" if self.tag else ''

        return f'{tag_open}{self.value}{tag_close}'