import logging
import sys

sys.path.append("./menus")

import menus
import consts as consts

logger = logging.getLogger(__name__)

# # 菜单名称
# menu_name = 'md pic base64'
# # 执行一个python脚本的命令，用于打印命令行参数的第二个参数（即选中的文件路径）
# py_command = rf'"{consts.pythonExe}" "{consts.projectDir}/menus/{__file__}" "%v"'
# reg_root = reg.HKEY_CLASSES_ROOT
# # * : 所有文件
# # AllFilesystemObjects: 所有文件/文件夹
# paths = [r'*\\shell']
# shortcut_key = 'B'
auto_reg = menus


def get_reg_info():
    ret = []
    import inspect
    for reg_module_name in dir(auto_reg):
        reg_module = getattr(auto_reg, reg_module_name)
        if reg_module is not None and inspect.ismodule(reg_module):
            try:
                reg_func = getattr(reg_module, "reg_self")
                if reg_func is not None and inspect.isfunction(reg_func):
                    logger.debug(f"get one module {reg_module_name}")
                else:
                    logger.error(f"fail, cannot get reg func {reg_module_name}")
                reg_name = getattr(reg_module, "menu_name")
                if reg_name is None or not isinstance(reg_name, str):
                    reg_name = "unknown"
                ret.append((reg_name, reg_func, reg_module_name))
            except Exception as e:
                logger.info(f"not need {reg_module_name}")
    return ret


def do_reg_all(is_reg=True):
    infos = get_reg_info()
    for name, func, reg_module_name in infos:
        logger.info(f"---  now reg({is_reg}) [{name}] by [{reg_module_name}]")
        try:
            func(is_reg)
        except Exception as e:
            logger.error(f"fail {e}")
            consts.on_error(e)


def do_reg_one(cmd_name, is_reg=True):
    infos = get_reg_info()
    for name, func, reg_module_name in infos:
        if name == cmd_name:
            logger.info(f"---  now reg({is_reg}) [{name}] by [{reg_module_name}]")
            try:
                func(is_reg)
            except Exception as e:
                logger.error(f"fail {e}")
                consts.on_error(e)


if __name__ == '__main__':
    if len(sys.argv) ==1:
        logger.info("register all")
        do_reg_all(True)
    else:
        flag = "true" == sys.argv[1].lower()
        logger.info(f"is register {flag}")
        do_reg_all(flag)
        pass
    # do_reg_one("md pic from clip", True)
    pass
