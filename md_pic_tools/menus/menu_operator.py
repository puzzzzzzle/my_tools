import winreg as reg

import logging

logger = logging.getLogger(__name__)


def add_context_menu(menu_name, command, reg_root_key_path, reg_key_path, shortcut_key):
    """
    封装的添加一个右键菜单的方法
    :param menu_name: 显示的菜单名称
    :param command: 菜单执行的命令
    :param reg_root_key_path: 注册表根键路径
    :param reg_key_path: 要添加到的注册表父键的路径（相对路径）
    :param shortcut_key: 菜单快捷键，如：'S'
    :return:
    """
    # 打开名称父键
    key = reg.OpenKey(reg_root_key_path, reg_key_path)
    # 为key创建一个名称为menu_name的sub_key，并设置sub_key的值为menu_name加上快捷键，数据类型为REG_SZ字符串类型
    reg.SetValue(key, menu_name, reg.REG_SZ, menu_name + f'(&{shortcut_key})')

    # 打开刚刚创建的名为menu_name的sub_key
    sub_key = reg.OpenKey(key, menu_name)
    # 为sub_key添加名为'command'的子键，并设置其值为command 数据类型为REG_SZ字符串类型
    reg.SetValue(sub_key, 'command', reg.REG_SZ, command)

    # 关闭sub_key和key
    reg.CloseKey(sub_key)
    reg.CloseKey(key)


def delete_reg_key(root_key, key, menu_name):
    """
    删除一个右键菜单注册表子键
    :param root_key:根键
    :param key: 父键
    :param menu_name: 菜单子键名称
    :return: None
    """
    try:
        parent_key = reg.OpenKey(root_key, key)
    except Exception as msg:
        logger.info(f"del fail, may already deleted {msg}")
        return
    if parent_key:
        try:
            menu_key = reg.OpenKey(parent_key, menu_name)
        except Exception as msg:
            logger.info(f"del fail, may already deleted {msg}")
            return
        if menu_key:
            try:
                # 必须先删除子键的子键，才能删除子键本身
                reg.DeleteKey(menu_key, 'command')
            except Exception as msg:
                logger.info(f"del fail, may already deleted {msg}")
                return
            else:
                reg.DeleteKey(parent_key, menu_name)


def batch_add(reg_root, menu_name, paths, py_command, shortcut_key):
    for item in paths:
        try:
            add_context_menu(menu_name, py_command, reg_root, item, shortcut_key)
        except Exception as e:
            logger.error(e)


def batch_remove(reg_root, menu_name, paths):
    for item in paths:
        try:
            delete_reg_key(reg_root, item, menu_name)
        except Exception as e:
            logger.error(e)
