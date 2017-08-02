#coding:utf-8
from handlers.base.base_handler import BaseHandler
from models.friends.friends_model import User1
from models.friends.friends_model import Message, Comment,  Flike, Friends
from models.upload_file.upload_file_model import MessageImage


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
            user.username = self.get_argument('username', '')
            self.db.add(user)
            self.db.commit()
            self.redirect('/')
        else:
            self.write('error no')

class FriendlistHandler(BaseHandler):
    def get(self):
        messages = self.db.query(Message).order_by(Message.createtime.desc()).all()
        print self.current_user.username
        # print self.current_user.friends[0].friend.username
        # print self.current_user.friends[1].friend.username
        fr = self.current_user.friends
        self.render("friends/friends_list.html", messages=messages, friends=fr)


class AddmessageHandler(BaseHandler):
    def post(self, *args, **kwargs):
        message = self.get_argument('message', '')
        filename_post = self.request.files.get('myfilename', '')
        mes = Message()
        mes.message = message
        mes.user1 = self.current_user
        self.db.add(mes)
        self.db.commit()
        for files in filename_post:
            msg = self.save_file(files, mes)
            print msg
        self.redirect('/friendslist')

    def save_file(self, files, message):
        file_name = files['filename']
        url = 'files/upload_files/messageimages/' + file_name
        if not MessageImage.file_is_existed(files['body']):
            with open(url, 'wb') as f:
                f.write(files['body'])
        fi = MessageImage()
        fi.filename = file_name
        fi.content_length = len(files['body'])
        fi.content_type = files['content_type']
        fi.file_hash = files['body']
        fi.message = message
        self.db.add(fi)
        self.db.commit()
        return u'文件  %s  保存成功' % file_name


class FlikeHandler(BaseHandler):
    def get(self):
        uuid = self.get_argument('uuid', '')
        mes = Message.by_uuid(uuid)
        mes.message_user.append(self.current_user)
        self.db.add(mes)
        self.db.commit()
        self.redirect('/friendslist')


class AddComment(BaseHandler):
    def post(self):
        uuid = self.get_argument("uuid", '')
        comment = self.get_argument("comment", '')
        print uuid, comment
        status = 200,
        message = "提交成功"
        user1 = self.current_user
        print user1
        mes = Message.by_uuid(uuid)
        com = Comment()
        com.comment = comment
        com.message = mes
        com.user1 = user1
        self.db.add(com)
        self.db.commit()
        rsp = {
            'status': status,
            'message': message,
            'data':{

            }
        }
        self.write(rsp)