# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : json_work.py
@Project  : common_tools
@Time     : 2023/10/26 10:29
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/26 10:29            1.0             Zhang ZiXu
"""


def parse_multi_dict(_dict, keys=(), default={}) -> dict or type:
    """
    解析dict
    :param _dict: 目标dict
    :param keys: 按照key层级排序的key列表
    :return: 解析出的value
    :param default: 默认值，默认为空dict
    """
    if default is None:
        default = {}
    if not _dict:
        return default
    if keys:
        try:
            data = _dict[keys[0]]
        except (IndexError, KeyError) as e:
            return default
        if not data:
            return default
    else:
        return _dict
    for key in keys[1:]:
        try:
            data = data[key]
        except (IndexError, KeyError) as e:
            return default
    return data


def extract_keys_with_path(data, target_key, current_path=None, paths=None) -> list:
    """
    递归提取json中指定key的路径
    Args:
        data: 数据源
        target_key: 需要查询的字段
        current_path: 起始路径, 这块属于自定义, 觉得太麻烦可以先自己截取一部分 JSON 在运行这个函数, 默认是
                      None, 即从根节点开始
        paths: 存储路径

    Returns:
        不存在则返回空列表, 如果查询字段存在则返回 [["p1", "p2", ...]]
    """
    if current_path is None:
        current_path = []
    if paths is None:
        paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                paths.append(current_path + [key])
            if isinstance(value, list):
                for index, item in enumerate(value):
                    if isinstance(item, dict):
                        if target_key in item:
                            paths.append(current_path + [key, index, target_key])
            if isinstance(value, (dict, list)):
                extract_keys_with_path(value, target_key, current_path + [key], paths)

    return paths


if __name__ == '__main__':
    a = {
        "user_info": {
            "ad_signed": 0,
            "id": "",
            "login_app_id": "",
            "login_open_id": "",
            "login_state": 0,
            "member_level": 0,
            "type": 7,
            "ad_info": [{
                "rpt_msg_ad_info": "abc"
            }, {
                "rpt_msg_ad_infos": "bcd"
            }
            ]
        },
        "user_location": {},
        "user_type": 0
    }
    # extract_keys_with_path(a, "rpt_msg_ad_info")
    print(parse_multi_dict(a, ("user_info", "ad_info"), default=[]))