# Food Billing System - Test Cases Documentation

A comprehensive testing documentation project for a web-based Food Billing System, developed as part of SWE30009 Software Testing and Reliability coursework.

## Project Overview

This project implements and documents the testing of a food billing system that allows users to:
- Select food items from a menu
- Specify quantities for each item
- Apply discounts (50%)
- Calculate bills with SST (6%)
- Generate detailed bill summaries

## Features

- Interactive menu with 8 food items
- Real-time bill calculation
- 50% discount option
- 6% SST calculation
- Responsive design for various screen sizes
- Input validation
- Detailed bill summary

## Test Coverage

The project includes 10 comprehensive test cases covering:

1. Basic Functionality Tests
   - Basic order calculation
   - Multiple items ordering
   - Empty order validation

2. Discount Application Tests
   - Single item with discount
   - Multiple items with discount
   - Edge cases with discount

3. Edge Cases
   - Maximum quantity orders
   - Various item combinations
   - Boundary value testing

## Technology Stack

- Frontend: HTML, CSS, JavaScript
- Backend: PHP, MySQL
- Testing: Selenium WebDriver (Python)
- Styling: Custom CSS with responsive design
- Database: MySQL

## Test Files Structure

├── test_screenshots/
├── selenium_test_cases.csv
├── food_billing_test.py
└── test_results.csv

## Running the Tests

1. Setup Requirements:
   - Python 3.x
   - Selenium WebDriver
   - Chrome WebDriver
   - Required Python packages (see requirements.txt)

2. Install Dependencies:
pip install -r requirements.txt

3. Run Tests:
python food_billing_test.py

## Test Results

Current test coverage metrics:
- Menu Items: 100%
- Price Points: 100%
- Business Rules: 100%
- Error Scenarios: 100%
- Feature Combinations: 100%

All 10 test cases are passing with successful validation of:
- Order calculations
- Discount applications
- SST calculations
- Input validations
- Edge cases

## Documentation

Detailed documentation includes:
- Test case descriptions
- Input parameters
- Expected results
- Coverage analysis
- Risk assessment
- Technical challenges and solutions

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License


## Author

Munieb Awad Elsheikhidris Abdelrahman

