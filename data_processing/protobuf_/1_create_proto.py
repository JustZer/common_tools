# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : create_proto.py
@Project  : common_tools
@Time     : 2023/10/16 10:12
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/16 10:12            1.0             Zhang ZiXu
"""
import requests

from data_processing.protobuf_ import requests_pb2

headers = {
    "Accept": "application/proto"
}

proto_message = requests_pb2.TestRequest()

proto_message.field1 = 123456

proto_message.field2 = "78910"

proto_message.field3.extend([1, 2, 3, 4])

response = requests.post("http://localhost:5001/receive_proto", headers=headers, data=proto_message.SerializeToString())

print(response.text)
print(response.status_code)
