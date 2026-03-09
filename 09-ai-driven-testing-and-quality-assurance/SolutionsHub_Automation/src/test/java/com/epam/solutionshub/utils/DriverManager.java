package com.epam.solutionshub.utils;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;

import java.io.FileInputStream;
import java.io.IOException;
import java.time.Duration;
import java.util.Properties;

public class DriverManager {
    private static WebDriver driver;
    private static Properties properties;

    public static void initializeDriver() {
        loadProperties();
        String browser = properties.getProperty("browser", "chrome").toLowerCase();
        boolean headless = Boolean.parseBoolean(properties.getProperty("headless", "false"));

        switch (browser) {
            case "chrome":
                WebDriverManager.chromedriver().setup();
                ChromeOptions chromeOptions = new ChromeOptions();
                if (headless) {
                    chromeOptions.addArguments("--headless");
                }
                chromeOptions.addArguments("--remote-allow-origins=*");
                chromeOptions.addArguments("--disable-blink-features=AutomationControlled");
                driver = new ChromeDriver(chromeOptions);
                break;
            case "firefox":
                WebDriverManager.firefoxdriver().setup();
                driver = new FirefoxDriver();
                break;
            case "edge":
                WebDriverManager.edgedriver().setup();
                driver = new EdgeDriver();
                break;
            default:
                throw new IllegalArgumentException("Browser not supported: " + browser);
        }

        int implicitWait = Integer.parseInt(properties.getProperty("implicit.wait", "10"));
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(implicitWait));
        driver.manage().window().maximize();
    }

    public static WebDriver getDriver() {
        if (driver == null) {
            initializeDriver();
        }
        return driver;
    }

    public static void quitDriver() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }

    public static String getBaseUrl() {
        if (properties == null) {
            loadProperties();
        }
        return properties.getProperty("base.url", "https://solutionshub.epam.com");
    }

    private static void loadProperties() {
        properties = new Properties();
        try {
            FileInputStream fis = new FileInputStream("src/test/resources/config.properties");
            properties.load(fis);
        } catch (IOException e) {
            System.out.println("Config file not found, using defaults");
            properties.setProperty("base.url", "https://solutionshub.epam.com");
            properties.setProperty("browser", "chrome");
            properties.setProperty("headless", "false");
            properties.setProperty("implicit.wait", "10");
        }
    }

    public static int getExplicitWait() {
        if (properties == null) {
            loadProperties();
        }
        return Integer.parseInt(properties.getProperty("explicit.wait", "20"));
    }
}
