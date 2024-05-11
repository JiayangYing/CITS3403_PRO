import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timezone
from typing import Optional

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=False)
    is_seller : so.Mapped[bool] = so.mapped_column(unique=False, default=False)
    is_active : so.Mapped[bool] = so.mapped_column(unique=False, default=True)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    postcode: so.Mapped[int] = so.mapped_column(unique=False, nullable=True)
    shop_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False, nullable=True)
    products: so.WriteOnlyMapped['Product'] = so.relationship(
        back_populates='owner')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        
        return check_password_hash(self.password_hash, password)
    
    def get_products(self):
        return sa.select(Product).where(Product.user_id == self.id)

    
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    condition = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now())
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='products')

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)
    