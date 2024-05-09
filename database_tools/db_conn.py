# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Project  : webspiders
@Time     : 2024/4/7
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     : 采用 peewee 实现的数据库链接工具
@Last Modify          @Version        @Author
---------------       --------        -----------
2024/4/7               1.0             Zhang ZiXu
"""
import os
from importlib import import_module
from types import ModuleType

from peewee import Model
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin


class RetryPoolMysqlDatabase(ReconnectMixin, PooledMySQLDatabase):

    def __init__(self, *args, **kwargs):
        reconnect_error = kwargs.get("reconnect_error")
        # 处理用户自定义异常重试连接
        if reconnect_error and isinstance(reconnect_error, tuple):
            ReconnectMixin.reconnect_errors = ReconnectMixin.reconnect_errors + kwargs.get("reconnect_error")
            kwargs.pop("reconnect_error")
        super().__init__(*args, **kwargs)

    def sequence_exists(self, seq):
        pass

    @classmethod
    def pool_instance(cls, name: str = None, default=None):
        """
        根据业务侧定义database连接信息进行连接，如果多数据库连接，可以指定连接的key
        Args:
            name: db连接配置中的某一个连接
            default: 默认异常返回值

        Returns:
            mysql重试连接池
        """
        work_status = bool(os.environ.get("PYTHON_IS_ONLINE"))
        # 获取项目路径，确认引入module路径
        # 确定module name
        module_name = "database_settings_debug" if not work_status else "database_settings"
        try:
            module: ModuleType = import_module("." + f"configs.{module_name}", package="common_tools")
        except Exception as e:
            print(">> !!!!! 数据库 module 动态导入失败. 请检查环境配置. ")
            return None
        # 如果module未定义，直接返回
        if not module:
            return None
        # 如果业务侧自定义连接信息，加载连接信息，支持多数据源
        if name:
            return cls(**getattr(module, name, default))
        return cls(**getattr(module, "MYSQL_CONNECT", default))


class BaseModel(Model):
    class Meta:
        database = RetryPoolMysqlDatabase.pool_instance(name="MYSQL_CONNECT")
