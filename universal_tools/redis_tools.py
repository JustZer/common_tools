# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : redis_tools.py
@Project  : common_tools
@Time     : 2023/10/26 9:58
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     : 输出 redis 中 key 的大小
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/10/26 9:58            1.0             Zhang ZiXu
"""
import redis
from collections import defaultdict
import json


class RedisScanner:
    def __init__(self, host, port, password=None):
        self.r = redis.StrictRedis(host=host, port=port, password=password, decode_responses=False)
        self.memory_dict = defaultdict(lambda: defaultdict(float))

    def calculate_size(self, size, key):
        if size > 1024:
            size /= 1024
            size_unit = "kb"
            if size > 1024:
                size /= 1024
                size_unit = "mb"
                if size > 1024:
                    size /= 1024
                    size_unit = "gb"
        else:
            size_unit = "b"
        self.memory_dict[size_unit][key.decode()] = size
        return f"{size} {size_unit}"

    def scan_redis(self):
        keys = self.r.keys()
        print(f"共有 {len(keys)} 条.")
        output = []
        for key in keys:
            key_type = self.r.type(key)
            if key_type == b'string':
                value = self.r.get(key)
                value_length = len(value)
                value_size = value_length
            elif key_type == b'hash':
                values = self.r.hgetall(key)
                value_length = len(values)
                value_size = value_length * sum(len(value) for value in values.values())
            elif key_type == b'list':
                values = self.r.lrange(key, 0, -1)
                value_length = len(values)
                value_size = sum(len(value) for value in values)
            elif key_type == b'set':
                values = self.r.smembers(key)
                value_length = len(values)
                value_size = sum(len(value) for value in values)
            elif key_type == b'zset':
                values = self.r.zrange(key, 0, -1)
                value_length = len(values)
                value_size = sum(len(value) for value in values)
            else:
                continue  # Skip other types
            result = {
                "key": key.decode(),
                "type": key_type.decode(),
                "length": value_length,
                "size": self.calculate_size(value_size, key)
            }
            output.append(result)
        output.append(self.memory_dict)
        return json.dumps(output)


import hashlib
import redis


class RedisBloomFilter:
    """基于 Redis 的布隆过滤器类。"""

    def __init__(self, redis_host, redis_port, key, size, hash_count):
        """
        初始化基于 Redis 的布隆过滤器。

        Args:
            redis_host (str): Redis 服务器地址。
            redis_port (int): Redis 服务器端口。
            key (str): Redis 中用于存储布隆过滤器的键。
            size (int): 位数组的大小。
            hash_count (int): 哈希函数的数量。
        """
        self.redis = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
        self.key = key
        self.size = size
        self.hash_count = hash_count

    def add(self, item):
        """
        向布隆过滤器中添加元素。

        Args:
            item (str): 要添加的元素。
        """
        for i in range(self.hash_count):
            index = self.get_hash(item, i) % self.size
            self.redis.setbit(self.key, index, 1)

    def contains(self, item):
        """
        检查元素是否可能在布隆过滤器中。

        Args:
            item (str): 要检查的元素。

        Returns:
            bool: 如果元素可能存在则为True，否则为False。
        """
        for i in range(self.hash_count):
            index = self.get_hash(item, i) % self.size
            if not self.redis.getbit(self.key, index):
                return False
        return True

    def get_hash(self, item, i):
        """
        使用哈希函数生成哈希值。

        Args:
            item (str): 要哈希的元素。
            i (int): 哈希函数的索引。

        Returns:
            int: 哈希值。
        """
        hash_func = hashlib.sha256
        return int(hash_func((item + str(i)).encode()).hexdigest(), 16)



if __name__ == "__main__":
    test = False
    if test:
        host = "localhost"
        port = 6379
    else:
        host = "172.27.91.57"
        port = 8090

    scanner = RedisScanner(host=host, port=port)
    # json_output = scanner.scan_redis()
    # print(json_output)

    # 使用示例（请根据您的 Redis 配置调整参数）
    bloom = RedisBloomFilter('localhost', 6379, 'my_bloom_filter', 1000, 10)
    bloom.add('apple')
    print(bloom.contains('apple'))  # 输出: True
    print(bloom.contains('banana'))  # 输出: False