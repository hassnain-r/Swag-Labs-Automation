#!/usr/bin/env python3
"""
WebDriver Setup Script for Sauce Demo WebUI Automation Framework

This script helps set up and troubleshoot WebDriver issues.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    
    print("✅ Python version is compatible")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'selenium',
        'webdriver-manager',
        'pytest',
        'pytest-html',
        'python-dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True


def check_browsers():
    """Check if browsers are installed"""
    system = platform.system().lower()
    
    browsers = {
        'chrome': {
            'windows': r'C:\Program Files\Google\Chrome\Application\chrome.exe',
            'darwin': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
            'linux': '/usr/bin/google-chrome'
        },
        'firefox': {
            'windows': r'C:\Program Files\Mozilla Firefox\firefox.exe',
            'darwin': '/Applications/Firefox.app/Contents/MacOS/firefox',
            'linux': '/usr/bin/firefox'
        },
        'edge': {
            'windows': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
            'darwin': '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
            'linux': '/usr/bin/microsoft-edge'
        }
    }
    
    available_browsers = []
    
    for browser, paths in browsers.items():
        if system in paths:
            path = paths[system]
            if os.path.exists(path):
                print(f"✅ {browser.capitalize()} is installed at: {path}")
                available_browsers.append(browser)
            else:
                print(f"❌ {browser.capitalize()} is not found at: {path}")
        else:
            print(f"⚠️  {browser.capitalize()} path not configured for {system}")
    
    return available_browsers


# Import required modules at the top
try:
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service as ChromeService
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

def test_webdriver_installation():
    """Test WebDriver installation"""
    print("\n🧪 Testing WebDriver installation...")
    
    if not SELENIUM_AVAILABLE:
        print("❌ Selenium and webdriver-manager not available")
        return False
    
    print("✅ Selenium and webdriver-manager imported successfully")
    
    # Test Chrome WebDriver
    try:
        print("Testing Chrome WebDriver...")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.quit()
        print("✅ Chrome WebDriver test successful")
        return True
    except Exception as e:
        print(f"❌ Chrome WebDriver test failed: {e}")
        return False


def install_webdrivers():
    """Install WebDrivers using webdriver-manager"""
    print("\n📥 Installing WebDrivers...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        # Install ChromeDriver
        try:
            chrome_path = ChromeDriverManager().install()
            print(f"✅ ChromeDriver installed at: {chrome_path}")
        except Exception as e:
            print(f"❌ ChromeDriver installation failed: {e}")
        
        # Install GeckoDriver
        try:
            firefox_path = GeckoDriverManager().install()
            print(f"✅ GeckoDriver installed at: {firefox_path}")
        except Exception as e:
            print(f"❌ GeckoDriver installation failed: {e}")
        
        # Install EdgeDriver
        try:
            edge_path = EdgeChromiumDriverManager().install()
            print(f"✅ EdgeDriver installed at: {edge_path}")
        except Exception as e:
            print(f"❌ EdgeDriver installation failed: {e}")
            
    except ImportError:
        print("❌ webdriver-manager not installed. Run: pip install webdriver-manager")


def create_test_script():
    """Create a simple test script to verify setup"""
    test_script = """
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from config.config import TestConfig

def test_basic_setup():
    try:
        # Create driver
        driver = DriverFactory.get_driver()
        print("✅ WebDriver created successfully")
        
        # Test login page
        login_page = LoginPage(driver)
        login_page.navigate_to_login_page()
        print("✅ Navigation to login page successful")
        
        # Test login
        login_page.login(TestConfig.VALID_USERNAME, TestConfig.VALID_PASSWORD)
        print("✅ Login successful")
        
        # Clean up
        driver.quit()
        print("✅ Test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    test_basic_setup()
"""
    
    with open('test_setup.py', 'w') as f:
        f.write(test_script)
    
    print("✅ Test script created: test_setup.py")


def main():
    """Main function"""
    print("🔧 Sauce Demo WebUI Automation Framework - Setup Check")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check dependencies
    if not check_dependencies():
        return 1
    
    # Check browsers
    available_browsers = check_browsers()
    if not available_browsers:
        print("\n⚠️  No browsers found. Please install at least one browser.")
    
    # Install WebDrivers
    install_webdrivers()
    
    # Test WebDriver installation
    if test_webdriver_installation():
        print("\n🎉 Setup completed successfully!")
        
        # Create test script
        create_test_script()
        print("\n📝 You can now run tests with:")
        print("   python run_tests.py")
        print("   python test_setup.py")
        
        return 0
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 