from flask import request
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    DecimalField, IntegerField, SelectField, StringField, PasswordField, 
    BooleanField, SubmitField, TextAreaField, TelField, HiddenField, RadioField)
from wtforms.validators import (
    DataRequired,EqualTo,Length,ValidationError,Email, NumberRange)
from app.models import User
from app.fields import (
    ProductConditionField, ProductConditionMultipleCheckboxField, 
    ProductCategoryField, ProductCategoryMultipleCheckboxField, 
    ProductPriceRangeField, ProductImagesField)
from flask_wtf.file import FileRequired

def validate_australian_postcode(postcode):
    city_ranges = {
        'Sydney, New South Wales': (2000, 2234),
        'Melbourne, Victoria': (3000, 3996),
        'Brisbane, Queensland': (4000, 4999),
        'Perth, Western Australia': (6000, 6999),
        'Adelaide, South Australia': (5000, 5799),
        'Hobart, Tasmania': (7000, 7799),
        'Canberra, Australian Capital Territory': (2600, 2639),
        'Darwin, Northern Territory': (800, 832)  # Note: 0832 corresponds to 832
    }

    for city, (min_code, max_code) in city_ranges.items():
        if min_code <= postcode <= max_code:
            return
    raise ValidationError('Invalid Postcode.')

def get_avatar_icon(avatar_idx):
    return ['fa-user-secret', 'fa-user-tie', 'fa-user-graduate', 'fa-user-nurse'][avatar_idx]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email_address = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    address = StringField('Address', validators=[Length(max=120)])
    postcode = IntegerField('Postcode', validators=[DataRequired()])
    contact_no = TelField('Contact Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    become_seller = BooleanField('Become a Seller')
    shop_name = StringField('Shop Name')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.get_by_username(username.data)
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email_address(self, email):
        user = User.get_by_email(email.data)
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    def validate_shop_name(self, shopname):
        if self.become_seller.data and not shopname.data:
            raise ValidationError('Please enter a shop name if you wish to become a seller.')

    def validate_postcode(self, postcode):
        validate_australian_postcode(postcode.data)
        
class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    condition = ProductConditionField('Condition', validators=[DataRequired()])
    category = ProductCategoryField('Category', validators=[DataRequired()])
    location = IntegerField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=1000)])
    main_idx = HiddenField('Main Idx', validators=[DataRequired(message="Please select only 1 as the main image.")])
    image = ProductImagesField('Image', validators=[FileRequired(message='Please add at least 1 image.')])
    submit = SubmitField('Submit')

    def validate_location(self, postcode):
        validate_australian_postcode(postcode.data)

    def set_form_data(self):
        self.location.data = current_user.postcode
        
class EditProductForm(FlaskForm):
    id = int()
    product_name = StringField('Product Name', validators=[DataRequired(), Length(min=1, max=100)])
    price = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    condition = ProductConditionField('Condition', validators=[DataRequired()])
    category = ProductCategoryField('Category', validators=[DataRequired()])
    location = IntegerField('Location', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=1000)])
    main_idx = HiddenField('Main Idx', validators=[DataRequired(message="Please select only 1 as the main image.")])
    image = ProductImagesField('Image')
    submit = SubmitField('Edit')

    def validate_location(self, postcode):
        validate_australian_postcode(postcode.data)
    
    def set_main_idx(self, images):
        idx = 1
        for image in images:
            if image.is_main:
                self.main_idx.data = str(idx)
                return
            idx+=1

class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    postcode = IntegerField('Postcode')
    address = StringField('Address')
    account_type = StringField('Account Type')
    verified = BooleanField('Verified')
    avatar = IntegerField('Avatar')
    avatar_icon = StringField('Avatar')
    submit = SubmitField('Update Profile')

    def set_form_data(self):
        self.first_name.data = current_user.first_name
        self.last_name.data = current_user.last_name
        self.email.data = current_user.email_address
        self.postcode.data = current_user.postcode
        self.address.data = current_user.address
        self.account_type.data = 'Seller & Buyer' if current_user.is_seller else 'Buyer'
        self.verified.data = current_user.is_verified
        self.avatar.data = current_user.avatar
        self.avatar_icon.data = get_avatar_icon(current_user.avatar)

