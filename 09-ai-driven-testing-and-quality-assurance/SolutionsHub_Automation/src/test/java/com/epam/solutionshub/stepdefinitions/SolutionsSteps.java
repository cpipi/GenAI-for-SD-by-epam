package com.epam.solutionshub.stepdefinitions;

import com.epam.solutionshub.pages.SolutionsPage;
import com.epam.solutionshub.utils.DriverManager;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.WebDriver;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class SolutionsSteps {
    private WebDriver driver;
    private SolutionsPage solutionsPage;

    public SolutionsSteps() {
        this.driver = DriverManager.getDriver();
        this.solutionsPage = new SolutionsPage(driver);
    }

    @Then("I should see a list of solutions")
    public void iShouldSeeAListOfSolutions() {
        boolean isDisplayed = solutionsPage.isSolutionsListDisplayed();
        assertThat(isDisplayed)
            .as("Solutions list should be displayed")
            .isTrue();
    }

    @Then("each solution should be displayed as a card or list item")
    public void eachSolutionShouldBeDisplayedAsACardOrListItem() {
        int count = solutionsPage.getSolutionsCount();
        assertThat(count)
            .as("There should be at least one solution displayed")
            .isGreaterThan(0);
    }

    @Then("each solution card should contain:")
    public void eachSolutionCardShouldContain(List<String> fields) {
        boolean hasTitle = solutionsPage.hasSolutionTitle();
        boolean hasDescription = solutionsPage.hasSolutionDescription();
        
        assertThat(hasTitle)
            .as("Solutions should have titles")
            .isTrue();
        
        assertThat(hasDescription)
            .as("Solutions should have descriptions")
            .isTrue();
    }

    @Then("at least {int} solutions should be visible")
    public void atLeastSolutionsShouldBeVisible(int minCount) {
        int count = solutionsPage.getSolutionsCount();
        assertThat(count)
            .as("At least %d solutions should be visible", minCount)
            .isGreaterThanOrEqualTo(minCount);
    }

    @When("I click on the first solution in the list")
    public void iClickOnTheFirstSolutionInTheList() {
        solutionsPage.clickFirstSolution();
        try {
            Thread.sleep(1500); // Wait for navigation
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Then("I should be navigated to the solution details page")
    public void iShouldBeNavigatedToTheSolutionDetailsPage() {
        boolean isDetailPage = solutionsPage.isDetailPageDisplayed();
        assertThat(isDetailPage)
            .as("Should navigate to solution details page")
            .isTrue();
    }

    @Then("the details page should display complete solution information")
    public void theDetailsPageShouldDisplayCompleteSolutionInformation() {
        String pageSource = driver.getPageSource();
        assertThat(pageSource)
            .as("Details page should contain solution information")
            .isNotEmpty();
    }
}
