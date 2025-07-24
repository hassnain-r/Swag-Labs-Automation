# Swag Labs WebUI Automation

A comprehensive Selenium WebUI testing automation for the [Swag Labs website](https://www.saucedemo.com) built with Python, Selenium, and pytest using the Page Object Model (POM) pattern.

## 🚀 Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Multi-browser Support**: Chrome, Firefox, and Edge browsers
- **Comprehensive Test Coverage**: Login, Inventory, Cart, and Checkout functionality
- **End-to-End Tests**: Complete user journey scenarios
- **Configurable**: Environment-based configuration
- **Robust Error Handling**: Explicit waits and error recovery
- **HTML Reports**: Detailed test execution reports
- **Cross-platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hassnain-r/Swag-Labs-Automation
   cd webui_automation
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script** (recommended for first-time setup):
   ```bash
   python setup_webdriver.py
   ```

## 🏗️ Project Structure

```
webui_automation/
├── config/
│   ├── __init__.py
│   ├── config.py              # Configuration settings
│   └── test_data.py           # Test data and user credentials
├── pages/
│   ├── __init__.py
│   ├── login_page.py          # Login page object
│   ├── inventory_page.py      # Inventory page object
│   ├── cart_page.py           # Cart page object
│   └── checkout_page.py       # Checkout page objects
├── tests/
│   ├── __init__.py
│   ├── test_login.py          # Login tests
│   ├── test_inventory.py      # Inventory tests
│   ├── test_cart.py           # Cart tests
│   ├── test_checkout.py       # Checkout tests
│   └── test_e2e.py            # End-to-end tests
├── utils/
│   ├── __init__.py
│   ├── base_page.py           # Base page class
│   ├── driver_factory.py      # WebDriver factory
│   ├── logger.py              # Logging utilities
│   └── path_manager.py        # Path management utilities
├── logs/                      # Test execution logs
├── reports/                   # HTML test reports
├── screenshots/               # Test failure screenshots
├── __init__.py               # Package initialization
├── check_tests.py            # Test validation script
├── conftest.py               # Pytest fixtures and configuration
├── open_report.py            # Report opening utility
├── pytest.ini               # Pytest configuration
├── quick_test.py            # Quick test runner
├── README.md                # This file
├── REPORTING_GUIDE.md       # Reporting documentation
├── requirements.txt         # Python dependencies
├── run_tests.py            # Test execution script
└── setup_webdriver.py      # WebDriver setup utility
```

## 🧪 Running Tests

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Login tests only
pytest -m login

# Inventory tests only
pytest -m inventory

# Cart tests only
pytest -m cart

# Checkout tests only
pytest -m checkout

# End-to-end tests only
pytest -m e2e

# Smoke tests
pytest -m smoke

# Regression tests
pytest -m regression
```

### Run Specific Test Files
```bash
# Run login tests
pytest tests/test_login.py

# Run end-to-end tests
pytest tests/test_e2e.py
```

### Run Tests with Different Browsers
```bash
# Chrome (default)
pytest

# Firefox
BROWSER=firefox pytest

# Edge
BROWSER=edge pytest
```

### Run Tests in Headless Mode
```bash
HEADLESS=true pytest
```

### Run Tests with Custom Configuration
```bash
# Set custom timeouts
IMPLICIT_WAIT=15 PAGE_LOAD_TIMEOUT=45 pytest

# Run with specific browser and headless mode
BROWSER=chrome HEADLESS=true pytest
```

## 📊 Test Reports

After running tests, HTML reports are automatically generated in the `reports/` directory:

```bash
# View the latest report
open reports/report.html
```

## 🔧 Configuration

### Environment Variables

You can configure the framework using environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `BROWSER` | `chrome` | Browser to use (chrome, firefox, edge) |
| `HEADLESS` | `false` | Run in headless mode (true/false) |
| `IMPLICIT_WAIT` | `10` | Implicit wait timeout in seconds |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout in seconds |
| `TEST_TIMEOUT` | `60` | Test timeout in seconds |

### Configuration File

The main configuration is in `config/config.py`:

```python
class TestConfig:
    BASE_URL = "https://www.saucedemo.com"
    VALID_USERNAME = "standard_user"
    VALID_PASSWORD = "secret_sauce"
    # ... other settings
```

## 🧩 Page Object Model

The framework follows the Page Object Model pattern:

### Base Page
- `utils/base_page.py`: Common functionality for all page objects
- Provides methods for element interaction, waiting, and navigation

### Page Objects
- `pages/login_page.py`: Login page interactions
- `pages/inventory_page.py`: Product inventory interactions
- `pages/cart_page.py`: Shopping cart interactions
- `pages/checkout_page.py`: Checkout process interactions

### Example Usage
```python
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Initialize page objects
login_page = LoginPage(driver)
inventory_page = InventoryPage(driver)

# Perform actions
login_page.login("username", "password")
inventory_page.add_item_to_cart_by_name("Sauce Labs Backpack")
```

## 🧪 Test Categories

### 1. Login Tests (`test_login.py`)
- Valid/invalid credentials
- Locked user scenarios
- Empty field validation
- UI element verification

### 2. Inventory Tests (`test_inventory.py`)
- Product display and sorting
- Add/remove items from cart
- Navigation and menu functionality
- Price and description verification

### 3. Cart Tests (`test_cart.py`)
- Cart management (add/remove items)
- Price calculations
- Navigation between pages
- Cart persistence

### 4. Checkout Tests (`test_checkout.py`)
- Form validation
- Checkout flow completion
- Price calculations and tax
- Order confirmation

### 5. End-to-End Tests (`test_e2e.py`)
- Complete purchase flows
- Multi-item scenarios
- Error handling and recovery
- Navigation patterns

## 🔍 Test Data

The framework includes test data for different user types:

| Username | Password | Description |
|----------|----------|-------------|
| `standard_user` | `secret_sauce` | Normal user (default) |
| `locked_out_user` | `secret_sauce` | Locked user (for error testing) |
| `problem_user` | `secret_sauce` | User with UI issues |
| `performance_glitch_user` | `secret_sauce` | User with performance issues |

## 🛠️ Customization

### Adding New Page Objects
1. Create a new file in the `pages/` directory
2. Inherit from `BasePage`
3. Define locators and methods
4. Add corresponding tests

### Adding New Test Cases
1. Create a new test file in the `tests/` directory
2. Use appropriate fixtures from `conftest.py`
3. Follow the existing naming conventions
4. Add appropriate markers

### Custom Browser Configuration
Modify `utils/driver_factory.py` to add custom browser options or new browser support.

## 🐛 Troubleshooting

### Common Issues

1. **WebDriver not found**: Ensure you have the latest version of the browser installed
2. **Element not found**: Check if the website structure has changed
3. **Timeout errors**: Increase timeout values in configuration
4. **Browser compatibility**: Try different browsers or update browser versions
5. **Win32 application error**: Run `python setup_webdriver.py` to reinstall WebDrivers
6. **Import errors**: Ensure you're running tests from the project root directory

### Debug Mode
Run tests with increased verbosity:
```bash
pytest -v -s
```

### Screenshots
Screenshots are automatically taken on test failures and saved in the `screenshots/` directory.

## 📈 Best Practices

1. **Use Page Objects**: Always interact with pages through page objects
2. **Explicit Waits**: Use explicit waits instead of implicit waits for better reliability
3. **Test Isolation**: Each test should be independent and not rely on other tests
4. **Meaningful Assertions**: Use descriptive assertion messages
5. **Error Handling**: Implement proper error handling and recovery
6. **Configuration**: Use environment variables for different environments

**Happy Testing!** 