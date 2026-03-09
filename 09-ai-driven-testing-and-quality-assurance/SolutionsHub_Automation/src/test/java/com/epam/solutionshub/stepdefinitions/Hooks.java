package com.epam.solutionshub.stepdefinitions;

import com.epam.solutionshub.utils.DriverManager;
import io.cucumber.java.After;
import io.cucumber.java.Before;
import io.cucumber.java.Scenario;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;

public class Hooks {

    private WebDriver driver;

    @Before
    public void setUp(Scenario scenario) {
        System.out.println("Starting scenario: " + scenario.getName());
        driver = DriverManager.getDriver();
    }

    @After
    public void tearDown(Scenario scenario) {
        if (scenario.isFailed()) {
            // Take screenshot on failure
            try {
                byte[] screenshot = ((TakesScreenshot) driver).getScreenshotAs(OutputType.BYTES);
                scenario.attach(screenshot, "image/png", "Failed_" + scenario.getName());
            } catch (Exception e) {
                System.err.println("Failed to take screenshot: " + e.getMessage());
            }
        }
        
        System.out.println("Finished scenario: " + scenario.getName() + " - Status: " + scenario.getStatus());
        
        // Close browser after each scenario
        DriverManager.quitDriver();
    }
}
