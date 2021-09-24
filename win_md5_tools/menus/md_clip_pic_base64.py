import os
import sys
import base64
from PIL import Image
from PIL import ImageGrab
from io import BytesIO
import pyperclip3
import winreg as reg
import logging

import consts
from file_base64 import get_file_base64
from menu_operator import batch_add, batch_remove

logger = logging.getLogger(__name__)
# picture_format = 'png'


picture_format = 'jpeg'


def encode_image_from_clip():
    image = ImageGrab.grabclipboard()
    if not isinstance(image, Image.Image):
        # tkinter.messagebox.showinfo("picture2base64", "not a image in clipboard.")
        logger.info("not a image in clipboard.")
        consts.on_error(Exception("not a image in clipboard."))
        return
    img_buffer = BytesIO()
    image.save(img_buffer, format=picture_format, optimize=True, quality=40)
    byte_data = img_buffer.getvalue()
    base64_byte = base64.b64encode(byte_data)
    # 去除首尾多余字符
    # base64_str = (str(base64_byte))[2:-1]
    base64_str = base64_byte.decode()
    msg = '[image]:data:image/' + picture_format + ';base64,' + base64_str
    pyperclip3.copy(msg)
    logger.info("send base64 to clipboard succeed! len: " + str(len(msg)))


# 菜单名称
menu_name = 'md pic from clip'
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
    encode_image_from_clip()
    consts.on_end(menu_name)
