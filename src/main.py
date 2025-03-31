import os
import shutil
import sys

from utils.utils import publish_static_files

def main() -> int:

    publish_static_files()

    return 0

if __name__ == '__main__':
    sys.exit(main()) 