from datetime import date as date_type

from flask import (
    Blueprint,
    current_app,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from hvp_db.models import Sample


bp = Blueprint("hvp", __name__, url_prefix="/hvp")


### Auth ###
@bp.before_request
def require_login():
    # Skip check if endpoint is unknown (static files, bad requests)
    if request.endpoint is None:
        return

    # These endpoints are allowed without auth
    exempt_endpoints = {"hvp.login", "static"}

    # If already authenticated, continue
    if session.get("authenticated"):
        return

    # If the request is for an exempt endpoint, allow
    if request.endpoint in exempt_endpoints:
        return

    # Prevent redirect loop: don't redirect /hvp/login?next=/hvp/login
    if request.path.startswith(url_for("hvp.login")):
        return

    # Redirect to login page with original path as `next`
    return redirect(url_for("hvp.login", next=request.path))


@bp.route("/login", methods=["GET", "POST"])
def login():
    error = None
    next_url = request.args.get("next") or url_for("hvp.index")

    if request.method == "POST":
        if request.form.get("password") == current_app.config["SHARED_PASSWORD"]:
            session["authenticated"] = True
            return redirect(next_url)
        error = "Incorrect password"

    return render_template("login.html", error=error)


@bp.route("/logout")
def logout():
    session.pop("authenticated", None)
    return redirect(url_for("hvp.login"))


### Pages ###
@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/samples")
def samples():
    table_columns = Sample.__table__.columns
    columns = [c.name for c in table_columns]
    date_columns = []
    for column in table_columns:
        try:
            python_type = column.type.python_type
        except NotImplementedError:
            continue
        if python_type is date_type:
            date_columns.append(column.name)
    return render_template("samples.html", columns=columns, date_columns=date_columns)


### API ###
@bp.route("/api/samples")
def samples_api():
    columns = [c.name for c in Sample.__table__.columns]
    db = g.db
    samples_data = []
    for sample in db.query(Sample).all():
        record = {}
        for col in columns:
            value = getattr(sample, col)
            if isinstance(value, date_type):
                record[col] = value.isoformat()
            else:
                record[col] = value
        samples_data.append(record)
    return jsonify({"data": samples_data})
