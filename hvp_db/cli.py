import argparse
import csv
from datetime import date
from hvp_db.app import main as run_web_app
from hvp_db.models import Sample, get_session_maker, init_engine
from sqlalchemy import Date, Enum
from typing import Dict


def _convert_row(row: Dict[str, str]) -> tuple[Dict[str, object], list[str]]:
    """Convert CSV string values to appropriate Python types.

    Returns a tuple of the converted row data and a list of validation errors
    encountered.  Errors are reported rather than raised so that all issues in a
    file can be collected and reported together.
    """

    columns = {c.name: c.type for c in Sample.__table__.columns}
    data: Dict[str, object] = {}
    errors: list[str] = []

    for key, value in row.items():
        if value in (None, ""):
            continue

        col_type = columns.get(key)
        if isinstance(col_type, Date):
            try:
                data[key] = date.fromisoformat(value)
            except ValueError:
                errors.append(f"{key}: invalid date {value!r}")
        elif isinstance(col_type, Enum):
            if value not in col_type.enums:
                allowed = ", ".join(col_type.enums)
                errors.append(f"{key}: {value!r} is not one of {allowed}")
            else:
                data[key] = value
        else:
            data[key] = value

    return data, errors


def _load_csv(url: str, csv_path: str, *, echo: bool = False) -> None:
    """Load ``Sample`` rows from a CSV file into the database.

    The CSV file is fully validated before any rows are written.  If invalid
    values are encountered (e.g. for enumerated fields) a :class:`ValueError`
    is raised summarizing all issues.
    """

    Session = get_session_maker(url, echo=echo)
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)
        errors: list[str] = []
        samples: list[Sample] = []
        for lineno, row in enumerate(reader, start=2):
            data, row_errors = _convert_row(row)
            if row_errors:
                errors.append(f"line {lineno}: " + "; ".join(row_errors))
            else:
                samples.append(Sample(**data))

        if errors:
            raise ValueError("Invalid data encountered\n" + "\n".join(errors))

    with Session() as session:
        session.add_all(samples)
        session.commit()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="hvp-db")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="initialize a new database")
    p_init.add_argument("url", help="database URL, e.g. sqlite:///hvp.db")
    p_init.add_argument("--echo", action="store_true", help="echo SQL statements")

    p_load = subparsers.add_parser("load", help="load sample rows from a CSV file")
    p_load.add_argument("url", help="database URL")
    p_load.add_argument("csvfile", help="path to CSV file")
    p_load.add_argument("--echo", action="store_true", help="echo SQL statements")

    p_web = subparsers.add_parser("web", help="run the Flask web application")
    p_web.add_argument("url", help="database URL")
    p_web.add_argument("password", help="shared password for login")

    args = parser.parse_args(argv)

    if args.command == "init":
        init_engine(args.url, echo=args.echo)
    elif args.command == "load":
        try:
            _load_csv(args.url, args.csvfile, echo=args.echo)
        except ValueError as exc:
            parser.error(str(exc))
    elif args.command == "web":
        run_web_app(args.url, args.password)
    else:
        parser.error(f"Unknown command {args.command}")


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    main()
