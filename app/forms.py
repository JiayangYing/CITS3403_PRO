from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,EqualTo,Length,ValidationError,Email
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

