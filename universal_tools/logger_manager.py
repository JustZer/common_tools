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
import logging
import os
from logging.handlers import RotatingFileHandler


class LoggerUtil:
    _instance = None

    def __init__(self, logger_name: str = 'root', config_name: str = 'DEFAULT', config_file: str = None,
                 logger_level: str = "INFO"):
        """
        初始化日志管理器，配置日志输出到控制台和文件。

        Args:
            logger_name: 日志名称（日志文件名）。
            config_name: 配置文件中的配置项名称，默认 'DEFAULT'。
            config_file: 配置文件路径。
            logger_level: 日志级别，默认为 'INFO'。
        """
        self.logger_name = logger_name
        self.logger_level = logger_level.upper()  # 保证是大写
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
        载入 logger 配置文件。

        Args:
            config_name: 配置文件中的配置项名称。
            config_file: 配置文件路径。

        Returns:
            dict: 配置文件中的配置项。
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
        """
        配置日志的格式和输出目标，包括控制台和文件。
        """
        log_level = getattr(logging, self.logger_level, logging.INFO)
        log_format = self.config.get('LOG_FORMAT', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self.logger.setLevel(log_level)
        formatter = logging.Formatter(log_format)

        # 流处理器：用于控制台输出
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 文件处理器：将日志保存到文件
        if bool(self.config.get('SAVE_FILE', False)):
            log_file_path = self.config.get('LOG_FILE_PATH', 'logs')
            log_file_name = f'{self.logger_name}.log'

            # 确保日志文件夹存在
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_directory = os.path.join(base_dir, log_file_path)
            os.makedirs(log_directory, exist_ok=True)

            log_file = os.path.join(log_directory, log_file_name)

            max_bytes = int(self.config.get('MAX_BYTES', 10485760))  # 默认10MB
            backup_count = int(self.config.get('BACKUP_COUNT', 5))
            file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        获取日志记录器实例。

        Returns:
            logging.Logger: 返回 Logger 实例。
        """
        return self.logger

    def log_exception(self, exception, message="An error occurred"):
        """
        日志记录异常信息，并显示堆栈追踪。

        Args:
            exception: 捕获的异常对象。
            message: 自定义消息。
        """
        self.logger.error(message, exc_info=exception)


if __name__ == '__main__':
    logger_util = LoggerUtil(logger_level="DEBUG")
    logger = logger_util.get_logger()
    logger.info("This is a test log message.")
    try:
        1 / 0
    except ZeroDivisionError as e:
        logger_util.log_exception(e, "Exception occurred while dividing by zero.")
