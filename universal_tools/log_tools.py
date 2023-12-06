# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : log_tools.py
@Project  : mobile_control
@Time     : 2023/8/22 10:25
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/8/22 10:25            1.1             Zhang ZiXu
"""
import datetime
import logging
import os
from logging.handlers import RotatingFileHandler

from universal_tools.func_tools import ThreadSafeSingleton


@ThreadSafeSingleton
class LoggerTool(logging.Logger):
    """
    自定义的日志记录器，继承自 logging.Logger。
    通过读取配置文件和创建文件和控制台处理器，实现日志的记录。
    使用单例模式以确保整个应用中只有一个日志记录器实例。
    """
    log_max_size = None
    log_backup_count = None

    def __init__(self, logger_name, **kwargs):
        """
        初始化日志记录器。

        Args:
            logger_name (str): 日志记录器的名称。
        """
        super().__init__(logger_name, logging.DEBUG)
        self.local_time = datetime.datetime.today().strftime("%Y-%m-%d")
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        self._init_file_configs()
        self._init_save_path(**kwargs)
        self._init_handlers()

    def _init_file_configs(self):
        """
        初始化文件配置
        Returns:

        """
        self.log_max_size = 1048576
        self.log_backup_count = 5

    def _init_save_path(self, **kwargs):
        """
        初始化日志文件的存储路径
        Args:
            kwargs:
                save_status(bool): 是否存储在本地项目的 Logs 文件夹中
                save_file_name(str): 日志存储文件名

        Returns:

        """
        try:
            save_file_name = str(kwargs.get("save_file_name", "logs"))
        except Exception as e:
            self.warning("## 日志存储文件名未设置，将使用默认文件名 logs")
            save_file_name = "logs"

        if bool(kwargs.get("save_status")) or False:
            script_path = os.path.abspath(__file__)
            self.script_gen_directory = os.path.dirname(os.path.dirname(script_path))

            # 创建日志目录
            if not os.path.exists(os.path.join(self.script_gen_directory, save_file_name)):
                os.mkdir(os.path.join(self.script_gen_directory, save_file_name))

            logs_directory = os.path.join(self.script_gen_directory, save_file_name)

            if not os.path.exists(os.path.join(logs_directory, self.name)):
                os.mkdir(os.path.join(logs_directory, self.name))

            script_logs_directory = os.path.join(logs_directory, self.name)
            script_logs_directory = os.path.join(script_logs_directory, f"{self.name}-{self.local_time}.log")

            rotating_handler = RotatingFileHandler(
                filename=script_logs_directory,
                maxBytes=self.log_max_size,
                backupCount=self.log_backup_count,
                encoding="utf-8"
            )
            rotating_handler.setFormatter(self.formatter)
            self.addHandler(rotating_handler)

    def _init_handlers(self):
        """
        初始化日志处理器。
        包括文件处理器和控制台处理器，用于记录日志到文件和控制台。
        """

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter)

        self.addHandler(stream_handler)


if __name__ == "__main__":
    logger = LoggerTool(logger_name="Logger")
    for i in range(100):
        logger.info(f"This is an example log message. for {i} <<<<<<<<<<<<<<<<")
