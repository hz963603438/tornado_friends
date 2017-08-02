#coding:utf-8

from handlers.base.base_handler import BaseHandler

class AboutHandler(BaseHandler):
    def get(self):
        self.write("说明:<br>我们是一个拥有小目标的网站")