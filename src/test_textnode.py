import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.LINK, "url://test")
        self.assertEqual(node.url, "url://test")

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "url://test")
        self.assertEqual("TextNode(This is a text node, link, url://test)", repr(node))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_html(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic_html(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_url_html(self):
        node = TextNode("This is a text node", TextType.LINK, "url://test")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "url://test"})
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")

    def test_image_html(self):
        node = TextNode("This is a text node", TextType.IMAGE, "url://test")
        html_node = text_node_to_html_node(node)
        self.assertEqual(
            html_node.props, {"src": "url://test", "alt": "This is a text node"}
        )
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")


if __name__ == "__main__":
    unittest.main()
