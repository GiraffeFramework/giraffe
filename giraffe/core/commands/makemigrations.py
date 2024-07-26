from typing import Dict, Optional, List, Union

from pathlib import Path

from ..db.connections import execute_script
from ..db.defaults import Migration
from ..db.models import Model

import importlib.util
import argparse
import inspect
import json
import sys
import os


MIGRATIONS_DIR = Path.cwd() / 'migrations'


def add_arguments(parser: argparse.ArgumentParser):
    return


def execute(args):
    # Get models and current version
    models = _get_models()
    version = _get_version()

    # Add migration table for initial migrations
    if not version:
        models.append(Migration)

    if not models:
        print("No migrations available.")

        return
    
    MIGRATIONS_DIR.mkdir(exist_ok=True)

    if version:
        with open(MIGRATIONS_DIR / f'{version.name}.json') as file:
            old_schemas = json.load(file)

    else:
        old_schemas = []

    migration_name = f'{sum(1 for entry in MIGRATIONS_DIR.iterdir() if entry.is_file())}.json'

    with open(os.path.join(MIGRATIONS_DIR, migration_name), 'w') as file:
        schemas: list = []

        for model in models:
            schema = model.get_schema()

            if not version:
                schema['table'] = "create"

            # COMPARE TO OLD SCHEMAS

            schemas.append(schema)

        json.dump(schemas, file, indent=4)

    return
    
    with open(os.path.join(MIGRATIONS_DIR, migration_name)) as f:
        sql = f.read()

    execute_script(sql)

    Migration({'name' : migration_name}).create()


def _get_models() -> list:
    """
    Get all model class objects defined in models.py files at the custom framework app level.
    """

    root = Path.cwd()
    models = []

    # loop over all models.py files that are in a Giraffe app.
    for models_file in root.glob("*/models.py"):
        # Load file to get access to the classes
        module_name = f"models_{models_file.stem}"
        spec = importlib.util.spec_from_file_location(module_name, models_file)

        if not spec:
            raise ValueError(f"Failed to load module {module_name}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module) # type: ignore

        # Extract all model classes from the module
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ != module.__name__:
                continue

            if not issubclass(obj, Model):
                continue
            
            models.append(obj)

    return models


def _get_version() -> Optional[Migration]:
    """
    Returns current database version.
    """

    try:
        return Migration().latest('applied_at')
    
    except:
        return None
