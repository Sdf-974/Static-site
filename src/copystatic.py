import os
import shutil

def cleaning_path(dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
        
    os.mkdir(dest)

def copy_recursive(src, dest):
    for entrie in os.listdir(src):
        src_path = os.path.join(src, entrie)
        dest_path = os.path.join(dest, entrie)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
            print(dest_path)
        else:
            os.mkdir(dest_path)
            copy_recursive(src_path, dest_path)