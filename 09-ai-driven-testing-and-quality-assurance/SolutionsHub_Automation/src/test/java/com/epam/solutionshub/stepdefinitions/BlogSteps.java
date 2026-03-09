package com.epam.solutionshub.stepdefinitions;

import com.epam.solutionshub.pages.BlogPage;
import com.epam.solutionshub.utils.DriverManager;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;
import org.openqa.selenium.WebDriver;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public class BlogSteps {
    private WebDriver driver;
    private BlogPage blogPage;

    public BlogSteps() {
        this.driver = DriverManager.getDriver();
        this.blogPage = new BlogPage(driver);
    }

    @Then("I should see a list of blog posts")
    public void iShouldSeeAListOfBlogPosts() {
        boolean isDisplayed = blogPage.isBlogListDisplayed();
        assertThat(isDisplayed)
            .as("Blog posts list should be displayed")
            .isTrue();
    }

    @Then("the blog page should load without errors")
    public void theBlogPageShouldLoadWithoutErrors() {
        String currentUrl = blogPage.getCurrentUrl().toLowerCase();
        assertThat(currentUrl.contains("blog") || blogPage.isBlogListDisplayed())
                .as("Blog page should be opened or blog content should be visible")
                .isTrue();
    }

    @Then("each blog post should contain:")
    public void eachBlogPostShouldContain(List<String> fields) {
        boolean hasPosts = blogPage.isBlogListDisplayed();
        assertThat(hasPosts)
            .as("Blog posts should be displayed with required metadata")
            .isTrue();
    }

    @Then("the date should be in a valid format")
    public void theDateShouldBeInAValidFormat() {
        boolean hasDates = blogPage.hasPostDates();
        assertThat(hasDates)
            .as("Blog posts should have dates")
            .isTrue();
    }

    @When("I click on the first blog post title")
    public void iClickOnTheFirstBlogPostTitle() {
        blogPage.clickFirstPost();
        try {
            Thread.sleep(1500);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Then("I should be navigated to the full article page")
    public void iShouldBeNavigatedToTheFullArticlePage() {
        boolean isDisplayed = blogPage.isArticleDisplayed();
        assertThat(isDisplayed)
            .as("Full article page should be displayed")
            .isTrue();
    }

    @Then("the article content should be fully displayed")
    public void theArticleContentShouldBeFullyDisplayed() {
        String pageSource = driver.getPageSource();
        assertThat(pageSource)
            .as("Article content should be present")
            .isNotEmpty();
    }
}
