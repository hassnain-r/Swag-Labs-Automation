import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage


@pytest.fixture(scope="function")
def driver():
    """Fixture to create and manage WebDriver instance"""
    driver = DriverFactory.get_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    """Fixture to create LoginPage instance"""
    return LoginPage(driver)


@pytest.fixture(scope="function")
def inventory_page(driver):
    """Fixture to create InventoryPage instance"""
    return InventoryPage(driver)


@pytest.fixture(scope="function")
def cart_page(driver):
    """Fixture to create CartPage instance"""
    return CartPage(driver)


@pytest.fixture(scope="function")
def checkout_page(driver):
    """Fixture to create CheckoutPage instance"""
    return CheckoutPage(driver)


@pytest.fixture(scope="function")
def checkout_overview_page(driver):
    """Fixture to create CheckoutOverviewPage instance"""
    return CheckoutOverviewPage(driver)


@pytest.fixture(scope="function")
def checkout_complete_page(driver):
    """Fixture to create CheckoutCompletePage instance"""
    return CheckoutCompletePage(driver)


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Fixture to provide a driver that's already logged in"""
    from config.config import TestConfig
    
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page()
    login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
    
    yield driver
    driver.quit() 