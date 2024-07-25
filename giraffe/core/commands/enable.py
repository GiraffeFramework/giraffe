from giraffe.utils.config import Config

from pathlib import Path

import argparse
import requests


FEATURE_URL = 'https://raw.githubusercontent.com/GiraffeFramework/giraffe_features/main/'


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("feature", help="Enable a Giraffe feature for your application.")


def execute(args):
    """
    Enable a Giraffe feature for your application. A list of available features:
    - spa = Enable Single Page Application support.
    """

    if args.feature == 'spa':
        _enable_spa()


def _enable_spa():
    root_dir = Path.cwd()

    js_path = root_dir / "static" / "js"

    js_path.mkdir(parents=True, exist_ok=True)

    response = requests.get(f'{FEATURE_URL}static/js/spa.js')
    response.raise_for_status()

    with open(js_path / "spa.js", 'wb') as file:
        file.write(response.content)