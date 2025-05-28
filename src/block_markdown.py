from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        stripped_blocks.append(block)
    return stripped_blocks


def block_to_block_type(markdown_block):
    block_splits = markdown_block.split("\n")
    if block_splits[0] == "```" and block_splits[-1] == "```":
        return BlockType.CODE
    elif all([block.startswith("> ") for block in block_splits]):
        return BlockType.QUOTE
    elif all([block.startswith("- ") for block in block_splits]):
        return BlockType.UNORDERED_LIST

    else:
        return BlockType.PARAGRAPH
