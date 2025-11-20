from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

def main():
    public_path = "./public"
    src_path = "./static"
    copy_files_recursive(src_path, public_path)
    from_path = "./content/index.md"
    dest_path = "./public/index.html"
    dir_path_content = "./content/"
    template_path = "./template.html"
    dest_dir_path = "./public/"
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)


    

main()