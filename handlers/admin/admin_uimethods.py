#coding:utf-8
from admin_handler import HasPermission

def menu_permission(self, menuname, types):
    if HasPermission().has_permission(self, menuname, types):
        return True
    return False



