#coding:utf-8
from handlers.admin import admin_uimethods

settings = dict(template_path='templates',
        static_path='static',
        debug=True,
        cookie_secret='aaaa',
        login_url='/login',
        xsrf_cookies=True,
        ui_methods=admin_uimethods,
         # pycket的配置信息
        pycket={
            'engine': 'redis',  # 设置存储器类型
            'storage': {
                'host': 'localhost',
                'port': 6379,
                'db_sessions': 5,
                'db_notifications': 11,
                'max_connections': 2 ** 31,
            },
            'cookies': {
                'expires_days': 30,  # 设置过期时间
                'max_age': 5000,
            },
        },
)