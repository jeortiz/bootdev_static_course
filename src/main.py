import sys

from utils.utils import generate_pages_recursive, publish_static_files

def main() -> int:

    
    basepath = sys.argv[1] if len(sys.argv) > 1 else '/'
    publish_static_files()

    generate_pages_recursive('content', 'template.html', 'docs', basepath)

    return 0

if __name__ == '__main__':
    sys.exit(main()) 