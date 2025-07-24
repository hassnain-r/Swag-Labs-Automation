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
from utils.logger import Logger
import os


class DriverFactory:
    """Factory class for creating WebDriver instances"""
    
    def __init__(self):
        self.logger = Logger().get_logger()
    
    @staticmethod
    def get_driver(browser_name=None, headless=None):
        """
        Create and return a WebDriver instance based on browser configuration
        
        Args:
            browser_name (str): Browser name (chrome, firefox, edge)
            headless (bool): Whether to run in headless mode
            
        Returns:
            WebDriver: Configured WebDriver instance
            
        Raises:
            RuntimeError: If no driver could be initialized after all attempts
        """
        factory = DriverFactory()
        browser = browser_name or TestConfig.BROWSER
        headless_mode = headless if headless is not None else TestConfig.HEADLESS
        
        factory.logger.info(f"Creating {browser} driver (headless: {headless_mode})")
        
        if browser == "chrome":
            return factory._create_chrome_driver(headless_mode)
        elif browser == "firefox":
            return factory._create_firefox_driver(headless_mode)
        elif browser == "edge":
            return factory._create_edge_driver(headless_mode)
        else:
            factory.logger.error(f"Unsupported browser: {browser}")
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _create_chrome_driver(self, headless=False):
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
        
        # Try multiple approaches to create Chrome driver
        driver = None
        
        # Attempt 1: ChromeDriverManager
        try:
            self.logger.info("Attempting to create Chrome driver using ChromeDriverManager")
            service = ChromeService(ChromeDriverManager(version="latest").install())
            driver = webdriver.Chrome(service=service, options=options)
            self.logger.info("Chrome driver created successfully using ChromeDriverManager")
        except Exception as e:
            self.logger.warning(f"ChromeDriverManager failed: {e}")
            
            # Attempt 2: System ChromeDriver
            try:
                self.logger.info("Attempting to create Chrome driver using system ChromeDriver")
                driver = webdriver.Chrome(options=options)
                self.logger.info("Chrome driver created successfully using system ChromeDriver")
            except Exception as e2:
                self.logger.warning(f"System ChromeDriver failed: {e2}")
                
                # Attempt 3: Last resort - try without service
                try:
                    self.logger.info("Attempting to create Chrome driver without service")
                    driver = webdriver.Chrome(options=options)
                    self.logger.info("Chrome driver created successfully without service")
                except Exception as e3:
                    self.logger.error(f"All Chrome driver creation attempts failed: {e3}")
                    raise RuntimeError(f"Failed to create Chrome driver after all attempts: {e3}")
        
        # Set timeouts
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    def _create_firefox_driver(self, headless=False):
        """Create Firefox WebDriver instance"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        # Try multiple approaches to create Firefox driver
        driver = None
        
        # Attempt 1: GeckoDriverManager
        try:
            self.logger.info("Attempting to create Firefox driver using GeckoDriverManager")
            service = FirefoxService(GeckoDriverManager(version="latest").install())
            driver = webdriver.Firefox(service=service, options=options)
            self.logger.info("Firefox driver created successfully using GeckoDriverManager")
        except Exception as e:
            self.logger.warning(f"GeckoDriverManager failed: {e}")
            
            # Attempt 2: System GeckoDriver
            try:
                self.logger.info("Attempting to create Firefox driver using system GeckoDriver")
                driver = webdriver.Firefox(options=options)
                self.logger.info("Firefox driver created successfully using system GeckoDriver")
            except Exception as e2:
                self.logger.warning(f"System GeckoDriver failed: {e2}")
                
                # Attempt 3: Last resort - try without service
                try:
                    self.logger.info("Attempting to create Firefox driver without service")
                    driver = webdriver.Firefox(options=options)
                    self.logger.info("Firefox driver created successfully without service")
                except Exception as e3:
                    self.logger.error(f"All Firefox driver creation attempts failed: {e3}")
                    raise RuntimeError(f"Failed to create Firefox driver after all attempts: {e3}")
        
        # Set timeouts
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    def _create_edge_driver(self, headless=False):
        """Create Edge WebDriver instance"""
        options = EdgeOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Try multiple approaches to create Edge driver
        driver = None
        
        # Attempt 1: EdgeChromiumDriverManager
        try:
            self.logger.info("Attempting to create Edge driver using EdgeChromiumDriverManager")
            service = EdgeService(EdgeChromiumDriverManager(version="latest").install())
            driver = webdriver.Edge(service=service, options=options)
            self.logger.info("Edge driver created successfully using EdgeChromiumDriverManager")
        except Exception as e:
            self.logger.warning(f"EdgeChromiumDriverManager failed: {e}")
            
            # Attempt 2: System EdgeDriver
            try:
                self.logger.info("Attempting to create Edge driver using system EdgeDriver")
                driver = webdriver.Edge(options=options)
                self.logger.info("Edge driver created successfully using system EdgeDriver")
            except Exception as e2:
                self.logger.warning(f"System EdgeDriver failed: {e2}")
                
                # Attempt 3: Last resort - try without service
                try:
                    self.logger.info("Attempting to create Edge driver without service")
                    driver = webdriver.Edge(options=options)
                    self.logger.info("Edge driver created successfully without service")
                except Exception as e3:
                    self.logger.error(f"All Edge driver creation attempts failed: {e3}")
                    raise RuntimeError(f"Failed to create Edge driver after all attempts: {e3}")
        
        # Set timeouts
        driver.implicitly_wait(TestConfig.IMPLICIT_WAIT)
        driver.set_page_load_timeout(TestConfig.PAGE_LOAD_TIMEOUT)
        
        return driver 