from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive
import sys

base_path ="/"
if len(sys.argv) > 1:
    base_path = sys.argv[1]

def main():
    docs_path = "./docs"
    src_path = "./static"
    copy_files_recursive(src_path, docs_path)
    dir_path_content = "./content/"
    template_path = "./template.html"
    dest_dir_path = docs_path
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path)


    

main()