from flask import render_template, flash, redirect,request,jsonify,url_for,Blueprint
from flask_login import current_user, login_user,login_required,logout_user
from app import app,db
from app.models import User,Product, Order
from app.forms import \
    LoginForm, RegistrationForm, ProductForm, ProfileForm, EditProfileForm, \
    ChangePasswordForm, UpdateAccountForm, DeactivateAccountForm, Orderform
from urllib.parse import urlsplit
import os
import sqlalchemy as sa

@app.context_processor
def inject_global_variable():
    return dict(company="EcoHUB")

@app.route('/error')
@app.errorhandler(404)
def error(error = None):
    return render_template('/layout/page_not_found.html'), 404

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
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))
        if not user.is_active:
            flash('User deactivated. Please contact admin.', 'error')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home')
        flash('Successfully login!', 'success')
        return redirect(next_page)
    return render_template('users/login.html', title='Sign In', form=form)

@app.route('/home')
def home():
    return render_template('/home/home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            is_seller = form.become_seller.data, 
            email_address=form.email_address.data, 
            postcode = form.postcode.data,
            address = form.address.data,
            contact_no = form.contact_no.data,
            shop_name = form.shop_name.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Register successfully {}'.format(form.username.data), 'success')
        return redirect(url_for('login'))
    return render_template('/users/signup.html', form=form)

@app.route('/sdg_img_dirs', methods=['POST'])
def get_sdg_img_dirs():
    is_dark_mode = request.json.get('isDarkMode')
    path = 'web-inverted'
    if is_dark_mode:
        path = 'web'
    img_dir = os.path.join(app.root_path, 'static', 'img', 'sdg', path)
    sdg_images = [path+'/'+img for img in os.listdir(img_dir) if img.endswith('png')]
    return jsonify({'sdg_images': sdg_images})

products = [
    {'title': 'Cloth 1 is very long title with long description in the title', 'price': 29.99, 'quantity': 2, 'location': 'Belmont', 'img':'product_image/image.jpg',
     'description':'This is the description of the Cloth1.'*10},
    {'title': 'Cloth 2', 'price': 39.99, 'quantity': 1, 'location': 'East Perth', 'img':'product_image/image2.jpg',
     'description':'Cloth2.'*5},
    {'title': 'Cloth 3', 'price': 19.99, 'quantity': 3, 'location': 'Nedlands', 'img':'product_image/image3.jpg'}
]

@app.route('/product')
def product():
    query = sa.select(Product).order_by(Product.created_on.desc()).limit(10)
    products = db.session.scalars(query).all()
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

@app.route('/product/<product_id>', methods=['GET'])
@login_required
def product_detail(product_id):
    product = db.first_or_404(sa.select(Product).where(Product.id == product_id))
    if not product:
        return url_for('error')
    form = Orderform()
    form.set_product_qty(product.quantity)
    form.set_form_data()
    return render_template('/product/product_detail.html', product=product, form=form)

@app.route('/contact_seller/<product_id>', methods=['POST'])
@login_required
def contact_seller(product_id):
    product = db.first_or_404(sa.select(Product).where(Product.id == product_id))
    if not product:
        return url_for('error')
    form = Orderform()
    form.set_product_qty(product.quantity)
    if form.validate_on_submit():
        order = Order(
            quantity=form.quantity.data,
            first_name=form.first_name.data, 
            last_name = form.last_name.data,
            email_address = form.email_address.data,
            postcode = form.postcode.data, 
            contact_no = form.contact_no.data,
            remarks = form.remarks.data,
            product_id = product_id,
            buyer = current_user
        )
        db.session.add(order)
        # current_user.add_order()
        db.session.commit()
        flash('Your order request has been sent!', 'success')
        return redirect(url_for('product'))
    return render_template('/product/product_detail.html', product=product, form=form, show_modal=True)

@app.route('/seller')
@login_required
def seller():
    if(not current_user.is_seller):
        return redirect(url_for('error'))
    page = request.args.get('page', 1, type=int)
    products = db.paginate(current_user.get_products(), page=page, 
                           per_page=app.config['PRODUCT_LISTING_PER_PAGE'], 
                           error_out=False)
    for pro in products:
        pro.orders = pro.get_pending_order_counts()
    next_url, prev_url, pages = None, None, []
    if products.has_prev:
        prev_url = url_for('seller', page=products.prev_num)
        pages.append(page-1)
    pages.append(page)
    if products.has_next:
        next_url = url_for('seller', page=products.next_num)
        pages.append(page+1)
    return render_template('/seller/product.html', products=products.items, pages = pages,
                           next_url=next_url, prev_url=prev_url)

@app.route('/profile')
@login_required
def profile():
    form = ProfileForm()
    account_form = UpdateAccountForm()
    deactivate_form = DeactivateAccountForm()
    if request.method == 'GET':
        form.set_form_data()
        account_form.set_form_data()
    return render_template('/users/profile.html', form=form, account_form=account_form, deactivate_form=deactivate_form)
    
@app.route('/manage_product/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if request.method == 'GET':
        form.set_form_data()
    if form.validate_on_submit():
        product = Product(
            product_name=form.product_name.data,
            category=form.category.data,
            price=form.price.data,
            quantity=form.quantity.data,
            condition=form.condition.data,
            location=form.location.data,
            description = form.description.data,
            owner = current_user
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('seller'))
    return render_template('/manage_product/add.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successfully', 'success')
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    change_pass_form = ChangePasswordForm()
    if request.method == 'GET':
        form.set_form_data()
    elif form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.email_address = form.email.data
        current_user.postcode = form.postcode.data
        current_user.address = form.address.data
        db.session.commit()
        flash('Your profile details have been saved.', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('users/edit_profile.html', form=form, pass_form = change_pass_form)

@app.route('/update_account_type', methods=['GET', 'POST'])
@login_required
def update_account_type():
    form = ProfileForm()
    form.set_form_data()
    account_form = UpdateAccountForm()
    deactivate_form = DeactivateAccountForm()
    user = db.session.scalar(sa.select(User).where(User.username == current_user.username))
    if account_form.validate_on_submit():
        current_user.is_seller = not user.is_seller
        db.session.commit()
        flash('Your account type has been changed.', 'success')
        return redirect(url_for('profile'))
    return render_template('/users/profile.html', form=form, account_form=account_form, deactivate_form=deactivate_form, show=True)


@app.route('/deactivate', methods=['GET', 'POST'])
@login_required
def deactivate():
    form = ProfileForm()
    form.set_form_data()
    account_form = UpdateAccountForm()
    deactivate_form = DeactivateAccountForm()
    if deactivate_form.validate_on_submit():
        current_user.is_active = False
        db.session.commit()
        flash('Your account is deactivated.', 'success')
        return redirect(url_for('logout'))
    return render_template('/users/profile.html', form=form, account_form=account_form, deactivate_form=deactivate_form, show_modal=True)

@app.route('/change_pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    user = db.session.scalar(
            sa.select(User).where(User.email_address == current_user.email_address))
    form = EditProfileForm()
    form.set_form_data()
    change_pass_form = ChangePasswordForm()
    if change_pass_form.validate_on_submit():
        user.set_password(change_pass_form.new_password.data)
        current_user.password_hash = user.password_hash
        db.session.commit()
        flash('Your password has been changed.', 'success')
        return redirect(url_for('edit_profile'))
    return render_template('users/edit_profile.html', form=form, pass_form = change_pass_form)

@app.route('/get_orders/<product_id>', methods=['POST'])
def get_product_orders(product_id):
    page = request.json.get('page')
    orders = db.paginate(Order.get_orders_by_product_id(self=Order, id=product_id), page=page, 
                           per_page=app.config['ORDER_LISTING_PER_PAGE'], 
                           error_out=False)
    pages = []
    if orders.has_prev:
        pages.append(page-1)
    pages.append(page)
    if orders.has_next:
        pages.append(page+1)
    return jsonify({'orders': [o.to_json() for o in orders], 'pages':pages})

@app.route('/reset_order/<order_id>', methods=['GET'])
def reset_order(order_id):
    Order.reset_pending(order_id)
    return jsonify({'message': 'done.', 'success': True})

@app.route('/approve_order/<order_id>', methods=['POST'])
def approve_order(order_id):
    if current_user.is_authenticated:
        return jsonify(Order.set_pending_status(order_id, current_user.id, 'Approved'))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@app.route('/reject_order/<order_id>', methods=['POST'])
def reject_order(order_id):
    if current_user.is_authenticated:
        return jsonify(Order.set_pending_status(order_id, current_user.id, 'Rejected'))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@app.route('/cancel_order/<order_id>', methods=['POST'])
def cancel_order(order_id):
    if current_user.is_authenticated:
        return jsonify(Order.set_pending_status_from_buyer(order_id, current_user.id, 'Cancelled'))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@app.route('/product_activation/<product_id>', methods=['POST'])
def product_activation(product_id):
    if current_user.is_authenticated:
        return jsonify(Product.activation(product_id, current_user.id))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@app.route('/forget_password')
def f_password():
    return render_template('/users/f_password.html', forget_password=f_password)

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "This is the login page."

@auth.route('/logout')
def logout():
    return "You have been logged out."