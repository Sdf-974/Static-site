from textnode import TextNode, TextType
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"





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


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = []
    sections = markdown.split("\n\n")
    for i in range(0, len(sections)):
        cleaned_block = sections[i].strip()
        if cleaned_block != "":
            blocks.append(cleaned_block)
    return blocks 


def block_to_block_type(block):
    lines = block.split("\n")

    if len(lines) == 1:
        line = lines[0]
        prefixes = ("# ", "## ", "### ", "#### ", "##### ", "###### ")
        if line.startswith(prefixes):
            return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE
    
    is_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST
    
    if is_ordered_list(block):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    


def is_ordered_list(block):
    lines = block.split("\n")
    expected_nums = 1
    for line in lines:
        index = line.find(" ")
        
        if index == -1:
            return False
        
        prefix = line[:index]
        
        if prefix[-1] != ".":
            return False
        
        if not prefix[:-1].isdigit():
            return False
        
        if int(prefix[:-1]) != expected_nums:
            return False
        expected_nums += 1

    return True


