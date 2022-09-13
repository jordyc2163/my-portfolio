from crypt import methods
from urllib import request
from app import app
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, ContactForm, PostForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/post', methods = ['POST'], endpoint='post')
@app.route('/send', methods = ['POST'], endpoint='send')
@app.route('/login', methods=['GET', 'POST'], endpoint='login')
@app.route('/register', methods=['GET', 'POST'], endpoint='register')
@app.route('/', methods=['GET'])
def index():
    modal = False
    modal2 = False

    if request.path == '/login':
        modal = True # modal will show on page load
    
    if request.path == '/register':
        modal2 = True

    if current_user.is_authenticated:
        name = current_user.first_name # user's name will be welcomed if already logged in

    form = LoginForm()
    contact_form = ContactForm()
    post_form = PostForm()
    register_form = RegisterForm()


    if register_form.register.data and register_form.validate_on_submit():
        print(register_form.register.data, request.path, register_form.first_name.data, register_form.last_name.data, register_form.username.data, register_form.email.data)
        return redirect(url_for('index'))

    if form.submit.data and form.validate_on_submit():
        print("I'm running for some reason", form.submit.data)
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash("Success! You're in!", 'success')
        return redirect(url_for('index'))
    
    
    if post_form.post.data and post_form.validate_on_submit():
        print(post_form.comment.data, post_form.checkbox.data)
        if current_user.is_anonymous:
            flash('Sorry you must be logged in to do that', 'error')
            return redirect('login')
        flash('Scroll down to see your new post!', 'success')
        return redirect(url_for('index'))

    if contact_form.send.data and contact_form.validate_on_submit():
        print(contact_form.send.data, contact_form.subject.data, contact_form.body.data)
        return redirect(url_for('index'))
   
    return render_template("index.html", form=form, contact_form=contact_form, post_form=post_form, register_form=register_form, modal=modal, modal2=modal2)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

