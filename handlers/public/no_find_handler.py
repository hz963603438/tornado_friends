#coding:utf-8
from handlers.base.base_handler import BaseHandler

class NoFindHandler(BaseHandler):
    def get(self, *args, **kwagrs):
        self.redirect('/admin')