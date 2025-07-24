#!/usr/bin/env python3
"""
Test Status Checker - Check test environment and provide helpful information
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python():
    """Check Python version and installation"""
    print("🐍 Python Check:")
    print(f"   Python Version: {sys.version}")
    print(f"   Python Executable: {sys.executable}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Dependencies Check:")
    
    required_packages = [
        'selenium',
        'pytest', 
        'pytest-html',
        'webdriver-manager'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} (missing)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n   Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def check_directories():
    """Check if required directories exist"""
    print("\n📁 Directory Check:")
    
    directories = ['tests', 'pages', 'utils', 'config', 'reports']
    
    for directory in directories:
        if Path(directory).exists():
            print(f"   ✅ {directory}/")
        else:
            print(f"   ❌ {directory}/ (missing)")
            Path(directory).mkdir(exist_ok=True)
            print(f"   ✅ {directory}/ (created)")

def check_test_files():
    """Check if test files exist"""
    print("\n🧪 Test Files Check:")
    
    test_files = [
        'tests/test_login.py',
        'tests/test_inventory.py', 
        'tests/test_cart.py',
        'tests/test_checkout.py',
        'tests/test_e2e.py'
    ]
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"   ✅ {test_file}")
        else:
            print(f"   ❌ {test_file} (missing)")

def check_reports():
    """Check for existing reports"""
    print("\n📊 Reports Check:")
    
    reports_dir = Path("reports")
    if reports_dir.exists():
        report_files = list(reports_dir.glob("*.html"))
        if report_files:
            print("   Existing HTML reports:")
            for report in report_files:
                print(f"   📄 {report.name}")
        else:
            print("   No HTML reports found")
    else:
        print("   Reports directory not found")

def run_simple_test():
    """Run a very simple test to check if everything works"""
    print("\n🧪 Running Simple Test:")
    
    try:
        # Try to import and run a simple test
        result = subprocess.run([
            "python", "-m", "pytest", 
            "tests/test_login.py::TestLogin::test_successful_login_with_valid_credentials",
            "--tb=short",
            "-q"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ Test ran successfully!")
        else:
            print("   ❌ Test failed (this is expected if website is not accessible)")
            print(f"   Error: {result.stderr[:200]}...")
        
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("   ⏰ Test timed out")
        return False
    except Exception as e:
        print(f"   ❌ Error running test: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Test Environment Check")
    print("=" * 50)
    
    # Run all checks
    check_python()
    deps_ok = check_dependencies()
    check_directories()
    check_test_files()
    check_reports()
    
    print("\n" + "=" * 50)
    
    if deps_ok:
        print("✅ Environment looks good!")
        print("\n🚀 To run tests with reports:")
        print("   python run_tests.py --report-format html")
        print("   python quick_test.py")
        print("   python quick_test.py all")
        
        print("\n📊 To view reports:")
        print("   python open_report.py")
        
        # Try a simple test
        run_simple_test()
    else:
        print("❌ Please install missing dependencies first")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main() 