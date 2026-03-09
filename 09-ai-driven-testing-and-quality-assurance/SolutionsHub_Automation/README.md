# SolutionsHub Test Automation Framework

## Overview
This is a BDD-based Test Automation Framework for testing https://solutionshub.epam.com/ using Cucumber, Selenium WebDriver, JUnit 5, and Gradle.

## Technology Stack
- **Java**: 11
- **Build Tool**: Gradle
- **Testing Framework**: JUnit 5
- **BDD Framework**: Cucumber 7.14.0
- **WebDriver**: Selenium 4.15.0
- **WebDriver Manager**: Bonigarcia WebDriverManager 5.6.2
- **Assertions**: AssertJ 3.24.2

## Project Structure
```
SolutionsHub_Automation/
├── src/
│   └── test/
│       ├── java/
│       │   └── com/
│       │       └── epam/
│       │           └── solutionshub/
│       │               ├── pages/           # Page Object Model classes
│       │               ├── stepdefinitions/ # Cucumber step definitions
│       │               ├── runners/         # Test runners
│       │               └── utils/           # Utility classes
│       └── resources/
│           ├── features/                    # Gherkin feature files
│           └── config.properties            # Configuration file
├── build.gradle                             # Gradle build configuration
└── README.md                                # This file
```

## Test Cases Covered

### 10 Automated Test Scenarios:

1. **TC-GEN-001**: Verify all 5 tabs are visible on homepage
2. **TC-GEN-004**: Navigate to Solutions page
3. **TC-GEN-015**: Verify smooth navigation between tabs
4. **TC-SOL-001**: Verify solutions list is displayed
5. **TC-SOL-002**: Verify solution item contains required metadata
6. **TC-SOL-003**: Open solution details page
7. **TC-AST-001**: Verify assets list is displayed
8. **TC-AST-002**: Verify asset card contains required fields
9. **TC-AST-003**: Verify asset detail or download flow
10. **TC-GUD-001**: Verify guides list is displayed
11. **TC-GUD-002**: Open full guide details
12. **TC-BLG-001**: Verify blog list is displayed
13. **TC-BLG-002**: Verify blog post contains required metadata
14. **TC-BLG-003**: Open full blog article
15. **TC-ABT-001**: Verify company information is displayed
16. **TC-ABT-002**: Verify mission, goals, and team sections

## Prerequisites
- Java 11 or higher installed
- Chrome browser installed (or modify config.properties for other browsers)
- Internet connection

## Installation

### 1. Navigate to the project directory:
```bash
cd SolutionsHub_Automation
```

### 2. Download Gradle wrapper (if not present):
```bash
gradle wrapper
```

## Configuration

Edit `src/test/resources/config.properties` to customize:
```properties
base.url=https://solutionshub.epam.com
browser=chrome
headless=false
implicit.wait=10
explicit.wait=20
```

## Running Tests

### Run all tests:
```bash
gradlew test
```

or

```bash
./gradlew test
```

### Run tests with specific tags:
```bash
gradlew test -Dcucumber.filter.tags="@smoke"
```

### Run specific feature file:
```bash
gradlew test -Dcucumber.features="src/test/resources/features/01_general_navigation.feature"
```

### Available tags:
- `@smoke` - Smoke tests
- `@navigation` - Navigation tests
- `@solutions` - Solutions tab tests
- `@assets` - Assets tab tests
- `@guides` - Guides tab tests
- `@blog` - Blog tab tests
- `@about` - About tab tests
- `@high` - High priority tests

## Building the Project

```bash
gradlew build
```

## Test Reports

After test execution, reports are generated in:
- HTML Report: `target/cucumber-reports/cucumber.html`
- JSON Report: `target/cucumber-reports/cucumber.json`
- Console output with test results

## Features

### Page Object Model (POM)
- Separation of test logic from page structure
- Reusable page methods
- Easy maintenance

### BDD with Cucumber
- Human-readable test scenarios in Gherkin
- Business-friendly documentation
- Supports behavior-driven development

### WebDriver Manager
- Automatic driver management
- No manual driver downloads needed
- Supports Chrome, Firefox, Edge

### Hooks
- Setup and teardown for each scenario
- Screenshot capture on test failure
- Clean browser state for each test

## Test Execution Flow

1. **Before Hook**: Initialize WebDriver
2. **Background**: Navigate to homepage (if specified in feature)
3. **Scenario Steps**: Execute test steps
4. **After Hook**: Take screenshot if failed, close browser

## Debugging Tests

### Run in debug mode:
1. Open test runner class in IDE
2. Set breakpoints in step definitions
3. Run in debug mode

### Enable headless mode:
Set `headless=true` in config.properties for CI/CD environments

## Troubleshooting

### Common Issues:

1. **ChromeDriver issues**: WebDriverManager handles this automatically
2. **Element not found**: Increase wait times in config.properties
3. **Tests fail randomly**: May need to adjust explicit waits or element locators

### Logs:
Check console output for detailed error messages and stack traces.

## Contributing

When adding new tests:
1. Create feature file in `src/test/resources/features/`
2. Add page objects in `pages/` package
3. Implement step definitions in `stepdefinitions/` package
4. Follow existing naming conventions

## Notes

- Tests are designed to work with the live website
- Some locators may need adjustment based on actual website structure
- Framework uses flexible locators to handle different page layouts
- Tests include proper waits and error handling

## Author
**Anuar Sultan**  
EPAM - AI-Driven Testing and Quality Assurance Course

## Date
March 2026
