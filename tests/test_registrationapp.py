
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

@pytest.fixture
def setup_teardown():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def get_alert(driver):
    alert = Alert(driver)
    text = alert.text
    alert.accept()
    return text

def test_empty_username(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").clear()
    driver.find_element(By.NAME, "pwd").send_keys("abc")
    driver.find_element(By.NAME, "sb").click()
    alert= get_alert(driver)
    assert alert == "Username cannot be empty."


def test_empty_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("alice")
    driver.find_element(By.NAME, "pwd").clear()
    driver.find_element(By.NAME, "sb").click()
    alert = get_alert(driver)
    assert alert == "Password cannot be empty."

def test_short_password(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc1")
    driver.find_element(By.NAME, "sb").click()
    alert = get_alert(driver)
    assert alert == "Password length is less than 6"

def test_valid_input(setup_teardown):
    driver = setup_teardown
    driver.get("http://127.0.0.1:5000/")
    driver.find_element(By.NAME, "username").send_keys("alice")
    driver.find_element(By.NAME, "pwd").send_keys("abc123")
    driver.find_element(By.NAME, "sb").click()
    assert "/submit" in driver.current_url
    body_text = driver.find_element(By.TAG_NAME, "body").text
    assert "Hello, alice! Welcome to the website" in body_text
