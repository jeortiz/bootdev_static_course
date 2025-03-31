import sys

from utils.utils import generate_page, generate_pages_recursive, publish_static_files

def main() -> int:

    publish_static_files()

    generate_pages_recursive('content', 'template.html', 'public')

    return 0

if __name__ == '__main__':
    sys.exit(main()) 