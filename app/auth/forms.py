from flask_wtf import FlaskForm #importing a class
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.auth.models import User
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField("Username",
                    validators=[DataRequired(),Length(min=2, max=20, message="must be more than 2 and less than 20 characters")])
                    #having a bracket next to class means activating
    email = StringField("Email address", validators=[DataRequired(),Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Please confirm your password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already registered")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is already reigstered")


class LoginForm(FlaskForm):
     email = StringField("Email address", validators=[DataRequired(), Email()])
     password = PasswordField("Password",validators=[DataRequired()])
     remember = BooleanField("I want to remember my Login settings")
     submit = SubmitField("Login")

     def validate_email(self, email):
         user = User.query.filter_by(email=email.data).first()
         if not user:
             raise ValidationError("Email doesn't exist")



class UpdateAccount(FlaskForm):
    username = StringField("Username",
                    validators=[DataRequired(),Length(min=2, max=20,message="must be more than 2 and less than 20 characters")])
                    #having a bracket next to class means activating

    email = StringField("Email address", validators=[DataRequired(),Email()])

    picture = FileField("upload your picture", validators=[FileAllowed(['jpg','png','jpeg','gif'])])


    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is already registered")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() #sends database query to see if the same email exists
            if user:
                raise ValidationError("This email is already reigstered")

class ResetPassword(FlaskForm):
    email = StringField("Email address", validators=[DataRequired(),Email()])

    submit = SubmitField("Send Request")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #sends database query to see if the same email exists
        if not user:
            raise ValidationError("This email doesn't exist.")


class ResetPasswordForm(FlaskForm):

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Please confirm your password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset")
