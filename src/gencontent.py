import os
from inline_markdown import markdown_to_html_node


def extract_title(markdown):
    if markdown.startswith("# "):
        title = markdown.split("# ")
        return title[1]
    else:
        raise Exception("Error: missing title!")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    with open(template_path, "r") as t:
        template = t.read()
    content = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    temp_html = template.replace("{{ Title }}", title)
    html = temp_html.replace("{{ Content }}", content)
    dir = os.path.dirname(dest_path)
    if dir != "":
        os.makedirs(dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(html)