from typing import List

from ..db.defaults import _Migration

import argparse


def add_arguments(parser: argparse.ArgumentParser):
    return


def execute(args):
    available_migrations = _Migration().all('applied_at')
