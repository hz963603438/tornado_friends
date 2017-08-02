#coding:utf-8
from tornado.web import StaticFileHandler
from main_handler import MainHandler
from handlers.admin.admin_urls import admin_urls
from handlers.blog.blog_urls import blog_urls
from handlers.friends.friends_urls import friends_urls
from handlers.public.admin_accounts.admin_urls import admin_accounts_urls
from handlers.websocket.websocket_urls import websocket_urls
from handlers.upload_file.upload_file_urls import upload_file_url
from handlers.public.about_handler import AboutHandler
from handlers.public.no_find_handler import NoFindHandler
from handlers.public.user_accounts.user_accounts_urls import user_accounts_urls


handlers = [
    (r'/', MainHandler),
    (r'/about', AboutHandler),
    (r'/images/(.*\.(png|jpg|jpeg|gif|mp3|mp4|ogg|bmp|mkv))',
     StaticFileHandler, {'path': 'files/upload_files/'}),
    (r'/messageimages/(.*\.(png|jpg|jpeg|gif|mp3|mp4|ogg|bmp|mkv))',
     StaticFileHandler, {'path': 'files/upload_files/messageimages/'}),
]

handlers += friends_urls
handlers += admin_accounts_urls
handlers += websocket_urls
handlers += blog_urls
handlers += admin_urls
handlers += upload_file_url
handlers += user_accounts_urls

#handlers += [(r'/(.*)', NoFindHandler)]
