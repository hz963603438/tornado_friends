#coding:utf-8
import tornado.web
from handlers.base.base_handler import BaseHandler
from models.friends.friends_model import User1


class MainHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        #为用户添加头像
        # user = self.db.query(User1).filter(User1.id==1).first()
        # user.avatar = open("static/images/avatar11.jpg", "rb").read()
        # self.db.add(user)
        # self.db.commit()
        # user = self.db.query(User1).filter(User1.id == 2).first()
        # user.avatar = open("static/images/headpictrue.jpg", "rb").read()
        # self.db.add(user)
        # self.db.commit()
        user = self.db.query(User1).filter(User1.id == 3).first()

        user.avatar = open("static/images/headpictrue.jpg", "rb").read()

        self.db.add(user)
        self.db.commit()
        print '-' * 80
        users = User1.all()
        self.render(u"main/main.html",
                    currentuser=self.current_user,
                    users=users
                    )
