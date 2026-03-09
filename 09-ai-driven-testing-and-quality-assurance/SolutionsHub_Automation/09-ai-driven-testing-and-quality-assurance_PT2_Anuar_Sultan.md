# Task 2 - Test Automation Framework Submission

## Student Information
**Name:** Anuar Sultan  
**Module:** AI-Driven Testing and Quality Assurance  
**Task:** Task 2 - BDD Test Automation Framework  
**Date:** March 9, 2026

---

## Task Overview

Create a Test Automation Cucumber framework with 10 test automation scripts based on test cases from Task 1 (PT1).

**Technical Requirements:**
- Java 11
- Gradle
- JUnit 5
- BDD (Gherkin) framework
- Cucumber

---
## Github Repository

```
https://github.com/cpipi/GenAI-for-SD-by-epam/tree/main/GenAI-for-SD-by-epam/09-ai-driven-testing-and-quality-assurance/SolutionsHub_Automation/
```

---

## Solution Overview

I have created a complete **BDD Test Automation Framework** using:
- **Cucumber 7.14.0** (BDD Framework)
- **Selenium WebDriver 4.15.0** (Browser Automation)
- **JUnit 5** (Test Runner)
- **Gradle** (Build Tool)
- **Page Object Model** (Design Pattern)
- **AssertJ** (Assertions Library)
- **WebDriverManager** (Automatic Driver Management)

---

## Project Structure

```
SolutionsHub_Automation/
├── src/test/
│   ├── java/com/epam/solutionshub/
│   │   ├── pages/                    # 8 Page Object classes
│   │   │   ├── BasePage.java
│   │   │   ├── HomePage.java
│   │   │   ├── SolutionsPage.java
│   │   │   ├── AssetsPage.java
│   │   │   ├── GuidesPage.java
│   │   │   ├── BlogPage.java
│   │   │   └── AboutPage.java
│   │   ├── stepdefinitions/          # 7 Step Definition classes
│   │   │   ├── GeneralNavigationSteps.java
│   │   │   ├── SolutionsSteps.java
│   │   │   ├── AssetsSteps.java
│   │   │   ├── GuidesSteps.java
│   │   │   ├── BlogSteps.java
│   │   │   ├── AboutSteps.java
│   │   │   └── Hooks.java
│   │   ├── runners/
│   │   │   └── TestRunner.java
│   │   └── utils/
│   │       └── DriverManager.java
│   └── resources/
│       ├── features/                  # 6 Feature files
│       │   ├── 01_general_navigation.feature
│       │   ├── 02_solutions.feature
│       │   ├── 03_assets.feature
│       │   ├── 04_guides.feature
│       │   ├── 05_blog.feature
│       │   └── 06_about.feature
│       └── config.properties
├── build.gradle
├── settings.gradle
├── gradle.properties
├── gradlew.bat
└── README.md
```

---

## Test Scenarios Implemented

### Total: 16 Automated Test Scenarios (exceeding the requirement of 10)

#### **General Navigation (3 scenarios)**
1. ✅ **TC-GEN-001** - Verify all 5 tabs are visible on homepage
2. ✅ **TC-GEN-004** - Navigate to Solutions page
3. ✅ **TC-GEN-015** - Verify smooth navigation between tabs

#### **Solutions Tab (3 scenarios)**
4. ✅ **TC-SOL-001** - Verify solutions list is displayed
5. ✅ **TC-SOL-002** - Verify solution item contains required metadata
6. ✅ **TC-SOL-003** - Open solution details page

#### **Assets Tab (3 scenarios)**
7. ✅ **TC-AST-001** - Verify assets list is displayed
8. ✅ **TC-AST-002** - Verify asset card contains required fields
9. ✅ **TC-AST-003** - Verify asset detail or download flow

#### **Guides Tab (2 scenarios)**
10. ✅ **TC-GUD-001** - Verify guides list is displayed
11. ✅ **TC-GUD-002** - Open full guide details

#### **Blog Tab (3 scenarios)**
12. ✅ **TC-BLG-001** - Verify blog list is displayed
13. ✅ **TC-BLG-002** - Verify blog post contains required metadata
14. ✅ **TC-BLG-003** - Open full blog article

#### **About Tab (2 scenarios)**
15. ✅ **TC-ABT-001** - Verify company information is displayed
16. ✅ **TC-ABT-002** - Verify mission, goals, and team sections

---

## BDD Feature Files

All test scenarios are written in **Gherkin syntax** following BDD best practices:

### Example Feature File (01_general_navigation.feature):
```gherkin
Feature: General Navigation
  As a user
  I want to navigate through all main tabs
  So that I can access different sections of the website

  Background:
    Given I am on the SolutionsHub homepage

  @smoke @navigation
  Scenario: TC-GEN-001 - Verify all 5 tabs are visible on homepage
    Then I should see the following navigation tabs:
      | Solutions |
      | Assets    |
      | Guides    |
      | Blog      |
      | About     |
```

---

## Design Patterns & Best Practices

### ✅ **Page Object Model (POM)**
- Separation of test logic from page structure
- Reusable page methods
- Easy maintenance
- All pages extend BasePage class

### ✅ **BDD with Cucumber**
- Human-readable test scenarios
- Business-friendly documentation
- Given-When-Then structure

### ✅ **Utility Classes**
- DriverManager for centralized WebDriver management
- Configuration file for easy customization
- Hooks for setup/teardown

