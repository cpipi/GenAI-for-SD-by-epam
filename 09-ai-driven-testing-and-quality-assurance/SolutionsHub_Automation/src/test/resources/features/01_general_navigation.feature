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

  @smoke @navigation
  Scenario: TC-GEN-004 - Navigate to Solutions page
    When I click on the "Solutions" tab
    Then I should be on the Solutions page
    And the page URL should contain "/solutions"
    And the "Solutions" tab should be highlighted

  @smoke @navigation
  Scenario: TC-GEN-015 - Verify smooth navigation between tabs
    When I rapidly navigate through all tabs:
      | Solutions |
      | Assets    |
      | Guides    |
      | Blog      |
      | About     |
    Then there should be no errors or delays
    And each page should load successfully
