# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Project  : dcg-spider-data
@Time     : 2024/4/10
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     : redis 链接工具
                * 目前仅支持 cluster 集群模式
@Last Modify          @Version        @Author
---------------       --------        -----------
2024/4/10               1.0             Zhang ZiXu
"""
import os
from rediscluster import RedisCluster
from importlib import import_module


class ReconnectMixin:
    """提供重连功能的 Mixin"""
    reconnect_errors = (ConnectionError, TimeoutError)


class RetryPoolRedisCluster(ReconnectMixin):
    def __init__(self, *args, **kwargs):
        reconnect_error = kwargs.pop("reconnect_error", None)
        if reconnect_error and isinstance(reconnect_error, tuple):
            self.reconnect_errors += reconnect_error
        self.cluster = RedisCluster(*args, **kwargs)

    @classmethod
    def cluster_instance(cls, name: str = None, default=None):
        """根据业务侧定义 Redis 集群连接信息进行连接"""
        debug_status = os.environ.get("PYTHON_IS_ONLINE", False)
        module_name = "redis_settings_debug" if debug_status else "redis_settings"
        try:
            module = import_module("." + f"configs.{module_name}", package="common_tools")
        except Exception as e:
            print(">> !!!!! Redis cluster module 动态导入失败. 请检查环境配置. ")
            return None
        if not module:
            return None
        if name:
            return cls(**getattr(module, name, default))
        return cls(**getattr(module, "REDIS_CLUSTER_CONNECT", default))


# 使用示例
if __name__ == "__main__":
    redis_cluster_instance = RetryPoolRedisCluster.cluster_instance().cluster
    if redis_cluster_instance is not None:
        print(redis_cluster_instance.get("t1"))
