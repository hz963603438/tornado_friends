#coding:utf-8
from admin_handler import AdminLoginHandler, AdminLoginOutHandler,AdminLockScreenHandler

admin_accounts_urls = [
         (r'/admin/adminlogin', AdminLoginHandler),
         (r'/admin/adminloginout', AdminLoginOutHandler),
         (r'/admin/adminlock', AdminLockScreenHandler)
]