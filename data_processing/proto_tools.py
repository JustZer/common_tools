# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : proto_tools.py
@Project  : MyProject
@Time     : 2023/11/15 11:30
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/11/15 11:30            1.0             Zhang ZiXu
"""
import os
import subprocess


def decode_proto_from_protoc(file_path=None, file_content=None, return_output=True):
    """
    使用 'protoc --decode_raw' 命令解码 protobuf 数据。
    Args:
        file_path: protobuf 文件的路径。如果提供了 file_content，则忽略此参数。
        file_content: 直接提供的 protobuf 文件内容（二进制格式）。
        return_output: 如果为 True，则返回解码后的输出。

    Returns:
        解码后的输出（如果 return_output 为 True）。
    """
    # 确保至少提供了 file_path 或 file_content 之一
    if file_content is None and (file_path is None or not os.path.exists(file_path)):
        print("必须提供有效的文件路径或文件内容。")
        return

    # 从文件中读取内容（如果未提供 file_content）
    if file_content is None:
        with open(file_path, "rb") as file:
            file_content = file.read()

    command = ["protoc", "--decode_raw"]

    # 创建 subprocess 进程来执行命令
    with subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE) as protoc_process:
        # 传递 protobuf 数据到 protoc 命令
        output, error = protoc_process.communicate(input=file_content)

    # 检查进程是否成功执行
    if protoc_process.returncode != 0:
        print("protoc 命令执行错误:", error.decode())
        return

    # 如果要求返回输出，则返回解码后的输出
    if return_output:
        return output.decode()
    return True
