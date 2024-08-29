# Migrating

Everytime you make changes to any of your models.py files, migrations must be made to update the database. This is done by running the following sequence of commands:

```bash
giraffe makemigrations
giraffe migrate [MIGRATION_ID]
```

`giraffe makemigrations` will create a new migration file in the migrations folder. The migration ID is the name of the migration file, this will also be outputted in the terminal.
