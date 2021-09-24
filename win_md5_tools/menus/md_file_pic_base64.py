import sys

from PIL import Image
from PIL import ImageGrab
from io import BytesIO
import winreg as reg
import logging

import consts
from md_pic_base64 import encode_to_clip
from menu_operator import batch_add, batch_remove

logger = logging.getLogger(__name__)
picture_format = 'png'


# picture_format = 'jpeg'


def encode_image_from_clip(path):
    logger.info(path)
    with open(path,"rb") as f:
        encode_to_clip(f.read())


# 菜单名称
menu_name = 'md pic file base64'
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
    try:
        encode_image_from_clip(sys.argv[1])
        consts.on_end(menu_name)
    except Exception as e:
        logger.error(f"fail {e}")
        consts.on_error(e)
