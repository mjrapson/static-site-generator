from blocktype import BlockType

import re

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    block_strings = list(map(lambda x: x.strip(), split_markdown))
    block_strings = list(filter(lambda x: x != "", block_strings))
    return block_strings

def block_to_block_type(block):
    lines = block.split("\n")

    # Check heading
    if re.match(r"#+\s", block):
        return BlockType.HEADING
    
    # Check code
    if len(lines) > 1: 
        if lines[0].startswith("```") and lines[-1].startswith("```"):
            return BlockType.CODE
    else:
        if block.startswith("```") and block.endswith("```"):
            return BlockType.CODE
    
    # Check quote
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    
    # Check unordered list
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    
    # Check ordered list
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH