# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : func_tools.py
@Project  : common_tools
@Time     : 2023/12/6 15:16
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/12/6 15:16            1.0             Zhang ZiXu
"""
import threading


class ThreadSafeSingleton(object):
    _instances = {}
    _singleton_lock = threading.Lock()

    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instances:
            with self._singleton_lock:
                if self._cls not in self._instances:
                    self._instances[self._cls] = self._cls(*args, **kwargs)
        return self._instances[self._cls]