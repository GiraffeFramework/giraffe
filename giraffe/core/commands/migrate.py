from typing import List

from ..db.defaults import Migration

import argparse


def add_arguments(parser: argparse.ArgumentParser):
    return


def execute(args):
    available_migrations = _get_migrations()

    if not available_migrations:
        print(Migration().get_schema())


def _get_migrations():
    try:
        return Migration().all('applied_at')

    except:
        return []