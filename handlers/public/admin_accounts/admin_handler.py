#coding:utf-8
from datetime import datetime
from handlers.public.error.error import AuthError
from handlers.base.base_handler import BaseHandler
from models.friends.friends_model import User1
from models.admin.permission_model import Employee


class AdminLoginHandler(BaseHandler):
    def get(self):
        self.render("public/admin_accounts/admin_login.html", nextname=self.get_argument("next", "/"))

    def post(self):
        employee = Employee.by_name(self.get_argument('name', ''))
        password = self.get_argument("password", "")
        remember = self.get_argument("remember", "")
        print remember
        if not employee.locked:
            if employee and employee.auth_password(password):
                self.success_login(employee)
                if employee.loginnum == 1:
                    self.write('newuser.html')
                else:
                    self.redirect("/admin")
            else:
                self.write("登录失败")
        else:
            self.write("此用户已经被锁定，请联系管理员")

    def success_login(self, employee):
        print employee.username
        employee.last_login = datetime.now()
        employee.loginnum += 1
        self.db.add(employee)
        self.db.commit()
        self.session.set('user_name', employee.username)
        self.session.set('ip_address', self.request.remote_ip)

class AdminLoginOutHandler(BaseHandler):
    def get(self):
        self.session.delete("user_name")
        self.redirect("/admin/adminlogin")


class AdminLockScreenHandler(BaseHandler):
    def get(self):
        self.render("public/admin_accounts/admin_lock_screen.html")

    def post(self):
        if self._check_argument():
            self.redirect('/admin')
        else:
            self.render('public/admin_accounts/admin_lock_screen.html')

    def _check_argument(self):
        password = self.get_argument('password', '')
        return True if self.current_user.auth_password(password) else False

