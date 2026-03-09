package com.epam.solutionshub.pages;

import org.openqa.selenium.By;
import org.openqa.selenium.ElementClickInterceptedException;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

public class BasePage {
    protected WebDriver driver;
    protected WebDriverWait wait;

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, Duration.ofSeconds(20));
        PageFactory.initElements(driver, this);
    }

    protected void waitForElementToBeClickable(WebElement element) {
        wait.until(ExpectedConditions.elementToBeClickable(element));
    }

    protected void waitForElementToBeVisible(WebElement element) {
        wait.until(ExpectedConditions.visibilityOf(element));
    }

    protected void clickElement(WebElement element) {
        RuntimeException lastException = null;
        for (int attempt = 0; attempt < 3; attempt++) {
            try {
                waitForElementToBeClickable(element);
                element.click();
                return;
            } catch (ElementClickInterceptedException e) {
                lastException = new RuntimeException(e);
                dismissCookieBannerIfPresent();
                try {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", element);
                    return;
                } catch (Exception ignored) {
                    // retry
                }
            } catch (StaleElementReferenceException | NoSuchElementException | TimeoutException e) {
                lastException = new RuntimeException(e);
                try {
                    ((JavascriptExecutor) driver).executeScript("arguments[0].click();", element);
                    return;
                } catch (Exception ignored) {
                    // retry
                }
            }
        }
        if (lastException != null) {
            throw lastException;
        }
    }

    protected void dismissCookieBannerIfPresent() {
        try {
            var buttons = driver.findElements(By.id("onetrust-accept-btn-handler"));
            if (!buttons.isEmpty() && buttons.get(0).isDisplayed()) {
                buttons.get(0).click();
            }
        } catch (Exception ignored) {
            // no cookie banner present
        }
    }

    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }

    public String getPageTitle() {
        return driver.getTitle();
    }
}
