import os
import sqlite3
import sys
from datetime import datetime

DATABASE = 'your_database.db'
MIGRATIONS_DIR = 'migrations'


def get_applied_migrations(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM migrations ORDER BY applied_at")
    return [row[0] for row in cursor.fetchall()]


def apply_migration(conn, migration_name):
    with open(os.path.join(MIGRATIONS_DIR, migration_name)) as f:
        sql = f.read()

    up_sql = sql.split('-- up')[1].split('-- down')[0].strip()

    cursor = conn.cursor()
    cursor.executescript(up_sql)
    cursor.execute("INSERT INTO migrations (name) VALUES (?)", (migration_name,))
    conn.commit()


def revert_migration(conn, migration_name):
    with open(os.path.join(MIGRATIONS_DIR, migration_name)) as f:
        sql = f.read()

    down_sql = sql.split('-- down')[1].strip()

    cursor = conn.cursor()
    cursor.executescript(down_sql)
    cursor.execute("DELETE FROM migrations WHERE name = ?", (migration_name,))
    conn.commit()


def migrate(conn):
    applied_migrations = get_applied_migrations(conn)
    available_migrations = sorted(os.listdir(MIGRATIONS_DIR))

    for migration in available_migrations:
        if migration not in applied_migrations:
            print(f"Applying {migration}...")
            apply_migration(conn, migration)


def rollback(conn):
    applied_migrations = get_applied_migrations(conn)
    if not applied_migrations:
        print("No migrations to rollback.")
        return

    last_migration = applied_migrations[-1]
    print(f"Reverting {last_migration}...")
    revert_migration(conn, last_migration)


def main():
    if len(sys.argv) < 2:
        print("Usage: python migrate.py [migrate|rollback]")
        return

    command = sys.argv[1]

    conn = sqlite3.connect(DATABASE)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS migrations (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    if command == "migrate":
        migrate(conn)
    elif command == "rollback":
        rollback(conn)
    else:
        print(f"Unknown command: {command}")

    conn.close()


if __name__ == "__main__":
    main()
