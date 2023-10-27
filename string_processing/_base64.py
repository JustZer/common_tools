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
    d = "ZR1Yby0UtCAy37llidpPqyKUWiZr+kD1YWcBsvWG5n6X+mmNmY+sIklXKyRxU1jzFQs4LcYw6coix4ngSXHyBCftBoWAltl1KYYMRFNtHrEoBN0+wInM95hRvH0U86JlG/prA/OI7yeFb+VgdsYEtiA/45fpmT1N9ky/rtd4ZtGFU/gcBXX7b7LzmsjL4tZfmfGzFsv+/wFih6gPOtWdhhKGkPEJTsneezFea/TxJlByUU/vsiJr33hApsSRW+XXs5WiI1gqWb21tYmFkRrUwIBsxfps47jaPBXuq1yA/bB5PoY6BMuH+2QqeecBhcNaAUfLQTfnwlSG2I1uDsvPwDhvHnyf1YGAT4wViHcNDkM62wH20GTjdOw5wC3Tpvh2RWBObj9/OvixME+KOC1yTtS9yoUmCl1Ho1a/KUZ/bV0EMldD7ubgu53rB25nnBCYYOrkpqDfyitcaCp2iIaLZZvOmdZURZqiDmJf8tYOhDi1vU/5SMLy7l4LJlbRP7SXYf4IZvt4z5TCqlIdsbKD6uskIl5ukY1FHeHsRQMD72CpnW7BbE9JfS1luJHeM9XDvHdm6JUOTI0peCTu9phLeM/9/a6nVmy651ZUbLu/Z7A34nTWKTs42T9OnIiSnqrgtm32EMZUIhPvmJRJHx6aKemVd74YGhYIKz5yTu/XXUUN8crSmJGHCgq/h4OYRDqkKRvx5pjHNWyNr4Ec6g2b16VvXFR5oS6UarfsC5lEkuSkmsTNQKjE16bCi7AYSF6mRE9ARVwemiaMw0+G7ZZz0y64K449kwMHDRo1dkK/75OZG6qQI3Y0+Wm/w+3pWOfWYf2UxEhtJfZEzKbdT/hzp1WFcDeOL1nBrNsh2vZ5cU4="
    print(_base64(d, "encode"))
