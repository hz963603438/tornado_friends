#coding:utf-8
from datetime import datetime
import tornado.escape
from handlers.base.base_handler import BaseHandler, BaseWebSocket



class MessageWebSocket(BaseWebSocket):

    cache=[]

    users=set()

    def open(self):
        print '-----------open------------'
        print self.request.remote_ip
        MessageWebSocket.users.add(self)
        print MessageWebSocket.users


    def on_close(self):
        print '-----------on_close------------'
        pass


    def on_message(self, message):
        print '-----------on_message------------'
        print message
        print type(message)
        '{"content": "111"}'
        msg =  tornado.escape.json_decode(message)
        print type(msg)
        msg.update({
            "useravatar": self.current_user.avatar,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        MessageWebSocket.cache.append(msg)
        print MessageWebSocket.cache

        for user in MessageWebSocket.users:
            if user != self:
                try:
                    user.write_message(msg)
                except Exception as e:
                    print e


class MessageHandler(BaseHandler):
    def get(self):
        aa = 1111
        bb='cccc'
        cc='dddd'

        self.render("websocket/websocket.html",
                    username=self.current_user,
                    messages=[],
                    cache=MessageWebSocket.cache[:-6:-1],
                    #cache=reversed(MessageWebSocket.cache)
                    )
