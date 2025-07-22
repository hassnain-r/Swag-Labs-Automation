from selenium.webdriver.common.by import By
from utils.base_page import BasePage
from config.config import TestConfig


class LoginPage(BasePage):
    """Page object for the Sauce Demo login page"""
    
    # Locators
    USERNAME_FIELD = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    ERROR_MESSAGE_TEXT = (By.CLASS_NAME, "error-message-container")
    LOGO = (By.CLASS_NAME, "login_logo")
    BOT_COLUMN = (By.CLASS_NAME, "bot_column")
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = TestConfig.BASE_URL
    
    def navigate_to_login_page(self):
        """Navigate to the login page"""
        self.navigate_to(self.url)
        self.wait_for_page_load()
    
    def enter_username(self, username):
        """Enter username in the username field"""
        self.send_keys_to_element(self.USERNAME_FIELD, username)
    
    def enter_password(self, password):
        """Enter password in the password field"""
        self.send_keys_to_element(self.PASSWORD_FIELD, password)
    
    def click_login_button(self):
        """Click the login button"""
        self.click_element(self.LOGIN_BUTTON)
    
    def login(self, username, password):
        """Perform login with given credentials"""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
    
    def get_error_message(self):
        """Get the error message text"""
        try:
            return self.get_element_text(self.ERROR_MESSAGE_TEXT)
        except:
            return ""
    
    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def is_login_button_enabled(self):
        """Check if login button is enabled"""
        try:
            element = self.find_element(self.LOGIN_BUTTON)
            return element.is_enabled()
        except:
            return False
    
    def get_username_field_value(self):
        """Get the value of username field"""
        return self.get_element_attribute(self.USERNAME_FIELD, "value")
    
    def get_password_field_value(self):
        """Get the value of password field"""
        return self.get_element_attribute(self.PASSWORD_FIELD, "value")
    
    def clear_username_field(self):
        """Clear the username field"""
        element = self.find_element(self.USERNAME_FIELD)
        element.clear()
    
    def clear_password_field(self):
        """Clear the password field"""
        element = self.find_element(self.PASSWORD_FIELD)
        element.clear()
    
    def is_logo_displayed(self):
        """Check if the logo is displayed"""
        return self.is_element_visible(self.LOGO)
    
    def is_bot_column_displayed(self):
        """Check if the bot column is displayed"""
        return self.is_element_visible(self.BOT_COLUMN)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_title()
    
    def wait_for_login_page_to_load(self):
        """Wait for login page to load completely"""
        self.wait_for_element_visible(self.USERNAME_FIELD)
        self.wait_for_element_visible(self.PASSWORD_FIELD)
        self.wait_for_element_visible(self.LOGIN_BUTTON) 