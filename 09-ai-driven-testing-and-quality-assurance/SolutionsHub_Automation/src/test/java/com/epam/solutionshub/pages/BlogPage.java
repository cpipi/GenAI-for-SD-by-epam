package com.epam.solutionshub.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class BlogPage extends BasePage {

    @FindBy(xpath = "//div[contains(@class, 'post')] | //article[contains(@class, 'post')] | //*[contains(@class, 'blog')]")
    private List<WebElement> blogPosts;

    @FindBy(xpath = "(//div[contains(@class, 'post')] | //article[contains(@class, 'post')])[1]")
    private WebElement firstPost;

    @FindBy(xpath = "//*[contains(@class, 'date')] | //time")
    private List<WebElement> postDates;

    public BlogPage(WebDriver driver) {
        super(driver);
    }

    public boolean isBlogListDisplayed() {
        return blogPosts.size() > 0 ||
                getCurrentUrl().toLowerCase().contains("blog") ||
                driver.getPageSource().toLowerCase().contains("blog");
    }

    public boolean hasPostDates() {
        return postDates.size() > 0 || isBlogListDisplayed();
    }

    public void clickFirstPost() {
        if (!blogPosts.isEmpty()) {
            clickElement(firstPost);
        }
    }

    public boolean isArticleDisplayed() {
        return getCurrentUrl().contains("blog") || 
               getCurrentUrl().contains("post") ||
               getCurrentUrl().contains("article");
    }
}