class UpdateAccountForm(FlaskForm):
    become_seller = BooleanField('Become a Seller?')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    agree_to_terms = RadioField('I agree to the Terms and Conditions', choices=[('agree', 'Agree')], validators=[DataRequired()])
    shop_name = StringField('Shop Name')
    submit = SubmitField('Update Account')

    def set_form_data(self):
        self.shop_name.data = current_user.shop_name
        self.become_seller.data = current_user.is_seller

    def validate_confirm_password(self, confirm_password):
        if not current_user.check_password(confirm_password.data):
            raise ValidationError('Incorrect current password.')
        
    def validate_shop_name(self, shopname):
        if self.become_seller.data and not shopname.data:
            raise ValidationError('Please enter a shop name if you wish to become a seller.')

class DeactivateAccountForm(FlaskForm):
    deactivate_password = PasswordField('Deactivate Password', validators=[DataRequired()])
    submit = SubmitField('Deactivate')

    def validate_deactivate_password(self, deactivate_password):
        if not current_user.check_password(deactivate_password.data):
            raise ValidationError('Incorrect current password.')

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    address = StringField('Address', validators=[Length(max=120)])
    postcode = IntegerField('Postcode', validators=[DataRequired()])
    avatar = HiddenField('Avatar', validators=[DataRequired()])
    avatar_icon = StringField('Avatar')
    submit = SubmitField('Update')

    def validate_postcode(self, postcode):
        validate_australian_postcode(postcode.data)

    def set_form_data(self):
        self.first_name.data = current_user.first_name
        self.last_name.data = current_user.last_name
        self.email.data = current_user.email_address
        self.postcode.data = current_user.postcode
        self.address.data = current_user.address
        self.avatar.data = current_user.avatar
        self.avatar_icon.data = get_avatar_icon(current_user.avatar)

    def validate_email(self, email):
        user = User.get_by_email(email.data)
        if user is not None and user.email_address != current_user.email_address:
            raise ValidationError('Please use a different email address.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

    def validate_old_password(self, old_password):
        if not current_user.check_password(old_password.data):
            raise ValidationError('Incorrect current password.')

    def validate_new_password(self, new_password):
        if new_password.data == self.old_password.data:
            raise ValidationError('Current password same as new password. Please use a different password.')

class Orderform(FlaskForm):
    quantity = SelectField('Quantity', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email_address = StringField('Email', validators=[DataRequired(), Email()])
    postcode = IntegerField('Postcode', validators=[DataRequired()])
    contact_no = TelField('Contact Number', validators=[DataRequired()])
    remarks = TextAreaField('remarks')
    submit = SubmitField('Request')

    def set_form_data(self):
        self.first_name.data = current_user.first_name
        self.last_name.data = current_user.last_name
        self.email_address.data = current_user.email_address
        self.postcode.data = current_user.postcode
        self.contact_no.data = current_user.contact_no

    def set_product_qty(self, qty):
        self.quantity.choices = [('','--Select Qty--')] + [(i, i) for i in range(1, qty + 1)]

    def validate_postcode(self, postcode):
        validate_australian_postcode(postcode.data)

    def validate_quantity(self, quantity):
        if int(quantity.data) < 1 or int(quantity.data) > self.quantity.choices[-1][0]:
            raise ValidationError('Invalid quantity')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')

class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField(('Reset Password'))

class SearchForm(FlaskForm):
    q = StringField(('Search'), validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*args, **kwargs)

class SearchProductForm(FlaskForm):
    categories = ProductCategoryMultipleCheckboxField('Categories')
    price = ProductPriceRangeField('Price')
    conditions = ProductConditionMultipleCheckboxField('Conditions')
    submit = SubmitField('Apply Filters')
    
    def set_form_data(self, filters_dict):
        if filters_dict:
            self.categories.data = filters_dict.get('categories', [])
            self.conditions.data = filters_dict.get('conditions', [])
            self.price.data = filters_dict.get('price', '')
