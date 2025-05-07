import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        new_nodes = []
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise Exception("invalid markdown: no matching delimiter")

        for i, split in enumerate(splits):
            if split == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split, text_type=TextType.TEXT))
            else:
                new_nodes.append(TextNode(split, text_type=text_type))
        split_nodes.extend(new_nodes)

    return split_nodes


def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches


def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex, text)
    return matches
