import argparse
import importlib
import pkgutil


def main():
    print("loaded cli")

    parser = argparse.ArgumentParser(description="Giraffe Command Line Interface")
    subparsers = parser.add_subparsers(dest="command")

    commands_package = "giraffe.core.commands"

    for _, module_name, _ in pkgutil.iter_modules([commands_package.replace(".", "/")]):
        module = importlib.import_module(f"{commands_package}.{module_name}")
        command_parser = subparsers.add_parser(module_name, help=module.__doc__)
        module.add_arguments(command_parser)

    args = parser.parse_args()

    if args.command:
        module = importlib.import_module(f"{commands_package}.{args.command}")
        module.execute(args)

    else:
        parser.print_help()
