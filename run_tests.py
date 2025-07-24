#!/usr/bin/env python3
"""
Test Runner Script for Sauce Demo WebUI Automation Framework

This script provides an easy way to run tests with different configurations.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def create_directories():
    """Create necessary directories if they don't exist"""
    directories = ['reports', 'screenshots']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)


def run_tests(args):
    """Run tests with the specified arguments"""
    cmd = ['pytest']
    
    # Add test path if specified
    if args.test_path:
        cmd.append(args.test_path)
    
    # Add markers if specified
    if args.markers:
        for marker in args.markers:
            cmd.extend(['-m', marker])
    
    # Add browser if specified
    if args.browser:
        os.environ['BROWSER'] = args.browser
    
    # Add headless mode if specified
    if args.headless:
        os.environ['HEADLESS'] = 'true'
    
    # Add custom timeouts if specified
    if args.implicit_wait:
        os.environ['IMPLICIT_WAIT'] = str(args.implicit_wait)
    
    if args.page_load_timeout:
        os.environ['PAGE_LOAD_TIMEOUT'] = str(args.page_load_timeout)
    
    # Add verbosity
    if args.verbose:
        cmd.append('-v')
    
    # Add stop on first failure
    if args.stop_on_failure:
        cmd.append('-x')
    
    # Add parallel execution
    if args.parallel:
        cmd.extend(['-n', 'auto'])
    
    # Add reporting options
    if args.report_format:
        if args.report_format == 'html':
            cmd.extend(['--html=reports/report.html', '--self-contained-html'])
        elif args.report_format == 'json':
            cmd.extend(['--json-report', '--json-report-file=reports/report.json'])
        elif args.report_format == 'xml':
            cmd.extend(['--junitxml=reports/report.xml'])
        elif args.report_format == 'all':
            cmd.extend([
                '--html=reports/report.html', 
                '--self-contained-html',
                '--json-report', 
                '--json-report-file=reports/report.json',
                '--junitxml=reports/report.xml'
            ])
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"Environment: BROWSER={os.environ.get('BROWSER', 'chrome')}, "
          f"HEADLESS={os.environ.get('HEADLESS', 'false')}")
    print("-" * 50)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("-" * 50)
        print("✅ Tests completed successfully!")
        
        # Show report locations
        if args.report_format:
            print("\n📊 Reports generated:")
            if args.report_format in ['html', 'all']:
                print(f"   HTML Report: {os.path.abspath('reports/report.html')}")
            if args.report_format in ['json', 'all']:
                print(f"   JSON Report: {os.path.abspath('reports/report.json')}")
            if args.report_format in ['xml', 'all']:
                print(f"   XML Report: {os.path.abspath('reports/report.xml')}")
        
        return result.returncode
    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"❌ Tests failed with exit code: {e.returncode}")
        
        # Show report locations even on failure
        if args.report_format:
            print("\n📊 Reports generated (may contain failure details):")
            if args.report_format in ['html', 'all']:
                print(f"   HTML Report: {os.path.abspath('reports/report.html')}")
            if args.report_format in ['json', 'all']:
                print(f"   JSON Report: {os.path.abspath('reports/report.json')}")
            if args.report_format in ['xml', 'all']:
                print(f"   XML Report: {os.path.abspath('reports/report.xml')}")
        
        return e.returncode


def main():
    """Main function to parse arguments and run tests"""
    parser = argparse.ArgumentParser(
        description='Sauce Demo WebUI Automation Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            python run_tests.py                           # Run all tests
            python run_tests.py -m login                  # Run login tests only
            python run_tests.py -m e2e -b firefox        # Run e2e tests in Firefox
            python run_tests.py --headless               # Run tests in headless mode
            python run_tests.py tests/test_login.py      # Run specific test file
            python run_tests.py -m smoke --parallel      # Run smoke tests in parallel
            python run_tests.py --report-format html     # Generate HTML report
            python run_tests.py --report-format all      # Generate all report formats
        """
    )
    
    parser.add_argument(
        'test_path',
        nargs='?',
        help='Path to specific test file or directory'
    )
    
    parser.add_argument(
        '-m', '--markers',
        nargs='+',
        choices=['login', 'inventory', 'cart', 'checkout', 'e2e', 'smoke', 'regression'],
        help='Test markers to run'
    )
    
    parser.add_argument(
        '-b', '--browser',
        choices=['chrome', 'firefox', 'edge'],
        default='chrome',
        help='Browser to use for testing (default: chrome)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run tests in headless mode'
    )
    
    parser.add_argument(
        '--implicit-wait',
        type=int,
        help='Implicit wait timeout in seconds'
    )
    
    parser.add_argument(
        '--page-load-timeout',
        type=int,
        help='Page load timeout in seconds'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Increase verbosity'
    )
    
    parser.add_argument(
        '-x', '--stop-on-failure',
        action='store_true',
        help='Stop on first failure'
    )
    
    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tests in parallel'
    )
    
    parser.add_argument(
        '--report-format',
        choices=['html', 'json', 'xml', 'all'],
        help='Generate test reports in specified format(s)'
    )
    
    args = parser.parse_args()
    
    # Create necessary directories
    create_directories()
    
    # Run tests
    return run_tests(args)


if __name__ == '__main__':
    sys.exit(main()) 