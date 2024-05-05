from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    is_seller : so.Mapped[bool] = so.mapped_column(unique=False, default=False)
    is_active : so.Mapped[bool] = so.mapped_column(unique=False, default=True)
    email_address: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    postcode: so.Mapped[int] = so.mapped_column(unique=False)
    shop_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,unique=True)
    def __repr__(self):
        return '<User {}>'.format(self.username)