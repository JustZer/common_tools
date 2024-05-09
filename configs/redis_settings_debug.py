# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@Project  : dcg-spider-data
@Time     : 2024/4/10
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify          @Version        @Author
---------------       --------        -----------
2024/4/10               1.0             Zhang ZiXu
"""
REDIS_CLUSTER_CONNECT = {
    "startup_nodes": [
        {"host": "192.168.92.121", "port": "7000"},
        {"host": "192.168.92.121", "port": "7001"},
        {"host": "192.168.92.121", "port": "7002"},
        {"host": "192.168.92.122", "port": "7003"},
        {"host": "192.168.92.122", "port": "7004"},
        {"host": "192.168.92.122", "port": "7005"},
    ],
    "password": "Lgsc@2021",  # 如果你的Redis集群设置了密码
    "decode_responses": True,  # 根据需要设置
    "skip_full_coverage_check": True  # 如果你的Redis集群不支持或未启用完全覆盖检查
}
