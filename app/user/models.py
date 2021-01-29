# -*- coding: utf-8 -*-
"""User models"""
import datetime as dt
import jwt
from flask import current_app
from marshmallow import Schema, fields
from flask_login import UserMixin
from app.database import (
    Column,
    Model,
    SurrogatePK,
    db
)
from app.extensions import bcrypt


class UserSchema(Schema):
    userId = fields.Int(attribute='id')
    account = fields.Str()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    active = fields.Bool()
    is_admin = fields.Bool()
    email = fields.Email()
    created_at = fields.DateTime()


class EntityBase(object):
    def to_json(self):
        fields = self.__dict__
        if "_sa_instance_state" in fields:
            del fields["_sa_instance_state"]
        if "password" in fields:
            del fields["password"]

        return fields


class User(UserMixin, SurrogatePK, Model, EntityBase):
    """A user of the app."""

    __tablename__ = "users"
    account = Column(db.String(80), unique=True, nullable=False)
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.LargeBinary(128), nullable=True)
    created_at = Column(db.DateTime, nullable=False,
                        default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    def __init__(self, account, email, password=None, **kwargs):
        """Create instance."""
        db.Model.__init__(self, account=account, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def get_id(self):
        """获取用户ID"""
        return self.id

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<User({self.account!r})>"

    @classmethod
    def verify_auth_token(cls, token):
        data = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=['HS256'])
        return cls.query.get(data["id"])

    def generate_token(self):
        return jwt.encode({"id": self.id}, current_app.config["SECRET_KEY"], algorithm='HS256')
