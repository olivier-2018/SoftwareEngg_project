from flask import Blueprint, flash, render_template
from flask_login import current_user, login_required
from flask import current_app

misc = Blueprint("misc", __name__)


@misc.route("/home")
@misc.route("/")
def home():
    """Makes a digit prediction by uploading a wav file using the audio MNIST ML model

    Returns:
        [render_template]: Render template object with prediction variable (int)
    """
    if not current_user.is_authenticated:
        flash("Please log in to access full app functionality !", category="error")
        return render_template("home.html", user=None)
    else:
        return render_template("home.html", user=current_user)


@misc.route("/profile", methods=["GET"])
@login_required
def profile():
    current_app.logger.info("Redirected to profile page.")
    return render_template("profile.html", user=current_user)


@misc.route("/logfile", methods=["GET"])
@login_required
def get_logfile():
    current_app.logger.info("Redirected to logfile page.")
    return render_template("logfile.html", user=current_user, filename="app.log")


@misc.route("/ver_history", methods=["GET"])
@login_required
def get_ver_history():
    current_app.logger.info("Redirected to ver_history page.")
    return render_template(
        "ver_history.html",
        user=current_user,
    )


@misc.route("/about")
def about():
    current_app.logger.info("Redirected to about page.")

    if not current_user.is_authenticated:
        return render_template("about.html", user=None)
    else:
        return render_template("about.html", user=current_user)
