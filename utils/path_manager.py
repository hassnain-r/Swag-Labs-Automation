"""Path management utilities for the automation framework"""

import sys
from pathlib import Path


class PathManager:
    """Centralized path management for the automation framework"""
    
    _project_root = None
    
    @classmethod
    def get_project_root(cls):
        """Get the project root directory"""
        if cls._project_root is None:
            # Find the project root by looking for the config directory
            current_path = Path(__file__).parent
            while current_path.parent != current_path:  # Stop at filesystem root
                if (current_path / "config").exists() and (current_path / "tests").exists():
                    cls._project_root = current_path
                    break
                current_path = current_path.parent
            
            if cls._project_root is None:
                # Fallback: assume we're in the project root
                cls._project_root = Path(__file__).parent.parent
        
        return cls._project_root
    
    @classmethod
    def setup_python_path(cls):
        """Setup Python path to include project root"""
        project_root = cls.get_project_root()
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
    
    @classmethod
    def get_config_path(cls):
        """Get the config directory path"""
        return cls.get_project_root() / "config"
    
    @classmethod
    def get_tests_path(cls):
        """Get the tests directory path"""
        return cls.get_project_root() / "tests"
    
    @classmethod
    def get_pages_path(cls):
        """Get the pages directory path"""
        return cls.get_project_root() / "pages"
    
    @classmethod
    def get_utils_path(cls):
        """Get the utils directory path"""
        return cls.get_project_root() / "utils"
    
    @classmethod
    def get_screenshots_path(cls):
        """Get the screenshots directory path"""
        return cls.get_project_root() / "screenshots"
    
    @classmethod
    def get_logs_path(cls):
        """Get the logs directory path"""
        return cls.get_project_root() / "logs"
    
    @classmethod
    def get_reports_path(cls):
        """Get the reports directory path"""
        return cls.get_project_root() / "reports"
    
    @classmethod
    def ensure_directory_exists(cls, directory_path):
        """Ensure a directory exists, create if it doesn't"""
        directory_path = Path(directory_path)
        directory_path.mkdir(parents=True, exist_ok=True)
        return directory_path 