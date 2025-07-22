from selenium.webdriver.common.by import By
from utils.base_page import BasePage


class CartPage(BasePage):
    """Page object for the Sauce Demo cart page"""
    
    # Locators
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITIES = (By.CLASS_NAME, "cart_quantity")
    REMOVE_BUTTONS = (By.CLASS_NAME, "btn_secondary")
    CONTINUE_SHOPPING_BUTTON = (By.CLASS_NAME, "btn_secondary")
    CHECKOUT_BUTTON = (By.CLASS_NAME, "btn_action")
    CART_TITLE = (By.CLASS_NAME, "subheader")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_cart_page_to_load(self):
        """Wait for cart page to load completely"""
        self.wait_for_element_visible(self.CART_LIST)
    
    def get_cart_items_count(self):
        """Get the number of items in cart"""
        items = self.find_elements(self.CART_ITEMS)
        return len(items)
    
    def get_all_item_names(self):
        """Get all item names in cart"""
        items = self.find_elements(self.ITEM_NAMES)
        return [item.text for item in items]
    
    def get_all_item_prices(self):
        """Get all item prices in cart"""
        items = self.find_elements(self.ITEM_PRICES)
        return [item.text for item in items]
    
    def get_all_item_quantities(self):
        """Get all item quantities in cart"""
        items = self.find_elements(self.ITEM_QUANTITIES)
        return [item.text for item in items]
    
    def get_item_by_name(self, item_name):
        """Get cart item element by name"""
        items = self.find_elements(self.CART_ITEMS)
        for item in items:
            name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_element.text == item_name:
                return item
        return None
    
    def remove_item_by_name(self, item_name):
        """Remove item from cart by name"""
        item = self.get_item_by_name(item_name)
        if item:
            remove_button = item.find_element(By.CLASS_NAME, "btn_secondary")
            remove_button.click()
            return True
        return False
    
    def get_item_price_by_name(self, item_name):
        """Get item price by name"""
        item = self.get_item_by_name(item_name)
        if item:
            price_element = item.find_element(By.CLASS_NAME, "inventory_item_price")
            return price_element.text
        return None
    
    def get_item_quantity_by_name(self, item_name):
        """Get item quantity by name"""
        item = self.get_item_by_name(item_name)
        if item:
            quantity_element = item.find_element(By.CLASS_NAME, "cart_quantity")
            return quantity_element.text
        return None
    
    def click_continue_shopping(self):
        """Click continue shopping button"""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
    
    def click_checkout(self):
        """Click checkout button"""
        self.click_element(self.CHECKOUT_BUTTON)
    
    def is_cart_empty(self):
        """Check if cart is empty"""
        return self.get_cart_items_count() == 0
    
    def is_item_in_cart(self, item_name):
        """Check if item is in cart"""
        return self.get_item_by_name(item_name) is not None
    
    def get_cart_title(self):
        """Get cart page title"""
        return self.get_element_text(self.CART_TITLE)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_title()
    
    def calculate_total_price(self):
        """Calculate total price of all items in cart"""
        prices = self.get_all_item_prices()
        total = 0
        for price in prices:
            # Remove '$' and convert to float
            price_value = float(price.replace('$', ''))
            total += price_value
        return total
    
    def get_all_remove_buttons(self):
        """Get all remove buttons"""
        return self.find_elements(self.REMOVE_BUTTONS)
    
    def remove_all_items(self):
        """Remove all items from cart"""
        remove_buttons = self.get_all_remove_buttons()
        for button in remove_buttons:
            button.click()
    
    def is_continue_shopping_button_enabled(self):
        """Check if continue shopping button is enabled"""
        try:
            element = self.find_element(self.CONTINUE_SHOPPING_BUTTON)
            return element.is_enabled()
        except:
            return False
    
    def is_checkout_button_enabled(self):
        """Check if checkout button is enabled"""
        try:
            element = self.find_element(self.CHECKOUT_BUTTON)
            return element.is_enabled()
        except:
            return False 