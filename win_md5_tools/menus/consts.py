import os
import time
import logging
from pathlib import Path
import sys

sourceDir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
projectDir = os.path.abspath(Path(sourceDir))
pythonExe = sys.executable


def get_logger(name):
    return logging.getLogger(name)


def mkdir_recursively(path):
    '''
    Create the path recursively, same as os.makedirs().

    Return True if success, or return False.

    e.g.
    mkdir_recursively('d:\\a\\b\\c') will create the d:\\a, d:\\a\\b, and d:\\a\\b\\c if these paths does not exist.
    '''

    # First transform '\\' to '/'
    local_path = path.replace('\\', '/')

    path_list = local_path.split('/')

    if path_list is None: return path

    # For windows, we should add the '\\' at the end of disk name. e.g. C: -> C:\\
    disk_name = path_list[0]
    if len(disk_name) >= 1 and disk_name[1] == ':': path_list[0] = path_list[0] + '\\'

    curr_dir = ''
    for path_item in path_list:
        curr_dir = os.path.join(curr_dir, path_item)
        if os.path.exists(curr_dir):
            if os.path.isdir(curr_dir):
                pass
            else:  # Maybe a regular file, symlink, etc.
                return False
        else:
            try:
                os.mkdir(curr_dir)
            except Exception as e:
                print(f"mkdir error: {curr_dir} {e}")

    return path


def __init_logger():
    """
    初始化日志系统
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel("DEBUG")
    basic_format = "[%(asctime)s]\t[%(levelname)s]\t%(message)s\t[\"%(pathname)s:%(lineno)s\"] [%(name)s]"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(basic_format, date_format)
    # cli
    cli_log = logging.StreamHandler()
    cli_log.setFormatter(formatter)
    cli_log.setLevel("DEBUG")
    logger.addHandler(cli_log)
    # # curr log file
    # base_log_dir = mkdir_recursively(str(Path(projectDir) / "logs"))
    # once_log = logging.FileHandler(f"{base_log_dir}/all.log")
    # once_log.setFormatter(formatter)
    # logger.addHandler(once_log)
    # # all log file
    # all_log = logging.FileHandler(f"{base_log_dir}/curr.log", "w")
    # all_log.setFormatter(formatter)
    # logger.addHandler(all_log)
    # logging.info(f"log init at {time.asctime(time.localtime(time.time()))}")


__init_logger()

_global_dict = {}


def set_value(key, value):
    """ 定义一个全局变量 """
    global _global_dict
    _global_dict[key] = value


def get_value(key, default=None):
    """ 获得一个全局变量,不存在则返回默认值 """
    global _global_dict
    if key not in _global_dict.keys():
        return default
    return _global_dict[key]


def on_error(e):
    logging.getLogger(__name__).error(e)
    # os.system('pause')


def on_end(para):
    logging.getLogger(__name__).info(para)
    os.system('pause')


def get_exe_str(file):
    p = Path(projectDir) / os.path.basename(file)
    return f'"{pythonExe}" "{str(p)}"'
