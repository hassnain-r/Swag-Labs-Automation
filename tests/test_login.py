import pytest

# Setup Python path using PathManager
from utils.path_manager import PathManager
PathManager.setup_python_path()

from config.config import TestConfig
from config.test_data import TestData


class TestLogin:
    """Test cases for login functionality"""
    
    def test_successful_login_with_valid_credentials(self, login_page):
        """Test successful login with valid credentials"""
        # Navigate to login page
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Verify page elements are present
        assert login_page.is_logo_displayed()
        assert login_page.is_bot_column_displayed()
        assert login_page.is_login_button_enabled()
        
        # Perform login
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Verify successful login by checking URL change
        assert "/inventory.html" in login_page.get_current_url()
        assert "Products" in login_page.get_page_title()
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("invalid_user", TestConfig.VALID_PASSWORD, "Username and password do not match"),
        (TestConfig.VALID_USERNAME, "invalid_password", "Username and password do not match"),
        (TestConfig.LOCKED_USERNAME, TestConfig.VALID_PASSWORD, "Sorry, this user has been locked out"),
    ])
    def test_failed_login_scenarios(self, login_page, username, password, expected_error):
        """Test various failed login scenarios"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Perform login with invalid credentials
        login_page.login(username, password)
        
        # Verify error message is displayed
        assert login_page.is_error_message_displayed()
        error_message = login_page.get_error_message()
        assert "Epic sadface" in error_message
        assert expected_error in error_message
    
    @pytest.mark.parametrize("username,password,expected_error", [
        ("", TestConfig.VALID_PASSWORD, "Username is required"),
        (TestConfig.VALID_USERNAME, "", "Password is required"),
        ("", "", "Username is required"),  # Empty credentials
    ])
    def test_login_with_empty_fields(self, login_page, username, password, expected_error):
        """Test login with empty fields"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Perform login with empty fields
        login_page.login(username, password)
        
        # Verify error message is displayed
        assert login_page.is_error_message_displayed()
        error_message = login_page.get_error_message()
        assert "Epic sadface" in error_message
        assert expected_error in error_message
    
    def test_login_page_elements_visibility(self, login_page):
        """Test that all login page elements are visible"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Verify all elements are present and visible
        assert login_page.is_element_visible(login_page.USERNAME_FIELD)
        assert login_page.is_element_visible(login_page.PASSWORD_FIELD)
        assert login_page.is_element_visible(login_page.LOGIN_BUTTON)
        assert login_page.is_logo_displayed()
        assert login_page.is_bot_column_displayed()
    
    def test_login_button_state(self, login_page):
        """Test login button state"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Verify login button is enabled by default
        assert login_page.is_login_button_enabled()
        
        # Verify login button text
        button_text = login_page.get_element_text(login_page.LOGIN_BUTTON)
        assert button_text == "Login"
    
    def test_username_field_functionality(self, login_page):
        """Test username field functionality"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Test entering username
        test_username = "test_user"
        login_page.enter_username(test_username)
        
        # Verify username is entered
        assert login_page.get_username_field_value() == test_username
        
        # Test clearing username
        login_page.clear_username_field()
        assert login_page.get_username_field_value() == ""
    
    def test_password_field_functionality(self, login_page):
        """Test password field functionality"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Test entering password
        test_password = "test_password"
        login_page.enter_password(test_password)
        
        # Verify password is entered
        assert login_page.get_password_field_value() == test_password
        
        # Test clearing password
        login_page.clear_password_field()
        assert login_page.get_password_field_value() == ""
    
    def test_page_title(self, login_page):
        """Test login page title"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Verify page title
        assert "Swag Labs" in login_page.get_page_title()
    
    def test_problem_user_login(self, login_page):
        """Test login with problem user"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Perform login with problem user
        login_page.login(TestConfig.PROBLEM_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Verify successful login (problem user can still login)
        assert "/inventory.html" in login_page.get_current_url()
    
    def test_performance_user_login(self, login_page):
        """Test login with performance glitch user"""
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        
        # Perform login with performance glitch user
        login_page.login(TestConfig.PERFORMANCE_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Verify successful login (performance user can still login)
        assert "/inventory.html" in login_page.get_current_url() 