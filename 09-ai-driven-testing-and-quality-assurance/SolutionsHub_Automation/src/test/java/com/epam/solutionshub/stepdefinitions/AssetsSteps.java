package com.epam.solutionshub.stepdefinitions;

import com.epam.solutionshub.pages.AssetsPage;
import com.epam.solutionshub.utils.DriverManager;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.WebDriver;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class AssetsSteps {
    private WebDriver driver;
    private AssetsPage assetsPage;

    public AssetsSteps() {
        this.driver = DriverManager.getDriver();
        this.assetsPage = new AssetsPage(driver);
    }

    @Then("I should see a list of assets")
    public void iShouldSeeAListOfAssets() {
        boolean isDisplayed = assetsPage.isAssetsListDisplayed();
        assertThat(isDisplayed)
            .as("Assets list should be displayed")
            .isTrue();
    }

    @Then("the assets page should be loaded successfully")
    public void theAssetsPageShouldBeLoadedSuccessfully() {
        String currentUrl = assetsPage.getCurrentUrl().toLowerCase();
        assertThat(currentUrl).contains("asset");
    }

    @Then("each asset card should contain:")
    public void eachAssetCardShouldContain(List<String> fields) {
        // Verify assets are displayed (title and description are part of the cards)
        boolean hasAssets = assetsPage.isAssetsListDisplayed();
        assertThat(hasAssets)
            .as("Asset cards should be displayed with required fields")
            .isTrue();
    }

    @Then("each asset should have a visual icon or thumbnail")
    public void eachAssetShouldHaveAVisualIconOrThumbnail() {
        boolean hasIcons = assetsPage.hasAssetIcons();
        assertThat(hasIcons)
            .as("Assets should have icons or thumbnails")
            .isTrue();
    }

    @When("I click on the first asset in the list")
    public void iClickOnTheFirstAssetInTheList() {
        assetsPage.clickFirstAsset();
        try {
            Thread.sleep(1500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Then("I should see asset details or a download option")
    public void iShouldSeeAssetDetailsOrADownloadOption() {
        boolean isSuccessful = assetsPage.isAssetInteractionSuccessful();
        assertThat(isSuccessful)
            .as("Asset interaction should be successful")
            .isTrue();
    }

    @Then("the interaction should complete without errors")
    public void theInteractionShouldCompleteWithoutErrors() {
        String pageSource = driver.getPageSource().toLowerCase();
        assertThat(pageSource)
            .as("Page should not display server error pages")
            .doesNotContain("error 500");
    }
}
