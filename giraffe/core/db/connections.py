from typing import List

import sqlite3


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


def execute(query: str) -> List:
    print('query', query)

    cursor.execute(query)

    return []


def execute_script(script: str) -> None:
    print('script', script)

    cursor.executescript(script)

    return None