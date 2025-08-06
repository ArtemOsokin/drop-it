import re
import time

from app.core import logger


def test_logger_stdout_and_file(tmp_path, capfd):
    log_file = tmp_path / "test.log"
    logger.settings.LOG_PATH = str(log_file)
    logger.settings.LOG_LEVEL = "DEBUG"

    test_logger = logger.configure_logger()

    test_logger.debug("Debug message")
    test_logger.info("Info message")
    test_logger.warning("Warning message")
    test_logger.error("Error message")

    captured = capfd.readouterr()
    assert "Debug message" in captured.out
    assert "Info message" in captured.out
    assert "Warning message" in captured.out
    assert "Error message" in captured.out

    # Немного подождём, чтобы лог-файл записался
    time.sleep(0.1)
    assert log_file.exists()

    content = log_file.read_text()
    # Проверяем, что все сообщения есть и в файле
    assert "Debug message" in content
    assert "Info message" in content
    assert "Warning message" in content
    assert "Error message" in content

    # Проверим формат времени и уровни (пример простой проверки по шаблону)
    log_line_pattern = re.compile(
        r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \| (DEBUG|INFO|WARNING|ERROR) {0,4}\| .* - .*"
    )
    assert any(log_line_pattern.search(line) for line in content.splitlines())
