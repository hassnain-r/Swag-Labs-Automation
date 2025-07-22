import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import TestConfig


class TestInventory:
    """Test cases for inventory functionality"""
    
    def test_inventory_page_loads_after_login(self, logged_in_driver, inventory_page):
        """Test that inventory page loads correctly after login"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Verify page elements are present
        assert inventory_page.get_inventory_items_count() > 0
        assert "Products" in inventory_page.get_page_title()
        assert "/inventory.html" in inventory_page.get_current_url()
    
    def test_inventory_items_display(self, logged_in_driver, inventory_page):
        """Test that all inventory items are displayed correctly"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Get all items
        item_names = inventory_page.get_all_item_names()
        item_prices = inventory_page.get_all_item_prices()
        item_descriptions = inventory_page.get_all_item_descriptions()
        
        # Verify items are present
        assert len(item_names) > 0
        assert len(item_prices) > 0
        assert len(item_descriptions) > 0
        
        # Verify all items have names, prices, and descriptions
        assert len(item_names) == len(item_prices) == len(item_descriptions)
        
        # Verify expected items are present
        expected_items = [
            "Sauce Labs Backpack",
            "Sauce Labs Bike Light",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Fleece Jacket",
            "Sauce Labs Onesie",
            "Test.allTheThings() T-Shirt (Red)"
        ]
        
        for expected_item in expected_items:
            assert expected_item in item_names
    
    def test_add_item_to_cart(self, logged_in_driver, inventory_page):
        """Test adding an item to cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Get initial cart count
        initial_cart_count = inventory_page.get_cart_items_count()
        
        # Add an item to cart
        item_name = "Sauce Labs Backpack"
        assert inventory_page.add_item_to_cart_by_name(item_name)
        
        # Verify item is added to cart
        assert inventory_page.get_cart_items_count() == initial_cart_count + 1
        assert inventory_page.is_item_in_cart(item_name)
    
    def test_remove_item_from_cart(self, logged_in_driver, inventory_page):
        """Test removing an item from cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add an item to cart first
        item_name = "Sauce Labs Backpack"
        inventory_page.add_item_to_cart_by_name(item_name)
        
        # Get cart count after adding
        cart_count_after_add = inventory_page.get_cart_items_count()
        
        # Remove the item from cart
        assert inventory_page.remove_item_from_cart_by_name(item_name)
        
        # Verify item is removed from cart
        assert inventory_page.get_cart_items_count() == cart_count_after_add - 1
        assert not inventory_page.is_item_in_cart(item_name)
    
    def test_add_multiple_items_to_cart(self, logged_in_driver, inventory_page):
        """Test adding multiple items to cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Get initial cart count
        initial_cart_count = inventory_page.get_cart_items_count()
        
        # Add multiple items
        items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light", "Sauce Labs Bolt T-Shirt"]
        
        for item in items_to_add:
            assert inventory_page.add_item_to_cart_by_name(item)
        
        # Verify all items are added
        assert inventory_page.get_cart_items_count() == initial_cart_count + len(items_to_add)
        
        for item in items_to_add:
            assert inventory_page.is_item_in_cart(item)
    
    def test_sort_items_by_name_az(self, logged_in_driver, inventory_page):
        """Test sorting items by name A-Z"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Sort by name A-Z
        inventory_page.sort_items_by("az")
        
        # Get sorted items
        item_names = inventory_page.get_all_item_names()
        
        # Verify items are sorted alphabetically
        sorted_names = sorted(item_names)
        assert item_names == sorted_names
    
    def test_sort_items_by_name_za(self, logged_in_driver, inventory_page):
        """Test sorting items by name Z-A"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Sort by name Z-A
        inventory_page.sort_items_by("za")
        
        # Get sorted items
        item_names = inventory_page.get_all_item_names()
        
        # Verify items are sorted in reverse alphabetical order
        sorted_names = sorted(item_names, reverse=True)
        assert item_names == sorted_names
    
    def test_sort_items_by_price_low_high(self, logged_in_driver, inventory_page):
        """Test sorting items by price low to high"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Sort by price low to high
        inventory_page.sort_items_by("lohi")
        
        # Get sorted prices
        item_prices = inventory_page.get_all_item_prices()
        
        # Convert prices to float for comparison
        price_values = [float(price.replace('$', '')) for price in item_prices]
        
        # Verify prices are sorted from low to high
        sorted_prices = sorted(price_values)
        assert price_values == sorted_prices
    
    def test_sort_items_by_price_high_low(self, logged_in_driver, inventory_page):
        """Test sorting items by price high to low"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Sort by price high to low
        inventory_page.sort_items_by("hilo")
        
        # Get sorted prices
        item_prices = inventory_page.get_all_item_prices()
        
        # Convert prices to float for comparison
        price_values = [float(price.replace('$', '')) for price in item_prices]
        
        # Verify prices are sorted from high to low
        sorted_prices = sorted(price_values, reverse=True)
        assert price_values == sorted_prices
    
    def test_click_item_name_navigates_to_details(self, logged_in_driver, inventory_page):
        """Test clicking item name navigates to item details"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Click on an item name
        item_name = "Sauce Labs Backpack"
        assert inventory_page.click_item_name(item_name)
        
        # Verify navigation to item details page
        assert "/inventory-item.html" in inventory_page.get_current_url()
    
    def test_click_item_image_navigates_to_details(self, logged_in_driver, inventory_page):
        """Test clicking item image navigates to item details"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Click on an item image
        item_name = "Sauce Labs Backpack"
        assert inventory_page.click_item_image(item_name)
        
        # Verify navigation to item details page
        assert "/inventory-item.html" in inventory_page.get_current_url()
    
    def test_shopping_cart_navigation(self, logged_in_driver, inventory_page):
        """Test navigation to shopping cart"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Click on shopping cart
        inventory_page.click_shopping_cart()
        
        # Verify navigation to cart page
        assert "/cart.html" in inventory_page.get_current_url()
    
    def test_burger_menu_functionality(self, logged_in_driver, inventory_page):
        """Test burger menu functionality"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Open burger menu
        inventory_page.open_burger_menu()
        assert inventory_page.is_burger_menu_open()
        
        # Close burger menu
        inventory_page.close_burger_menu()
        assert not inventory_page.is_burger_menu_open()
    
    def test_logout_functionality(self, logged_in_driver, inventory_page):
        """Test logout functionality"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Logout
        inventory_page.click_logout()
        
        # Verify navigation back to login page
        assert "/" in inventory_page.get_current_url()
        assert "Swag Labs" in inventory_page.get_page_title()
    
    def test_about_link_functionality(self, logged_in_driver, inventory_page):
        """Test about link functionality"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Click about link
        inventory_page.click_about()
        
        # Verify navigation to about page
        assert "saucelabs.com" in inventory_page.get_current_url()
    
    def test_reset_app_state_functionality(self, logged_in_driver, inventory_page):
        """Test reset app state functionality"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Add an item to cart first
        item_name = "Sauce Labs Backpack"
        inventory_page.add_item_to_cart_by_name(item_name)
        assert inventory_page.is_item_in_cart(item_name)
        
        # Reset app state
        inventory_page.click_reset_app_state()
        
        # Verify cart is cleared
        assert inventory_page.get_cart_items_count() == 0
        assert not inventory_page.is_item_in_cart(item_name)
    
    def test_item_price_display(self, logged_in_driver, inventory_page):
        """Test that item prices are displayed correctly"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Check specific item prices
        expected_prices = {
            "Sauce Labs Backpack": "$29.99",
            "Sauce Labs Bike Light": "$9.99",
            "Sauce Labs Bolt T-Shirt": "$15.99",
            "Sauce Labs Fleece Jacket": "$49.99",
            "Sauce Labs Onesie": "$7.99",
            "Test.allTheThings() T-Shirt (Red)": "$15.99"
        }
        
        for item_name, expected_price in expected_prices.items():
            actual_price = inventory_page.get_item_price_by_name(item_name)
            assert actual_price == expected_price
    
    def test_item_description_display(self, logged_in_driver, inventory_page):
        """Test that item descriptions are displayed correctly"""
        inventory_page.wait_for_inventory_page_to_load()
        
        # Check that all items have descriptions
        item_names = inventory_page.get_all_item_names()
        
        for item_name in item_names:
            description = inventory_page.get_item_description_by_name(item_name)
            assert description is not None
            assert len(description) > 0 