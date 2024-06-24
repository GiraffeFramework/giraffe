from typing import Dict, Optional

from ..db.defaults import Migration

import argparse
import os


MIGRATIONS_DIR = 'migrations'


def add_arguments(parser: argparse.ArgumentParser):
    return


def execute(args):
    available_migrations = _get_migrations()

    if not available_migrations:
        _generate_migration(Migration().get_schema(), None)


def _get_migrations():
    try:
        return Migration().all('applied_at')

    except:
        return []
    

def _generate_migration(current_schema: Dict, previous_schema: Optional[Dict]={}) -> None:
    table: str = list(current_schema.keys())[0]
    schema: dict = current_schema[table]

    migration_steps = []

    for field, field_data in schema.items():
        if previous_schema and previous_schema[table]:
            migration_steps.append(f"ALTER TABLE {table} ADD COLUMN {field} {field_data['type']}")
        
        else:
            migration_steps.append(f"CREATE TABLE {table} ({field} {field_data['type']})")

    if not migration_steps:
        print("No changes detected.")
        
        return
    
    if not os.path.exists(MIGRATIONS_DIR):
        os.mkdir(MIGRATIONS_DIR)
    
    migration_file = os.path.join(MIGRATIONS_DIR, f'migration_{len(os.listdir(MIGRATIONS_DIR))}.sql')
    
    with open(migration_file, 'w') as f:
        f.write('\n'.join(migration_steps))
    
    print(f'Migration created: {migration_file}')
