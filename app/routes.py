from app import app,db
from app.forms import LoginForm,RegistrationForm,ProductForm
from app.models import Product
import os
from flask import render_template, flash, redirect,request,jsonify,url_for,flash,Blueprint
from flask_login import current_user, login_user,login_required,logout_user

    
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
    print('aaaaa')
    return render_template('/home/home.html',hideNav = True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
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

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            product_name=form.product_name.data,
            category=form.category.data,
            price=form.price.data,
            quantity=form.quantity.data,
            condition=form.condition.data,
            location=form.location.data  # Handling new field
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!')
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

