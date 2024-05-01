from app import app
from flask import render_template, flash, redirect, request, jsonify
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
        return redirect(url_for('index'))
    return render_template('users/login.html', title='Sign In', form=form)

@app.route('/home')
def home():
    return render_template('/home/home.html')

@app.route('/sdg_img_dirs', methods=['POST'])
def get_sdg_img_dirs():
    is_dark_mode = request.json.get('isDarkMode')
    path = 'web-inverted'
    if is_dark_mode:
        path = 'web'
    img_dir = os.path.join(app.root_path, 'static', 'img', 'sdg', path)
    sdg_images = [path+'/'+img for img in os.listdir(img_dir) if img.endswith('png')]
    return jsonify({'sdg_images': sdg_images})

@app.route('/signup')
def signup():
    return render_template('/users/signup.html', hideNav=True)
products = [
    {'title': 'Cloth 1 is very long title with long description in the title', 'price': 29.99, 'quantity': 2, 'location': 'Belmont', 'img':'static/img/product_image/image.jpg'},
    {'title': 'Cloth 2', 'price': 39.99, 'quantity': 1, 'location': 'East Perth', 'img':'static/img/product_image/image2.jpg'},
    {'title': 'Cloth 3', 'price': 19.99, 'quantity': 3, 'location': 'Nedlands', 'img':'static/img/product_image/image3.jpg'}
]

@app.route('/product')
def product():
    return render_template('/product/product.html', products=products)
