import os
import shutil
import sys
from htmlnode import HtmlNode
from textnode import TextNode, TextType

def publish_static_files():
    static_folder = '../static'
    public_folder = '../public'

    try:
        if os.path.isdir(public_folder):
            shutil.rmtree(public_folder)
        
            os.mkdir(public_folder)
            copy_dir_files(static_folder, public_folder)
    except OSError as e:
        print(f"Failed - error: {e}")

def copy_dir_files(src, dest):
    files = os.listdir(src)

    for f in files:
        f_path = os.path.join(src,f)

        if os.path.isfile(f_path):
            shutil.copy(f_path, dest)
        elif os.path.isdir(f_path):
            dest_dir = os.path.join(dest,f)
            os.mkdir(dest_dir)
            copy_dir_files(f_path, dest_dir)
    
    return

def main() -> int:

    publish_static_files()

    return 0

if __name__ == '__main__':
    sys.exit(main()) 