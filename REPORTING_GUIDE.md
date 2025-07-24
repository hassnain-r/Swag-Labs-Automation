# Test Reporting Guide

This guide explains how to run tests and generate various types of reports in the Sauce Demo WebUI Automation Framework.

## Quick Start

### 1. Run All Tests with HTML Report
```bash
python run_tests.py --report-format html
```

### 2. Open the HTML Report
```bash
python open_report.py
```

## Available Report Formats

The framework supports multiple report formats:

- **HTML**: Interactive web-based report (default)
- **JSON**: Machine-readable format for CI/CD
- **XML**: JUnit format for CI/CD integration
- **All**: Generate all formats simultaneously

## Running Tests with Reports

### Basic Commands

```bash
# Run all tests with HTML report
python run_tests.py --report-format html

# Run all tests with all report formats
python run_tests.py --report-format all

# Run specific test category with HTML report
python run_tests.py -m login --report-format html
python run_tests.py -m cart --report-format html
python run_tests.py -m checkout --report-format html
python run_tests.py -m inventory --report-format html
python run_tests.py -m e2e --report-format html

# Run specific test file with report
python run_tests.py tests/test_login.py --report-format html
```

### Advanced Options

```bash
# Run tests in headless mode with HTML report
python run_tests.py --headless --report-format html

# Run tests in different browser with report
python run_tests.py -b firefox --report-format html
python run_tests.py -b edge --report-format html

# Run tests in parallel with report
python run_tests.py --parallel --report-format html

# Run with verbose output and report
python run_tests.py -v --report-format html

# Stop on first failure with report
python run_tests.py -x --report-format html
```

## Report Locations

Reports are generated in the `reports/` directory:

- **HTML Report**: `reports/report.html`
- **JSON Report**: `reports/report.json`
- **XML Report**: `reports/report.xml`

## Opening Reports

### HTML Report (Recommended)
```bash
# Automatically open in default browser
python open_report.py

# List available reports
python open_report.py --list
```

### Manual Opening
- **HTML**: Double-click `reports/report.html` or open in any web browser
- **JSON**: Open with any text editor or JSON viewer
- **XML**: Open with any text editor or XML viewer

## Report Features

### HTML Report
- **Interactive Dashboard**: Summary of test results
- **Test Details**: Individual test results with pass/fail status
- **Error Information**: Detailed error messages and stack traces
- **Screenshots**: Automatic screenshots for failed tests
- **Filtering**: Filter tests by status, duration, etc.
- **Search**: Search for specific tests or error messages

### JSON Report
- **Machine Readable**: Perfect for CI/CD integration
- **Structured Data**: Easy to parse and analyze
- **Test Metadata**: Includes timing, status, and error details

### XML Report (JUnit)
- **CI/CD Compatible**: Works with Jenkins, GitLab CI, etc.
- **Standard Format**: Widely supported by build tools
- **Test Results**: Structured test results for automation

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run Tests
  run: |
    python run_tests.py --report-format all --headless

- name: Upload HTML Report
  uses: actions/upload-artifact@v2
  with:
    name: test-report-html
    path: reports/report.html

- name: Upload XML Report
  uses: actions/upload-artifact@v2
  with:
    name: test-report-xml
    path: reports/report.xml
```

### Jenkins Example
```groovy
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'python run_tests.py --report-format xml --headless'
            }
        }
    }
    post {
        always {
            publishTestResults testResultsPattern: 'reports/report.xml'
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Test Report'
            ])
        }
    }
}
```

## Troubleshooting

### No Reports Generated
1. Check if tests ran successfully
2. Verify the `reports/` directory exists
3. Ensure you specified `--report-format` parameter

### HTML Report Not Opening
```bash
# Check if report exists
ls -la reports/

# Try manual opening
python open_report.py --list
```

### Missing Dependencies
```bash
# Install required packages
pip install pytest-html pytest-json-report

# Or install all requirements
pip install -r requirements.txt
```

## Customizing Reports

### Pytest Configuration
Edit `pytest.ini` to customize default report settings:

```ini
[tool:pytest]
addopts = 
    -v
    --tb=short
    --html=reports/report.html
    --self-contained-html
    --json-report
    --json-report-file=reports/report.json
```

### Environment Variables
```bash
# Set browser
export BROWSER=firefox

# Set headless mode
export HEADLESS=true

# Set timeouts
export IMPLICIT_WAIT=10
export PAGE_LOAD_TIMEOUT=30
```

## Best Practices

1. **Always generate reports**: Use `--report-format html` for local development
2. **Use headless mode**: Add `--headless` for CI/CD environments
3. **Parallel execution**: Use `--parallel` for faster test execution
4. **Verbose output**: Use `-v` for detailed test information
5. **Stop on failure**: Use `-x` during development to catch issues early

## Report Analysis

### HTML Report Sections
- **Summary**: Overall test results and statistics
- **Environment**: Browser, headless mode, timeouts
- **Test Results**: Individual test details
- **Errors**: Detailed error information and screenshots

### Key Metrics
- **Total Tests**: Number of tests executed
- **Passed**: Number of successful tests
- **Failed**: Number of failed tests
- **Duration**: Total execution time
- **Success Rate**: Percentage of passed tests

## Examples

### Development Workflow
```bash
# Run tests with HTML report
python run_tests.py --report-format html -v

# Open report to analyze results
python open_report.py

# Fix issues and re-run
python run_tests.py --report-format html -v
```

### CI/CD Pipeline
```bash
# Run all tests in headless mode with all reports
python run_tests.py --headless --report-format all --parallel

# Check exit code for pipeline success/failure
echo $?
```

### Debugging Failed Tests
```bash
# Run specific failing test with verbose output
python run_tests.py tests/test_login.py -v --report-format html

# Stop on first failure for quick debugging
python run_tests.py -x --report-format html
```

This comprehensive reporting system provides detailed insights into test execution and helps identify and resolve issues quickly. 