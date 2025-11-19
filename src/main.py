from copystatic import copy_files_recursive
from gencontent import generate_page

def main():
    public_path = "./public"
    src_path = "./static"
    copy_files_recursive(src_path, public_path)
    from_path = "./content/index.md"
    template_path = "./template.html"
    dest_path = "./public/index.html"
    generate_page(from_path, template_path, dest_path)


    

main()