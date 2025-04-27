import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            tag="<a>",
            value="test",
            children=["a", "b"],
            props={"href": "https://www.google.com"},
        )
        self.assertEqual(
            "HTMLNode(<a>, test, ['a', 'b'], {'href': 'https://www.google.com'})",
            repr(node),
        )

    def test_none(self):
        node = HTMLNode(
            tag="<a>",
            value="test",
            children=["a", "b"],
        )
        self.assertIs(node.props, None)

    def test_prop_to_html(self):
        node = HTMLNode(
            tag="<a>",
            value="test",
            children=["a", "b"],
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )

    def test_prop_to_html_none(self):
        node = HTMLNode(
            tag="<a>",
            value="test",
            children=["a", "b"],
        )
        self.assertEqual("", node.props_to_html())

    def test_to_html(self):
        node = HTMLNode(
            tag="<a>",
            value="test",
            children=["a", "b"],
            props={"href": "https://www.google.com"},
        )
        with self.assertRaises(NotImplementedError):
            node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_value_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "text value")
        self.assertEqual("text value", node.to_html())

    def test_leaf_a_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent_node = ParentNode("p", children)
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
