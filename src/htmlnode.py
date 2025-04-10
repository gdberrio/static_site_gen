class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        html_doc = ""
        for prop in self.props:
            html_doc += f' {prop}="{self.props[prop]}"'
        return html_doc

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None) -> None:
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("all leafNodes must have a value")
        if self.tag is None:
            return self.value
        html_doc = ""
        html_doc += f"<{self.tag}{self.props_to_html()}>"
        html_doc += self.value
        html_doc += f"</{self.tag}>"
        return html_doc
