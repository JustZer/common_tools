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
import zs_protobuf

from data_processing.protobuf_ import requests_pb2
from data_processing.protobuf_ import response_pb2


headers = {
    "Accept": "application/proto"
}

proto_message = requests_pb2.TestRequest()

proto_message.field1 = 123456

proto_message.field2 = "ZingFront"

# proto_message.field3.extend([1,2,4])

response = requests.post("http://localhost:5001/receive_proto", headers=headers, data=proto_message.SerializeToString())

print(response.text)
print(response.status_code)
#
message, message_type = zs_protobuf.decode_message(response.content)
print(message)
print(message_type)



response_message = response_pb2.Reponse()
response_message.ParseFromString(response.content)
print(response_message.field1)
print(response_message.field2)