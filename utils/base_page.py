from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from datetime import datetime
from .path_manager import PathManager


class BasePage:
    """Base page class that provides common functionality for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.actions = ActionChains(driver)
    
    def navigate_to(self, url):
        """Navigate to a specific URL"""
        self.driver.get(url)
    
    def get_title(self):
        """Get the page title"""
        return self.driver.title
    
    def get_current_url(self):
        """Get the current URL"""
        return self.driver.current_url
    
    def find_element(self, locator, timeout=10):
        """Find element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator, timeout=10):
        """Find elements with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))
    
    def click_element(self, locator, timeout=10):
        """Click element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def send_keys_to_element(self, locator, text, timeout=10):
        """Send keys to element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    
    def get_element_text(self, locator, timeout=10):
        """Get element text with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        return element.text
    
    def get_element_attribute(self, locator, attribute, timeout=10):
        """Get element attribute with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator))
        return element.get_attribute(attribute)
    
    def is_element_present(self, locator, timeout=10):
        """Check if element is present"""
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(self, locator, timeout=10):
        """Check if element is visible"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_visible(self, locator, timeout=10):
        """Wait for element to be visible"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_element_invisible(self, locator, timeout=10):
        """Wait for element to be invisible"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
    
    def hover_over_element(self, locator):
        """Hover over element"""
        element = self.find_element(locator)
        self.actions.move_to_element(element).perform()
    
    def take_screenshot(self, filename=None):
        """Take screenshot and save it"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        # Create screenshots directory if it doesn't exist
        screenshot_dir = PathManager.ensure_directory_exists(PathManager.get_screenshots_path())
        
        filepath = screenshot_dir / filename
        self.driver.save_screenshot(str(filepath))
        return str(filepath)
    
    def wait_for_page_load(self, timeout=30):
        """Wait for page to load completely"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            print(f"Page load timeout after {timeout} seconds")
    
    def refresh_page(self):
        """Refresh the current page"""
        self.driver.refresh()
        self.wait_for_page_load()
    
    def go_back(self):
        """Go back to previous page"""
        self.driver.back()
        self.wait_for_page_load()
    
    def go_forward(self):
        """Go forward to next page"""
        self.driver.forward()
        self.wait_for_page_load() 