# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : file_spider.py
@Project  : common_tools
@Time     : 2023/11/6 16:51
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     : SCRAPY 请求中配置文件
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/11/6 16:51            1.0             Zhang ZiXu
"""
import os

import scrapy
from requests.models import RequestEncodingMixin

from scrapy import Request


class MultipartFormRequest(Request):
    def __init__(self, *args, **kwargs):
        super(MultipartFormRequest, self).__init__(*args, **kwargs)

        files = kwargs.pop("file", "")

        # 百度贴吧的特殊需求
        formdata = kwargs.pop('formdata', None)
        if formdata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        #
        if formdata:
            # _encode_files 函数是关键, 这里面需要传输两个值
            #   - files: 普遍情况下没有这个值的传参
            #   - formdata: 就是普通 POST 请求下的 fromdata 参数
            body, content_type = RequestEncodingMixin._encode_files(files, formdata)
            self._set_body(body)
            self.headers[b'Content-Type'] = content_type.encode('utf-8')


class FileSpider(scrapy.Spider):
    name = "file_spider"

    def start_requests(self):
        urls = [
            "https://www.baidu.com/",
            "https://www.sogou.com/",
            "https://www.google.com/",
        ]
        # file = get_file_content()
        for url in urls:
            yield MultipartFormRequest(
                url=url,
                callback=self.parse,
                # file=file
            )

    def get_file_content(self, current_directory, file_name):
        """
        如何给表单传递文件
            * 不同的服务端表单填写的方式不一样, 这里是以百度贴吧为例子
        Args:
            file_name: 完整的文件名称
            current_directory: 文件地址

        Returns:

        """
        file_path = os.path.join(current_directory, file_name)

        files = [(
            # data 指的是表单名称
            'data', (
                # 文件名称
                file_name,
                # 文件内容
                open(file_path, 'rb')
            )
        )]

        return files

    def parse(self, response, **kwargs):
        pass


if __name__ == '__main__':
    pass
