from flask import render_template
from app import app

@app.context_processor
def inject_global_variable():
    return dict(company="EcoHUB")

@app.route('/')
@app.route('/login')
def login():
    return render_template("/users/login.html", title="Home", hideNav=True)

@app.route('/home')
def home():
    return render_template('/base.html')

@app.route('/signup')
def signup():
    return render_template('/users/signup.html', hideNav=True)
