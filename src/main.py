import sys

from utils.utils import generate_page, publish_static_files

def main() -> int:

    publish_static_files()

    generate_page('content/index.md', 'template.html', 'public/index.html')
    generate_page('content/blog/glorfindel/index.md', 'template.html', 'public/blog/glorfindel/index.html')
    generate_page('content/blog/majesty/index.md', 'template.html', 'public/blog/majesty/index.html')
    generate_page('content/blog/tom/index.md', 'template.html', 'public/blog/tom/index.html')
    generate_page('content/contact/index.md', 'template.html', 'public/contact/index.html')

    return 0

if __name__ == '__main__':
    sys.exit(main()) 