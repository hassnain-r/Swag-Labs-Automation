import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import TestConfig


class TestCart:
    """Test cases for cart functionality"""
    
    def test_cart_page_loads_correctly(self, logged_in_driver, inventory_page, cart_page):
        """Test that cart page loads correctly"""
        # Add an item to cart first
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify cart page elements
        assert "/cart.html" in cart_page.get_current_url()
        assert "Your Cart" in cart_page.get_cart_title()
        assert cart_page.get_cart_items_count() > 0
    
    def test_empty_cart_display(self, logged_in_driver, inventory_page, cart_page):
        """Test empty cart display"""
        # Navigate to cart without adding items
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify cart is empty
        assert cart_page.is_cart_empty()
        assert cart_page.get_cart_items_count() == 0
        assert "Your Cart" in cart_page.get_cart_title()
    
    def test_add_item_to_cart_and_verify(self, logged_in_driver, inventory_page, cart_page):
        """Test adding item to cart and verifying in cart page"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add item to cart
        item_name = "Sauce Labs Backpack"
        inventory_page.add_item_to_cart_by_name(item_name)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify item is in cart
        assert cart_page.is_item_in_cart(item_name)
        assert cart_page.get_cart_items_count() == 1
        
        # Verify item details
        item_names = cart_page.get_all_item_names()
        item_prices = cart_page.get_all_item_prices()
        item_quantities = cart_page.get_all_item_quantities()
        
        assert item_name in item_names
        assert len(item_prices) == 1
        assert len(item_quantities) == 1
        assert item_quantities[0] == "1"
    
    def test_add_multiple_items_to_cart(self, logged_in_driver, inventory_page, cart_page):
        """Test adding multiple items to cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add multiple items
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for item in items_to_add:
            inventory_page.add_item_to_cart_by_name(item)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify all items are in cart
        assert cart_page.get_cart_items_count() == len(items_to_add)
        
        for item in items_to_add:
            assert cart_page.is_item_in_cart(item)
    
    def test_remove_item_from_cart(self, logged_in_driver, inventory_page, cart_page):
        """Test removing item from cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add item to cart
        item_name = "Sauce Labs Backpack"
        inventory_page.add_item_to_cart_by_name(item_name)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify item is in cart
        assert cart_page.is_item_in_cart(item_name)
        initial_count = cart_page.get_cart_items_count()
        
        # Remove item from cart
        assert cart_page.remove_item_by_name(item_name)
        
        # Verify item is removed
        assert not cart_page.is_item_in_cart(item_name)
        assert cart_page.get_cart_items_count() == initial_count - 1
    
    def test_remove_all_items_from_cart(self, logged_in_driver, inventory_page, cart_page):
        """Test removing all items from cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add multiple items
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for item in items_to_add:
            inventory_page.add_item_to_cart_by_name(item)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify items are in cart
        assert cart_page.get_cart_items_count() == len(items_to_add)
        
        # Remove all items
        cart_page.remove_all_items()
        
        # Verify cart is empty
        assert cart_page.is_cart_empty()
        assert cart_page.get_cart_items_count() == 0
    
    def test_cart_total_calculation(self, logged_in_driver, inventory_page, cart_page):
        """Test cart total calculation"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add items with known prices
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        expected_prices = {"Sauce Labs Backpack": 29.99, "Sauce Labs Bike Light": 9.99}
        expected_total = sum(expected_prices.values())
        
        for item in items_to_add:
            inventory_page.add_item_to_cart_by_name(item)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Calculate total
        calculated_total = cart_page.calculate_total_price()
        
        # Verify total calculation
        assert abs(calculated_total - expected_total) < 0.01  # Allow for floating point precision
    
    def test_continue_shopping_functionality(self, logged_in_driver, inventory_page, cart_page):
        """Test continue shopping functionality"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add item and go to cart
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Click continue shopping
        cart_page.click_continue_shopping()
        
        # Verify navigation back to inventory
        assert "/inventory.html" in cart_page.get_current_url()
        assert "Products" in cart_page.get_page_title()
    
    def test_checkout_functionality(self, logged_in_driver, inventory_page, cart_page):
        """Test checkout functionality"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add item and go to cart
        inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Click checkout
        cart_page.click_checkout()
        
        # Verify navigation to checkout page
        assert "/checkout-step-one.html" in cart_page.get_current_url()
    
    def test_cart_with_empty_inventory(self, logged_in_driver, inventory_page, cart_page):
        """Test cart behavior with empty inventory"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Go to cart without adding items
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify cart is empty
        assert cart_page.is_cart_empty()
        assert cart_page.get_cart_items_count() == 0
        
        # Verify buttons are enabled/disabled appropriately
        assert cart_page.is_continue_shopping_button_enabled()
        assert not cart_page.is_checkout_button_enabled()  # Should be disabled when cart is empty
    
    def test_cart_item_quantities(self, logged_in_driver, inventory_page, cart_page):
        """Test cart item quantities"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add multiple items
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for item in items_to_add:
            inventory_page.add_item_to_cart_by_name(item)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify quantities
        quantities = cart_page.get_all_item_quantities()
        
        # Each item should have quantity 1
        for quantity in quantities:
            assert quantity == "1"
        
        assert len(quantities) == len(items_to_add)
    
    def test_cart_item_prices(self, logged_in_driver, inventory_page, cart_page):
        """Test cart item prices"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add item with known price
        item_name = "Sauce Labs Backpack"
        expected_price = "$29.99"
        
        inventory_page.add_item_to_cart_by_name(item_name)
        
        # Navigate to cart
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify price
        actual_price = cart_page.get_item_price_by_name(item_name)
        assert actual_price == expected_price
    
    def test_cart_page_title(self, logged_in_driver, inventory_page, cart_page):
        """Test cart page title"""
        inventory_page.wait_for_inventory_page_to_load()
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify page title
        assert "Swag Labs" in cart_page.get_page_title()
    
    def test_cart_navigation_from_inventory(self, logged_in_driver, inventory_page, cart_page):
        """Test navigation to cart from inventory page"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Click shopping cart from inventory
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        
        # Verify navigation
        assert "/cart.html" in cart_page.get_current_url()
        assert "Your Cart" in cart_page.get_cart_title()
    
    def test_cart_badge_count(self, logged_in_driver, inventory_page):
        """Test cart badge count updates correctly"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Verify initial cart count is 0
        assert inventory_page.get_cart_items_count() == 0
        
        # Add items and verify badge count
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
        
        for i, item in enumerate(items_to_add, 1):
            inventory_page.add_item_to_cart_by_name(item)
            assert inventory_page.get_cart_items_count() == i
    
    def test_cart_persistence_after_navigation(self, logged_in_driver, inventory_page, cart_page):
        """Test that cart items persist after navigation"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add item to cart
        item_name = "Sauce Labs Backpack"
        inventory_page.add_item_to_cart_by_name(item_name)
        
        # Navigate to cart and back
        inventory_page.click_shopping_cart()
        cart_page.wait_for_cart_page_to_load()
        cart_page.click_continue_shopping()
        
        # Verify item is still in cart
        assert inventory_page.get_cart_items_count() == 1
        assert inventory_page.is_item_in_cart(item_name) 