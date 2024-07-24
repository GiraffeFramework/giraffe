from pathlib import Path

import importlib.util
import os


class Config:
    def __init__(self) -> None:
        self._project_name: str = os.environ.get('GIRAFFE_APP', "")

        if not self._project_name:
            raise Exception("No project found. Run giraffe create {name} first.")

        self._load_config()
    
    def _load_config(self) -> None:
        path = Path.cwd() / self._project_name / "config.py"

        spec = importlib.util.spec_from_file_location("config", path)

        if not spec:
            raise Exception("Config file not found.")

        config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config) # type: ignore

        self._root = config.ROOT
        self._apps = config.APPS

    def _save_config(self) -> None:
        path = Path.cwd() / self._project_name / "config.py"

        with open(path, "w") as f:
            f.write(f"""# config file
 
ROOT = "{self._root}"

PROJECT_NAME = "{self._project_name}"

APPS = {self._apps}
""")

    @property
    def root(self) -> str:
        return self._root
    
    @property
    def project(self) -> str:
        return self._project_name
    
    @property
    def apps(self) -> list:
        return self._apps
    
    @apps.setter
    def apps(self, apps: list) -> None:
        self._apps = apps

        self._save_config()
