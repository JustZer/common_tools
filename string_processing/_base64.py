# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : _base64.py
@Project  : common_tools
@Time     : 2023/10/10 10:10
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/10 10:10            1.0             Zhang ZiXu
"""
import base64

DECODE = "decode"
ENCODE = "encode"


def _base64(input_string, model=DECODE, encodeing="utf-8"):
    """
    使用 BASE64 编码字符串。
    :param input_string: 要编码的字符串。
    :param model: 要编码的字符串。
    :return: 编码后的 BASE64 字符串。
    """
    input_string = input_string.replace("%3D", "=")

    if model == "encode":
        try:
            encoded_bytes = base64.b64encode(input_string.encode(encodeing))
            encoded_string = encoded_bytes.decode(encodeing)
            return encoded_string
        except Exception as e:
            return f"Error: {e}"
    elif model == "decode":
        decoded_bytes = ""
        try:
            decoded_bytes = base64.b64decode(input_string.encode(encodeing))
            decoded_string = decoded_bytes.decode(encodeing)
            return decoded_string
        except Exception as e:
            print(decoded_bytes)
            return f"Error: {e}"


if __name__ == '__main__':
    d = "87rq0AsSGohubMGUKyKZ/0jnCH6s6hTv4GhiijrPig1MGOjrzX4vEvNUnQlZKpp/6JhNa0VP/4Zn9MNfu4sGJVJ4CY1RwJjWCXKbPP2FeVWd6ZjV6io+aI9UQiDBTz07Lb8FWX74ljZIlEPV7KN46jGkweP8KUGnqMuDZ+oYKgk="
    a = "jeFc5FrnJg3CjrK1XF3FzYoBmBwvXwneEfgwy5wtl2S427Kfj55Db4LmAPAU1fAgInVL6Nc8aSq65a0s4F8w756WZekx9Cysi+2/4EOC9mS9qgcJRQV9jhPZjaZAH+8/2BXYvUuSFlAKW5p+rqE4Kx7x3ogueH20SIodtzuy/QQ="
    print(_base64(a))
