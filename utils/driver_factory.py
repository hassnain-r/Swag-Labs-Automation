from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config.config import TestConfig
import os


class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    @staticmethod
    def get_driver(browser_name=None, headless=None):
        """
        Create and return a WebDriver instance based on browser configuration
        
        Args:
            browser_name (str): Browser name (chrome, firefox, edge)
            headless (bool): Whether to run in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
        """
        browser = browser_name or TestConfig.BROWSER
        headless_mode = headless if headless is not None else TestConfig.HEADLESS
        
        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless_mode)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless_mode)
        elif browser == "edge":
            return DriverFactory._create_edge_driver(headless_mode)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless=False):
        """Create Chrome WebDriver instance"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless=new")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Try to use ChromeDriverManager with specific version
            service = ChromeService(ChromeDriverManager(version="latest").install())
            driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"ChromeDriverManager failed: {e}")
            # Fallback to system ChromeDriver
            try:
                driver = webdriver.Chrome(options=options)
            except Exception as e2:
                print(f"System ChromeDriver failed: {e2}")
                # Last resort - try without service
                driver = webdriver.Chrome(options=options)
        
        # Set timeouts
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless=False):
        """Create Firefox WebDriver instance"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        try:
            # Try to use GeckoDriverManager with specific version
            service = FirefoxService(GeckoDriverManager(version="latest").install())
            driver = webdriver.Firefox(service=service, options=options)
        except Exception as e:
            print(f"GeckoDriverManager failed: {e}")
            # Fallback to system GeckoDriver
            try:
                driver = webdriver.Firefox(options=options)
            except Exception as e2:
                print(f"System GeckoDriver failed: {e2}")
                # Last resort - try without service
                driver = webdriver.Firefox(options=options)
        
        # Set timeouts
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _create_edge_driver(headless=False):
        """Create Edge WebDriver instance"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        try:
            # Try to use EdgeChromiumDriverManager with specific version
            service = EdgeService(EdgeChromiumDriverManager(version="latest").install())
            driver = webdriver.Edge(service=service, options=options)
        except Exception as e:
            print(f"EdgeChromiumDriverManager failed: {e}")
            # Fallback to system EdgeDriver
            try:
                driver = webdriver.Edge(options=options)
            except Exception as e2:
                print(f"System EdgeDriver failed: {e2}")
                # Last resort - try without service
                driver = webdriver.Edge(options=options)
        
        # Set timeouts
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
        
        return driver 