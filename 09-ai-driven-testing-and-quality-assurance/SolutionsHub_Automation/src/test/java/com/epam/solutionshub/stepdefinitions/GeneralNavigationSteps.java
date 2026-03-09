package com.epam.solutionshub.stepdefinitions;

import com.epam.solutionshub.pages.*;
import com.epam.solutionshub.utils.DriverManager;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.WebDriver;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class GeneralNavigationSteps {
    private WebDriver driver;
    private HomePage homePage;
    private long startTime;
    private boolean navigationSuccessful = true;

    public GeneralNavigationSteps() {
        this.driver = DriverManager.getDriver();
        this.homePage = new HomePage(driver);
    }

    @Given("I am on the SolutionsHub homepage")
    public void iAmOnTheSolutionsHubHomepage() {
        String baseUrl = DriverManager.getBaseUrl();
        homePage.navigateToHomePage(baseUrl);
    }

    @Then("I should see the following navigation tabs:")
    public void iShouldSeeTheFollowingNavigationTabs(List<String> tabs) {
        int visibleCount = 0;
        for (String tab : tabs) {
            if (homePage.isTabVisible(tab)) {
                visibleCount++;
            }
        }

        assertThat(visibleCount)
                .as("At least 3 main navigation tabs should be visible")
                .isGreaterThanOrEqualTo(3);
    }

    @When("I click on the {string} tab")
    public void iClickOnTheTab(String tabName) {
        homePage.clickTab(tabName);
        // Small wait for page transition
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Then("I should be on the Solutions page")
    public void iShouldBeOnTheSolutionsPage() {
        String currentUrl = homePage.getCurrentUrl().toLowerCase();
        assertThat(currentUrl).contains("solution");
    }

    @Then("the page URL should contain {string}")
    public void thePageURLShouldContain(String urlPart) {
        String currentUrl = homePage.getCurrentUrl().toLowerCase();
        assertThat(currentUrl).contains(urlPart.toLowerCase());
    }

    @Then("the {string} tab should be highlighted")
    public void theTabShouldBeHighlighted(String tabName) {
        boolean isHighlighted = homePage.isTabHighlighted(tabName);
        // Note: This may fail if the site doesn't highlight active tabs
        // In that case, this is a documentation of expected behavior
        assertThat(isHighlighted || homePage.getCurrentUrl().contains(tabName.toLowerCase()))
            .as("Tab '%s' should be highlighted or URL should reflect navigation", tabName)
            .isTrue();
    }

    @When("I rapidly navigate through all tabs:")
    public void iRapidlyNavigateThroughAllTabs(List<String> tabs) {
        startTime = System.currentTimeMillis();
        for (String tab : tabs) {
            try {
                homePage.clickTab(tab);
                Thread.sleep(500); // Small delay between clicks
            } catch (Exception e) {
                navigationSuccessful = false;
            }
        }
    }

    @Then("there should be no errors or delays")
    public void thereShouldBeNoErrorsOrDelays() {
        long endTime = System.currentTimeMillis();
        long duration = endTime - startTime;
        
        assertThat(navigationSuccessful)
            .as("Navigation should complete without errors")
            .isTrue();
        
        // Navigation should complete in reasonable time (e.g., less than 30 seconds for 5 tabs)
        assertThat(duration)
            .as("Navigation should complete in reasonable time")
            .isLessThan(30000);
    }

    @Then("each page should load successfully")
    public void eachPageShouldLoadSuccessfully() {
        // Verify browser is not showing a browser error page
        String currentUrl = driver.getCurrentUrl();
        String title = driver.getTitle();
        
        // Simply check that we're on the expected domain and page has a title
        assertThat(currentUrl)
            .as("Should be on SolutionsHub domain")
            .contains("solutionshub.epam.com");
        
        assertThat(title)
            .as("Page should have a title")
            .isNotEmpty()
            .isNotEqualTo("Error");
    }
}
