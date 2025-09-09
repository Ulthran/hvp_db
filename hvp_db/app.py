import os
import uuid
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from hvp_db.models import get_session_maker, Sample
from sqlalchemy import select
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
    SessionMaker = get_session_maker(database_url)

    ### Auth ###
    @app.before_request
    def require_login():
        if request.endpoint not in {"login", "static"} and not session.get(
            "authenticated"
        ):
            return redirect(url_for("login", next=request.path))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            if request.form.get("password") == app.config["SHARED_PASSWORD"]:
                session["authenticated"] = True
                return redirect(request.args.get("next") or url_for("index"))
            error = "Incorrect password"
        return render_template("login.html", error=error)

    @app.route("/logout")
    def logout():
        session.pop("authenticated", None)
        return redirect(url_for("login"))

    ### Pages ###
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/samples")
    def samples():
        columns = [c.name for c in Sample.__table__.columns]
        return render_template("samples.html", columns=columns)

    ### API ###
    @app.route("/api/samples")
    def samples_api():
        with SessionMaker() as session:
            columns = [c.name for c in Sample.__table__.columns]
            samples_data = []
            for sample in session.scalars(select(Sample)).all():
                samples_data.append({col: getattr(sample, col) for col in columns})
        return jsonify({"data": samples_data})

    return app


def main(database_url: str, shared_password: str) -> None:
    app = create_app(database_url, shared_password)
    app.run(debug=True)


if __name__ == "__main__":
    main("sqlite:///hvp.db", "password")
