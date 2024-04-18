from flask import render_template
from app import app

@app.route('/')
@app.route('/login')
def login():
    return render_template("/users/login.html", title="Home")

@app.route('/home')
def home():
    company = "Name1"
    return render_template('/base.html', company=company)