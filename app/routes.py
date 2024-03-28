from flask import render_template
from app import app

@app.route('/')
@app.route('/login')
def login():
    return render_template("/users/login.html", title="Home")

@app.route('/index')
def index():
    user = {'username': 'Miguel'}
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
    return render_template("index.html", title="Home", user=user,
    posts=posts)