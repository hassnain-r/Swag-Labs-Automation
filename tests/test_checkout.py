import pytest

# Setup Python path using PathManager
from utils.path_manager import PathManager
PathManager.setup_python_path()

from config.config import TestConfig
from config.test_data import TestData


class TestCheckout:
    """Test cases for checkout functionality"""
    
    def test_checkout_page_loads_correctly(self, checkout_page_with_item):
        """Test that checkout page loads correctly"""
        # Verify checkout page elements
        assert "/checkout-step-one.html" in checkout_page_with_item.get_current_url()
        assert "Checkout: Your Information" in checkout_page_with_item.get_checkout_title()
        assert checkout_page_with_item.is_element_visible(checkout_page_with_item.FIRST_NAME_FIELD)
        assert checkout_page_with_item.is_element_visible(checkout_page_with_item.LAST_NAME_FIELD)
        assert checkout_page_with_item.is_element_visible(checkout_page_with_item.POSTAL_CODE_FIELD)
    
    def test_checkout_form_validation_empty_fields(self, checkout_page_with_item):
        """Test checkout form validation with empty fields"""
        # Try to continue with empty fields
        checkout_page_with_item.click_continue()
        
        # Verify error message
        assert checkout_page_with_item.is_error_message_displayed()
        error_message = checkout_page_with_item.get_error_message()
        assert "Error" in error_message
    
    def test_checkout_form_validation_missing_first_name(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout form validation with missing first name"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Fill form without first name
        checkout_page.enter_last_name("Doe")
        checkout_page.enter_postal_code("12345")
        checkout_page.click_continue()
        
        # Verify error message
        assert checkout_page.is_error_message_displayed()
    
    def test_checkout_form_validation_missing_last_name(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout form validation with missing last name"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Fill form without last name
        checkout_page.enter_first_name("John")
        checkout_page.enter_postal_code("12345")
        checkout_page.click_continue()
        
        # Verify error message
        assert checkout_page.is_error_message_displayed()
    
    def test_checkout_form_validation_missing_postal_code(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout form validation with missing postal code"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Fill form without postal code
        checkout_page.enter_first_name("John")
        checkout_page.enter_last_name("Doe")
        checkout_page.click_continue()
        
        # Verify error message
        assert checkout_page.is_error_message_displayed()
    
    def test_successful_checkout_form_submission(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page):
        """Test successful checkout form submission"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Fill checkout form
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Verify navigation to overview page
        checkout_overview_page.wait_for_overview_page_to_load()
        assert "/checkout-step-two.html" in checkout_overview_page.get_current_url()
        assert "Checkout: Overview" in checkout_overview_page.get_overview_title()
    
    def test_checkout_form_field_functionality(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout form field functionality"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Test first name field
        checkout_page.enter_first_name("John")
        assert checkout_page.get_first_name_value() == "John"
        checkout_page.clear_first_name()
        assert checkout_page.get_first_name_value() == ""
        
        # Test last name field
        checkout_page.enter_last_name("Doe")
        assert checkout_page.get_last_name_value() == "Doe"
        checkout_page.clear_last_name()
        assert checkout_page.get_last_name_value() == ""
        
        # Test postal code field
        checkout_page.enter_postal_code("12345")
        assert checkout_page.get_postal_code_value() == "12345"
        checkout_page.clear_postal_code()
        assert checkout_page.get_postal_code_value() == ""
    
    def test_checkout_cancel_functionality(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout cancel functionality"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Click cancel
        checkout_page.click_cancel()
        
        # Verify navigation back to cart
        assert "/cart.html" in checkout_page.get_current_url()
    
    def test_checkout_overview_page_display(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page):
        """Test checkout overview page displays correctly"""
        # Complete checkout form
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Verify overview page
        checkout_overview_page.wait_for_overview_page_to_load()
        assert checkout_overview_page.get_cart_items_count() > 0
        assert "Item total:" in checkout_overview_page.get_subtotal_text()
        assert "Tax:" in checkout_overview_page.get_tax_text()
        assert "Total:" in checkout_overview_page.get_total_text()
    
    def test_checkout_overview_calculations(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page):
        """Test checkout overview calculations"""
        # Complete checkout form
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Verify calculations
        checkout_overview_page.wait_for_overview_page_to_load()
        subtotal = checkout_overview_page.get_subtotal_amount()
        tax = checkout_overview_page.get_tax_amount()
        total = checkout_overview_page.get_total_amount()
        
        # Verify tax calculation (8% tax rate)
        expected_tax = subtotal * 0.08
        assert abs(tax - expected_tax) < 0.01
        
        # Verify total calculation
        expected_total = subtotal + tax
        assert abs(total - expected_total) < 0.01
    
    def test_checkout_overview_cancel_functionality(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page):
        """Test checkout overview cancel functionality"""
        # Complete checkout form
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Cancel from overview
        checkout_overview_page.wait_for_overview_page_to_load()
        checkout_overview_page.click_cancel()
        
        # Verify navigation back to inventory
        assert "/inventory.html" in checkout_overview_page.get_current_url()
    
    def test_checkout_complete_flow(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page, checkout_complete_page):
        """Test complete checkout flow from cart to completion"""
        # Start checkout process
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Fill checkout form
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Complete checkout
        checkout_overview_page.wait_for_overview_page_to_load()
        checkout_overview_page.click_finish()
        
        # Verify completion page
        checkout_complete_page.wait_for_complete_page_to_load()
        assert "/checkout-complete.html" in checkout_complete_page.get_current_url()
        assert "Thank you for your order!" in checkout_complete_page.get_complete_header()
        assert checkout_complete_page.is_pony_express_image_displayed()
    
    def test_checkout_complete_back_home_functionality(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page, checkout_complete_page):
        """Test back home functionality from completion page"""
        # Complete checkout flow
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        checkout_overview_page.wait_for_overview_page_to_load()
        checkout_overview_page.click_finish()
        
        # Click back home
        checkout_complete_page.wait_for_complete_page_to_load()
        checkout_complete_page.click_back_home()
        
        # Verify navigation back to inventory
        assert "/inventory.html" in checkout_complete_page.get_current_url()
    
    def test_checkout_with_multiple_items(self, logged_in_driver, inventory_page, cart_page, checkout_page, checkout_overview_page):
        """Test checkout with multiple items"""
        # Add multiple items
        inventory_page.wait_for_inventory_page_to_load()
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        for item in items_to_add:
            inventory_page.add_item_to_cart_by_name(item)
        
        # Complete checkout
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        checkout_page.click_continue()
        
        # Verify overview shows all items
        checkout_overview_page.wait_for_overview_page_to_load()
        assert checkout_overview_page.get_cart_items_count() == len(items_to_add)
        
        item_names = checkout_overview_page.get_all_item_names()
        for item in items_to_add:
            assert item in item_names
    
    def test_checkout_form_clear_functionality(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout form clear functionality"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Fill form
        checkout_page.fill_checkout_form("John", "Doe", "12345")
        
        # Clear all fields
        checkout_page.clear_all_fields()
        
        # Verify fields are cleared
        assert checkout_page.get_first_name_value() == ""
        assert checkout_page.get_last_name_value() == ""
        assert checkout_page.get_postal_code_value() == ""
    
    def test_checkout_page_title(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout page title"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Verify page title
        assert "Swag Labs" in checkout_page.get_page_title()
    
    def test_checkout_button_states(self, logged_in_driver, inventory_page, cart_page, checkout_page):
        """Test checkout button states"""
        # Navigate to checkout
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_checkout()
        checkout_page.wait_for_checkout_page_to_load()
        
        # Verify buttons are enabled
        assert checkout_page.is_continue_button_enabled()
        assert checkout_page.is_cancel_button_enabled() 