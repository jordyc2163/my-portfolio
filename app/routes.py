from crypt import methods
from email import message
from urllib import request
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, ContactForm, PostForm, EditPostForm, RegisterForm, DeletePost
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post, Message
from werkzeug.urls import url_parse
from datetime import datetime


# This application will do all functionality on the same page

@app.route('/edit/post/<id>', methods=['GET', 'POST'], endpoint=('edit'))
@app.route('/post', methods = ['POST'], endpoint='post')
@app.route('/send', methods = ['POST'], endpoint='send')
@app.route('/login', methods=['GET', 'POST'], endpoint='login')
@app.route('/register', methods=['GET', 'POST'], endpoint='register')
@app.route('/', methods=['GET'])
def index(id=''):
    modal = False
    modal2 = False
    modal3 = False

    form = LoginForm()
    contact_form = ContactForm()
    post_form = PostForm()
    register_form = RegisterForm()
    edit_post_form = EditPostForm()
    delete_post = DeletePost()

    all_posts = Post.query.all()

    # Conditional rendering of modals based on path

    if request.method == 'GET':
        if request.path == '/login':
            if current_user.is_authenticated:
                flash('You are already logged in', 'error')
                return redirect(url_for('index'))
            modal = True # modal will show on page load
        
        if request.path == '/register':
            if current_user.is_authenticated:
                flash('You are already have an account', 'error')
                return redirect(url_for('index'))
            modal2 = True

        if request.path == f'/edit/post/{id}':
            post = current_user.posts.filter_by(id=id).first()
            if not post:
                flash('This post does not belong to this user', 'error')
                return redirect(url_for('index'))
            edit_post_form.edit_comment.data = post.body
            edit_post_form.edit_checkbox.data = post.anonymous
            modal3 = True


    # Conditional form submissions for each route
    if request.method == 'POST':
        if register_form.register.data and register_form.validate_on_submit():
            user = User(first_name=register_form.first_name.data, last_name=register_form.last_name.data, username=register_form.username.data, email=register_form.email.data)
            user.set_password(register_form.password.data)
            print(user.first_name, user.last_name, user.username, user.email, user.password_hash, user.id)
            db.session.add(user)
            db.session.commit()
            flash("Thank you for registering to my website!", "success")
            login_user(user)
            return redirect(url_for('index'))

        if form.submit.data and form.validate_on_submit():
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
            if current_user.is_anonymous:
                flash('Sorry you must be logged in to do that', 'error')
                return redirect('login')
            post = Post(body=post_form.comment.data, anonymous=post_form.checkbox.data, author=current_user)
            db.session.add(post)
            db.session.commit()
            print(post.author, post.body, post.anonymous, post.timestamp)
            flash('Scroll down to see your new post!', 'success')
            return redirect(url_for('index'))

        if edit_post_form.edit_post.data and edit_post_form.validate_on_submit():
            if current_user.is_anonymous:
                flash('Sorry you must be logged in to do that', 'error')
                return redirect('login')
            original_post = Post.query.filter_by(id=id).first()
            edit_post = original_post
            if edit_post:
                edit_post.body = edit_post_form.edit_comment.data
                edit_post.anonymous = edit_post_form.edit_checkbox.data
                edit_post.timestamp = datetime.utcnow()
                
                db.session.commit()

                flash('Post updated successfully', 'success')
                return redirect(url_for('index'))
            
            flash('Cannot find the post you are looking for', 'error')
            return redirect(url_for('index'))
        

        if contact_form.send.data and contact_form.validate_on_submit():
            print(contact_form.send.data, contact_form.subject.data, contact_form.body.data)
            message = Message(subject=contact_form.subject.data, body=contact_form.body.data, sender=current_user)
            print(message)
            db.session.add(message)
            db.session.commit()

            return redirect(url_for('index'))
   
    return render_template("index.html", form=form, contact_form=contact_form, post_form=post_form, register_form=register_form, edit_post_form=edit_post_form, delete_post=delete_post, all_posts=all_posts, modal=modal, modal2=modal2, modal3=modal3, post_id=id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/messages')
@login_required
def messages():
    messages = Message.query.all()
    return render_template('messages.html', messages=messages)

@app.route('/post/<id>', methods=['POST'])
@login_required
def delete_post(id):
    post = current_user.posts.filter_by(id=id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        flash('Post successfully deleted', 'success')
        return redirect(url_for('index'))
    
    flash('The post does not belong to the current user', 'error')
    return redirect(url_for('index'))


