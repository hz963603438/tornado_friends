#coding:utf-8
from websocket_handler import MessageWebSocket, MessageHandler

websocket_urls = [
     (r'/message', MessageHandler),
     (r'/messagewebsocket', MessageWebSocket)
]

