#!/usr/bin/env python3
"""
Quick Test Runner - Simple script to run tests and generate reports
"""

import subprocess
import sys
import os
from pathlib import Path

def run_quick_test():
    """Run a quick test with HTML report"""
    print("🚀 Running Quick Test with HTML Report...")
    print("=" * 50)
    
    # Create reports directory if it doesn't exist
    Path("reports").mkdir(exist_ok=True)
    
    # Run a simple test with HTML report
    cmd = [
        "python", "-m", "pytest", 
        "tests/test_login.py::TestLogin::test_successful_login_with_valid_credentials",
        "--html=reports/quick_report.html",
        "--self-contained-html",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("Command Output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        print("=" * 50)
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
            print(f"📊 HTML Report: {os.path.abspath('reports/quick_report.html')}")
        else:
            print("❌ Test failed!")
            print(f"📊 HTML Report (with failure details): {os.path.abspath('reports/quick_report.html')}")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running test: {e}")
        return 1

def run_all_tests():
    """Run all tests with HTML report"""
    print("🚀 Running All Tests with HTML Report...")
    print("=" * 50)
    
    # Create reports directory if it doesn't exist
    Path("reports").mkdir(exist_ok=True)
    
    # Run all tests with HTML report
    cmd = [
        "python", "-m", "pytest", 
        "--html=reports/full_report.html",
        "--self-contained-html",
        "-v"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("Command Output:")
        print(result.stdout)
        
        if result.stderr:
            print("Errors:")
            print(result.stderr)
        
        print("=" * 50)
        
        if result.returncode == 0:
            print("✅ All tests completed successfully!")
        else:
            print("❌ Some tests failed!")
        
        print(f"📊 HTML Report: {os.path.abspath('reports/full_report.html')}")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "all":
            return run_all_tests()
        else:
            print("Usage: python quick_test.py [all]")
            print("  no args: Run single login test")
            print("  all: Run all tests")
            return 1
    
    return run_quick_test()

if __name__ == "__main__":
    sys.exit(main()) 