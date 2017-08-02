#coding=utf-8
import tornado.escape
from pycket.session import SessionMixin
import tornado.websocket
import tornado.web
from libs.db.dbsession import dbSession
from models.friends.friends_model import User1
from models.admin.permission_model import Employee
from libs.redis_conn.redis_conn import conn


class BaseHandler(tornado.web.RequestHandler, SessionMixin):
    def initialize(self):
        self.db=dbSession
        self.conn=conn

    def get_current_user(self):
        username = self.session.get("user_name")
        if username:
            user = User1.by_name(username)
            if user:
                return user
            else:
                return Employee.by_name(username)
        else:
            return None

    def on_finish(self):
        self.db.close()

    # def write_error(self, *args, **kwargs):
    #     self.render('public/404.html')

class BaseWebSocket(tornado.websocket.WebSocketHandler, SessionMixin):
    def get_current_user(self):
        if self.session.get("user_name"):
            return User1.by_name(self.session.get("user_name"))
        else:
            return None