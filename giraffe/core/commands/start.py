from pathlib import Path

import argparse
import os


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("name", help="Name of your new Giraffe project")


def execute(args):
    """
    Start a Giraffe project with chosen name.
    Creates necessary files for a basic Giraffe project.
    """

    root_dir = Path.cwd()

    with open(os.path.join(root_dir, "wsgi.py"), "w") as f:
        f.write(f"""# app entry point
from {args.name} import create_app


app = create_app()


if __name__ == '__main__':
    app.start()

""")

    project_dir = root_dir / args.name

    os.mkdir(project_dir)

    config_path = project_dir / "config.py"

    with open(config_path, "w") as f:
        f.write(f"""# config file
 
ROOT = "{root_dir}"

PROJECT_NAME = "{args.name}"

APPS = []
""")
        
    init_path = project_dir / "__init__.py"

    with open(init_path, "w") as f:
        f.write(f"""from giraffe import Giraffe


def create_app():
    app = Giraffe(__name__, port=4000)

    return app
""")
        
    os.environ['GIRAFFE_APP'] = args.name

    