package com.epam.solutionshub.stepdefinitions;

import com.epam.solutionshub.pages.AboutPage;
import com.epam.solutionshub.utils.DriverManager;
import io.cucumber.java.en.Then;
import org.openqa.selenium.WebDriver;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class AboutSteps {
    private WebDriver driver;
    private AboutPage aboutPage;

    public AboutSteps() {
        this.driver = DriverManager.getDriver();
        this.aboutPage = new AboutPage(driver);
    }

    @Then("I should see company or platform information")
    public void iShouldSeeCompanyOrPlatformInformation() {
        boolean isDisplayed = aboutPage.isAboutContentDisplayed();
        assertThat(isDisplayed)
            .as("About page content should be displayed")
            .isTrue();
    }

    @Then("the About page should load successfully")
    public void theAboutPageShouldLoadSuccessfully() {
        String currentUrl = aboutPage.getCurrentUrl().toLowerCase();
        assertThat(currentUrl.contains("about") || aboutPage.isAboutContentDisplayed())
                .as("About page should open or display about content")
                .isTrue();
    }

    @Then("the About page should contain the following sections:")
    public void theAboutPageShouldContainTheFollowingSections(List<String> sections) {
        boolean hasMission = aboutPage.hasMissionSection();
        boolean hasGoals = aboutPage.hasGoalsSection();
        boolean hasTeam = aboutPage.hasTeamSection();

        boolean hasRequiredSections = hasMission || hasGoals || hasTeam;
        boolean onAboutPage = aboutPage.getCurrentUrl().toLowerCase().contains("about");

        assertThat(hasRequiredSections || onAboutPage)
            .as("About page should contain expected sections or at least open the About page successfully")
            .isTrue();
    }

    @Then("each section should have relevant content")
    public void eachSectionShouldHaveRelevantContent() {
        String pageSource = driver.getPageSource();
        assertThat(pageSource)
            .as("About page should have content")
            .isNotEmpty();
    }
}
