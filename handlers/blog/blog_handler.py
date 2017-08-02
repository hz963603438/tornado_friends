#coding:utf-8
from handlers.base.base_handler import BaseHandler

class BlogHandler(BaseHandler):

    def get(self):
        self.write("我是比克")