from giraffe.utils.config import Config

from pathlib import Path

import subprocess
import argparse
import os
import re

def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("port", help="Port", nargs='?', default='8000')


def execute(args):
    """
    Run your Giraffe server
    """

    root_dir = Path.cwd()

    wsgi_path = root_dir / "wsgi.py"

    if not os.path.exists(wsgi_path):
        raise Exception(f"No wsgi.py file found.")
    
    if args.port:
        with open(wsgi_path, 'r') as file:
            content = file.read()

        content = re.sub(r'port=\d{4}', f'port={args.port}', content)

        with open(wsgi_path, 'w') as file:
            file.write(content)
    
    subprocess.run(["python", str(wsgi_path)])
