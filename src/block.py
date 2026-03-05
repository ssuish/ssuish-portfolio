import re
from enum import Enum
from parentnode import ParentNode
from inline import text_to_textnodes, text_node_to_html_node
from textnode import TextNode, TextType


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []
    for block in blocks:
        block = block.strip()

        if not block:
            continue

        lines = [x.strip() for x in block.split("\n")]
        result.append("\n".join(lines))

    return result


def block_to_block_type(block):
    lines = block.split("\n")

    if re.search(r"^#{1,6} .+", block):
        return BlockType.HEADING

    if len(lines) > 1 and block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    if lines[0].startswith(">"):
        for l in lines[1:]:
            if not l.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if lines[0].startswith("- "):
        for l in lines[1:]:
            if not l.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for l in lines:
            if not l.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def calculate_heading_hierarchy(block):
    # More than 6 instances of '#' already results to paragraph
    return len(block) - len(block.lstrip("#"))


def code_block_to_html_node(block):
    lines = block.split("\n")
    inner_content = "\n".join(lines[1:-1]) + ("\n" if len(lines) > 2 else "")
    text_node = TextNode(text=inner_content, text_type=TextType.CODE)
    code_node = text_node_to_html_node(text_node)
    return ParentNode(tag="pre", children=[code_node])


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []

    i = 1
    for line in lines:
        li = line.split(f"{i}. ")
        li_node = ParentNode(tag="li", children=text_to_children(li))
        li_nodes.append(li_node)

        i += 1

    return ParentNode(tag="ol", children=li_nodes)


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    li_nodes = []

    for line in lines:
        li = line.split("- ")
        li_node = ParentNode(tag="li", children=text_to_children(li))
        li_nodes.append(li_node)

    return ParentNode(tag="ul", children=li_nodes)


def block_to_html_node(block, block_type):
    if block_type == BlockType.CODE:
        return code_block_to_html_node(block)

    if block_type == BlockType.PARAGRAPH:
        text = block.replace("\n", " ")
    elif block_type == BlockType.QUOTE:
        text = " ".join(line.lstrip(">").strip() for line in block.split("\n"))
    elif block_type == BlockType.HEADING:
        text = block.lstrip("#").strip().replace("\n", " ")
    else:
        text = block

    leaf_nodes = text_to_children(text)

    if block_type == BlockType.QUOTE:
        return ParentNode(tag="blockquote", children=leaf_nodes)

    if block_type == BlockType.PARAGRAPH:
        return ParentNode(tag="p", children=leaf_nodes)

    if block_type == BlockType.HEADING:
        return ParentNode(tag=calculate_heading_hierarchy(block), children=leaf_nodes)

    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)


def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_html_node(block, block_type))

    return ParentNode(tag="div", children=children)

def text_to_children(text):
    children = text_to_textnodes(text)
    children_nodes = []

    for child in children:
        children_nodes.append(text_node_to_html_node(child))

    return children_nodes
