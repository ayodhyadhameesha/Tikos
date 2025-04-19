import logging
import os
from datetime import datetime
from pathlib import Path

# Create logs/ directory if not exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Keep only the latest 100 error logs
MAX_LOGS = 100
#Cleaning old logs
def cleanup_old_logs():
    log_files = sorted(LOG_DIR.glob("error_*.log"), key=lambda f: f.stat().st_mtime, reverse=True)
    old_logs = log_files[MAX_LOGS:]
    for log in old_logs:
        try:
            log.unlink()
        except Exception as e:
            print(f" Failed to delete old log {log.name}: {e}")

# Create a unique log file for each error (timestamped)
def get_error_logger():
    
    cleanup_old_logs()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = LOG_DIR / f"error_{timestamp}.log"

    logger = logging.getLogger(f"error_logger_{timestamp}")
    logger.setLevel(logging.ERROR)

    # Avoid adding multiple handlers if this logger already exists
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
