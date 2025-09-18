"""WSGI entry point for the hvp_web application."""

import os
from hvp_db.app import create_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


# Determine the database URL from the environment, defaulting to the
# project's standard SQLite database if not specified.
DATABASE_URL = os.environ.get("HVP_DB_URI", "sqlite:///hvp.db")

# Determine the script name (URL prefix) from the environment, defaulting to
# the root if not specified.
script_name = os.environ.get("HVP_PROXY_PATH", "/hvp")

# The Flask application object for WSGI servers to use.
app = create_app(database_url=DATABASE_URL)
app = DispatcherMiddleware(app, {script_name: app})
