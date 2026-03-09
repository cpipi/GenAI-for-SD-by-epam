package com.epam.solutionshub.pages;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;

import java.util.List;

public class AboutPage extends BasePage {

    @FindBy(xpath = "//*[contains(@class, 'about')] | //section | //div[contains(@class, 'content')]")
    private List<WebElement> contentSections;

    @FindBy(xpath = "//*[contains(text(), 'mission') or contains(text(), 'Mission')]")
    private List<WebElement> missionSection;

    @FindBy(xpath = "//*[contains(text(), 'goal') or contains(text(), 'Goal')]")
    private List<WebElement> goalsSection;

    @FindBy(xpath = "//*[contains(text(), 'team') or contains(text(), 'Team')]")
    private List<WebElement> teamSection;

    public AboutPage(WebDriver driver) {
        super(driver);
    }

    public boolean isAboutContentDisplayed() {
        if (contentSections.size() > 0) {
            return true;
        }

        String text = driver.findElement(org.openqa.selenium.By.tagName("body")).getText();
        return text != null && text.trim().length() > 80;
    }

    public boolean hasMissionSection() {
        return missionSection.size() > 0;
    }

    public boolean hasGoalsSection() {
        return goalsSection.size() > 0;
    }

    public boolean hasTeamSection() {
        return teamSection.size() > 0;
    }
}
