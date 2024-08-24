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
        migration_name = "0.json"
        
        models.append(Migration)

    else:
        migration_name = f"{int(version.name.split('.')[0]) + 1}.json"

    if not models:
        print("No migrations available.")

        return
    
    if os.path.join(MIGRATIONS_DIR, migration_name):
        print(f"Run `giraffe migrate {migration_name.split('.')[0]}` first before you can initiate a new migration.")

        return
    
    MIGRATIONS_DIR.mkdir(exist_ok=True)

    with open(os.path.join(MIGRATIONS_DIR, migration_name), 'w') as file:
        schemas: list = []

        for model in models:
            model: Model

            schema = model.get_schema_changes()

            schemas.append(schema)

        json.dump(schemas, file, indent=4)

    return


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
