from typing import List

import sqlite3


conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()


def change_db(action: str) -> List:
    print('change_query: ', action)

    cursor.execute(action)
    conn.commit()

    return []


def query_all(query: str) -> List:
    print('all_query: ', query)

    cursor.execute(query)
    rows = cursor.fetchall()

    print(rows)

    return rows


def query_one(query: str) -> List:
    print('one_query: ', query)

    cursor.execute(query)
    rows = cursor.fetchone()

    print(rows)

    return rows



def execute_script(script: str) -> None:
    print('script', script)

    cursor.executescript(script)
    conn.commit()

    return None
