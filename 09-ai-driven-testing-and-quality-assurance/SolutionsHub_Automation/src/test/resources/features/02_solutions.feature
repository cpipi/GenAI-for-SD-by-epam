Feature: Solutions Tab
  As a user
  I want to browse available solutions
  So that I can find solutions relevant to my needs

  Background:
    Given I am on the SolutionsHub homepage
    When I click on the "Solutions" tab

  @smoke @solutions
  Scenario: TC-SOL-001 - Verify solutions list is displayed
    Then I should see a list of solutions
    And each solution should be displayed as a card or list item

  @high @solutions
  Scenario: TC-SOL-002 - Verify solution item contains required metadata
    Then each solution card should contain:
      | title             |
      | short description |
    And at least 3 solutions should be visible

  @high @solutions
  Scenario: TC-SOL-003 - Open solution details page
    When I click on the first solution in the list
    Then I should be navigated to the solution details page
    And the details page should display complete solution information
