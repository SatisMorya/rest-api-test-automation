"""Structured file logging: timestamp | level | test name | message."""
import logging

from config.settings import PROJECT_ROOT

LOG_FILE = PROJECT_ROOT / "logs" / "api_tests.log"
_current_test = "-"


def set_current_test(name: str) -> None:
    """Called by a fixture so every log line carries the running test name."""
    global _current_test
    _current_test = name


class _TestNameFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.test_name = _current_test
        return True


def get_logger(name: str = "api_tests") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    handler.addFilter(_TestNameFilter())
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(test_name)s | %(message)s")
    )
    logger.addHandler(handler)
    return logger
