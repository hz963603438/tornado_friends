#coding:utf-8
from user_accounts_handler import TestHandler, LoginHandler, RegistHandler, MobileCode

user_accounts_urls = [
    (r'/captcha', TestHandler),
    (r'/login', LoginHandler),
    (r'/regist', RegistHandler),
    (r'/mobilecode', MobileCode),
]