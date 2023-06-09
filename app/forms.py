from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, validators, PasswordField, IntegerField

# Add any form classes for Flask-WTF here

# UserForm collects user data to be sent to the database
class UserForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = StringField('Password', [validators.InputRequired()])
    firstname = StringField('First Name', [validators.InputRequired()])
    lastname = StringField('Last Name', [validators.InputRequired()])
    email = StringField('Email', [validators.InputRequired()])
    location = StringField('Location', [validators.InputRequired()])
    biography = StringField('Biography', [validators.InputRequired()])

    profile_photo = FileField('Profile Photo', validators=[
                FileRequired(),
                FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!')
            ]
    )

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.InputRequired()])

class NewPost(FlaskForm):
    caption = StringField('Caption', [validators.InputRequired()])

    photo = FileField('Photo', validators=[
                FileRequired(),
                FileAllowed(['jpg', 'png', 'jpeg'], 'Images Only!')
            ]
    )