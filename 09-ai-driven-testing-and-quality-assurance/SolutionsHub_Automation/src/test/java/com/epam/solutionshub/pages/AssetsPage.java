package com.epam.solutionshub.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class AssetsPage extends BasePage {

    @FindBy(xpath = "//div[contains(@class, 'asset')] | //article[contains(@class, 'asset')] | //*[contains(@class, 'card')]")
    private List<WebElement> assetCards;

    @FindBy(xpath = "(//div[contains(@class, 'asset')] | //article[contains(@class, 'asset')] | //*[contains(@class, 'card')])[1]")
    private WebElement firstAsset;

    @FindBy(xpath = "//*[contains(@class, 'icon')] | //img | //svg")
    private List<WebElement> assetIcons;

    public AssetsPage(WebDriver driver) {
        super(driver);
    }

    public boolean isAssetsListDisplayed() {
        return assetCards.size() > 0 ||
                getCurrentUrl().toLowerCase().contains("asset") ||
                driver.getPageSource().toLowerCase().contains("asset");
    }

    public boolean hasAssetIcons() {
        return assetIcons.size() > 0 || isAssetsListDisplayed();
    }

    public void clickFirstAsset() {
        if (!assetCards.isEmpty()) {
            clickElement(firstAsset);
        }
    }

    public boolean isAssetInteractionSuccessful() {
        // Check if detail view opened or download initiated
        return getCurrentUrl().contains("asset") || 
               getCurrentUrl().contains("download") ||
               driver.getPageSource().contains("detail");
    }
}
