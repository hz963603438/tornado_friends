#coding:utf-8
from uuid import uuid4
from datetime import datetime
from string import printable
from models.admin.permission_model import (Permission,Menu,Employee,Role,
                                           PermissionToRole,EmployeeToRole)

from pbkdf2 import PBKDF2
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base
from libs.db.dbsession import dbSession

import hashlib
def hash_data(datas):
    h = hashlib.sha1()
    h.update(datas)
    return h.hexdigest()


class Files(Base):

    __tablename__ = 'files'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(50), nullable=False)
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    viewnum = Column(Integer, default=0)
    content_length = Column(Integer)
    upload_user = Column(String(50))
    content_type = Column(String(50))
    _file_hash = Column(String(50), unique=True, nullable=False)
    _locked = Column(Boolean, default=False, nullable=False)
    p_id = Column(Integer, ForeignKey("permission.id"))

    permission = relationship('Permission')



    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self, datas):
        self._file_hash = hash_data(datas)

    @classmethod
    def file_is_existed(cls, other_dates):
        other_dates_hash = hash_data(other_dates)
        return cls.by_hash(other_dates_hash)

    @classmethod
    def by_hash(cls, other_dates_hash):
        return dbSession.query(cls).filter_by(_file_hash=other_dates_hash).first()

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def display_file_list(cls):
        return dbSession.query(cls).filter(cls._locked == False).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(filename=name).first()

    @property
    def locked(self):
        return self._locked



    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value


class MessageImage(Base):

    __tablename__ = 'message_image'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(50), nullable=False)
    createtime = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    viewnum = Column(Integer, default=0)
    content_length= Column(Integer)
    upload_user=Column(String(50))
    content_type = Column(String(50))
    _file_hash = Column(String(50))
    _locked = Column(Boolean, default=False, nullable=False)

    m_id = Column(Integer, ForeignKey("message.mid"))

    message = relationship("Message", backref='m_images')

    @property
    def file_hash(self):
        return self._file_hash

    @file_hash.setter
    def file_hash(self, datas):
        self._file_hash = hash_data(datas)

    @classmethod
    def file_is_existed(cls, other_dates):
        other_dates_hash = hash_data(other_dates)
        return cls.by_hash(other_dates_hash)


    @classmethod
    def by_hash(cls, other_dates_hash):
        return dbSession.query(cls).filter_by(_file_hash=other_dates_hash).first()


    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def display_file_list(cls):
        return dbSession.query(cls).filter(cls._locked == False).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(filename=name).first()

    @property
    def locked(self):
        return self._locked


    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value