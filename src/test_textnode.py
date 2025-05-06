import unittest

from textnode import TextNode, TextType, split_nodes_delimiter, text_node_to_html_node


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

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is **bold** and *italic* text", TextType.TEXT)
        # First split by bold delimiter
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        # Then split resulting nodes by italic delimiter
        final_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)

        self.assertEqual(
            final_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_no_delimiters(self):
        node = TextNode("No special formatting here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("No special formatting here", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_all_special(self):
        node = TextNode("**All bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("", TextType.TEXT),  # Empty text node before bold
                TextNode("All bold", TextType.BOLD),
                TextNode("", TextType.TEXT),  # Empty text node after bold
            ],
        )

    def test_split_nodes_delimiter_consecutive_delimiters(self):
        node = TextNode("This has **bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("more bold", TextType.BOLD),
                TextNode("", TextType.TEXT),  # Empty text node at the end
            ],
        )

    def test_split_nodes_delimiter_empty_between_delimiters(self):
        node = TextNode("This has an empty bold section: ****, right?", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This has an empty bold section: ", TextType.TEXT),
                TextNode("", TextType.BOLD),  # Empty bold section
                TextNode(", right?", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_missing_closing_delimiter(self):
        node = TextNode("This has an unclosed **bold section", TextType.TEXT)

        # This should raise an exception
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)


if __name__ == "__main__":
    unittest.main()
