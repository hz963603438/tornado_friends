#coding:utf-8
from admin_handler import AdminIndexHandler, FilesTableHandler, JumppageHandler

admin_urls = [
    (r"/admin", AdminIndexHandler),
    (r"/filestable/(.*)", FilesTableHandler),
    (r"/jumppage", JumppageHandler),
]