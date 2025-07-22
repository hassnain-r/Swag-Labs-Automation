from selenium.webdriver.common.by import By
from utils.base_page import BasePage


class CheckoutPage(BasePage):
    """Page object for the Sauce Demo checkout page"""
    
    # Locators
    CHECKOUT_INFO_CONTAINER = (By.ID, "checkout_info_container")
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.CLASS_NAME, "btn_primary")
    CANCEL_BUTTON = (By.CLASS_NAME, "btn_secondary")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message-container")
    ERROR_MESSAGE_TEXT = (By.CLASS_NAME, "error-message-container")
    CHECKOUT_TITLE = (By.CLASS_NAME, "subheader")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_checkout_page_to_load(self):
        """Wait for checkout page to load completely"""
        self.wait_for_element_visible(self.CHECKOUT_INFO_CONTAINER)
    
    def enter_first_name(self, first_name):
        """Enter first name"""
        self.send_keys_to_element(self.FIRST_NAME_FIELD, first_name)
    
    def enter_last_name(self, last_name):
        """Enter last name"""
        self.send_keys_to_element(self.LAST_NAME_FIELD, last_name)
    
    def enter_postal_code(self, postal_code):
        """Enter postal code"""
        self.send_keys_to_element(self.POSTAL_CODE_FIELD, postal_code)
    
    def fill_checkout_form(self, first_name, last_name, postal_code):
        """Fill the complete checkout form"""
        self.enter_first_name(first_name)
        self.enter_last_name(last_name)
        self.enter_postal_code(postal_code)
    
    def click_continue(self):
        """Click continue button"""
        self.click_element(self.CONTINUE_BUTTON)
    
    def click_cancel(self):
        """Click cancel button"""
        self.click_element(self.CANCEL_BUTTON)
    
    def get_error_message(self):
        """Get error message text"""
        try:
            return self.get_element_text(self.ERROR_MESSAGE_TEXT)
        except:
            return ""
    
    def is_error_message_displayed(self):
        """Check if error message is displayed"""
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def get_first_name_value(self):
        """Get first name field value"""
        return self.get_element_attribute(self.FIRST_NAME_FIELD, "value")
    
    def get_last_name_value(self):
        """Get last name field value"""
        return self.get_element_attribute(self.LAST_NAME_FIELD, "value")
    
    def get_postal_code_value(self):
        """Get postal code field value"""
        return self.get_element_attribute(self.POSTAL_CODE_FIELD, "value")
    
    def clear_first_name(self):
        """Clear first name field"""
        element = self.find_element(self.FIRST_NAME_FIELD)
        element.clear()
    
    def clear_last_name(self):
        """Clear last name field"""
        element = self.find_element(self.LAST_NAME_FIELD)
        element.clear()
    
    def clear_postal_code(self):
        """Clear postal code field"""
        element = self.find_element(self.POSTAL_CODE_FIELD)
        element.clear()
    
    def clear_all_fields(self):
        """Clear all form fields"""
        self.clear_first_name()
        self.clear_last_name()
        self.clear_postal_code()
    
    def get_checkout_title(self):
        """Get checkout page title"""
        return self.get_element_text(self.CHECKOUT_TITLE)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_title()
    
    def is_continue_button_enabled(self):
        """Check if continue button is enabled"""
        try:
            element = self.find_element(self.CONTINUE_BUTTON)
            return element.is_enabled()
        except:
            return False
    
    def is_cancel_button_enabled(self):
        """Check if cancel button is enabled"""
        try:
            element = self.find_element(self.CANCEL_BUTTON)
            return element.is_enabled()
        except:
            return False


class CheckoutOverviewPage(BasePage):
    """Page object for the Sauce Demo checkout overview page"""
    
    # Locators
    CHECKOUT_SUMMARY_CONTAINER = (By.ID, "checkout_summary_container")
    CART_LIST = (By.CLASS_NAME, "cart_list")
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    ITEM_QUANTITIES = (By.CLASS_NAME, "cart_quantity")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.CLASS_NAME, "btn_action")
    CANCEL_BUTTON = (By.CLASS_NAME, "btn_secondary")
    OVERVIEW_TITLE = (By.CLASS_NAME, "subheader")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_overview_page_to_load(self):
        """Wait for overview page to load completely"""
        self.wait_for_element_visible(self.CHECKOUT_SUMMARY_CONTAINER)
    
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
    
    def get_subtotal_text(self):
        """Get subtotal text"""
        return self.get_element_text(self.SUBTOTAL_LABEL)
    
    def get_tax_text(self):
        """Get tax text"""
        return self.get_element_text(self.TAX_LABEL)
    
    def get_total_text(self):
        """Get total text"""
        return self.get_element_text(self.TOTAL_LABEL)
    
    def get_subtotal_amount(self):
        """Get subtotal amount as float"""
        subtotal_text = self.get_subtotal_text()
        # Extract amount from "Item total: $XX.XX"
        amount = subtotal_text.split('$')[1]
        return float(amount)
    
    def get_tax_amount(self):
        """Get tax amount as float"""
        tax_text = self.get_tax_text()
        # Extract amount from "Tax: $XX.XX"
        amount = tax_text.split('$')[1]
        return float(amount)
    
    def get_total_amount(self):
        """Get total amount as float"""
        total_text = self.get_total_text()
        # Extract amount from "Total: $XX.XX"
        amount = total_text.split('$')[1]
        return float(amount)
    
    def click_finish(self):
        """Click finish button"""
        self.click_element(self.FINISH_BUTTON)
    
    def click_cancel(self):
        """Click cancel button"""
        self.click_element(self.CANCEL_BUTTON)
    
    def get_overview_title(self):
        """Get overview page title"""
        return self.get_element_text(self.OVERVIEW_TITLE)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_title()
    
    def is_finish_button_enabled(self):
        """Check if finish button is enabled"""
        try:
            element = self.find_element(self.FINISH_BUTTON)
            return element.is_enabled()
        except:
            return False
    
    def is_cancel_button_enabled(self):
        """Check if cancel button is enabled"""
        try:
            element = self.find_element(self.CANCEL_BUTTON)
            return element.is_enabled()
        except:
            return False


class CheckoutCompletePage(BasePage):
    """Page object for the Sauce Demo checkout complete page"""
    
    # Locators
    CHECKOUT_COMPLETE_CONTAINER = (By.ID, "checkout_complete_container")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    PONY_EXPRESS_IMAGE = (By.CLASS_NAME, "pony_express")
    BACK_HOME_BUTTON = (By.CLASS_NAME, "btn_primary")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def wait_for_complete_page_to_load(self):
        """Wait for complete page to load completely"""
        self.wait_for_element_visible(self.CHECKOUT_COMPLETE_CONTAINER)
    
    def get_complete_header(self):
        """Get complete header text"""
        return self.get_element_text(self.COMPLETE_HEADER)
    
    def get_complete_text(self):
        """Get complete text"""
        return self.get_element_text(self.COMPLETE_TEXT)
    
    def click_back_home(self):
        """Click back home button"""
        self.click_element(self.BACK_HOME_BUTTON)
    
    def is_pony_express_image_displayed(self):
        """Check if pony express image is displayed"""
        return self.is_element_visible(self.PONY_EXPRESS_IMAGE)
    
    def get_page_title(self):
        """Get the page title"""
        return self.get_title()
    
    def is_back_home_button_enabled(self):
        """Check if back home button is enabled"""
        try:
            element = self.find_element(self.BACK_HOME_BUTTON)
            return element.is_enabled()
        except:
            return False 