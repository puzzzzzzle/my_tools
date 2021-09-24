# coding:utf-8
# 打印出命令行参数第2个参数
import sys
import os
import logging
import winreg as reg

import consts
from menu_operator import batch_add, batch_remove

logger = logging.getLogger(__name__)
# 菜单名称
menu_name = 'Show file path'
py_command = rf'{consts.get_exe_str(__file__)} "%v"'
reg_root = reg.HKEY_CLASSES_ROOT
# paths = [r'*\\shell', r'Directory\\shell', r'Directory\\Background\\shell', r'Drive\\shell']
paths = [r'*', r'*\\shell', r'Directory\\shell', r'Directory\\Background\\shell', r'Drive\\shell']
shortcut_key = 'S'


def reg_self(is_reg):
    if is_reg:
        batch_add(reg_root, menu_name, paths, py_command, shortcut_key)
    else:
        batch_remove(reg_root, menu_name, paths)


if __name__ == '__main__':
    print(f'current path is: {sys.argv[1]}')
    os.system('pause')

    # consts.on_end(menu_name)
