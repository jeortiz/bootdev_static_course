from htmlnode import HtmlNode


class ParentNode(HtmlNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('No tag specified.')
        if not self.children:
            raise ValueError('No children specified.')
        
        tag_open = f"<{self.tag}>"
        tag_close = f"</{self.tag}>"

        html = tag_open

        for child in self.children:
            html += child.to_html()

        html += tag_close

        return html