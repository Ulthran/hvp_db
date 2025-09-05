# hvp_db

UPenn Human Virome Project sample database.

## Install

```bash
git clone https://github.com/Ulthran/hvp_db
cd hvp_db
python -m venv env
source env/bin/activate
pip install -e .[web]
```

## 

The package installs a small CLI named `hvp-db`.

Initialize a new SQLite database:

```bash
hvp-db init sqlite:///hvp.db
```

Load samples from a CSV file:

```bash
hvp-db load-csv sqlite:///hvp.db samples.csv
```

CSV columns should match the fields of the `Sample` model and dates must be in
ISO format (`YYYY-MM-DD`).
