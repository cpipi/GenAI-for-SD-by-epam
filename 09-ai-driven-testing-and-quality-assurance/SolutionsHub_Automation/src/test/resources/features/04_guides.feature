Feature: Guides Tab
  As a user
  I want to access guides and documentation
  So that I can learn how to use the platform effectively

  Background:
    Given I am on the SolutionsHub homepage
    When I click on the "Guides" tab

  @smoke @guides
  Scenario: TC-GUD-001 - Verify guides list is displayed
    Then I should see a list of guides
    And each guide should have a title and description

  @high @guides
  Scenario: TC-GUD-002 - Open full guide details
    When I click on the first guide in the list
    Then I should be navigated to the full guide page
    And the guide content should be displayed completely
