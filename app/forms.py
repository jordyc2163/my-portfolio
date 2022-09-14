from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from app.models import User
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    email = EmailField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))

class RegisterForm(FlaskForm):
    first_name = StringField(_l('First Name'), validators=[DataRequired()])
    last_name = StringField(_l('Last Name'), validators=[DataRequired()])
    username = StringField(_l('Username'), validators=[DataRequired()])
    email = EmailField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=8, max=20)])
    password2 = PasswordField(_l('Re-enter Password'), validators=[DataRequired(), EqualTo('password')])
    register = SubmitField(_l('Register'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(_l('Username already taken'))
    
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError(_l('Email address already in use'))


class ContactForm(FlaskForm):
    subject = StringField(_l('Subject'), validators=[DataRequired()])
    body = TextAreaField(_l('Message'), validators=[DataRequired(), Length(min = 1, max = 300)])
    send = SubmitField(_l('Send'))

class PostForm(FlaskForm):
    comment = StringField(_l('Comment'), validators=[DataRequired(), Length(min = 1, max = 80)])
    checkbox = BooleanField(_l('Post Anonymously?'))
    post = SubmitField(_l('Post'))

class EditPostForm(FlaskForm):
    edit_comment = StringField(_l('Edit Comment'), validators=[DataRequired(), Length(min = 1, max = 80)])
    edit_checkbox = BooleanField(_l('Post Anonymously?'))
    edit_post = SubmitField(_l('Save Changes'))

class DeletePost(FlaskForm):
    delete = SubmitField(_l('Delete'))