from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from flask import current_app

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    current_app.logger.info("Redirected to login page.")
    if request.method == "POST":
        username = request.form.get("userName")
        current_app.logger.debug("entered username=%s", username)
        password = request.form.get("password")
        # current_app.logger.debug("entered password=%s",password)

        user = User.query.filter_by(user_name=username).first()
        current_app.logger.debug("Search for username in db (None=not existing): %s", user)

        if user:
            current_app.logger.debug("User found: %s", user)
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                current_app.logger.info("User Logged in successfully!")

                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
                current_app.logger.info("Incorrect password")
        else:
            flash("Username does not exist.", category="error")
            current_app.logger.info("Incorrect username")

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    current_app.logger.info("Redirected to Sign-up page.")
    if request.method == "POST":
        username = request.form.get("userName")
        current_app.logger.debug("selected username=%s", username)
        firstname = request.form.get("firstName")
        current_app.logger.debug("selected firstName=%s", firstname)
        lastname = request.form.get("lastName")
        current_app.logger.debug("selected lastName=%s", lastname)
        email = request.form.get("email")
        current_app.logger.debug("selected email=%s", email)
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(user_name=username).first()
        current_app.logger.info("Search for username in db (None=not existing): %s", user)

        if user:
            flash("Username already taken.", category="error")
            current_app.logger.info("Username already taken.")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
            current_app.logger.info("Email must be greater than 3 characters.")
        elif len(firstname) < 2:
            flash("First name must be greater than 1 character.", category="error")
            current_app.logger.info("First name must be greater than 1 character.")
        elif len(lastname) < 2:
            flash("Last name must be greater than 1 character.", category="error")
            current_app.logger.info("Last name must be greater than 1 character.")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
            current_app.logger.info("Passwords don't match.")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
            current_app.logger.info("Password must be at least 7 characters.")
        else:
            new_user = User(
                user_name=username, email=email, first_name=firstname, last_name=lastname, password=generate_password_hash(password1, method="sha256")
            )
            current_app.logger.info("New user created:%s", username)

            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            current_app.logger.info("Account created!")

            return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    current_app.logger.info("Redirected to logout page.")
    logout_user()
    current_app.logger.info("User %s logged out.", current_user)
    return redirect(url_for("auth.login"))


@auth.route("/profile", methods=["GET"])
@login_required
def profile():
    current_app.logger.info("Redirected to profile page.")
    return render_template("profile.html", user=current_user)


@auth.route("/about")
def about():
    current_app.logger.info("Redirected to about page.")
    return render_template("about.html", user=None)
