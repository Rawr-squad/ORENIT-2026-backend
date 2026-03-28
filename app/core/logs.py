import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

REQUEST_LOG_FILE = LOG_DIR / "requests.log"
ERROR_LOG_FILE = LOG_DIR / "errors.log"


def setup_logging():
    """Настройка логирования в файлы"""

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    root_logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    error_handler = RotatingFileHandler(
        ERROR_LOG_FILE,
        maxBytes=10_485_760,
        backupCount=5,
        encoding="utf-8"
    )
    error_handler.setLevel(logging.WARNING)  # WARNING и выше
    error_handler.setFormatter(formatter)
    root_logger.addHandler(error_handler)

    request_logger = logging.getLogger("requests")
    request_logger.setLevel(logging.INFO)
    request_logger.propagate = False

    request_handler = RotatingFileHandler(
        REQUEST_LOG_FILE,
        maxBytes=10_485_760,
        backupCount=5,
        encoding="utf-8"
    )
    request_handler.setFormatter(formatter)
    request_logger.addHandler(request_handler)


    logging.info("Логирование настроено")
    logging.info(f"Логи пишутся в: {LOG_DIR.absolute()}")