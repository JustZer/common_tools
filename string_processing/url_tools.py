# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : url_tools.py
@Project  : MyProject
@Time     : 2023/11/10 14:02
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/11/10 14:02            1.0             Zhang ZiXu
"""
from urllib import parse


def is_valid_url(url: str) -> bool:
    """
    判断一个字符串是否符合 URL 格式。

    Args:
        url (str): 待判断的字符串。

    Returns:
        bool: 如果字符串符合 URL 格式，返回 True；否则返回 False。
    """
    try:
        result = parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def parse_url_params(url: str) -> tuple:
    """
    解析 URL 并提取查询参数。

    Args:
        url (str): 待解析的 URL。

    Returns:
        tuple: 包含 API 地址和查询参数的元组 (api, params)。
    """
    params = {}
    if not is_valid_url(url):
        return url, params

    parsed_url = parse.urlparse(url)
    api = f"{parsed_url.scheme}://{parsed_url.hostname}{parsed_url.path}"

    # 从解析后的结果中获取查询参数部分，并使用 parse_qs 解析成字典形式
    query_params = parse.parse_qs(parsed_url.query)
    for key, value in query_params:
        params[key]: value[0]
    return api, params


def build_url(api: str, params: dict) -> str:
    """
    根据 API 地址和参数构建完整的 URL。

    Args:
        api (str): API 地址。
        params (dict): 查询参数字典。

    Returns:
        str: 构建完成的 URL。
    """
    # 将参数编码为查询字符串
    encoded_params = parse.urlencode(params)
    # 将 API 地址和查询字符串拼接成完整的 URL
    full_url = f"{api}?{encoded_params}"
    return full_url


if __name__ == '__main__':
    url = ("https://jc.zhcw.com/port/client_json.php?callback=jQuery11220623738832912706_1699587391154&"
           "transactionType=10001001&lotteryId=1&issueCount=30&endDate=&type=0&pageNum=1&pageSize=30&"
           "tt=0.22023995540406527&_=1699587391155")
    api, params = parse_url_params(url)


