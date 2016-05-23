"""
User related Models

Includes the following models:
    User
    Role
    Permission

"""
from datetime import datetime

import re
import sqlalchemy.types as types
from server.data import BaseModel
from server.exceptions import ValidationException
from sqlalchemy import (Column, String, Integer, DateTime, Boolean,
                        Table, ForeignKey)
from sqlalchemy.orm import validates, relationship, backref

###########################
#         Utilities       #
###########################

email_regex = re.compile("[a-z0-9!#$%&'*+/=?^_`{|}~-]+"
                         "(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*"
                         "@"
                         "(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+"
                         "[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")


###########################
#          Models         #
###########################


# Association table for linking permissions to roles
_role_permission = Table(
    'role_permission',
    BaseModel.metadata,
    Column('role_psk', Integer, ForeignKey('role.psk')),
    Column('permission_psk', Integer, ForeignKey('permission.psk')))


# Association table for linking roles to users
_user_role = Table(
    'user_role',
    BaseModel.metadata,
    Column('user_psk', Integer, ForeignKey('user.psk')),
    Column('role_psk', Integer, ForeignKey('role.psk')))


class Role(BaseModel):
    """
    Defines the roles available to users.
    """
    __tablename__ = 'role'

    psk = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True)
    permissions = relationship('Permission', secondary=_role_permission,
                               backref=backref('roles', lazy='dynamic'))


class Permission(BaseModel):
    """
    Defines individual permissions that can be attached to roles.
    """
    __tablename__ = 'permission'

    psk = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, index=True)


class User(BaseModel):
    """
    Represents a logistics wizard User.
    The password property will be automatically hashed before being stored
    in the database.
    """
    __tablename__ = 'user'

    psk = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.utcnow)
    modified = Column(DateTime)
    deleted = Column(DateTime)
    user_id = Column(String(120), unique=True, index=True)
    email = Column(String(120), unique=True, index=True)
    password = Column(String(120), unique=False, index=False)
    roles = relationship('Role', secondary=_user_role,
                         backref=backref('users', lazy='dynamic'))

    @property
    def permissions(self):
        for role in self.roles:
            for perm in role.permissions:
                yield perm.name

    @validates('password')
    def _validate_password(self, key, password):
        """
        Verify that the password is:
        at least 6 characters and cannot be empty.
        """
        if password is None:
            raise ValidationException('Password cannot be empty')
        if len(password) < 6:
            raise ValidationException('Password must be at least 6 characters')
        return password

    @validates('email')
    def _validate_email(self, key, address):
        """
        Verify that the email is a valid email address
        """
        if email_regex.match(address) is None:
            raise ValidationException("Invalid email address")
        return address

    def verify_password(self, password):
        return _hasher.verify(password, self.password)

    def __repr__(self):
        return '<User psk: %d, id: %r>' % (self.psk, self.user_id)
