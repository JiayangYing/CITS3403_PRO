from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm

@app.context_processor
def inject_global_variable():
    return dict(company="EcoHUB")

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('users/login.html', title='Sign In', form=form)

@app.route('/home')
def home():
    return render_template('/base.html')

@app.route('/signup')
def signup():
    return render_template('/users/signup.html', hideNav=True)
