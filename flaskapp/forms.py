from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, HiddenField
from wtforms.validators import InputRequired, Length, ValidationError, Email
import os

from .models import User

# TODO need to test whether or not this works
EMAIL_REGEX = r"\b^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$\b"

KEY = os.environ.get("SIGNUP_KEY")


class SignUpForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )
    key = PasswordField(render_kw={"placeholder": "Key"})
    email = EmailField(
        validators=[InputRequired(), Email(), Length(min=6, max=120)],
        render_kw={"placeholder": "Email"},
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        existing_user_names = User.query.filter_by(username=username.data).first()
        if existing_user_names:
            raise ValidationError(
                "The username already exists. Please choose a different username."
            )

    def validate_key(self, key):
        if key.data != KEY:
            raise ValidationError("The provided key is not valid.")

    def validate_email(self, email):
        existing_email = User.query.filter_by(email=email.data).first()
        if existing_email:
            raise ValidationError("This email is already in use.")
        # see if this check is necessary
        # if not re.match(EMAIL_REGEX, email.data):
        #     print(re.match(EMAIL_REGEX, email.data))
        #     raise ValidationError("Invalid email!")


class LogInForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )
    submit = SubmitField("Log In")


class ForgotPasswordForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    submit = SubmitField("Send Email")


class ResetPasswordForm(FlaskForm):
    username = HiddenField()
    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )
    reset_count = HiddenField()
    submit = SubmitField("Reset Password")


class ResendForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )
    submit = SubmitField("Resend Email")
