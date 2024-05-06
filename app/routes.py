from app import app
from flask import render_template, flash, redirect,request,jsonify,url_for
from app.forms import LoginForm,RegistrationForm
import os

from flask_login import current_user, login_user
import sqlalchemy as sa
from app import db
from app.models import User
from flask_login import login_required

from flask import request
from urllib.parse import urlsplit

@app.context_processor
def inject_global_variable():
    return dict(company="EcoHUB")

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('users/login.html', title='Sign In', form=form)



@app.route('/home')
@login_required
def home():
    print('aaaaa')
    return render_template('/home/home.html',hideNav = True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email_address=form.email_address.data, first_name = form.first_name.data,
                    last_name = form.last_name.data, is_seller = form.become_seller.data, shop_name = form.shop_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('regsiter successfully {}'.format(form.username.data))
        return redirect(url_for('home'))
    return render_template('/users/signup.html', form=form,hideNav=True)

@app.route('/sdg_img_dirs', methods=['POST'])
def get_sdg_img_dirs():
    data = request.json
    sdg_id = data.get('sdg_id')
    image_dirs = ['sdg_images/dir1', 'sdg_images/dir2', 'sdg_images/dir3']
    return jsonify({'image_dirs': image_dirs})

products = [
    {'title': 'Cloth 1 is very long title with long description in the title', 'price': 29.99, 'quantity': 2, 'location': 'Belmont', 'img':'product_image/image.jpg',
     'description':'This is the description of the Cloth1.'*10},
    {'title': 'Cloth 2', 'price': 39.99, 'quantity': 1, 'location': 'East Perth', 'img':'product_image/image2.jpg',
     'description':'Cloth2.'*5},
    {'title': 'Cloth 3', 'price': 19.99, 'quantity': 3, 'location': 'Nedlands', 'img':'product_image/image3.jpg'}
]

@app.route('/product')
def product():
    return render_template('/product/product.html', products=products)

@app.route('/categories')
def categories():
    categories = [
        {'Men': products[0:2] },
        {'Women': products[1:] }
    ]
    page = request.args.get('page', 1, type=int)
    view = request.args.get('view', 'grid', type=str)
    if page==2:
        print(view)
        categories = [
            {'Men': [products[0]] },
            {'Women': [products[2]] }
        ]
    pages=[1,2]
    return render_template('/product/categories.html', categories=categories, page=page, pages=pages, view=view)

@app.route('/product/<product_id>')
def product_detail(product_id):
    print(product_id)
    product = {'title': 'Cloth 1 is very long title with long description in the title', 'price': 29.99, 'quantity': 2, 'location': 'Belmont', 
               'imgs':['product_image/image.jpg','product_image/image2.jpg','product_image/image3.jpg']*2, 'description':'This is the description of the Cloth1.'*10}
    return render_template('/product/product_detail.html', product=product)
