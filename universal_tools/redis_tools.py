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
        keys = self.r.scan_iter()
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


if __name__ == "__main__":
    scanner = RedisScanner(host="localhost", port=6379)
    json_output = scanner.scan_redis()
    print(json_output)
