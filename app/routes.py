from app import app
from flask import render_template


@app.route('/')
def index():
    user = {'username': 'Jordy'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html", user=user, posts=posts)
