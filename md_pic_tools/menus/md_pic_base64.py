import base64
import pyperclip3
import logging

logger = logging.getLogger(__name__)
# picture_format = 'png'

picture_format = 'jpeg'


def encode_to_clip(byte_data):
    base64_byte = base64.b64encode(byte_data)
    # 去除首尾多余字符
    # base64_str = (str(base64_byte))[2:-1]
    base64_str = base64_byte.decode()
    msg = '[image]:data:image/' + picture_format + ';base64,' + base64_str
    pyperclip3.copy(msg)
    logger.info("send base64 to clipboard succeed! len: " + str(len(msg)))


