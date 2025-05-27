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


def split_nodes_image(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        new_nodes = []
        node_text = node.text
        while len(node_text) > 0:
            links = extract_markdown_images(node_text)
            min = float("inf")
            first_link_name = None
            first_link_url = None
            for link_name, link_url in links:
                pos = node_text.find(f"![{link_name}]({link_url})")
                if pos < min:
                    min = pos
                    first_link_name = link_name
                    first_link_url = link_url
            if first_link_name is None:
                new_node = TextNode(text=node_text, text_type=TextType.TEXT)
                new_nodes.append(new_node)
                break
            else:
                splits = node_text.split(
                    f"![{first_link_name}]({first_link_url})", maxsplit=1
                )
                if len(splits) > 1:
                    before_node = TextNode(text=splits[0], text_type=TextType.TEXT)
                    new_nodes.append(before_node)
                    new_nodes.append(
                        TextNode(
                            text=first_link_name,
                            text_type=TextType.IMAGE,
                            url=first_link_url,
                        )
                    )
                    node_text = splits[1]
                else:
                    if node_text:
                        new_node = TextNode(text=node_text, text_type=TextType.TEXT)
                        new_nodes.append(new_node)
                    break

        split_nodes.extend(new_nodes)

    return split_nodes


def split_nodes_link(old_nodes):
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        new_nodes = []
        node_text = node.text
        while len(node_text) > 0:
            links = extract_markdown_links(node_text)
            min = float("inf")
            first_link_name = None
            first_link_url = None
            for link_name, link_url in links:
                pos = node_text.find(f"[{link_name}]({link_url})")
                if pos < min:
                    min = pos
                    first_link_name = link_name
                    first_link_url = link_url
            if first_link_name is None:
                new_node = TextNode(text=node_text, text_type=TextType.TEXT)
                new_nodes.append(new_node)
                break
            else:
                splits = node_text.split(
                    f"[{first_link_name}]({first_link_url})", maxsplit=1
                )
                if len(splits) > 1:
                    before_node = TextNode(text=splits[0], text_type=TextType.TEXT)
                    new_nodes.append(before_node)
                    new_nodes.append(
                        TextNode(
                            text=first_link_name,
                            text_type=TextType.LINK,
                            url=first_link_url,
                        )
                    )
                    node_text = splits[1]
                else:
                    if node_text:
                        new_node = TextNode(text=node_text, text_type=TextType.TEXT)
                        new_nodes.append(new_node)
                    break

        split_nodes.extend(new_nodes)

    return split_nodes


def text_to_textnodes(text):
    node_to_split = TextNode(text=text, text_type=TextType.TEXT)
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}
    new_nodes = [node_to_split]
    for key, value in delimiters.items():
        new_nodes = split_nodes_delimiter(new_nodes, key, value)
        print(f"key = {key}, value = {value}: {new_nodes}")

    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_image(new_nodes)
    return new_nodes
