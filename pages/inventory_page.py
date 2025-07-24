from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from utils.base_page import BasePage


class InventoryPage(BasePage):
    """Page object for the Sauce Demo inventory page"""
    
    # Locators
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_DESCRIPTIONS = (By.CLASS_NAME, "inventory_item_desc")
    ADD_TO_CART_BUTTONS = (By.CLASS_NAME, "btn_inventory")
    REMOVE_BUTTONS = (By.CLASS_NAME, "btn_inventory")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    BURGER_MENU_ITEMS = (By.CLASS_NAME, "bm-item-list")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    ABOUT_LINK = (By.ID, "about_sidebar_link")
    RESET_APP_STATE_LINK = (By.ID, "reset_sidebar_link")
    CLOSE_BURGER_MENU = (By.ID, "react-burger-cross-btn")
    SORT_CONTAINER = (By.CLASS_NAME, "product_sort_container")
    ACTIVE_OPTION = (By.CLASS_NAME, "active_option")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_inventory_page_to_load(self):
        """Wait for inventory page to load completely"""
        self.wait_for_element_visible(self.INVENTORY_CONTAINER)
        self.wait_for_element_visible(self.INVENTORY_LIST)
    
    def get_inventory_items_count(self):
        """Get the number of inventory items"""
        items = self.find_elements(self.INVENTORY_ITEMS)
        return len(items)
    
    def get_all_item_names(self):
        """Get all item names"""
        items = self.find_elements(self.ITEM_NAMES)
        return [item.text for item in items]
    
    def get_all_item_prices(self):
        """Get all item prices"""
        items = self.find_elements(self.ITEM_PRICES)
        return [item.text for item in items]
    
    def get_all_item_descriptions(self):
        """Get all item descriptions"""
        items = self.find_elements(self.ITEM_DESCRIPTIONS)
        return [item.text for item in items]
    
    def get_item_by_name(self, item_name):
        """Get item element by name"""
        items = self.find_elements(self.INVENTORY_ITEMS)
        for item in items:
            name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
            if name_element.text == item_name:
                return item
        return None
    
    def add_item_to_cart_by_name(self, item_name):
        """Add item to cart by name"""
        item = self.get_item_by_name(item_name)
        if item:
            add_button = item.find_element(By.CLASS_NAME, "btn_inventory")
            add_button.click()
            return True
        return False
    
    def remove_item_from_cart_by_name(self, item_name):
        """Remove item from cart by name"""
        item = self.get_item_by_name(item_name)
        if item:
            remove_button = item.find_element(By.CLASS_NAME, "btn_inventory")
            if remove_button.text == "Remove":
                remove_button.click()
                return True
        return False
    
    def get_cart_items_count(self):
        """Get the number of items in cart"""
        try:
            badge = self.find_element(self.SHOPPING_CART_BADGE)
            return int(badge.text)
        except (TimeoutException, NoSuchElementException):
            return 0
    
    def click_shopping_cart(self):
        """Click on shopping cart"""
        self.click_element(self.SHOPPING_CART_LINK)
    
    def open_burger_menu(self):
        """Open the burger menu"""
        self.click_element(self.BURGER_MENU)
        self.wait_for_element_visible(self.BURGER_MENU_ITEMS)
    
    def close_burger_menu(self):
        """Close the burger menu"""
        self.click_element(self.CLOSE_BURGER_MENU)
    
    def click_logout(self):
        """Click logout from burger menu"""
        self.open_burger_menu()
        self.click_element(self.LOGOUT_LINK)
    
    def click_about(self):
        """Click about from burger menu"""
        self.open_burger_menu()
        self.click_element(self.ABOUT_LINK)
    
    def click_reset_app_state(self):
        """Click reset app state from burger menu"""
        self.open_burger_menu()
        self.click_element(self.RESET_APP_STATE_LINK)
    
    def sort_items_by(self, sort_option):
        """Sort items by given option using Select class"""
        sort_element = self.find_element(self.SORT_CONTAINER)
        select = Select(sort_element)
        select.select_by_value(sort_option)
    
    def get_sort_option_text(self):
        """Get the current sort option text"""
        try:
            return self.get_element_text(self.ACTIVE_OPTION)
        except (TimeoutException, NoSuchElementException):
            return ""
    
    def is_item_in_cart(self, item_name):
        """Check if item is in cart"""
        item = self.get_item_by_name(item_name)
        if item:
            button = item.find_element(By.CLASS_NAME, "btn_inventory")
            return button.text == "Remove"
        return False
    
    def get_item_price_by_name(self, item_name):
        """Get item price by name"""
        item = self.get_item_by_name(item_name)
        if item:
            price_element = item.find_element(By.CLASS_NAME, "inventory_item_price")
            return price_element.text
        return None
    
    def get_item_description_by_name(self, item_name):
        """Get item description by name"""
        item = self.get_item_by_name(item_name)
        if item:
            desc_element = item.find_element(By.CLASS_NAME, "inventory_item_desc")
            return desc_element.text
        return None
    
    def click_item_name(self, item_name):
        """Click on item name to view details"""
        item = self.get_item_by_name(item_name)
        if item:
            name_element = item.find_element(By.CLASS_NAME, "inventory_item_name")
            name_element.click()
            return True
        return False
    
    def click_item_image(self, item_name):
        """Click on item image to view details"""
        item = self.get_item_by_name(item_name)
        if item:
            image_element = item.find_element(By.CLASS_NAME, "inventory_item_img")
            image_element.click()
            return True
        return False
    
    def is_burger_menu_open(self):
        """Check if burger menu is open"""
        return self.is_element_visible(self.BURGER_MENU_ITEMS)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_title() 