from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, SelectField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,EqualTo,Length,ValidationError,Email, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


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
        print(not shopname.data)
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


class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(min=3, max=10)])
    submit = SubmitField('Update Profile')
