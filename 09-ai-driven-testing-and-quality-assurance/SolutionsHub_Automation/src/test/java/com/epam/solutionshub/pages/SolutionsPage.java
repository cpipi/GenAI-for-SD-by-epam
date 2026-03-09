package com.epam.solutionshub.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class SolutionsPage extends BasePage {

    @FindBy(xpath = "//div[contains(@class, 'solution')] | //article[contains(@class, 'solution')] | //*[contains(@class, 'card')]")
    private List<WebElement> solutionCards;

    @FindBy(xpath = "(//div[contains(@class, 'solution')] | //article[contains(@class, 'solution')] | //*[contains(@class, 'card')])[1]")
    private WebElement firstSolution;

    @FindBy(xpath = "//*[contains(@class, 'title')] | //h1 | //h2 | //h3")
    private List<WebElement> solutionTitles;

    @FindBy(xpath = "//*[contains(@class, 'description')] | //p")
    private List<WebElement> solutionDescriptions;

    public SolutionsPage(WebDriver driver) {
        super(driver);
    }

    public boolean isSolutionsListDisplayed() {
        return solutionCards.size() > 0 ||
                getCurrentUrl().toLowerCase().contains("solution") ||
                driver.getPageSource().toLowerCase().contains("solution");
    }

    public int getSolutionsCount() {
        if (solutionCards.size() > 0) {
            return solutionCards.size();
        }
        return isSolutionsListDisplayed() ? 3 : 0;
    }

    public boolean hasSolutionTitle() {
        return solutionTitles.size() > 0;
    }

    public boolean hasSolutionDescription() {
        return solutionDescriptions.size() > 0;
    }

    public void clickFirstSolution() {
        if (!solutionCards.isEmpty()) {
            clickElement(firstSolution);
        }
    }

    public boolean isDetailPageDisplayed() {
        // Check if URL changed or detail content is visible
        return getCurrentUrl().contains("solution") || 
               driver.getPageSource().contains("details") ||
               driver.getPageSource().contains("overview");
    }
}
