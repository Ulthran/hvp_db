# hvp_db

UPenn Human Virome Project sample database

## Install

```bash
git clone https://github.com/Ulthran/hvp_db
cd hvp_db
python -m venv env
source env/bin/activate
pip install -e .[web]
```

## Init db

The package installs a small CLI named `hvp-db`.

Initialize a new SQLite database:

```bash
hvp-db init sqlite:///hvp.db
```

## Ingest data

Load samples from a CSV file:

```bash
hvp-db load sqlite:///hvp.db samples.csv
```

CSV columns should match the fields of the `Sample` model and dates must be in
ISO format (`YYYY-MM-DD`).

## View data

Run the Flask site in dev mode:

```bash
hvp-db web sqlite:///hvp.db password
```

Or put it into production as a system daemon with something like this (make sure to set the env vars `HVP_DB_URI` and `HVP_DB_PASSWORD` properly for your daemon):

```bash
gunicorn --workers 2 --bind unix:/run/hvp.sock hvp_db/wsgi:app
```