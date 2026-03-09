Feature: Assets Tab
  As a user
  I want to access and download assets
  So that I can utilize resources provided by the platform

  Background:
    Given I am on the SolutionsHub homepage
    When I click on the "Assets" tab

  @smoke @assets
  Scenario: TC-AST-001 - Verify assets list is displayed
    Then I should see a list of assets
    And the assets page should be loaded successfully

  @high @assets
  Scenario: TC-AST-002 - Verify asset card contains required fields
    Then each asset card should contain:
      | title       |
      | description |
    And each asset should have a visual icon or thumbnail

  @high @assets
  Scenario: TC-AST-003 - Verify asset detail or download flow
    When I click on the first asset in the list
    Then I should see asset details or a download option
    And the interaction should complete without errors
