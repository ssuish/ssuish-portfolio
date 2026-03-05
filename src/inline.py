import re
from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode):

    if text_node.text_type not in TextType:
        raise ValueError("Invalid text type")

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        delimiter_count = node.text.count(delimiter)

        if delimiter_count == 0:
            new_nodes.append(node)
            continue

        if delimiter_count % 2 == 1:
            raise ValueError("Invalid Markdown syntax")

        substrings = node.text.split(delimiter)

        for i in range(0, len(substrings)):
            part = substrings[i]

            if part == None or part == "":
                continue

            if i % 2 == 0:
                new_node = TextNode(part, TextType.TEXT)
            else:
                new_node = TextNode(part, text_type)

            new_nodes.append(new_node)

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches if matches else ()


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches if matches else ()


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        remaining_text = node.text

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for i in range(0, len(images)):
            alt_text, url = images[i]
            delimiter = f"![{alt_text}]({url})"
            part = remaining_text.split(delimiter, 1)

            if len(part) == 2:
                new_nodes.append(TextNode(part[0], text_type=TextType.TEXT))
                new_nodes.append(TextNode(alt_text, text_type=TextType.IMAGE, url=url))
                remaining_text = part[1]
            else:
                continue
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, text_type=TextType.TEXT))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_links(node.text)
        remaining_text = node.text

        if len(images) == 0:
            new_nodes.append(node)
            continue

        for i in range(0, len(images)):
            alt_text, url = images[i]
            delimiter = f"[{alt_text}]({url})"
            part = remaining_text.split(delimiter, 1)

            if len(part) == 2:
                new_nodes.append(TextNode(part[0], text_type=TextType.TEXT))
                new_nodes.append(TextNode(alt_text, text_type=TextType.LINK, url=url))
                remaining_text = part[1]
            else:
                continue
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, text_type=TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
