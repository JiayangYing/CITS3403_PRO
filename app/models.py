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
    is_verified : so.Mapped[bool] = so.mapped_column(unique=False, default=False)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    postcode: so.Mapped[int] = so.mapped_column(unique=False)
    address: so.Mapped[str] = so.mapped_column(unique=False, nullable=True)
    contact_no: so.Mapped[str] = so.mapped_column(unique=False, nullable=True)
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

    def add_order(self):
        o = Order(buyer=self)
        db.session.add(o)
        return o

class Product(db.Model):
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

    def get_orders_count(self, status):
        return db.session.scalar(
            sa.select(sa.func.count())
            .where(sa.and_(
                Order.product_id == self.id,
                Order.status == status))
        )
    
    def get_pending_order_counts(self):
        pending_count = self.get_orders_count(status='Pending')
        approved_count = self.get_orders_count(status='Approved')
        rejected_count = self.get_orders_count(status='Rejected')
        cancelled_count = self.get_orders_count(status='Cancelled')
        count_info = {
            'pending': pending_count,
            'approved': approved_count,
            'rejected': rejected_count,
            'cancelled': cancelled_count
        }
        return count_info
    
    def activation(self, id, current_user_id):
        product = Product.query.get(id)
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

    def get_orders_by_product_id(self, id):
        return (
            sa.select(Order)
            .where(self.product_id == id)
            .order_by(Order.created_on.desc())
        )

    def get_by_id(self, id):
        return db.session.execute(
            sa.select(Order)
            .where(self.id == id)
        ).fetchone()
    
    def set_pending_status(self, id, current_user_id,status):
        order = Order.query.get(id)
        if not order:
            return {'message': 'Order not found.', 'success': False}
        if order.status != 'Pending':
            return {'message': 'Order not in pending status.', 'success': False}
        product = Product.query.get(order.product_id)
        if not product:
            return {'message': 'Product not found.', 'success': False}
        if not product.is_active:
            return {'message': 'Product is not active.', 'success': False}
        if not product.user_id == current_user_id:
            return {'message': 'This is not your product.', 'success': False}
        order.status = status
        db.session.commit()
        return {'message': f'{status} the order.', 'success':True}        

    
    def set_pending_status_from_buyer(self, id, current_user_id,status):
        order = Order.query.get(id)
        if not order or order.status != 'Pending':
            return {'message': 'Order not found.', 'success': False}
        if not order.buyer_id == current_user_id:
            return {'message': 'This is not your order.', 'success': False}
        product = Product.query.get(order.product_id)
        if not product:
            return {'message': 'Product not found.', 'success': False}
        order.status = status
        db.session.commit()
        return {'message': f'{status} the order.', 'success':True}

    # just for testing
    def reset_pending(self, id):
        order = Order.query.get(id)
        order.status = 'Pending'
        db.session.commit() 

