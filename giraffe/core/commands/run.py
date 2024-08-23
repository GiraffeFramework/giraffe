from giraffe.utils.config import Config

from pathlib import Path

import subprocess
import argparse
import sys
import os
import re

def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("port", help="Port", nargs='?', default='8000')


def execute(args):
    """
    Run your Giraffe server
    """

    root_dir = Path.cwd()

    wsgi_path = root_dir / "entry.py"

    if not os.path.exists(wsgi_path):
        raise Exception(f"No entry.py file found.")
    
    if args.port:
        with open(wsgi_path, 'r') as file:
            content = file.read()

        content = re.sub(r'port=\d{4}', f'port={args.port}', content)

        with open(wsgi_path, 'w') as file:
            file.write(content)
    
    try:
        subprocess.run(["python", str(wsgi_path)], check=True)
    
    except KeyboardInterrupt:
        sys.exit(0)
