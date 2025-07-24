import logging
from datetime import datetime
from .path_manager import PathManager

class Logger:
    """Centralized logging utility for the automation framework"""
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance
    
    def _setup_logger(self):
        """Setup the logger with proper configuration"""
        if self._logger is None:
            # Create logs directory if it doesn't exist
            log_dir = PathManager.ensure_directory_exists(PathManager.get_logs_path())
            
            # Create logger
            self._logger = logging.getLogger('webui_automation')
            self._logger.setLevel(logging.DEBUG)
            
            # Prevent duplicate handlers
            if not self._logger.handlers:
                # Create formatters
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
                )
                console_formatter = logging.Formatter(
                    '%(levelname)s - %(message)s'
                )
                
                # File handler
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_handler = logging.FileHandler(
                    log_dir / f'automation_{timestamp}.log',
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(file_formatter)
                
                # Console handler
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                console_handler.setFormatter(console_formatter)
                
                # Add handlers
                self._logger.addHandler(file_handler)
                self._logger.addHandler(console_handler)
    
    def get_logger(self):
        """Get the configured logger instance"""
        return self._logger
    
    def debug(self, message):
        """Log debug message"""
        self._logger.debug(message)
    
    def info(self, message):
        """Log info message"""
        self._logger.info(message)
    
    def warning(self, message):
        """Log warning message"""
        self._logger.warning(message)
    
    def error(self, message):
        """Log error message"""
        self._logger.error(message)
    
    def critical(self, message):
        """Log critical message"""
        self._logger.critical(message) 