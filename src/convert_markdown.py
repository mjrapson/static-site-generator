from blocktype import BlockType
from convert_block import (block_to_block_type, markdown_to_blocks)
from convert import *
from htmlnode import HTMLNode
from leafnode import LeafNode

def paragraph_block_to_html_node(block):
    value = block.replace("\n", " ")
    content_html_nodes = []
    for node in text_to_textnodes(value):
        content_html_nodes.append(text_node_to_html_node(node))
    return ParentNode("p", content_html_nodes)

def heading_block_to_html_node(block):
    count = 0
    for char in block:
        if char == "#":
            count += 1
        else:
            break

    value = block[count + 1:]
    return LeafNode(f"h{count}", value)

def code_block_to_html_node(block):
    value = block.replace("```\n", "").replace("```", "")
    code_node = LeafNode("code", value)
    return ParentNode("pre", [code_node])

def quote_block_to_html_node(block):
    value = block.replace("\n", " ").replace("> ", "")
    content_html_nodes = []
    for node in text_to_textnodes(value):
        content_html_nodes.append(text_node_to_html_node(node))
    return ParentNode("blockquote", content_html_nodes)

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        line = line[2:]
        content_html_nodes = []
        for node in text_to_textnodes(line):
            content_html_nodes.append(text_node_to_html_node(node))
        list_nodes.append(ParentNode("li", content_html_nodes))
    return ParentNode("ul", list_nodes)

def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        line = line[3:]
        content_html_nodes = []
        for node in text_to_textnodes(line):
            content_html_nodes.append(text_node_to_html_node(node))
        list_nodes.append(ParentNode("li", content_html_nodes))
    return ParentNode("ol", list_nodes)

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        if block == "":
            continue
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                nodes.append(paragraph_block_to_html_node(block))
            case BlockType.HEADING:
                nodes.append(heading_block_to_html_node(block))
            case BlockType.CODE:
                nodes.append(code_block_to_html_node(block))
            case BlockType.QUOTE:
                nodes.append(quote_block_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                nodes.append(unordered_list_block_to_html_node(block))
            case BlockType.ORDERED_LIST:
                nodes.append(ordered_list_block_to_html_node(block))
            case _:
                raise Exception("Unknown block type")

    return ParentNode("div", nodes)

def extract_tile(markdown):
    blocks = markdown_to_blocks(markdown)
    title = ""
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING:
            if not block.startswith("# "):
                continue
            title = block.replace("# ", "").strip()
    if title == "":
        raise Exception("No header available to extract a title")
    return title
