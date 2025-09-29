import os
import uuid
from flask import Flask, g
from hvp_db.database import db_session
from hvp_db.routes import bp as hvp_bp
from typing import Optional


def create_app(
    database_url: str,
    shared_password: Optional[str] = None,
) -> Flask:
    """Create and configure the Flask application.

    Parameters
    ----------
    database_url:
        Database URL passed to :func:`hvp_db.get_session_maker`.
    shared_password:
        Password required to log in. If not provided, it will be read from
        the environment variable `HVP_DB_PASSWORD`
    """
    app = Flask(__name__)
    app.secret_key = uuid.uuid4().hex
    if shared_password is None:
        shared_password = os.environ.get("HVP_DB_PASSWORD")
    assert shared_password is not None, (
        "No shared password provided. Set the HVP_DB_PASSWORD environment variable or "
        "pass a password to create_app."
    )
    app.config["SHARED_PASSWORD"] = shared_password

    app.config["SESSION_COOKIE_PATH"] = "/hvp"

    @app.before_request
    def create_session():
        g.db = db_session(database_url)()

    @app.teardown_request
    def remove_session(exception=None):
        db = g.pop("db", None)
        if db is not None:
            if exception:
                db.rollback()
            else:
                db.commit()
            db.close()

    app.register_blueprint(hvp_bp, url_prefix="/hvp")

    return app


def main(database_url: str, shared_password: str) -> None:
    app = create_app(database_url, shared_password)
    app.run(debug=True)


if __name__ == "__main__":
    main("sqlite:///hvp.db", "password")
