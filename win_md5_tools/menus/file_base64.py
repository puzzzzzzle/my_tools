import base64
import sys
import pyperclip3
import winreg as reg
import logging

import consts
from menu_operator import batch_add, batch_remove

logger = logging.getLogger(__name__)


def get_file_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read())


def encode_to_clip(path):
    try:
        b64_str = get_file_base64(path)
    except Exception as e:
        b64_str = str(e)
        logger.error(e)
    logger.info(b64_str)
    pyperclip3.copy(b64_str)


# 菜单名称
menu_name = 'base64'
# 执行一个python脚本的命令，用于打印命令行参数的第二个参数（即选中的文件路径）
py_command = rf'{consts.get_exe_str(__file__)} "%v"'
reg_root = reg.HKEY_CLASSES_ROOT
# * : 所有文件
# AllFilesystemObjects: 所有文件/文件夹
paths = [r'*\\shell']
shortcut_key = 'B'


def reg_self(is_reg):
    if is_reg:
        batch_add(reg_root, menu_name, paths, py_command, shortcut_key)
    else:
        batch_remove(reg_root, menu_name, paths)
    pass


if __name__ == '__main__':
    encode_to_clip(sys.argv[1])
    consts.on_end(menu_name)
