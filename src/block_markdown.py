import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


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
    regex = "^(#{1,6}) "
    if block_splits[0] == "```" and block_splits[-1] == "```":
        return BlockType.CODE
    elif all(block.startswith("> ") for block in block_splits):
        return BlockType.QUOTE
    elif all(block.startswith("- ") for block in block_splits):
        return BlockType.ULIST
    elif all(x[1].startswith(f"{x[0]+1}. ") for x in enumerate(block_splits)):
        return BlockType.OLIST
    elif re.match(regex, block_splits[0]):
        return BlockType.HEADING
    else:
        return BlockType.PARAGRAPH
