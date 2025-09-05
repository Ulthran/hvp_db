import argparse
import csv
from datetime import date
from hvp_db.app import main as run_web_app
from hvp_db.models import Sample, get_session_maker, init_engine
from sqlalchemy import Date
from typing import Dict


def _convert_row(row: Dict[str, str]) -> Dict[str, object]:
    """Convert CSV string values to appropriate Python types."""
    columns = {c.name: c.type for c in Sample.__table__.columns}
    data: Dict[str, object] = {}
    for key, value in row.items():
        if value in (None, ""):
            continue
        col_type = columns.get(key)
        if isinstance(col_type, Date):
            data[key] = date.fromisoformat(value)
        else:
            data[key] = value
    return data


def _load_csv(url: str, csv_path: str, *, echo: bool = False) -> None:
    """Load ``Sample`` rows from a CSV file into the database."""
    Session = get_session_maker(url, echo=echo)
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)
        with Session() as session:
            for row in reader:
                sample = Sample(**_convert_row(row))
                session.add(sample)
            session.commit()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="hvp-db")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="initialize a new database")
    p_init.add_argument("url", help="database URL, e.g. sqlite:///hvp.db")
    p_init.add_argument("--echo", action="store_true", help="echo SQL statements")

    p_load = subparsers.add_parser("load-csv", help="load sample rows from a CSV file")
    p_load.add_argument("url", help="database URL")
    p_load.add_argument("csvfile", help="path to CSV file")
    p_load.add_argument("--echo", action="store_true", help="echo SQL statements")

    args = parser.parse_args(argv)

    if args.command == "init":
        init_engine(args.url, echo=args.echo)
    elif args.command == "load-csv":
        _load_csv(args.url, args.csvfile, echo=args.echo)
    elif args.command == "web":
        run_web_app()
    else:
        parser.error(f"Unknown command {args.command}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
