from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matching = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matching

def extract_markdown_links(text):
    matching = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matching    


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        images = extract_markdown_images(old_node.text)
        remaining_text = old_node.text
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        for img in images:
            alt = img[0]
            url = img[1]
            sections = remaining_text.split(f"![{alt}]({url})",1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = sections[1]
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        links = extract_markdown_links(old_node.text)
        remaining_text = old_node.text
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        for link in links:
            alt = link[0]
            url = link[1]
            sections = remaining_text.split(f"[{alt}]({url})",1)
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(alt, TextType.LINK, url))
            remaining_text = sections[1]
        if remaining_text != "":
            split_nodes.append(TextNode(remaining_text, TextType.TEXT))

        new_nodes.extend(split_nodes)
    return new_nodes