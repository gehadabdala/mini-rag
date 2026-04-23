## Run Alembic Migrations

## Configration

```bash
cp alembic.ini.example alembic.ini
```

- update the `alembic.ini` with your database credentials (`sqlalchemy.url`)

### optional create new migration

```bash
alembic revision --autogenerate -m "adding ..."
```

### upgrade the database

```bash
alembic upgrade head
```