from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo  # Updated import
from ..models import User

class RegistrationForm(FlaskForm):
    email = StringField("Your Email Address", validators=[DataRequired(), Email()])
    username = StringField("Your Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo("password_confirm", message="Passwords must match")])
    password_confirm = PasswordField("Confirm Passwords", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    # Custom email validation
    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError("There is an account with that email")

    # Custom username validation
    def validate_username(self, data_field):
        if User.query.filter_by(username=data_field.data).first():
            raise ValidationError("That username is taken")

class LoginForm(FlaskForm):
    email = StringField("Your Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Sign In")
