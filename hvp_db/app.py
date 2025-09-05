from flask import Flask, jsonify
from hvp_db import get_session_maker, Sample
from sqlalchemy import select


def create_app(database_url: str) -> Flask:
    """Create and configure the Flask application.

    Parameters
    ----------
    database_url:
        Database URL passed to :func:`hvp_db.get_session_maker`.
    """
    app = Flask(__name__)
    SessionMaker = get_session_maker(database_url)

    @app.route("/")
    def index() -> str:
        return "Human Virome Project Web"

    @app.route("/samples")
    def samples():
        with SessionMaker() as session:
            sample_ids = [s.sample_id for s in session.scalars(select(Sample)).all()]
        return jsonify(sample_ids)

    return app


def main(database_url: str) -> None:
    """Run the Flask application in debug for dev."""
    app = create_app(database_url)
    app.run(debug=True)


if __name__ == "__main__":
    main("sqlite:///hvp.db")
