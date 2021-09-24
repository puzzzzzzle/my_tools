from PIL import Image
from PIL import ImageGrab
from io import BytesIO
import winreg as reg
import logging

import consts
from md_pic_base64 import encode_to_clip
from menu_operator import batch_add, batch_remove

logger = logging.getLogger(__name__)
# picture_format = 'png'


picture_format = 'jpeg'


def encode_image_from_clip():
    image = ImageGrab.grabclipboard()
    if not isinstance(image, Image.Image):
        # tkinter.messagebox.showinfo("picture2base64", "not a image in clipboard.")
        logger.info("not a image in clipboard.")
        raise Exception("not a image in clipboard.")
    img_buffer = BytesIO()
    image.save(img_buffer, format=picture_format, optimize=True, quality=40)
    byte_data = img_buffer.getvalue()
    encode_to_clip(byte_data)


# 菜单名称
menu_name = 'md pic from clip'
# 执行一个python脚本的命令，用于打印命令行参数的第二个参数（即选中的文件路径）
py_command = rf'{consts.get_exe_str(__file__)} "%v"'
reg_root = reg.HKEY_CLASSES_ROOT
# * : 所有文件
# AllFilesystemObjects: 所有文件/文件夹
paths = [r'*\\shell', r'AllFilesystemObjects\\shell', r"Directory\\shell",r"Directory\\Background\\shell","Drive\\shell"]
shortcut_key = ''


def reg_self(is_reg):
    if is_reg:
        batch_add(reg_root, menu_name, paths, py_command, shortcut_key)
    else:
        batch_remove(reg_root, menu_name, paths)
    pass


if __name__ == '__main__':
    try:
        encode_image_from_clip()
        consts.on_end(menu_name)
    except Exception as e:
        logger.error(f"fail {e}")
        consts.on_error(e)
