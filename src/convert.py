from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType

import re

def text_node_to_html_node(text_node):
    match text_node.type:
        case TextType.PLAIN:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a", value=text_node.text, props={
                "href": f"{text_node.url}"})
        case TextType.IMAGE:
            return LeafNode(tag="img", value="", props={
                "src": f"{text_node.url}",
                "alt": f"{text_node.text}"
            })
        case _:
            raise Exception("Unknown TextType")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        arr = node.text.split(delimiter)

        if len(arr) % 2 == 0:
            raise Exception("Node contains invalid markdown - format mismatch")
        
        for i in range(0, len(arr)):
            if arr[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(arr[i], TextType.PLAIN))
            else:
                new_nodes.append(TextNode(arr[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    result = []
    matches = re.findall(r'!\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    for match in matches:
        result.append(match)

    return result

def extract_markdown_links(text):
    result = []
    matches = re.findall(r'(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)', text)
    for match in matches:
        result.append(match)

    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        md_images = extract_markdown_images(node.text)
        current_text = node.text
        for image, url in md_images:
            split = current_text.split(f"![{image}]({url})", 1)
            if len(split) == 2:
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.PLAIN))
                new_nodes.append(TextNode(image, TextType.IMAGE, url))
                current_text = split[1]
            else:
                current_text = split[0]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.PLAIN))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.type != TextType.PLAIN:
            new_nodes.append(node)
            continue

        md_links = extract_markdown_links(node.text)
        current_text = node.text
        for alt_text, url in md_links:
            split = current_text.split(f"[{alt_text}]({url})", 1)
            if len(split) == 2:
                if split[0] != "":
                    new_nodes.append(TextNode(split[0], TextType.PLAIN))
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                current_text = split[1]
            else:
                current_text = split[0]

        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.PLAIN))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes