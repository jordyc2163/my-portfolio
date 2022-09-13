from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    register = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Email address already in use')


class ContactForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Message', validators=[DataRequired(), Length(min = 1, max = 300)])
    send = SubmitField('Send')

class PostForm(FlaskForm):
    comment = StringField('Comment', validators=[DataRequired(), Length(min = 1, max = 80)])
    checkbox = BooleanField('Post Anonymously?')
    post = SubmitField('Post')

class EditPostForm(FlaskForm):
    edit_comment = StringField('Edit Comment', validators=[DataRequired(), Length(min = 1, max = 80)])
    edit_checkbox = BooleanField('Post Anonymously?')
    edit_post = SubmitField('Save Changes')

class DeletePost(FlaskForm):
    delete = SubmitField('Delete')