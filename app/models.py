import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from typing import Optional
from app.search import add_to_index, remove_from_index, query_index
from time import time
from flask import current_app
import jwt

class SearchableMixin:
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return [], 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        query = sa.select(cls).where(cls.id.in_(ids)).order_by(
            db.case(*when, value=cls.id))
        return db.session.scalars(query), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in db.session.scalars(sa.select(cls)):
            add_to_index(cls.__tablename__, obj)

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), unique=False)
    is_seller : so.Mapped[bool] = so.mapped_column(unique=False, default=False)
    is_active : so.Mapped[bool] = so.mapped_column(unique=False, default=True)
    is_verified : so.Mapped[bool] = so.mapped_column(unique=False, default=False)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    postcode: so.Mapped[int] = so.mapped_column(unique=False)
    address: so.Mapped[str] = so.mapped_column(unique=False, nullable=True)
    contact_no: so.Mapped[str] = so.mapped_column(unique=False, nullable=True)
    avatar: so.Mapped[int] = so.mapped_column(unique = False, default = 0)
    shop_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=False, nullable=True)
    products: so.WriteOnlyMapped['Product'] = so.relationship(back_populates='owner')
    orders: so.WriteOnlyMapped['Order'] = so.relationship(foreign_keys='Order.buyer_id', back_populates='buyer')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    @login.user_loader
    def load_user(id):
        return db.session.get(User, int(id))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)

    def get_verify_email_token(self, expires_in=3*24*60*60):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, # 3 days
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_verify_email_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except Exception:
            return
        return db.session.get(User, id)

    def get_products(self):
        return (
            sa.select(Product)
            .where(Product.user_id == self.id)
            .order_by(Product.created_on.desc())
        )

    def get_own_orders(self):
        return (
            sa.select(Order, Product)
            .join(Product, Order.product_id == Product.id)
            .where(Order.buyer_id == self.id)
            .order_by(Order.created_on.desc())
        )
    
    @staticmethod
    def get_by_username(username):
        query = sa.select(User).where(User.username==username)
        return db.session.scalar(query)
    
    @staticmethod
    def get_by_email(email):
        query = sa.select(User).where(User.email_address==email)
        return db.session.scalar(query)

    def add_order(self):
        o = Order(buyer=self)
        db.session.add(o)
        return o

class Product(SearchableMixin, db.Model):
    __searchable__ = ['product_name', 'category', 'condition', 'location', 'description']
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    product_name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    category: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    price: so.Mapped[float] = so.mapped_column(index=True)
    quantity: so.Mapped[int] = so.mapped_column(index=True)
    condition: so.Mapped[str] = so.mapped_column(sa.String(20), index=True)
    location: so.Mapped[int] = so.mapped_column(index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(1000))
    created_on: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())
    modified_on: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())
    is_active : so.Mapped[bool] = so.mapped_column(default=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    owner: so.Mapped[User] = so.relationship(back_populates='products')
    product_orders: so.WriteOnlyMapped['Order'] = so.relationship(back_populates='product')
    images: so.WriteOnlyMapped['Image'] = so.relationship(back_populates='product')

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)

    @staticmethod
    def get_orders_count(product_id, status):
        return db.session.query(sa.func.count(Order.id)). \
            filter(Order.product_id == product_id). \
            filter(Order.status == status). \
            scalar()
    
    def get_pending_order_counts(self):
        product_id = self.id
        pending_count = self.get_orders_count(product_id, 'Pending')
        approved_count = self.get_orders_count(product_id, 'Approved')
        rejected_count = self.get_orders_count(product_id, 'Rejected')
        cancelled_count = self.get_orders_count(product_id, 'Cancelled')
        count_info = {
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count,
            'cancelled': cancelled_count
        }
        return count_info
    
    @staticmethod
    def get_by_id(id): 
        return Product.query.get(id)

    @staticmethod
    def get_all(limit = None):
        query = sa.select(Product)\
            .where(Product.is_active)
        if limit is not None:
            query = query.limit(limit)
        return  db.session.scalars(query).all()
    
    @staticmethod
    def get_recently(limit = None):
        query = sa.select(Product)\
            .where(Product.is_active)\
            .order_by(Product.created_on.desc())
        if limit is not None:
            query = query.limit(limit)
        return  db.session.scalars(query).all()

    @staticmethod
    def get_top_sales(limit = None):
        product_orders_count = sa.func.count(Order.id).label('order_count')
        query = sa.select(Product, product_orders_count)\
            .join(Order, Product.id == Order.product_id)\
            .where(Product.is_active)\
            .group_by(Product.id)\
            .order_by(product_orders_count.desc())
        if limit is not None:
            query = query.limit(limit)
        return db.session.scalars(query).all()
    
    @staticmethod
    def get_by_category(category, limit = None):
        query = sa.select(Product)\
            .where(Product.category == category)\
            .where(Product.is_active)
        if limit is not None:
            query = query.limit(limit)
        return db.session.scalars(query).all()
    
    @staticmethod
    def get_product_images(id):
        return db.session.scalars(
            sa.select(Image)
            .join(Product, Image.product_id == Product.id)
            .where(Image.product_id == id)
        ).all()
    
    @staticmethod
    def activation(id, current_user_id):
        product = Product.get_by_id(id)
        if not product:
            return {'message': 'Product not found.', 'success': False}
        if product.user_id != current_user_id:
            return {'message': 'This is not your product.', 'success': False}
        product.is_active = not product.is_active
        db.session.commit()
        return {'message': f'Success {"activate" if product.is_active else "deactivate"} the product.', 'success':True}  
    
