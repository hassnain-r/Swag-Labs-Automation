import pytest

# Setup Python path using PathManager
from utils.path_manager import PathManager
PathManager.setup_python_path()

from config.config import TestConfig
from config.test_data import TestData


class TestEndToEnd:
    """End-to-end test cases covering complete user journeys"""
    
    @pytest.mark.parametrize("items,checkout_data", [
        (["Sauce Labs Backpack"], TestData.get_checkout_data("valid")),
        (["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"], 
         TestData.get_checkout_data("alternate")),
    ])
    def test_complete_purchase_flow(self, driver, items, checkout_data):
        """Test complete purchase flow with different item combinations"""
        from pages.login_page import LoginPage
        from pages.inventory_page import InventoryPage
        from pages.cart_page import CartPage
        from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage
        
        # Initialize page objects
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        checkout_overview_page = CheckoutOverviewPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)
        
        # Step 1: Login
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Step 2: Verify successful login
        inventory_page.wait_for_inventory_page_to_load()
        assert "/inventory.html" in inventory_page.get_current_url()
        assert inventory_page.get_inventory_items_count() > 0
        
        # Step 3: Add items to cart
        for item in items:
            assert inventory_page.add_item_to_cart_by_name(item)
        
        assert inventory_page.get_cart_items_count() == len(items)
        
        # Step 4: Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        assert "/cart.html" in cart_page.get_current_url()
        assert cart_page.get_cart_items_count() == len(items)
        
        for item in items:
            assert cart_page.is_item_in_cart(item)
        
        # Step 5: Calculate expected total
        expected_subtotal = sum([TestData.get_product_price_value(item) for item in items])
        expected_tax = TestData.calculate_tax(expected_subtotal)
        expected_total = TestData.calculate_total(expected_subtotal)
        
        # Step 6: Proceed to checkout
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        assert "/checkout-step-one.html" in checkout_page.get_current_url()
        
        # Step 7: Fill checkout information
        checkout_page.fill_checkout_form(
            checkout_data["first_name"], 
            checkout_data["last_name"], 
            checkout_data["postal_code"]
        )
        checkout_page.click_continue()
        
        # Step 8: Verify checkout overview
        checkout_overview_page.wait_for_overview_page_to_load()
        assert "/checkout-step-two.html" in checkout_overview_page.get_current_url()
        assert checkout_overview_page.get_cart_items_count() == len(items)
        
        # Verify calculations
        actual_subtotal = checkout_overview_page.get_subtotal_amount()
        actual_tax = checkout_overview_page.get_tax_amount()
        actual_total = checkout_overview_page.get_total_amount()
        
        assert abs(actual_subtotal - expected_subtotal) < 0.01
        assert abs(actual_tax - expected_tax) < 0.01
        assert abs(actual_total - expected_total) < 0.01
        
        # Step 9: Complete purchase
        checkout_overview_page.click_finish()
        
        # Step 10: Verify completion
        checkout_complete_page.wait_for_complete_page_to_load()
        assert "/checkout-complete.html" in checkout_complete_page.get_current_url()
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header()
        assert checkout_complete_page.is_pony_express_image_displayed()
        
        # Step 11: Return to inventory
        checkout_complete_page.click_back_home()
        assert "/inventory.html" in checkout_complete_page.get_current_url()
    
    def test_complete_flow_with_sorting_and_filtering(self, driver):
        """Test complete flow with sorting and filtering"""
        from pages.login_page import LoginPage
        from pages.inventory_page import InventoryPage
        from pages.cart_page import CartPage
        from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage
        
        # Initialize page objects
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        checkout_overview_page = CheckoutOverviewPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)
        
        # Step 1: Login
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Step 2: Sort items by price low to high
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.sort_items_by("lohi")
        
        # Step 3: Add the cheapest item
        item_names = inventory_page.get_all_item_names()
        item_prices = inventory_page.get_all_item_prices()
        
        # Find the cheapest item
        cheapest_price = float('inf')
        cheapest_item = None
        
        for name, price in zip(item_names, item_prices):
            price_value = float(price.replace('$', ''))
            if price_value < cheapest_price:
                cheapest_price = price_value
                cheapest_item = name
        
        # Step 4: Add cheapest item to cart
        assert inventory_page.add_item_to_cart_by_name(cheapest_item)
        
        # Step 5: Complete purchase flow
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("Alice", "Johnson", "98765")
        checkout_page.click_continue()
        checkout_overview_page.wait_for_overview_page_to_load()
        checkout_overview_page.click_finish()
        checkout_complete_page.wait_for_complete_page_to_load()
        
        # Step 6: Verify completion
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header()
    
    def test_complete_flow_with_cart_management(self, driver):
        """Test complete flow with cart management (add/remove items)"""
        from pages.login_page import LoginPage
        from pages.inventory_page import InventoryPage
        from pages.cart_page import CartPage
        from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage
        
        # Initialize page objects
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        checkout_overview_page = CheckoutOverviewPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)
        
        # Step 1: Login
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Step 2: Add multiple items
        inventory_page.wait_for_inventory_page_to_load()
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Fleece Jacket"]
        
        for item in items_to_add:
            inventory_page.add_item_to_cart_by_name(item)
        
        assert inventory_page.get_cart_items_count() == len(items_to_add)
        
        # Step 3: Remove one item from inventory
        inventory_page.remove_item_from_cart_by_name("Sauce Labs Fleece Jacket")
        assert inventory_page.get_cart_items_count() == len(items_to_add) - 1
        
        # Step 4: Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        assert cart_page.get_cart_items_count() == 2
        
        # Step 5: Remove another item from cart
        cart_page.remove_item_by_name("Sauce Labs Bike Light")
        assert cart_page.get_cart_items_count() == 1
        assert cart_page.is_item_in_cart("Sauce Labs Backpack")
        
        # Step 6: Complete purchase with remaining item
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("Bob", "Wilson", "11111")
        checkout_page.click_continue()
        checkout_overview_page.wait_for_overview_page_to_load()
        checkout_overview_page.click_finish()
        checkout_complete_page.wait_for_complete_page_to_load()
        
        # Step 7: Verify completion
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header()
    
    def test_complete_flow_with_navigation_and_return(self, driver):
        """Test complete flow with navigation and return to shopping"""
        from pages.login_page import LoginPage
        from pages.inventory_page import InventoryPage
        from pages.cart_page import CartPage
        from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage
        
        # Initialize page objects
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        checkout_overview_page = CheckoutOverviewPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)
        
        # Step 1: Login
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Step 2: Add item to cart
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        
        # Step 3: Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Step 4: Return to shopping
        cart_page.click_continue_shopping()
        assert "/inventory.html" in inventory_page.get_current_url()
        
        # Step 5: Add another item
        inventory_page.add_item_to_cart_by_name("Sauce Labs Bike Light")
        assert inventory_page.get_cart_items_count() == 2
        
        # Step 6: Complete purchase
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("Charlie", "Brown", "22222")
        checkout_page.click_continue()
        checkout_overview_page.wait_for_overview_page_to_load()
        checkout_overview_page.click_finish()
        checkout_complete_page.wait_for_complete_page_to_load()
        
        # Step 7: Verify completion
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header()
    
    def test_complete_flow_with_error_handling(self, driver):
        """Test complete flow with error handling and recovery"""
        from pages.login_page import LoginPage
        from pages.inventory_page import InventoryPage
        from pages.cart_page import CartPage
        from pages.checkout_page import CheckoutPage, CheckoutOverviewPage, CheckoutCompletePage
        
        # Initialize page objects
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)
        checkout_overview_page = CheckoutOverviewPage(driver)
        checkout_complete_page = CheckoutCompletePage(driver)
        
        # Step 1: Login
        login_page.navigate_to_login_page()
        login_page.wait_for_login_page_to_load()
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        
        # Step 2: Add item and proceed to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Step 3: Try to continue with empty form (should show error)
        checkout_page.click_continue()
        assert checkout_page.is_error_message_displayed()
        
        # Step 4: Fill form correctly and continue
        checkout_page.fill_checkout_form("David", "Miller", "33333")
        checkout_page.click_continue()
        checkout_overview_page.wait_for_overview_page_to_load()
        
        # Step 5: Complete purchase
        checkout_overview_page.click_finish()
        checkout_complete_page.wait_for_complete_page_to_load()
        
        # Step 6: Verify completion
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header() 