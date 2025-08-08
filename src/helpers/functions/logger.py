import logging
from datetime import datetime, timezone, tzinfo
import threading

class IsoFormatter(logging.Formatter):
    """Formatter que insere timestamps ISO8601 com timezone."""
    def formatTime(self, record, datefmt=None):
        # Gera datetime UTC e converte para ISO com Z ou +HH:MM
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        # Ex.: 2025-07-16T12:34:56.789+00:00
        return dt.isoformat()

class Logger:
    """Singleton para configuração global de logging."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, name: str = None, file: str = None, level: int = logging.INFO):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._configure(name or "root", file, level)
        return cls._instance

    def _configure(self, name: str, file: str, level: int):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        fmt = IsoFormatter(fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(fmt)
        self.logger.addHandler(ch)

        if file:
            fh = logging.FileHandler(file)
            fh.setLevel(level)
            fh.setFormatter(fmt)
            self.logger.addHandler(fh)

    @classmethod
    def get_logger(cls):
        """Retorna o logger pré-configurado."""
        if cls._instance is None:
            cls()
        return cls._instance.logger