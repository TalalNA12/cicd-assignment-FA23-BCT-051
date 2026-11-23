import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

BASE_URL = os.environ.get("BASE_URL", "http://localhost")

@pytest.fixture
def driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    browser = webdriver.Chrome(
        service=Service("/usr/bin/chromedriver"),
        options=options
    )
    yield browser
    browser.quit()

def test_page_title(driver):
    driver.get(BASE_URL)
    assert driver.title == "Talal | FA23-BCT-051"

def test_heading(driver):
    driver.get(BASE_URL)
    heading = driver.find_element(By.ID, "main-heading")
    assert heading.text == "Talal's CI/CD Project"

def test_roll_number(driver):
    driver.get(BASE_URL)
    roll = driver.find_element(By.ID, "roll-number")
    assert "FA23-BCT-051" in roll.text

def test_button_click(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "greet").click()
    message = driver.find_element(By.ID, "message")
    assert message.text == "Hello Talal! CI/CD is working!"

def test_text_input(driver):
    driver.get(BASE_URL)
    driver.find_element(By.ID, "user-input").send_keys("Selenium Test")
    driver.find_element(By.ID, "submit").click()
    output = driver.find_element(By.ID, "output")
    assert output.text == "Selenium Test"
    driver.save_screenshot("screenshot.png")
