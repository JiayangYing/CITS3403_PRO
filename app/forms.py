from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import DecimalField, IntegerField, SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,EqualTo,Length,ValidationError,Email, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User

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
    raise ValidationError('Invalid post code.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email_address = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    become_seller = BooleanField('Become a Seller')
    shop_name = StringField('Shop Name')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email_address(self, email):
        user = db.session.scalar(sa.select(User).where(User.email_address == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
    def validate_shop_name(self, shopname):
        if self.become_seller.data and not shopname.data:
            raise ValidationError('Please enter a shop name if you wish to become a seller.')
        
class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    price = DecimalField('Price', validators=[
        DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(), NumberRange(min=1)])
    condition = SelectField('Condition', choices=[
        ('new', 'New'), ('used', 'Used')], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('Electronics', 'Electronics'), ('Books', 'Books'), ('Clothing', 'Clothing'), ('Home', 'Home')], validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(), Length(min=1, max=100)])
    description = StringField('Description', validators=[
        DataRequired(), Length(min=1, max=200)])
    submit = SubmitField('Submit')

class ProfileForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    email = StringField('Email')
    postcode = IntegerField('Post Code')
    address = StringField('Address')
    account_type = StringField('Account Type')
    verified = BooleanField('Verified')
    submit = SubmitField('Update Profile')

    def set_form_data(self):
        self.first_name.data = current_user.first_name
        self.last_name.data = current_user.last_name
        self.email.data = current_user.email_address
        self.postcode.data = current_user.postcode
        self.address.data = current_user.address
        self.account_type.data = 'Seller' if current_user.is_seller else 'Buyer'
        self.verified.data = current_user.is_verified

class UpdateAccountForm(FlaskForm):
    become_seller = BooleanField('Become a Seller?')
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Update Account')

    def set_form_data(self):
        self.become_seller.data = current_user.is_seller

    def validate_confirm_password(self, confirm_password):
        if not current_user.check_password(confirm_password.data):
            raise ValidationError('Incorrect current password.')

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
    postcode = IntegerField('Post Code', validators=[DataRequired()])
    submit = SubmitField('Update')

    def validate_postcode(self, postcode):
        validate_australian_postcode(postcode.data)

    def set_form_data(self):
        self.first_name.data = current_user.first_name
        self.last_name.data = current_user.last_name
        self.email.data = current_user.email_address
        self.postcode.data = current_user.postcode
        self.address.data = current_user.address

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

    def validate_old_password(self, old_password):
        if old_password.data is None and not current_user.check_password(old_password.data):
            raise ValidationError('Incorrect current password.')

    def validate_old_password(self, old_password):
        if old_password.data == self.new_password.data:
            raise ValidationError('Current password same as new password. Please use a different password.')