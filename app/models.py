import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from typing import Optional
from app.search import add_to_index, remove_from_index, query_index

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

    def get_products(self):
        return (
            sa.select(Product)
            .where(Product.user_id == self.id,)
            .order_by(Product.created_on.desc())
        )
    
    @staticmethod
    def get_by_username(username):
        return db.session.scalar(
            sa.select(User).where(User.username==username)
        )
    
    @staticmethod
    def get_by_email(email):
        return db.session.scalar(
            sa.select(User).where(User.email_address==email)
        )

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

    def __repr__(self):
        return '<Product {}>'.format(self.product_name)

    @staticmethod
    def get_orders_count(status):
        return db.session.scalar(
            sa.select(sa.func.count())
            .where(sa.and_(
                Order.product_id == Product.id,
                Order.status == status))
        )
    
    def get_pending_order_counts(self):
        pending_count = self.get_orders_count('Pending')
        approved_count = self.get_orders_count('Approved')
        rejected_count = self.get_orders_count('Rejected')
        cancelled_count = self.get_orders_count('Cancelled')
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
    remarks: so.Mapped[str] = so.mapped_column(sa.String(5000))
    created_on: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now())
    product_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Product.id), index=True)
    status: so.Mapped[str] = so.mapped_column(sa.String(10), index=True, default="Pending")
    buyer_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    buyer: so.Mapped[User] = so.relationship(foreign_keys='Order.buyer_id', back_populates='orders')
    
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
    def set_pending_status(id, current_user_id,status):
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

