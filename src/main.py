import sys

from utils.utils import generate_page, publish_static_files

def main() -> int:

    publish_static_files()

    generate_page('content/index.md', 'template.html', 'public/index.html')

    return 0

if __name__ == '__main__':
    sys.exit(main()) 