import multiprocessing
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from unittest import TestCase

from app import create_app, db
from app.routes import f_password
from config import TestingConfig


localHost = "http://localhost:5000/"


class SeleniumTests(TestCase):
    def setUp(self):
        self.testApp = create_app(TestingConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()

        self.server_process = multiprocessing.Process(target=self.testApp.run)
        self.server_process.start()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(localHost)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

        self.server_process.terminate()
        self.driver.close()

    def test_home_page(self):
        driver = self.driver
        driver.get(self.base_url)
        self.assertIn("Home",driver.title)
    def test_login_page(self):
        driver = self.driver
        driver.get(self.base_url + "login")
        self.assertIsNotNone(driver.find_element_by_id("username"))
        self.assertIsNotNone(driver.find_element_by_id("password"))
        self.assertIsNotNone(driver.find_element_by_id("submit_button"))
    def test_sign_up__page(self):
     driver = self.driver
     driver.get(self.base_url + "register")
     self.assertIsNotNone(driver.find_element_by_id("username"))
     self.assertIsNotNone(driver.find_element_by_id("password"))
     self.assertIsNotNone(driver.find_element_by_id("email"))
     self.assertIsNotNone(driver.find_element_by_id("confirm_password"))
     self.assertIsNotNone(driver.find_element_by_id("Submit_button"))
    def test_search_functionality(self):
     driver = self.driver
     driver.get(self.base_url)
     search_input = driver.find_element_by_id("search_input")
     search_input.send_keys("example search query")
     search_input.send_keys(Keys.RETURN)
    def tearDown(self):
     self.driver.quit()

    def get_test_data():
     return {
         "username": "example_username",
         "password": "example_password"
     }

    def test_login_page(self):
     # Import test data
     test_data = SeleniumTests.get_test_data()
    
    
     # Assuming the IDs for username, password, and submit button elements
     username_element = self.driver.find_element(By.ID, "your_username_id")
     password_element = self.driver.find_element(By.ID, "your_password_id")
     submit_element   = self.driver.find_element(By.ID, "submit_button_id")
    
     # Test when username is missing
     username_element.clear()
     password_element.send_keys(f_password)
     submit_element.click()
     # Assuming the class name for messages on your page is different
     messages = self.driver.find_elements(By.CLASS_NAME, "your_message_class")
     self.assertEqual(len(messages), 1, "Expected there to be a single error message when username is missing")
     self.assertIn("Username is required", messages[0].text)
    
#     # Test when password is missing
     username_element.send_keys(test_data.username)
     password_element.clear()
     submit_element.click()
     messages = self.driver.find_elements(By.CLASS_NAME, "your_message_class")
     self.assertEqual(len(messages), 1, "Expected there to be a single error message when password is missing")
     self.assertIn("Password is required", messages[0].text)
    

        






