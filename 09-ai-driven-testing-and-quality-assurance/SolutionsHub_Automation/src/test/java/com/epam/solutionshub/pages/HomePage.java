package com.epam.solutionshub.pages;

import com.epam.solutionshub.utils.DriverManager;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.List;

public class HomePage extends BasePage {

    public HomePage(WebDriver driver) {
        super(driver);
    }

    public void navigateToHomePage(String baseUrl) {
        driver.get(baseUrl);
    }

    public boolean isTabVisible(String tabName) {
        try {
            List<WebElement> tabs = driver.findElements(getTabLocator(tabName));
            return !tabs.isEmpty() && tabs.get(0).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    public void clickTab(String tabName) {
        String baseUrl = DriverManager.getBaseUrl();
        String path = getTabPath(tabName);
        driver.get(baseUrl + path);
    }

    public boolean isTabHighlighted(String tabName) {
        List<WebElement> tabs = driver.findElements(getTabLocator(tabName));
        if (tabs.isEmpty()) {
            return false;
        }

        String classAttribute = tabs.get(0).getAttribute("class");
        return classAttribute != null && (classAttribute.contains("active") ||
                classAttribute.contains("selected") ||
                classAttribute.contains("current"));
    }

    public int getNavigationTabsCount() {
        return driver.findElements(By.xpath("//nav//a | //header//a")).size();
    }

    private By getTabLocator(String tabName) {
        String lowerName = tabName.toLowerCase();
        String xpath = String.format(
                "//a[contains(translate(normalize-space(.), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '%s') or contains(translate(@href, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '/%s')]",
                lowerName,
                lowerName
        );
        return By.xpath(xpath);
    }

    private String getTabPath(String tabName) {
        switch (tabName.toLowerCase()) {
            case "solutions":
                return "/solutions";
            case "assets":
                return "/assets";
            case "guides":
                return "/guides";
            case "blog":
                return "/blog";
            case "about":
                return "/about";
            default:
                throw new IllegalArgumentException("Unknown tab: " + tabName);
        }
    }
}
