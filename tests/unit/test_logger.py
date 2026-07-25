from pathlib import Path

from src.logger.logger_manager import LoggerManager


def test_logger_creates_file(tmp_path):

    log_file = tmp_path / "test.log"

    logger_manager = LoggerManager()
    logger_manager.initialise("INFO", str(log_file))

    logger_manager.logger.info("Hello World")

    assert log_file.exists()

    contents = log_file.read_text(encoding="utf-8")

    assert "Hello World" in contents