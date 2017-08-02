#coding:utf-8
from handlers.base.base_handler import BaseHandler
from constants import ADMIN
import functools
import tornado.web
from models.admin.permission_model import (Permission,Menu,Employee,Handler,Role,
                                           PermissionToRole,EmployeeToRole)
from models.upload_file.upload_file_model import Files
from constants import MAX_PAGE

def admin_auth(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if self.current_user:
            if self.session.get('ip_address', '') == self.request.remote_ip:
                return method(self, *args, **kwargs)
            else:
                self.write('ip地址不符')
        else:
            self.redirect('/admin/adminlogin')
    return wrapper


def admin_ip_list(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwags):
        if self.request.remote_ip in ADMIN:
            return method(self, *args, **kwags)
        else:
            self.write('不在管理员列表中')
    return wrapper


model = {
    "menu": Menu,
    "handler": Handler,
    "files": Files,
}


class HasPermission(object):
    def __init__(self):
        self.emp_permission = set()
        self.obj_permission = ""

    def has_permission(self, employee, name, types):
        #验证方法
        self._get_current_user_permission(employee)
        self._get_obj_permission(model[types], name)
        if self.obj_permission in self.emp_permission:
            return True
        return False

    def _get_current_user_permission(self, employee):
        #获取用户的权限
        for role in employee.current_user.roles:
            for permission in role.permissions:
                self.emp_permission.add(permission.pcode)

    def _get_obj_permission(self, model, name):
        #获取要验证物体的权限
        self.obj_permission = model.by_name(name).permission.pcode


# def has_permission(self, name, types):
    #1 查询数据库当前用户的权限
    # emp_permission = set()
    # for role in self.current_user.roles:
    #     for permission in role.permissions:
    #         emp_permission.add(permission.pcode)

    #2 查询数据库menu,handler,文件的权限
    # if types == 'menu':
    #     menu = Menu.by_name(name)
    #     menu_permission = menu.permission.pcode
    #     if menu_permission in emp_permission:
    #         return True
    #     return False
    #
    # elif types == 'handler':
    #     handler = Handler.by_name(name)
    #     handler_permission = handler.permission.pcode
    # if handler_permission in emp_permission:
    #     return True
    # return False

    #3 判断权限


def handler_permission(handlername, types):
    def func(get):
        def warpper(self, *args, **kwargs):
            if HasPermission().has_permission(self, handlername, types):
                return get(self, *args, **kwargs)
            else:
                self.write('判断失败')
        return warpper
    return func


class AdminIndexHandler(BaseHandler):
    @admin_auth      #防止劫持攻击
    @admin_ip_list   #白名单
    @handler_permission('AdminIndexHandler', 'handler')
    def get(self):
        # superadmin = self.db.query(Employee).filter(Employee.id ==1).first()
        # for role in superadmin.roles:
        #     for permission in role.permissions:
        #         print permission.pname
        # menu = self.db.query(Menu).filter(Menu.menuname == "menuboke").first()
        # print menu.permission.pname
        self.render("admin/admin_index.html")


class FilesTableHandler(BaseHandler):
    def get(self, page):
        files = Files.display_file_list()
        files_page = self.get_page_list(int(page), files, MAX_PAGE)

        self.render("admin/files_table.html", files=files_page['split_countent'],
                    files_page=files_page)

    def get_page_list(self, current_page, countent, MAX_PAGE):
        start = (current_page - 1) * MAX_PAGE
        end = start + MAX_PAGE

        split_countent = countent[start:end]
        count = len(countent)/MAX_PAGE
        if len(countent) % MAX_PAGE != 0:
            count += 1

        pre_page = current_page - 1
        next_page = current_page + 1
        if pre_page == 0:
            pre_page = 1
        if next_page > count:
            next_page = current_page

        if count<5:
            pages = [p for p in xrange(1, count+1)]
        elif current_page <=3:
            pages = [p for p in xrange(1, 6)]
        elif current_page >=count-2:
            pages = [p for p in xrange(count-4, count+1)]
        else:
            pages = [p for p in xrange(current_page -2, current_page+3)]
        return {
            'split_countent': split_countent,
            'count': count,
            'pre_page': pre_page,
            'next_page': next_page,
            'current_page': current_page,
            'pages': pages,
        }

class JumppageHandler(BaseHandler):
    def post(self):
        name = self.get_argument("huzheng", "")
        self.redirect('/filestable/%s' % name)

