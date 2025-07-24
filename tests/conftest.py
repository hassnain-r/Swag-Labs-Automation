import pytest

# Setup Python path using PathManager
from ..utils.path_manager import PathManager
PathManager.setup_python_path()

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage
from config.config import TestConfig


@pytest.fixture(scope="function")
def driver():
    """Fixture to create and manage WebDriver instance"""
    driver = DriverFactory.get_driver()
    yield driver
    # Teardown: Clean up driver after test
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
    login_page = LoginPage(driver)
    login_page.navigate_to_login_page()
    login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
    
    yield driver
    # Teardown: Clean up driver after test
    driver.quit()


@pytest.fixture(scope="function")
def cart_with_item(logged_in_driver, inventory_page, cart_page):
    """Fixture to provide a cart with a specific item"""
    inventory_page.wait_for_inventory_page_to_load()
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.click_shopping_cart()
    cart_page.wait_for_cart_page_to_load()
    
    yield cart_page


@pytest.fixture(scope="function")
def checkout_page_with_item(logged_in_driver, inventory_page, cart_page, checkout_page):
    """Fixture to provide a checkout page with a specific item"""
    inventory_page.wait_for_inventory_page_to_load()
    inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
    inventory_page.click_shopping_cart()
    cart_page.wait_for_cart_page_to_load()
    cart_page.click_checkout()
    checkout_page.wait_for_checkout_page_to_load()
    
    yield checkout_page 