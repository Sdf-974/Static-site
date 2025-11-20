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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entrie in os.listdir(dir_path_content):
        path = os.path.join(dir_path_content, entrie)
        dest_subdir = os.path.join(dest_dir_path, entrie)
        
        if not os.path.isfile(path): 
            if not os.path.exists(dest_subdir):
                os.mkdir(dest_subdir)
            generate_pages_recursive(path, template_path, dest_subdir)
        elif os.path.isfile(path) and entrie.endswith(".md"):
            html_name = os.path.splitext(entrie)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, html_name)
            generate_page(path, template_path, dest_path)
