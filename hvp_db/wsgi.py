import os
from hvp_db.app import create_app

# Pull DB URL and other config from environment
DATABASE_URL = os.environ.get("HVP_DB_URI", "sqlite:///./db.sqlite")

# Create the Flask app
app = create_app(database_url=DATABASE_URL)
