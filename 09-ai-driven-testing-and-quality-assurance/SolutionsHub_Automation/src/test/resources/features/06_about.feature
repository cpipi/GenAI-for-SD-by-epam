Feature: About Tab
  As a user
  I want to learn about the platform and company
  So that I can understand the mission and team behind SolutionsHub

  Background:
    Given I am on the SolutionsHub homepage
    When I click on the "About" tab

  @smoke @about
  Scenario: TC-ABT-001 - Verify company information is displayed
    Then I should see company or platform information
    And the About page should load successfully

  @high @about
  Scenario: TC-ABT-002 - Verify mission, goals, and team sections
    Then the About page should contain the following sections:
      | Mission |
      | Goals   |
      | Team    |
    And each section should have relevant content
