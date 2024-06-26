# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File     : logger_manager.py
@Project  : mobile_control
@Time     : 2023/8/22 10:25
@Author   : Zhang ZiXu
@Software : PyCharm
@Desc     :  
@Last Modify Time          @Version        @Author
--------------------       --------        -----------
2023/8/22 10:25            1.1             Zhang ZiXu
2024/1/4                   1.2             Zhang ZiXu
2024/5/11                  1.3             Zhang ZiXu
"""
import configparser
import os
import logging
from logging.handlers import RotatingFileHandler


class LoggerUtil:
    _instance = None

    def __init__(self, logger_name: str = 'root', config_name: str = 'DEFAULT', config_file: str = None,
                 logger_level: str = "INFO"):
        """

        Args:
            logger_name: 日志名称, 如配置中需要进行日志文件存储, 此参数即日志文件名称
            config_name: 配置文件名称, 默认为 DEFAULT
            config_file: 配置文件路径
        """
        self.logger_name = logger_name
        self.logger_level = logger_level
        self.logger = logging.getLogger(logger_name)
        self.config = self._load_config(config_name, config_file)
        self._setup_logger()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggerUtil, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def _load_config(config_name, config_file):
        """
        载入 logger 配置文件
        Args:
            config_name: logger 配置名称
            config_file: logger

        Returns:

        """
        if config_file is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_file = os.path.join(base_dir, 'configs', 'logger_config.ini')

        if not os.path.exists(config_file):
            raise FileNotFoundError(f"配置文件 {config_file} 不存在.")

        config = configparser.RawConfigParser()
        config.read(config_file)
        return config[config_name]

    def _setup_logger(self):
        log_level = getattr(logging, self.logger_level.upper() or self.config.get('LOG_LEVEL', 'INFO'))
        log_format = self.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger.setLevel(log_level)
        formatter = logging.Formatter(log_format)

        # 流处理器，用于控制台输出
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        if bool(self.config.get('SAVE_FILE', None)):
            # 最好不要设置 LOG_FILE_PATH 日志地址, 避免 .gitignore 没有覆盖到位导致日志上传
            log_file_path = self.config.get('LOG_FILE_PATH', 'logs')
            log_file_name = '{}.log'.format(self.logger_name)

            # 确保日志文件夹存在
            base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_directory: str = os.path.join(os.path.dirname(base_dir), log_file_path)
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)

            log_file = os.path.join(log_directory, log_file_name)

            max_bytes = int(self.config.get('MAX_BYTES', 10485760))  # 10MB
            backup_count = int(self.config.get('BACKUP_COUNT', 5))
            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


if __name__ == '__main__':
    logger_util = LoggerUtil(logger_level="DEBUG")
    logger = logger_util.get_logger()
    logger.info("This is a test log message.")
    logger.debug("This is a test log message.")
