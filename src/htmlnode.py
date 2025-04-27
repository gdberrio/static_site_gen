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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None) -> None:
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("all ParentNodes must have a tag")
        if self.children is None:
            raise ValueError("all ParentNodes must have children")
        html_doc = ""
        html_doc += f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_doc += f"{child.to_html()}"

        html_doc += f"</{self.tag}>"

        return html_doc
