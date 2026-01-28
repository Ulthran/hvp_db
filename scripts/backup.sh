#!/bin/bash

set -e

echo "Starting backup..."

hvp_db=/var/www/html/hvp/db/backups/$(date -I).sqlite

sqlite3 /var/www/html/hvp/db/db.sqlite ".backup '$hvp_db'"

echo "Backup completed successfully: $hvp_db"
