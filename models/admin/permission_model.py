#coding:utf-8
from uuid import uuid4
from datetime import datetime
from string import printable

from pbkdf2 import PBKDF2
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base
from libs.db.dbsession import dbSession


class Handler(Base):
    __tablename__ = 'handler'
    id = Column(Integer, primary_key=True, autoincrement=True)
    handlername = Column(String(50), nullable=False)
    p_id = Column(Integer, ForeignKey('permission.id'), unique=True)

    permission = relationship("Permission", uselist=False)

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(handlername=name).first()

class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    menuname = Column(String(50), nullable=False)
    p_id = Column(Integer, ForeignKey('permission.id'), unique=True)

    permission = relationship("Permission", uselist=False)

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(menuname=name).first()

class PermissionToRole(Base):
    __tablename__ = 'permissiontorole'
    p_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)
    r_id = Column(Integer, ForeignKey('role.id'), primary_key=True)


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pname = Column(String(50), nullable=False)
    pcode = Column(String(50), nullable=False)
    code = Column(Integer)

    roles = relationship("Role", secondary=PermissionToRole.__table__)

    menu = relationship("Menu", uselist=False)

class EmployeeToRole(Base):
    __tablename__ = 'employeetorole'
    e_id = Column(Integer, ForeignKey('employee.id'), primary_key=True)
    r_id = Column(Integer, ForeignKey('role.id'), primary_key=True)

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    rname = Column(String(50), nullable=False)

    employees = relationship("Employee", secondary=EmployeeToRole.__table__)

    permissions = relationship("Permission", secondary=PermissionToRole.__table__)

class Employee(Base):
    __tablename__ = 'employee'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    _password = Column('password', String(64))
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    last_login = Column(DateTime)
    loginnum = Column(Integer, default=0)
    _locked = Column(Boolean, default=False, nullable=False)

    _avatar = Column(String(64))

    roles = relationship("Role", secondary=EmployeeToRole.__table__)

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    def auth_password(self, other_password):
        if self._password:
            return self.password == PBKDF2.crypt(other_password, self.password)
        else:
            return False

    @property
    def avatar(self):
        return self._avatar if self._avatar else "default_avatar.jpeg"

    @avatar.setter
    def avatar(self, image_data):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)

        if 64 < len(image_data) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what("", h=image_data)
            print ext
            print self.uuid
            if ext in ['png', 'jpeg', 'gif', 'bmp'] and not self.is_xss_image(image_data):
                if self._avatar and os.path.exists("static/images/useravatars/" + self._avatar):
                    os.unlink("static/images/useravatars/" + self._avatar)
                file_path = str("static/images/useravatars/" + self.uuid + '.' + ext)

                with open(file_path, 'wb') as f:
                    f.write(image_data)

                self._avatar = self.uuid + '.' + ext
            else:
                raise ValidationError("not in ['png', 'jpeg', 'gif', 'bmp']")
        else:
            raise ValidationError("64 < len(image_data) < 1024 * 1024 bytes")

    def is_xss_image(self, data):
        return all([char in printable for char in data[:16]])

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(username=name).first()

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'last_login': self.last_login,
        }

    def __repr__(self):
        return u'<User1 - id: %s  name: %s>' % (self.id, self.username)