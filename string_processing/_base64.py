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
    d = "v5ZKZEjo9FMRKIWFbiEPe9ny4EM32FUqxBwCUs7paALi1sCb/NzQpqcOSGloELgOnEvlmOFnfvn9tVY6+XqVbSU55jjLKtRAYrIkC8hjYr8ET240u9cdidU40iu98Z4roIdr+iHTovFrQqqR/o95N54CDBm95CdgNQQGAs2Dzqs="
    print(_base64(d, "decode"))
