import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestConfig:
    """Configuration class for test settings"""
    
    # Base URL
    BASE_URL = "https://www.saucedemo.com/v1/"
    
    # Browser settings
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
    
    # Test data
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    LOCKED_USERNAME = "locked_out_user"
    PROBLEM_USERNAME = "problem_user"
    PERFORMANCE_USERNAME = "performance_glitch_user"
    
    # Screenshot settings
    SCREENSHOT_DIR = "screenshots"
    
    # Test timeout
    TEST_TIMEOUT = int(os.getenv("TEST_TIMEOUT", "60")) 