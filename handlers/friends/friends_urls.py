#coding:utf-8
from friends_handler import ModifyNameHandler, FriendlistHandler, AddmessageHandler, FlikeHandler, AddComment

friends_urls = [
    (r'/modifyname', ModifyNameHandler),
    (r'/friendslist', FriendlistHandler),
    (r'/addmessage', AddmessageHandler),
    (r'/flike', FlikeHandler),
    (r'/addcomment', AddComment),
]