class Order(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    quantity: so.Mapped[int] = so.mapped_column()
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64))
    email_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True)
    postcode: so.Mapped[int] = so.mapped_column()
    contact_no: so.Mapped[str] = so.mapped_column(nullable=True)
    remarks: so.Mapped[str] = so.mapped_column(sa.String(5000), nullable=True)
    created_on: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Product.id), index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(10), index=True, default="Pending")
    buyer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    buyer: so.Mapped[User] = so.relationship(foreign_keys='Order.buyer_id', back_populates='orders')
    product: so.Mapped[Product] = so.relationship(foreign_keys='Order.product_id', back_populates='product_orders')
    
    def to_json(self):
        data = {
            'id': self.id,
            'qty': self.quantity,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email_address,
            'postcode': self.postcode,
            'contact_no': self.contact_no,
            'remarks': self.remarks,
            'created_on': self.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            'status': self.status
        }
        return data

    def __repr__(self):
        return '<Order {}>'.format(self.id)

    @staticmethod
    def get_orders_by_product_id(id):
        return (
            sa.select(Order)
            .where(Order.product_id == id)
            .order_by(Order.created_on.desc())
        )

    @staticmethod
    def get_by_id(id): 
        return Order.query.get(id)
    
    @staticmethod
    def set_pending_status(id, current_user_id,status, update_qty=False):
        order = Order.get_by_id(id)
        if not order:
            return {'message': 'Order not found.', 'success': False}
        if order.status != 'Pending':
            return {'message': 'Order not in pending status.', 'success': False}
        product = Product.get_by_id(order.product_id)
        if not product:
            return {'message': 'Product not found.', 'success': False}
        if not product.is_active:
            return {'message': 'Product is not active.', 'success': False}
        if not product.user_id == current_user_id:
            return {'message': 'This is not your product.', 'success': False}
        order.status = status
        if update_qty:
            product.quantity = product.quantity-order.quantity
        db.session.commit()
        return {'message': f'{status} the order.', 'success':True}        

    @staticmethod
    def set_pending_status_from_buyer(id, current_user_id,status):
        order = Order.get_by_id(id)
        if not order or order.status != 'Pending':
            return {'message': 'Order not found.', 'success': False}
        if not order.buyer_id == current_user_id:
            return {'message': 'This is not your order.', 'success': False}
        product = Product.get_by_id(order.product_id)
        if not product:
            return {'message': 'Product not found.', 'success': False}
        order.status = status
        db.session.commit()
        return {'message': f'{status} the order.', 'success':True}

    # just for testing
    @staticmethod
    def reset_pending(id):
        order = Order.get_by_id(id)
        order.status = 'Pending'
        db.session.commit() 


class Image(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    image_name: so.Mapped[str] = so.mapped_column(sa.String(255))
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Product.id))
    product: so.Mapped[Product] = so.relationship(back_populates='images')
    is_main: so.Mapped[bool] = so.mapped_column(unique=False, default=False)

    @staticmethod
    def get_images_by_product_id(id): 
        return db.session.scalars(
            sa.select(Image).where(Image.product_id == id)
        )
    
    @staticmethod
    def get_main_image_by_product_id(id):
        return db.session.query(Image). \
            filter(Image.product_id == id). \
            filter(Image.is_main).first()