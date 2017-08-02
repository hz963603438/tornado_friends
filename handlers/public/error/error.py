#coding:utf-8

class AuthError(Exception):
    def __init__(self, msg):
        super(AuthError, self).__init__(msg)
