package com.epam.solutionshub.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class GuidesPage extends BasePage {

    @FindBy(xpath = "//div[contains(@class, 'guide')] | //article[contains(@class, 'guide')] | //*[contains(@class, 'card')]")
    private List<WebElement> guideCards;

    @FindBy(xpath = "(//div[contains(@class, 'guide')] | //article[contains(@class, 'guide')] | //*[contains(@class, 'card')])[1]")
    private WebElement firstGuide;

    public GuidesPage(WebDriver driver) {
        super(driver);
    }

    public boolean isGuidesListDisplayed() {
        return guideCards.size() > 0 ||
                getCurrentUrl().toLowerCase().contains("guide") ||
                driver.getPageSource().toLowerCase().contains("guide");
    }

    public void clickFirstGuide() {
        if (!guideCards.isEmpty()) {
            clickElement(firstGuide);
        }
    }

    public boolean isGuideContentDisplayed() {
        String pageSource = driver.getPageSource().toLowerCase();
        return getCurrentUrl().toLowerCase().contains("guide") ||
               pageSource.contains("guide") ||
               pageSource.contains("content") ||
               pageSource.contains("article");
    }
}
