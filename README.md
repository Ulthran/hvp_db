# hvp_db

SQLAlchemy models for the Human Virome Project database.

## Requirements

- Python 3.8 or newer
- SQLAlchemy 2.0.43 or newer

## Usage

```python
from datetime import date
from hvp_db import Sample, get_session_maker

Session = get_session_maker("sqlite:///hvp.db")

with Session() as session:
    sample = Sample(
        sample_id="SST12345",
        participant_id="PVP2001",
        anatomical_site="stool",
        date_collected=date(2021, 3, 8),
        storage_buffer="oral_cocktail",
        sample_use="pilot",
    )
    session.add(sample)
    session.commit()
```

The call to `get_session_maker` automatically creates the database tables if
needed.

## Command line interface

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
