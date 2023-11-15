# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : test_web.py
@Project  : common_tools
@Time     : 2023/10/16 10:16
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/16 10:16            1.0             Zhang ZiXu
"""
from flask import Flask, request, jsonify
from google.protobuf.json_format import MessageToJson

from data_processing.protobuf_ import server_response_pb2

app = Flask(__name__)


@app.route('/')
def welcome():
    return 'Welcome to the test page'


@app.route("/test")
def test():
    return "测试路由1"


@app.route('/receive_proto', methods=['POST'])
def receive_proto():
    response = server_response_pb2.Response()

    # 校验 Accept 字段是否为 application/proto
    if request.headers['Accept'] != 'application/proto':
        response.result_code = 400001
        response.message = 'Error ~ Invalid Accept header'
        return response.SerializeToString()

    # if response.headers.get("")

    data = request.data  # 这里获取了原始的 Proto 数据流
    # 在这里你可以对接收到的 Proto 数据进行处理，可以尝试使用相应的解析工具来解析 Proto 数据
    # 例如可以使用 protobuf 库解析数据
    # 例如：解析 Proto 数据
    proto_message = server_response_pb2.Response()
    proto_message.ParseFromString(data)

    # 校验数据结果
    if proto_message.message != "ZingFront":
        response.result_code = 400002
        response.message = 'Error ~ Wrong Key ~'
        return response.SerializeToString()


    len_string_list = len(proto_message.string_list)
    len_int_list = len(proto_message.int_list)

    if 3 < len_string_list < 5 or len_int_list > 3:
        response.result_code = 400003
        response.message = 'Error ~ Message Type ~'
        return response.SerializeToString()

    # 返回正常值
    response.result_code = 200000
    response.message = 'SUCCESS POST~'
    # 准备需要返回的值
    response.int_list.extend([11, 22, 33, 44, 55])
    response.nested_string = "Job details"
    response.string_map.update({"Test work": "ProtoText", "Preparations": "Touch the fish"})
    for i in range(3):
        repeated_nested_message = response.repeated_nested_message.add()
        if i == 1:
            nested_string = "Say important things three times!!!"
        else:
            nested_string = "leave work in one hour ~~~"
        repeated_nested_message.nested_int = i
        repeated_nested_message.nested_string = nested_string

    # 可以将解析后的数据转为 JSON 格式输出
    return response.SerializeToString()


# 返回测试 Proto 数据的路由
@app.route('/test_proto_data', methods=['GET'])
@app.route('/test_proto_data.json', methods=['GET'])
def test_proto_data():
    is_show = request.args.get('is_show', False)  # 获取 is_show 参数，默认为 False

    # 构建测试数据，根据 server_response.proto 定义的数据结构
    response = server_response_pb2.Response()
    response.result_code = 200000
    response.message = "Test Message"
    response.int_list.extend([1, 2, 3, 4, 5])
    response.string_list.extend(["string1", "string2", "string3"])
    response.float_number = 3.14
    response.double_number = 6.28
    response.is_success = True

    nested_message = response.nested_message
    nested_message.nested_int = 100
    nested_message.nested_string = "Nested String"

    for i in range(3):
        repeated_nested_message = response.repeated_nested_message.add()
        repeated_nested_message.nested_int = i
        repeated_nested_message.nested_string = f"Repeated Nested String {i}"

    response.string_map.update({"key1": "value1", "key2": "value2"})

    response.enum_field = server_response_pb2.EnumType.OPTION_B

    if is_show or request.path.endswith('.json'):
        if is_show:
            serialized_data = response.SerializeToString()
            return serialized_data
        else:
            json_data = MessageToJson(response)
            return jsonify(json_data)
    else:
        return 'Creat Proto Data Success'


if __name__ == '__main__':
    app.run(host="localhost", port=5001, debug=True)
