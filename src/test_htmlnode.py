import unittest

from htmlnode import HTMLNode


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
            " href=https://www.google.com target=_blank", node.props_to_html()
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
