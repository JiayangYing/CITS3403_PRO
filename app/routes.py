from flask import render_template, flash, redirect,request,jsonify,url_for,current_app, g
from flask_login import current_user, login_user,login_required,logout_user
from app import db
from app.models import User,Product, Order
from app.forms import (
    LoginForm, RegistrationForm, ProductForm, ProfileForm, EditProfileForm,
    ChangePasswordForm, UpdateAccountForm, DeactivateAccountForm, Orderform,
    EditProductForm, SearchForm, ForgotPasswordForm, ResetPasswordForm, SearchProductForm
)
from urllib.parse import urlsplit
import os, json
from app.blueprint import main
from app.email import send_password_reset_email
from app.helper import FilterHelper, PaginatorHelper

@main.context_processor
def inject_global_variable():
    return dict(company="EcoHUB")

@main.route('/error')
def error(error = None):
    return render_template('/layout/page_not_found.html'), 404

@main.route('/forgot_password', methods=['POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    forgot_pass_form = ForgotPasswordForm()
    if forgot_pass_form.validate_on_submit():
        user = User.get_by_email(forgot_pass_form.email.data)
        if not user:
            flash('Email address not registered.','error')
        else:
            send_password_reset_email(user)
            flash('Check your email for the instructions to reset your password','info')
            return redirect(url_for('main.login'))
    return render_template('users/login.html', form=LoginForm(), forgot_pass_form=forgot_pass_form, show_modal=True)

@main.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid method.','error')
        return redirect(url_for('main.home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('main.login'))
    return render_template('users/reset_password_form.html', form=form, token=token)

@main.route('/')
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    forgot_pass_form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('main.login'))
        if not user.is_active:
            flash('User deactivated. Please contact admin.', 'error')
            return redirect(url_for('main.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.home')
        flash('Successfully login!', 'success')
        return redirect(next_page)
    return render_template('users/login.html', form=form, forgot_pass_form = forgot_pass_form)

@main.route('/home')
def home():
    return render_template('/home/home.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
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
        return redirect(url_for('main.login'))
    return render_template('/users/signup.html', form=form)

@main.route('/sdg_img_dirs', methods=['POST'])
def get_sdg_img_dirs():
    is_dark_mode = request.json.get('isDarkMode')
    path = 'web-inverted'
    if is_dark_mode:
        path = 'web'
    img_dir = os.path.join(main.root_path, 'static', 'img', 'sdg', path)
    sdg_images = [path+'/'+img for img in os.listdir(img_dir) if img.endswith('png')]
    return jsonify({'sdg_images': sdg_images})

@main.route('/product')
def product():
    products = Product.get_all(limit=10)
    return render_template('/product/product.html', products=products)

@main.route('/categories')
def categories():
    products = Product.get_all(limit=10)
    page = request.args.get('page', 1, type=int)
    view = request.args.get('view', 'grid', type=str)
    return render_template('/product/categories.html', categories=categories, page=page, pages=pages, view=view)

@main.route('/product/<product_id>', methods=['GET'])
@login_required
def product_detail(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        return redirect(url_for('main.error'))
    form = Orderform()
    form.set_product_qty(product.quantity)
    form.set_form_data()
    return render_template('/product/product_detail.html', product=product, form=form)

@main.route('/contact_seller/<product_id>', methods=['POST'])
@login_required
def contact_seller(product_id):
    product = Product.get_by_id(product_id)
    if not product:
        return redirect(url_for('main.error'))
    form = Orderform()
    form.set_product_qty(product.quantity)
    if request.method == "POST":
        if product.user_id == current_user.id:
            flash('Your cannot order your own item!', 'error')
        elif form.validate_on_submit():
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
            return redirect(url_for('main.product'))
    return render_template('/product/product_detail.html', product=product, form=form, show_modal=True)

@main.route('/product_listing')
@login_required
def product_listing():
    if(not current_user.is_seller):
        return redirect(url_for('main.error'))
    page = request.args.get('page', 1, type=int)
    products = db.paginate(current_user.get_products(), page=page, 
                           per_page=current_app.config['PRODUCT_LISTING_PER_PAGE'], 
                           error_out=False)
    for pro in products:
        pro.orders = pro.get_pending_order_counts()
    paginator = PaginatorHelper('main.product_listing', page, 
                                products.has_prev, products.has_next, 
                                products.prev_num, products.next_num)
    next_url, prev_url, pages = paginator.get_pagination()
    return render_template('/seller/product.html', products=products.items, pages = pages,
                           next_url=next_url, prev_url=prev_url)
@main.route('/order_listing')
@login_required
def order_listing():
    page = request.args.get('page', 1, type=int)
    buyer_orders = db.paginate(current_user.get_own_orders(), page=page, 
                                             per_page=current_app.config['ORDER_LISTING_PER_PAGE'], 
                                             error_out=False)
    next_url, prev_url, pages = None, None, []
    if buyer_orders.has_prev:
        prev_url = url_for('main.order_listing', page=buyer_orders.prev_num)
        pages.append(page-1)
    pages.append(page)
    if buyer_orders.has_next:
        next_url = url_for('main.order_listing', page=buyer_orders.next_num)
        pages.append(page+1)
    return render_template('/buyer/order.html', orders=buyer_orders.items, pages = pages,
                           next_url=next_url, prev_url=prev_url)

@main.route('/profile')
@login_required
def profile():
    form = ProfileForm()
    account_form = UpdateAccountForm()
    deactivate_form = DeactivateAccountForm()
    if request.method == 'GET':
        form.set_form_data()
        account_form.set_form_data()
    return render_template('/users/profile.html', form=form, account_form=account_form, deactivate_form=deactivate_form)
    
@main.route('/manage_product/add', methods=['GET', 'POST'])
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
        return redirect(url_for('main.product_listing'))
    return render_template('/manage_product/add.html', form=form)

@main.route('/edit_product/<id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product=Product.get_by_id(id)
    form = EditProductForm(obj=product)
    form.id = id
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Your product details have been saved.', 'success')
        return redirect(url_for('main.edit_product', id=id))
    return render_template('manage_product/edit.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successfully', 'success')
    return redirect(url_for('main.login'))

@main.route('/edit_profile', methods=['GET', 'POST'])
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
        current_user.avatar = form.avatar.data
        db.session.commit()
        flash('Your profile details have been saved.', 'success')
        return redirect(url_for('main.edit_profile'))
    return render_template('users/edit_profile.html', form=form, pass_form = change_pass_form)

@main.route('/update_account_type', methods=['GET', 'POST'])
@login_required
def update_account_type():
    form = ProfileForm()
    form.set_form_data()
    account_form = UpdateAccountForm()
    deactivate_form = DeactivateAccountForm()
    user = User.get_by_username(current_user.username)
    if account_form.validate_on_submit():
        current_user.is_seller = not user.is_seller
        current_user.shop_name = account_form.shop_name.data
        db.session.commit()
        flash('Your account type has been changed.', 'success')
        return redirect(url_for('main.profile'))
    return render_template('/users/profile.html', form=form, account_form=account_form, deactivate_form=deactivate_form, show=True)


@main.route('/deactivate', methods=['GET', 'POST'])
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
        return redirect(url_for('main.logout'))
    return render_template('/users/profile.html', form=form, account_form=account_form, deactivate_form=deactivate_form, show_modal=True)

@main.route('/change_pass', methods=['GET', 'POST'])
@login_required
def change_pass():
    user = User.get_by_email(current_user.email_address)
    form = EditProfileForm()
    form.set_form_data()
    change_pass_form = ChangePasswordForm()
    if change_pass_form.validate_on_submit():
        user.set_password(change_pass_form.new_password.data)
        current_user.password_hash = user.password_hash
        db.session.commit()
        flash('Your password has been changed. Please login again.', 'success')
        return redirect(url_for('main.logout'))
    return render_template('users/edit_profile.html', form=form, pass_form = change_pass_form)

@main.route('/get_orders/<product_id>', methods=['POST'])
def get_product_orders(product_id):
    if current_user.is_authenticated:
        page = request.json.get('page')
        orders = db.paginate(Order.get_orders_by_product_id(product_id), page=page, 
                            per_page=current_app.config['ORDER_LISTING_PER_PAGE'], 
                            error_out=False)
        pages = []
        if orders.has_prev:
            pages.append(page-1)
        pages.append(page)
        if orders.has_next:
            pages.append(page+1)
        return jsonify({'orders': [o.to_json() for o in orders], 'pages':pages})
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@main.route('/reset_order/<order_id>', methods=['GET'])
def reset_order(order_id):
    Order.reset_pending(order_id)
    return jsonify({'message': 'done.', 'success': True})

@main.route('/approve_order/<order_id>', methods=['POST'])
def approve_order(order_id):
    if current_user.is_authenticated:
        return jsonify(Order.set_pending_status(order_id, current_user.id, 'Approved'))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@main.route('/reject_order/<order_id>', methods=['POST'])
def reject_order(order_id):
    if current_user.is_authenticated:
        return jsonify(Order.set_pending_status(order_id, current_user.id, 'Rejected'))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@main.route('/cancel_order/<order_id>', methods=['POST'])
def cancel_order(order_id):
    if current_user.is_authenticated:
        return jsonify(Order.set_pending_status_from_buyer(order_id, current_user.id, 'Cancelled'))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@main.route('/product_activation/<product_id>', methods=['POST'])
def product_activation(product_id):
    if current_user.is_authenticated:
        return jsonify(Product.activation(product_id, current_user.id))
    return jsonify({'message': 'you are not allowed to do this method.', 'success': False})

@main.route('/forget_password')
def f_password():
    return render_template('/users/f_password.html', forget_password=f_password)

@main.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    products, total = Product.search(g.search_form.q.data, page, current_app.config['PRODUCTS_PER_PAGE'])
    current_url = url_for('main.search', q=g.search_form.q.data, page=page)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['PRODUCTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    if products:
        flash(f'Your search has {total} result(s).', 'info')
    return render_template('/product/search.html', products=products, page=page,
                           current_url=current_url, next_url=next_url, prev_url=prev_url)

@main.before_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()

@main.route('/filter_products', methods=['GET', 'POST'])
def filter_products():
    filters = request.args.get('filters')
    filters_dict = json.loads(filters.replace("'", '"')) if filters else None
    form = SearchProductForm()
    form.set_form_data(filters_dict)
    if request.method == 'POST':
        filtered = SearchProductForm(request.form)
        filters = FilterHelper.filters_as_dict(request.form)
    else:
        filtered = form
    page = request.args.get('page', 1, type=int)
    view = request.args.get('view', 'grid', type=str)
    query = FilterHelper.generate_query(filtered)
    products = db.paginate(query, page=page, 
                           per_page=current_app.config['FILTER_PRODUCT_PER_PAGE'], 
                           error_out=False)
    paginator = PaginatorHelper('main.filter_products', page, 
                                products.has_prev, products.has_next, 
                                products.prev_num, products.next_num, 
                                view=view, filters=filters)
    next_url, prev_url, pages = paginator.get_pagination()
    return render_template('/product/categories.html', products=products, page=page, pages=pages, view=view, filters=filters,
                           form=form, next_url=next_url, prev_url=prev_url)