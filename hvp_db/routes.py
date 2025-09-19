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
    columns = [c.name for c in Sample.__table__.columns]
    return render_template("samples.html", columns=columns)


### API ###
@bp.route("/api/samples")
def samples_api():
    columns = [c.name for c in Sample.__table__.columns]
    db = g.db
    samples_data = []
    for sample in db.query(Sample).all():
        samples_data.append({col: getattr(sample, col) for col in columns})
    print(samples_data)
    return jsonify({"data": samples_data})
