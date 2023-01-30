from __future__ import annotations
from flask import Flask, render_template, request, redirect, url_for
from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
from flask_bcrypt import Bcrypt
import os
from flaskapp.models import User, db
from flaskapp.forms import (
    ResetPasswordForm,
    SignUpForm,
    LogInForm,
    ForgotPasswordForm,
    ResendForm,
)
from flaskapp.email import (
    EXPIRED,
    VERIFY_EMAIL_SALT,
    RESET_SALT,
    mail,
    mail_settings,
    confirm_token,
    generate_token,
    send_token_email,
)
from flaskapp.translator_bp import translator

_dir = os.path.dirname(__file__)
template_dir = os.path.join(_dir, "flaskapp/templates")
static_dir = os.path.join(_dir, "flaskapp/static")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.register_blueprint(translator)
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY"
)  # "something_secret"  # .from_object(MyConfig)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
for key, value in mail_settings.items():
    app.config[key] = value
encrypter = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db.init_app(app)
mail.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


DEBUG = True

with app.app_context():
    db.create_all()


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LogInForm()
    if not form.validate_on_submit():
        return render_template(
            "login.html", form=form, title="Login", user=current_user, myError=False
        )

    user = User.query.filter_by(username=form.username.data).first()
    # invalid username
    if not user:
        return render_template(
            "login.html",
            form=form,
            title="Login",
            user=current_user,
            myError="username",
        )
    # invalid password
    if not encrypter.check_password_hash(user.password, form.password.data):
        return render_template(
            "login.html",
            form=form,
            title="Login",
            user=current_user,
            myError="password",
        )
    # user not yet validated
    if not user.confirmed:
        return render_template(
            "login.html",
            form=form,
            title="Login",
            user=current_user,
            myError="verification",
        )

    login_user(user)
    return redirect(url_for("translator.sweet"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if not form.validate_on_submit():
        return render_template(
            "signup.html", form=form, title="Signup", user=current_user
        )

    hashed_pw = encrypter.generate_password_hash(form.password.data)
    new_user = User(
        username=form.username.data,
        password=hashed_pw,
        email=form.email.data,
    )
    db.session.add(new_user)
    db.session.commit()
    token = generate_token(form.email.data, VERIFY_EMAIL_SALT)
    confirm_url = url_for("confirm_email", token=token, _external=True)
    html = render_template(
        "email.html",
        message="Thank you for signing up! Please click this link to activate your account:",
        confirm_url=confirm_url,
    )
    send_token_email(app, new_user.email, "Confirm Email", html)
    return redirect(url_for("login"))


@app.route("/index")
def index():
    return render_template("index.html", title="About", user=current_user)


@app.route("/resources")
def resources():
    return render_template("resources.html", title="Resources", user=current_user)


@app.route("/team")
def team():
    return render_template("team.html", title="Team", user=current_user)


@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    form = ForgotPasswordForm()
    if not form.validate_on_submit():
        return render_template(
            "forgot.html", form=form, title="Forgot", user=current_user
        )

    user = User.query.filter_by(username=form.username.data).first()
    # invalid username
    if user is None:
        return render_template(
            "forgot.html",
            form=form,
            title="Forgot",
            user=current_user,
            myError="Invalid username!",
        )
    token = generate_token(f"{user.email} {user.reset_count}", RESET_SALT)
    confirm_url = url_for("reset", token=token, _external=True)
    html = render_template(
        "email.html",
        message="Please use the following link to reset your password:",
        confirm_url=confirm_url,
    )
    send_token_email(app, user.email, "Reset Password", html)
    return redirect(url_for("login"))


@app.route("/resend", methods=["GET", "POST"])
def resend():
    form = ResendForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            return render_template(
                "resend.html",
                form=form,
                title="Resend",
                user=current_user,
                myError="No user with that username found!",
            )
        if user.confirmed:
            return render_template(
                "resend.html",
                form=form,
                title="Resend",
                user=current_user,
                myError="User is already verified. Please log in.",
            )
        token = generate_token(user.email, VERIFY_EMAIL_SALT)
        confirm_url = url_for("confirm_email", token=token, _external=True)
        html = render_template(
            "email.html",
            message="Thank you for signing up! Please click this link to activate your account:",
            confirm_url=confirm_url,
        )
        send_token_email(app, user.email, "Confirm Email", html)
        return redirect(url_for("login"))

    return render_template("resend.html", form=form, title="Resend", user=current_user)


@app.route("/reset/<token>", methods=["GET", "POST"])
def reset(token):
    form = ResetPasswordForm()
    if request.method == "GET":
        result = confirm_token(token, RESET_SALT)
        if result == EXPIRED:
            return
        email, count = result.split()
        user = User.query.filter_by(email=email).first_or_404()
        if user.reset_count != int(count):
            return redirect(url_for("login"))
        form = ResetPasswordForm(username=user.username, reset_count=count)
        return render_template(
            "reset.html", form=form, title="Reset", user=current_user
        )
    elif form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.reset_count != int(form.reset_count.data):
            return redirect(url_for("login"))
        hashed_pw = encrypter.generate_password_hash(form.password.data)
        user.password = hashed_pw
        user.reset_count += 1
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("reset.html", form=form, title="Reset", user=current_user)


@app.route("/confirm/<token>")
def confirm_email(token):
    email = confirm_token(token, VERIFY_EMAIL_SALT)
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        print("already confirmed")
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
    return redirect(url_for("login"))


if __name__ == "__main__":
    if DEBUG:
        app.run(debug=True)
    else:
        app.run(host="0.0.0.0", port=5000, debug=False)
