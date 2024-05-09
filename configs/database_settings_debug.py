# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Project  : webspiders
@Time     : 2024/4/7
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify          @Version        @Author
---------------       --------        -----------
2024/4/7               1.0             Zhang ZiXu
"""
from peewee import OperationalError, InterfaceError

MYSQL_CONNECT = {
    # 数据库基础连接信息
    "host": "192.168.93.49",
    "password": "whlgcs",
    "user": "rays",
    "port": 3306,
    "database": "webspider",
    "charset": "utf8mb4",
    # 最大连接数。提供None无限。
    "max_connections": 32,
    # 允许使用连接的秒数
    "stale_timeout": 0,
    # 池已满时阻塞的秒数。默认情况下，当池已满时，peewee 不会阻塞，而只是抛出异常。要无限期地阻止，将此值设置为0。
    "timeout": 20,
    # 支持自定义异常重试连接，异常依tuple类型组织，否则无法识别
    # 测试是否支持 添加(OperationalError, '2003')，修改mysql IP 为无法连接IP，查看重试连接次数是否增加
    # "reconnect_error": ((OperationalError, "(0, '')"), (InterfaceError, "1234"))
}