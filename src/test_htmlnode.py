import unittest

from htmlnode import HTMLNode, LeafNode


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
