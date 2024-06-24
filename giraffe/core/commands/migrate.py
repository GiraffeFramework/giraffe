from typing import Dict, Optional

from ..db.connections import execute_script
from ..db.defaults import Migration

import argparse
import os


MIGRATIONS_DIR = 'migrations'


def add_arguments(parser: argparse.ArgumentParser):
    return


def execute(args):
    available_migrations = _get_migrations()

    if not available_migrations:
        schema = Migration().get_schema()
        #schema.update(other_migration)
        
        migration_name = _generate_migration(schema, None)

    #else:
        #_generate_migration(schema, available_migrations)

    if not migration_name:
        print("No migrations available.")

        return
    
    with open(os.path.join(MIGRATIONS_DIR, migration_name)) as f:
        sql = f.read()

    execute_script(sql)

    Migration({'name' : migration_name}).create()


def _get_migrations():
    try:
        return Migration().all('applied_at')

    except:
        return []
    

def _generate_migration(current_schema: Dict, previous_schema: Optional[Dict]={}) -> Optional[str]:
    table: str = list(current_schema.keys())[0]
    schema: dict = current_schema[table]

    print(current_schema)

    migration_steps = []

    for table, fields in current_schema.items():
        if previous_schema and previous_schema[table]:
            for field, field_type in fields.items():
                if field not in previous_schema[table]:
                    migration_steps.append(f"ALTER TABLE {table} ADD COLUMN {field} {field_type};")
            
        else:
            migration_steps.append(f"CREATE TABLE {table} ({', '.join(_get_field(field, field_data) for field, field_data in fields.items())});")
            
    if not migration_steps:
        print("No changes detected.")
        
        return
    
    if not os.path.exists(MIGRATIONS_DIR):
        os.mkdir(MIGRATIONS_DIR)
    
    migration_name = f'migration_{len(os.listdir(MIGRATIONS_DIR))}.sql'
    migration_file = os.path.join(MIGRATIONS_DIR, migration_name)
    
    with open(migration_file, 'w') as f:
        f.write('\n'.join(migration_steps))
    
    print(f'Migration created: {migration_file}')

    return migration_name


def _get_field(field, field_data):
    return f"{field} {field_data['type']}{' PRIMARY KEY' if field_data['primary_key'] else ''}"
