# -*- coding:utf-8 -*-
from .compat import basestring
from .extensions import db

# Alias common SQLAlchemy names
Column = db.Column
relationship = db.relationship


class CRUDMixin(object):
    """数据库的增删改查方法"""

    @classmethod
    def create(cls, **kwargs):
        """增"""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """改"""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """删"""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """https://blog.csdn.net/weixin_44038167/article/details/103620028"""

    __abstract__ = True


class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}

    id = Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, basestring) and record_id.isdigit(),
                isinstance(record_id, (int, float))
            )
        ):
            return cls.query.get(int(record_id))
        return None


def reference_col(
        tablename, nullable=False, pk_name="id", foreign_key_kwargs=None, column_kwargs=None
):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = reference_col('category')
        category = relationship('Category', backref='categories')
    """
    foreign_key_kwargs = foreign_key_kwargs or {}
    column_kwargs = column_kwargs or {}

    return Column(
        db.ForeignKey(f"{tablename}.{pk_name}", **foreign_key_kwargs),
        nullable=nullable,
        **column_kwargs,
    )