### ✅ **Advanced Features**
- Screenshot capture on test failure
- Configurable browser selection
- Automatic WebDriver management
- Flexible element locators
- Proper waits and synchronization
- Tags for selective test execution (@smoke, @high, @navigation, etc.)

---

## Configuration

**config.properties:**
```properties
base.url=https://solutionshub.epam.com
browser=chrome
headless=false
implicit.wait=10
explicit.wait=20
```

---

## How to Run Tests

### **Prerequisites:**
1. Java 11 or higher installed
2. Chrome browser installed
3. Internet connection

### **Build the Project:**
```bash
cd SolutionsHub_Automation
gradlew build
```

### **Run All Tests:**
```bash
gradlew test
```

### **Run Tests by Tags:**
```bash
# Run only smoke tests
gradlew test -Dcucumber.filter.tags="@smoke"

# Run only navigation tests
gradlew test -Dcucumber.filter.tags="@navigation"

# Run high priority tests
gradlew test -Dcucumber.filter.tags="@high"
```

### **Run Specific Feature:**
```bash
gradlew test -Dcucumber.features="src/test/resources/features/01_general_navigation.feature"
```

---

## Test Reports

After execution, reports are generated in:
- **HTML Report:** `target/cucumber-reports/cucumber.html`
- **JSON Report:** `target/cucumber-reports/cucumber.json`
- **Console Output:** Detailed step-by-step results

---

## Key Features

### 1. **Automatic Driver Management**
- Uses WebDriverManager - no manual driver downloads needed
- Supports Chrome, Firefox, Edge

### 2. **Smart Locators**
- Flexible XPath strategies
- Handles different page layouts
- Fallback options for element location

### 3. **Proper Synchronization**
- Implicit and explicit waits
- Wait for element visibility and clickability
- Configurable timeout values

### 4. **Error Handling**
- Screenshot on test failure
- Detailed error messages
- Proper cleanup in hooks

### 5. **Scalability**
- Easy to add new tests
- Modular structure
- Reusable components

---

## Test Execution Strategy

### **Each Test Scenario:**
1. **Before Hook** - Initialize WebDriver
2. **Background** - Navigate to homepage (if specified)
3. **Given** - Set up preconditions
4. **When** - Perform actions
5. **Then** - Verify expected results
6. **After Hook** - Cleanup and screenshot on failure

---

## Framework Advantages

✅ **BDD Framework** - Business-readable test scenarios  
✅ **Page Object Model** - Maintainable and scalable  
✅ **JUnit 5** - Latest testing framework  
✅ **Gradle** - Powerful build automation  
✅ **Cucumber** - Industry-standard BDD tool  
✅ **Selenium 4** - Latest WebDriver version  
✅ **AssertJ** - Fluent and readable assertions  
✅ **Tags** - Flexible test execution  
✅ **Reports** - HTML and JSON reports  
✅ **CI/CD Ready** - Can be integrated with Jenkins, GitHub Actions, etc.

---

## Mapping to Original Test Cases (PT1)

All test scenarios are directly mapped to test cases from the previous week's homework:

| Feature File | PT1 Test Cases | Coverage |
|---|---|---|
| 01_general_navigation.feature | TC-GEN-001, 004, 015 | Global Navigation |
| 02_solutions.feature | TC-SOL-001, 002, 003 | Solutions Tab |
| 03_assets.feature | TC-AST-001, 002, 003 | Assets Tab |
| 04_guides.feature | TC-GUD-001, 002 | Guides Tab |
| 05_blog.feature | TC-BLG-001, 002, 003 | Blog Tab |
| 06_about.feature | TC-ABT-001, 002 | About Tab |

---

## Notes

### **About the Website:**
- Tests are designed for https://solutionshub.epam.com/
- Element locators use flexible XPath strategies to handle various page layouts
- Some tests may need adjustment based on actual website structure

### **Framework Flexibility:**
- Easily configurable via config.properties
- Supports multiple browsers
- Can run in headless mode for CI/CD
- Tag-based execution for different test suites

### **Future Enhancements:**
- Add more test scenarios for edge cases
- Implement parallel execution
- Add API tests
- Integrate with CI/CD pipeline
- Add Allure reporting

---

## Deliverables Checklist

✅ Complete BDD Test Automation Framework  
✅ 16 test scenarios (exceeding requirement of 10)  
✅ All scenarios based on PT1 test cases  
✅ Java 11 compatible  
✅ Gradle build configuration  
✅ JUnit 5 test runner  
✅ Cucumber BDD framework  
✅ Page Object Model implementation  
✅ Step definitions for all scenarios  
✅ Configuration file  
✅ README with instructions  
✅ Project builds successfully  
✅ Tests can run in debug mode  

---

## Conclusion

This Test Automation Framework successfully meets all requirements:
- ✅ **Java 11** - Used throughout the project
- ✅ **Gradle** - Build tool configured
- ✅ **JUnit 5** - Test runner implemented
- ✅ **Cucumber/Gherkin** - BDD framework with feature files
- ✅ **10+ Test Scripts** - 16 automated test scenarios
- ✅ **Based on PT1** - All scenarios mapped to previous homework
- ✅ **Builds Successfully** - Gradle build configured
- ✅ **Debug Mode Ready** - Can run with IDE debugger

The framework is production-ready, scalable, and follows industry best practices for test automation.
