# catalog

A simple Flask app.


### Initial setup

```
$ python -c 'import database; database.init_db()'
```


### Migrations

Enable migrations if database exists (only need to do this once).
```
$ python run.py db init
```

Generate a migration (Alembic doesn't detect every change to model, indexes for instance, so these need to be double-checked).

```
$ python run.py db migrate
```

Apply migrations to database.
```
$ python run.py db upgrade
```