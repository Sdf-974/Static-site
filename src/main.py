from copystatic import cleaning_path, copy_recursive

def main():
    public_path = "./public"
    src_path = "./static"
    cleaning_path(public_path)
    copy_recursive(src_path, public_path)

    

main()