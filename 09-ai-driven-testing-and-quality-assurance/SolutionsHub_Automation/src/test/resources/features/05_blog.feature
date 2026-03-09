Feature: Blog Tab
  As a user
  I want to read blog posts
  So that I can stay informed about platform updates and insights

  Background:
    Given I am on the SolutionsHub homepage
    When I click on the "Blog" tab

  @smoke @blog
  Scenario: TC-BLG-001 - Verify blog list is displayed
    Then I should see a list of blog posts
    And the blog page should load without errors

  @high @blog
  Scenario: TC-BLG-002 - Verify blog post contains required metadata
    Then each blog post should contain:
      | title             |
      | date              |
      | short description |
    And the date should be in a valid format

  @high @blog
  Scenario: TC-BLG-003 - Open full blog article
    When I click on the first blog post title
    Then I should be navigated to the full article page
    And the article content should be fully displayed
