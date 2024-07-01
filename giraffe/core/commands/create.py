import argparse

import os


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("name", help="Name of your new Giraffe project")


def execute(args):
    f = open("wsgi.py", "w")
    f.write('# entry point')

    os.mkdir(args.name)

    f = open(f"{args.name}/config.py", "w")
    f.write(f'# config file\n\nPROJECT_NAME = "{args.name}"\n\nAPPS = []')

    print(args.name)