#coding:utf-8
from datetime import datetime
from random import randint
from handlers.base.base_handler import BaseHandler
from handlers.public.error.error import AuthError
from models.friends.friends_model import User1
from utills.captcha.captcha import pillow_test
from libs.yun_tong_xun.yun_tong_xun import sendTemplateSMS


class LoginHandler(BaseHandler):
    def get(self):
        self.render("public/user_accounts/login.html", nextname=self.get_argument("next", "/"))

    def post(self):
        user = User1.by_name(self.get_argument('name', ''))
        password = self.get_argument("password", "")
        if not user.locked:
            if user and user.auth_password(password):
                self.success_login(user)
                if user.loginnum == 1:
                    self.write('newuser.html')
                else:
                    self.redirect(self.get_argument("aaa", "/"))
            else:
                self.write("登录失败")
        else:
            self.write("此用户已经被锁定，请联系管理员")

    def success_login(self, user):
        print user.username
        user.last_login = datetime.now()
        user.loginnum += 1
        self.db.add(user)
        self.db.commit()
        self.session.set('user_name', user.username)


class RegistHandler(BaseHandler):
    def get(self):
        # if self.current_user:
        #     self.redirect('/')
        # else:
        self.render("public/user_accounts/regist.html", error=None)

    def post(self):
        if self._check_argument():
            try:
                self._create_user()
                self.redirect('/login')
            except AuthError as e:
                self.render("public/user_accounts/regist.html", error=e)
            except Exception as e:
                self.render("regist.html", error=e)
        else:
            self.render("public/user_accounts/regist.html", error="input error")


    def _check_argument(self):
        name = self.get_argument("name", "")
        password = self.get_argument("password", "")
        mobile_captcha = self.get_argument('mobile_captcha', '')
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')
        if self.conn.get("mobile_code:%s" % mobile) == mobile_captcha and\
            self.conn.get("captcha:%s" % code) == captcha.lower():
            return True
        else:
            return False


    def _create_user(self):
        if User1.by_name(self.get_argument('name', '')):
            raise AuthError("name is registered")
        if self.get_argument('password1', '') != self.get_argument('password2', ''):
            raise AuthError("Password error")
        user = User1()
        user.username = self.get_argument('name', '')
        user.password = self.get_argument('password1', '')
        self.db.add(user)
        self.db.commit()

class ModifyNameHandler(BaseHandler):

    def get(self):
        user = User1.by_uuid(self.get_argument('uuid', ''))
        self.db.delete(user)
        self.db.commit()
        self.redirect('/')


    def post(self):
        user = User1.by_uuid(self.get_argument('uuid', ''))
        delete = self.get_argument('delete', '')
        if delete == 'delete':
            self.db.delete(user)
            self.db.commit()
            self.redirect('/')
        elif user:
            user.username=self.get_argument('username', '')
            self.db.add(user)
            self.db.commit()
            self.redirect('/')
        else:
            self.write('error no')


class TestHandler(BaseHandler):
    def get(self):
        pre_code = self.get_argument('pre_code', '')
        code = self.get_argument('code', '')
        print pre_code, code
        if pre_code:
            self.conn.delete("captcha:%s" % pre_code)
        text, img = pillow_test()
        self.conn.setex("captcha:%s" % code, text.lower(), 60)
        self.set_header("Content-Type", "image/jpg")
        self.write(img)

class MobileCode(BaseHandler):
    def post(self, *args, **kwargs):
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')
        status = 200
        message = mobile
        if not captcha:
            status = 400
            message = '缺少验证码'
        elif self.conn.get("captcha:%s" % code) != captcha.lower():
            status = 400
            message = '验证码不正确'
        else:
            mobile_code = randint(1000, 9999)
            print mobile_code
            self.conn.setex("mobile_code:%s" % mobile, mobile_code, 1800)
            sendTemplateSMS(mobile, [mobile_code, 30], 1)

        print mobile, '==========='
        print code, '-------------'
        data = {
            'status': status,
            'message': message,
            'data': [{
                'haha': 'hehe'
            }]
        }
        self.write(data)