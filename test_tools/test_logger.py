import logging
from pathlib import Path


def create_test_logger():

    logger = logging.getLogger("robot_test")

    logger.setLevel(logging.INFO)

    if not logger.handlers:

        # 1. 创建日志目录
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # 2. 创建日志格式
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        # 3. 终端输出
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # 4. 文件输出
        file_handler = logging.FileHandler(
            log_dir / "robot_test.log"
        )
        file_handler.setFormatter(formatter)

        # 5. 注册 Handler
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger