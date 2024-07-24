from giraffe.utils.config import Config

from pathlib import Path

import argparse
import os


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("name", help="Name of your new Giraffe project")


def execute(args):
    """
    Add an app to your Giraffe project.
    Creates necessary files for a Giraffe app.
    """

    root_dir = Path.cwd()

    app_dir = root_dir / args.name

    if os.path.exists(app_dir):
        raise Exception(f"App {args.name} already exists. This app is not registered in your config.py file.")

    os.mkdir(app_dir)

    init_path = app_dir / "__init__.py"

    with open(init_path, "w") as f:
        f.write('')

    models_path = app_dir / "models.py"

    with open(models_path, "w") as f:
        f.write('from giraffe.core.db import Model, fields\n\n')
        
    views_path = app_dir / "views.py"

    with open(views_path, "w") as f:
        f.write(f"""from giraffe.core.routes import Routes


# Add app.add_routes({args.name}_routes) to your project __init__.py file.
{args.name}_routes = Routes()          
""")