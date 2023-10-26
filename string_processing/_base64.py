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


def _base64(input_string, model="encode", encodeing="utf-8"):
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
    d = "eJoEFIhnAceJnFv2eSzGAg8b4eqn33knlSSQSyOWguZ68OGl13xU1n4RA6Q2gZNJLBSpIT5D1mTi8hDc7Ca1EFjXpOtTYo0NC/6EU88FLh4LjvxdzDqE3yiaqBs2c0IdQr0u2U8gFXuzYGpI/G6Ur+EIUptdskyvwahvcrumc8Y="
    print(_base64(d, "decode"))
