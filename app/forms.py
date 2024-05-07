from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,DecimalField,IntegerField,SelectField
from wtforms.validators import DataRequired,EqualTo,Length,ValidationError,Email,NumberRange
import sqlalchemy as sa
from app import db
from app.models import User
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email_address = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    re_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    become_seller = BooleanField('Become a Seller')
    shop_name = StringField('Shop Name')
    submit = SubmitField('Register')

class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[
        DataRequired(), Length(min=1, max=100)])
    category = StringField('Category', validators=[
        DataRequired(), Length(min=1, max=50)])
    price = DecimalField('Price', validators=[
        DataRequired(), NumberRange(min=0)])
    quantity = IntegerField('Quantity', validators=[
        DataRequired(), NumberRange(min=1)])
    condition = SelectField('Condition', choices=[
        ('new', 'New'), ('used', 'Used')], validators=[DataRequired()])
    location = StringField('Location', validators=[
        DataRequired(), Length(min=1, max=100)])
    submit = SubmitField('Submit')


    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')

