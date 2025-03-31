from textnode import TextNode, TextType


class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None and self.value:
            return self.value
        props = self.props_to_html()

        if self.value == None and self.children:
            children_html = ''
            for child in self.children:
                children_html += child.to_html()
                
            return f"<{self.tag}{' '+props if props else ''}>{children_html}</{self.tag}>"

        return f"<{self.tag}{' '+props if props else ''}>{self.value}</{self.tag}>"
    
    def props_to_html(self):
        if self.props is None:
            return ""
        html=""
        for key, value in self.props.items():
            html += f' {key}="{value}"'
        return html

    def __eq__(self, value):
        if self.tag == value.tag and self.value == value.value and self.children == value.children and self.props == value.props:
            return True
        return False

    def __repr__(self):
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {self.props})"
            
