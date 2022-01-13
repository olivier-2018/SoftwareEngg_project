from flask import Blueprint, render_template
from flask_login import current_user, login_required
from flask import current_app

profile = Blueprint("profile", __name__)


@profile.route("/profile", methods=["GET"])
@login_required
def profile():
    current_app.logger.info("Redirected to profile page.")

    return render_template("profile.html", user=current_user)
