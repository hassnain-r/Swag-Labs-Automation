#!/usr/bin/env python3
"""
Script to open the HTML test report in the default browser
"""

import os
import sys
import webbrowser
from pathlib import Path


def open_html_report():
    """Open the HTML test report in the default browser"""
    report_path = Path("reports/report.html")
    
    if not report_path.exists():
        print("❌ HTML report not found!")
        print(f"Expected location: {report_path.absolute()}")
        print("\nTo generate a report, run:")
        print("python run_tests.py --report-format html")
        return False
    
    # Convert to absolute path
    absolute_path = report_path.absolute()
    
    print(f"📊 Opening HTML report: {absolute_path}")
    
    try:
        # Open in default browser
        webbrowser.open(f"file://{absolute_path}")
        print("✅ Report opened successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to open report: {e}")
        print(f"Please manually open: {absolute_path}")
        return False


def list_available_reports():
    """List all available reports in the reports directory"""
    reports_dir = Path("reports")
    
    if not reports_dir.exists():
        print("❌ Reports directory not found!")
        return
    
    print("📁 Available reports:")
    for report_file in reports_dir.glob("*"):
        if report_file.is_file():
            size = report_file.stat().st_size
            print(f"   {report_file.name} ({size} bytes)")


def main():
    """Main function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        list_available_reports()
        return
    
    success = open_html_report()
    if not success:
        list_available_reports()


if __name__ == "__main__":
    main() 