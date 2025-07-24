"""Test data configuration for the automation framework"""

class TestData:
    """Centralized test data for all tests"""
    
    # Product data
    PRODUCTS = {
        "Sauce Labs Backpack": {
            "name": "Sauce Labs Backpack",
            "price": "$29.99",
            "price_value": 29.99,
            "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection."
        },
        "Sauce Labs Bike Light": {
            "name": "Sauce Labs Bike Light",
            "price": "$9.99",
            "price_value": 9.99,
            "description": "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included."
        },
        "Sauce Labs Bolt T-Shirt": {
            "name": "Sauce Labs Bolt T-Shirt",
            "price": "$15.99",
            "price_value": 15.99,
            "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt."
        },
        "Sauce Labs Fleece Jacket": {
            "name": "Sauce Labs Fleece Jacket",
            "price": "$49.99",
            "price_value": 49.99,
            "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office."
        },
        "Sauce Labs Onesie": {
            "name": "Sauce Labs Onesie",
            "price": "$7.99",
            "price_value": 7.99,
            "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel."
        },
        "Test.allTheThings() T-Shirt (Red)": {
            "name": "Test.allTheThings() T-Shirt (Red)",
            "price": "$15.99",
            "price_value": 15.99,
            "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton."
        }
    }
    
    # Expected product lists
    EXPECTED_ITEMS = [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light", 
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Fleece Jacket",
        "Sauce Labs Onesie",
        "Test.allTheThings() T-Shirt (Red)"
    ]
    
    # Expected prices dictionary
    EXPECTED_PRICES = {
        "Sauce Labs Backpack": "$29.99",
        "Sauce Labs Bike Light": "$9.99",
        "Sauce Labs Bolt T-Shirt": "$15.99",
        "Sauce Labs Fleece Jacket": "$49.99",
        "Sauce Labs Onesie": "$7.99",
        "Test.allTheThings() T-Shirt (Red)": "$15.99"
    }
    
    # Expected price values (float)
    EXPECTED_PRICE_VALUES = {
        "Sauce Labs Backpack": 29.99,
        "Sauce Labs Bike Light": 9.99,
        "Sauce Labs Bolt T-Shirt": 15.99,
        "Sauce Labs Fleece Jacket": 49.99,
        "Sauce Labs Onesie": 7.99,
        "Test.allTheThings() T-Shirt (Red)": 15.99
    }
    
    # Test user data
    USERS = {
        "valid": {
            "username": "standard_user",
            "password": "secret_sauce"
        },
        "locked": {
            "username": "locked_out_user", 
            "password": "secret_sauce"
        },
        "problem": {
            "username": "problem_user",
            "password": "secret_sauce"
        },
        "performance": {
            "username": "performance_glitch_user",
            "password": "secret_sauce"
        },
        "invalid": {
            "username": "invalid_user",
            "password": "invalid_password"
        }
    }
    
    # Checkout test data
    CHECKOUT_DATA = {
        "valid": {
            "first_name": "John",
            "last_name": "Doe", 
            "postal_code": "12345"
        },
        "alternate": {
            "first_name": "Jane",
            "last_name": "Smith",
            "postal_code": "54321"
        },
        "another": {
            "first_name": "Alice",
            "last_name": "Johnson",
            "postal_code": "98765"
        }
    }
    
    # Error messages
    ERROR_MESSAGES = {
        "invalid_credentials": "Epic sadface: Username and password do not match any user in this service",
        "locked_user": "Epic sadface: Sorry, this user has been locked out",
        "empty_username": "Epic sadface: Username is required",
        "empty_password": "Epic sadface: Password is required",
        "checkout_error": "Error: First Name is required"
    }
    
    # Sort options
    SORT_OPTIONS = {
        "name_az": "az",
        "name_za": "za", 
        "price_low_high": "lohi",
        "price_high_low": "hilo"
    }
    
    # Tax rate
    TAX_RATE = 0.08  # 8%
    
    @classmethod
    def get_product_price(cls, product_name):
        """Get product price by name"""
        return cls.PRODUCTS.get(product_name, {}).get("price", "")
    
    @classmethod
    def get_product_price_value(cls, product_name):
        """Get product price value (float) by name"""
        return cls.PRODUCTS.get(product_name, {}).get("price_value", 0.0)
    
    @classmethod
    def get_product_description(cls, product_name):
        """Get product description by name"""
        return cls.PRODUCTS.get(product_name, {}).get("description", "")
    
    @classmethod
    def get_user_credentials(cls, user_type):
        """Get user credentials by type"""
        return cls.USERS.get(user_type, {})
    
    @classmethod
    def get_checkout_data(cls, data_type):
        """Get checkout data by type"""
        return cls.CHECKOUT_DATA.get(data_type, {})
    
    @classmethod
    def get_error_message(cls, error_type):
        """Get error message by type"""
        return cls.ERROR_MESSAGES.get(error_type, "")
    
    @classmethod
    def get_sort_option(cls, sort_type):
        """Get sort option by type"""
        return cls.SORT_OPTIONS.get(sort_type, "")
    
    @classmethod
    def calculate_tax(cls, subtotal):
        """Calculate tax amount"""
        return subtotal * cls.TAX_RATE
    
    @classmethod
    def calculate_total(cls, subtotal):
        """Calculate total amount including tax"""
        tax = cls.calculate_tax(subtotal)
        return subtotal + tax 