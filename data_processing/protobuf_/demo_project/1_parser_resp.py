# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : 1_parser_resp.py
@Project  : common_tools
@Time     : 2023/10/27 15:25
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/27 15:25            1.0             Zhang ZiXu
"""
import json

import requests
import zs_protobuf

# 数据源 <二进制>
response = requests.get("http://localhost:5001/test_proto_data?is_show=T")

message, message_type = zs_protobuf.decode_message(response.content)

print(json.dumps(message))
print(json.dumps(message_type))
