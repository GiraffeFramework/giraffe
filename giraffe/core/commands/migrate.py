from pathlib import Path

from ..db.connections import execute_script
from ..db.defaults import Migration

import argparse
import json


MIGRATIONS_DIR = Path.cwd() / 'migrations'


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument("migration", help="The migration name to apply.")

    return


def execute(args):
    migration = MIGRATIONS_DIR / f'{args.migration}.json'

    if not migration:
        print("Migration {args.migration} not found.")

        return
    
    with open(migration) as file:
        migration = json.load(file)

    migration_steps = _get_migration_steps(migration)

    if not migration_steps:
        print("No migrations available.")

        return
    
    execute_script(migration_steps)

    migration, errors = Migration.query.create(body={'name' : args.migration}, required_fields=[Migration.name])

    if errors:
        print(f"Creating migration instance raised error: {errors['error']}")
    

def _get_migration_steps(migration: list) -> str:
    migration_steps: str = ''

    for schema in migration:
        if schema['table'] == 'create':
            migration_steps += f" CREATE TABLE IF NOT EXISTS {schema['name']} ({', '.join(_get_field(field) for field in schema['fields'])});"

        else:
            # TODO

            print('incoming')

    return migration_steps


def _get_field(field: dict):
    return f"{field['name']} {field['type']}{' NOT NULL' if field['notnull'] else ''}{' PRIMARY KEY' if field['pk'] else ''}"
