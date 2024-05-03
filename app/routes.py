from app import app
from flask import render_template, flash, redirect,request,jsonify,url_for
from app.forms import LoginForm
import os
    
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
        return redirect(url_for('home'))
    return render_template('users/login.html', title='Sign In', form=form, hideNav = True)

@app.route('/home')
def home():
    return render_template('/home/home.html',hideNav = True)

@app.route('/signup')
def signup():
    return render_template('/home/home.html', hideNav=True)
@app.route('sdg_img_dirs',methods=['POST'])
def get_sdg_img_dirs():
    data = request.json
    sdg_id = data.get('sdg_id')
    image_dirs = ['sdg_images/dir1', 'sdg_images/dir2', 'sdg_images/dir3']
    return jsonify({'image_dirs': image_dirs})

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

