import re
from datetime import datetime

from werkzeug.security import gen_salt

import sqlalchemy as sa

from sqlalchemy import Column, Integer, TEXT, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

import bcrypt

from app.database import Base, db_session
from flask import current_app


slug_pattern = r"^[a-zA-Z0-9][a-zA-Z0-9-_]*[a-zA-Z0-9]$"


class CustomBase(Base):
    __abstract__ = True
    id = sa.Column('id', Integer(), primary_key=True)
    created_at = Column('created_at', DateTime, default=datetime.now)
    updated_at = Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return self._repr()

    def _repr(self, **fields: str) -> str:
        field_strings = []
        at_least_one_attached_attribute = False
        for key, field in fields.items():
            try:
                field_strings.append(f'{key}={field!r}')
            except sa.orm.exc.DetachedInstanceError:
                field_strings.append(f'{key}=DetachedInstanceError')
            else:
                at_least_one_attached_attribute = True
        if at_least_one_attached_attribute:
            return f"<{self.__class__.__name__}({','.join(field_strings)})>"
        return f"<{self.__class__.__name__} {id(self)}>"

    def save(self):
        db_session.add(self)
        db_session.commit()
        return True


class User(CustomBase):
    __tablename__ = 'user_table'
    username = Column('username', String(64), index=True, unique=True)
    email = Column('email', String(256), index=True, unique=True)
    bio = Column('bio', TEXT())

    _salt = Column('salt', String(64))
    _password_hash = Column('password', String(128))

    namespaces = relationship('NameSpace', back_populates='user')
    books = relationship('Book', back_populates='user')
    pages = relationship('Page', back_populates='user')

    def __str__(self):
        return self._repr(username=self.username, email=self.email)

    def __init__(self, username, email):
        self.username: str = username
        self.email: str = email

    def get_validations_errors(self):
        errors = []

        if len(self.username) < 3:
            errors.append('username must be > 3')
        else:  # only execute re if pass check of length
            if not re.match(slug_pattern, self.username):
                errors.append('Username: A-Z, 0-9,-,_ (both last not at init)')

        if len(self.email) < 3:
            errors.append('email must be < 3')
        else:
            if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', self.email):
                errors.append('email address needs be an email address')

        return errors

    def set_password(self, password):
        self._salt = bytes(gen_salt(32), 'utf-8')
        self._password_hash = bcrypt.hashpw(
            password=bytes(password, 'utf-8') + self._salt,
            salt=bcrypt.gensalt(6)
        )
        self.save()

    def check_password(self, password):
        return bcrypt.checkpw(bytes(password, 'utf-8')+self._salt, self._password_hash)


class NameSpace(CustomBase):
    __tablename__ = 'namespace_table'
    name = Column('name', String(256), index=True, unique=True)

    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    user = relationship("User", back_populates="namespaces")

    books = relationship('Book', back_populates='namespace')


class Book(CustomBase):
    __tablename__ = 'book_table'
    name = Column('name', String(256), index=True, unique=True)

    description = Column('description', TEXT())

    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    user = relationship("User", back_populates="books")

    namespace_id = Column(Integer, ForeignKey("namespace_table.id"), nullable=False)
    namespace = relationship("NameSpace", back_populates="books")

    pages = relationship('Page', back_populates='book')


class Page(CustomBase):
    __tablename__ = 'page_table'
    name = Column('name', String(256), index=True, unique=True)

    content = Column('content', TEXT())

    user_id = Column(Integer, ForeignKey("user_table.id"), nullable=False)
    user = relationship("User", back_populates="pages")

    book_id = Column(Integer, ForeignKey("book_table.id"), nullable=False)
    book = relationship("Book", back_populates="pages")
