from typing import List

import sqlite3


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


def execute(query: str) -> List:
    print(query)

    cursor.execute(query)

    print(cursor.fetchall())

    return []