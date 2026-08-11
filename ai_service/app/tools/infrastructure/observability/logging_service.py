import logging
from typing import Any, Dict, Optional

class LoggingService:
    """
    Centralized logging service for the application.
    """
    def __init__(self, name: str = "ai_service"):
        self.logger = logging.getLogger(name)

    def info(self, message: str, **kwargs: Any) -> None:
        self.logger.info(message, extra=kwargs)

    def error(self, message: str, exc_info: Optional[Exception] = None, **kwargs: Any) -> None:
        self.logger.error(message, exc_info=exc_info is not None, extra={"exception": str(exc_info), **kwargs})

    def warning(self, message: str, **kwargs: Any) -> None:
        self.logger.warning(message, extra=kwargs)
        
    def debug(self, message: str, **kwargs: Any) -> None:
        self.logger.debug(message, extra=kwargs)
