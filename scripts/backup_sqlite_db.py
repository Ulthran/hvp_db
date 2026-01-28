#!/usr/bin/env python3
"""Create a timestamped SQLite backup and email the result."""

from __future__ import annotations

import argparse
import os
import shutil
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path


def send_email(
    *,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str | None,
    smtp_password: str | None,
    sender: str,
    recipient: str,
    subject: str,
    body: str,
    starttls: bool,
) -> None:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(smtp_host, smtp_port) as smtp:
        smtp.ehlo()
        if starttls:
            smtp.starttls()
            smtp.ehlo()
        if smtp_user and smtp_password:
            smtp.login(smtp_user, smtp_password)
        smtp.send_message(message)


def backup_sqlite(db_path: Path, backup_dir: Path) -> Path:
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    backup_path = backup_dir / f"{db_path.stem}_{timestamp}{db_path.suffix}"
    shutil.copy2(db_path, backup_path)
    return backup_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a SQLite backup and email the outcome."
    )
    parser.add_argument("--db-path", required=True, help="Path to the SQLite database")
    parser.add_argument(
        "--backup-dir",
        required=True,
        help="Directory where backups should be stored",
    )
    parser.add_argument("--smtp-host", required=True, help="SMTP hostname")
    parser.add_argument("--smtp-port", type=int, default=587, help="SMTP port")
    parser.add_argument("--smtp-user", help="SMTP username (optional)")
    parser.add_argument("--smtp-password", help="SMTP password (optional)")
    parser.add_argument("--email-from", required=True, help="Sender email address")
    parser.add_argument("--email-to", required=True, help="Recipient email address")
    parser.add_argument(
        "--smtp-starttls",
        action="store_true",
        help="Use STARTTLS for SMTP",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    db_path = Path(args.db_path)
    backup_dir = Path(args.backup_dir)
    subject_prefix = f"SQLite backup for {db_path.name}"

    try:
        backup_path = backup_sqlite(db_path, backup_dir)
        subject = f"{subject_prefix}: success"
        body = (
            "Backup completed successfully.\n"
            f"Database: {db_path}\n"
            f"Backup: {backup_path}\n"
            f"Host: {os.uname().nodename}\n"
        )
        send_email(
            smtp_host=args.smtp_host,
            smtp_port=args.smtp_port,
            smtp_user=args.smtp_user,
            smtp_password=args.smtp_password,
            sender=args.email_from,
            recipient=args.email_to,
            subject=subject,
            body=body,
            starttls=args.smtp_starttls,
        )
        return 0
    except Exception as exc:  # noqa: BLE001
        subject = f"{subject_prefix}: failure"
        body = (
            "Backup failed.\n"
            f"Database: {db_path}\n"
            f"Backup directory: {backup_dir}\n"
            f"Host: {os.uname().nodename}\n"
            f"Error: {exc}\n"
        )
        try:
            send_email(
                smtp_host=args.smtp_host,
                smtp_port=args.smtp_port,
                smtp_user=args.smtp_user,
                smtp_password=args.smtp_password,
                sender=args.email_from,
                recipient=args.email_to,
                subject=subject,
                body=body,
                starttls=args.smtp_starttls,
            )
        except Exception as email_exc:  # noqa: BLE001
            print(f"Failed to send failure email: {email_exc}", file=sys.stderr)
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
