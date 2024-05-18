import threading
import unittest
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from app import create_app, db
from config import SeleniumTestingConfig

localHost = "http://localhost:5000/"

class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        options = webdriver.ChromeOptions()
        # options.add_argument('headless') # Uncomment if you want headless mode
        try:
            cls.client = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"Error starting browser: {e}")
            cls.client = None
        if cls.client:
            cls.testApp = create_app(SeleniumTestingConfig)
            cls.app_context = cls.testApp.app_context()
            cls.app_context.push()
            db.create_all()

            cls.server_thread = threading.Thread(target=cls.testApp.run, kwargs={'port': 5000, 'use_reloader': False})
            cls.server_thread.start()
            
            sleep(1)  # Give the server time to start

    @classmethod
    def tearDownClass(cls):
        try:
            if cls.client:
                pass
                cls.client.quit()
            if hasattr(cls, 'app_context'):
                cls.app_context.pop()
            if hasattr(cls, 'server_thread'):
                cls.server_thread.join(timeout=1)
            db.drop_all()
            db.session.remove()
        except Exception as e:
            print(f"Error during teardown: {e}")

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_company_title(self):
        self.client.get(localHost)
        self.assertIn("EcoHUB", self.client.title)

    def test_login_when_failed(self):
        self.client.get(localHost)
        # Find the login form elements and enter invalid credentials
        username_input = self.client.find_element(By.NAME, "username")
        password_input = self.client.find_element(By.NAME, "password")
        username_input.send_keys("invalid_user")
        password_input.send_keys("invalid_password")
        
        # Submit the login form
        login_button = self.client.find_element(By.XPATH, "//input[@value='Log In']")
        self.client.execute_script('arguments[0].click();', login_button)

        # Wait for the error message to appear
        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        # Verify the error message
        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-danger")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Invalid username or password", error_message.text)

    def test_login_sucess(self):
        self.client.get(localHost)
        username_input = self.client.find_element(By.NAME, "username")
        password_input = self.client.find_element(By.NAME, "password")
        username_input.send_keys("johndoe")
        password_input.send_keys("password123")
        
        login_button = self.client.find_element(By.XPATH, "//input[@value='Log In']")
        self.client.execute_script('arguments[0].click();', login_button)

        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))
        )

        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-success")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Successfully login!", error_message.text)

        logout_link = self.client.find_element(By.XPATH, "//a[@href='/logout']")
        self.client.execute_script('arguments[0].click();', logout_link)

        WebDriverWait(self.client, 10).until(
            EC.url_to_be(localHost+'login')
        )

    def test_login_navigate_signup(self):
        self.client.get(localHost)
        signup_url = localHost + 'signup'

        signup_link = self.client.find_element(By.XPATH, "//a[@href='signup']")
        self.client.execute_script('arguments[0].click();', signup_link)

        WebDriverWait(self.client, 10).until(
            EC.url_to_be(signup_url)
        )
        self.assertEqual(self.client.current_url, signup_url)

        form_present = self.client.find_element(By.ID, "signupForm")
        self.assertIsNotNone(form_present)
    
    def test_signup_username_exists(self):
        self.client.get(localHost + 'signup')

        self.client.find_element(By.ID, "first_name").send_keys("John")
        self.client.find_element(By.ID, "last_name").send_keys("Doe")
        exists_username = 'johndoe'
        self.client.find_element(By.ID, "username").send_keys(exists_username)
        self.client.find_element(By.ID, "email_address").send_keys("john.doe2@example.com")
        self.client.find_element(By.ID, "contact_no").send_keys("1234567890")
        self.client.find_element(By.ID, "postcode").send_keys("6000")
        self.client.find_element(By.ID, "password").send_keys("password123")
        self.client.find_element(By.ID, "re_password").send_keys("password123")

        signup_btn = self.client.find_element(By.XPATH, "//input[@value='Sign Up']")
        self.client.execute_script('arguments[0].click();', signup_btn)

        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-danger")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Please use a different username.", error_message.text)
    
    def test_signup_invalid_email(self):
        self.client.get(localHost + 'signup')

        self.client.find_element(By.ID, "first_name").send_keys("John")
        self.client.find_element(By.ID, "last_name").send_keys("Doe")
        self.client.find_element(By.ID, "username").send_keys("johndoe2")
        invalid_email = 'asdasd'
        self.client.find_element(By.ID, "email_address").send_keys(invalid_email)
        self.client.find_element(By.ID, "contact_no").send_keys("1234567890")
        self.client.find_element(By.ID, "postcode").send_keys("6000")
        self.client.find_element(By.ID, "password").send_keys("password123")
        self.client.find_element(By.ID, "re_password").send_keys("password123")

        signup_btn = self.client.find_element(By.XPATH, "//input[@value='Sign Up']")
        self.client.execute_script('arguments[0].click();', signup_btn)

        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-danger")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Invalid email address.", error_message.text)

    def test_signup_email_exists(self):
        self.client.get(localHost + 'signup')

        self.client.find_element(By.ID, "first_name").send_keys("John")
        self.client.find_element(By.ID, "last_name").send_keys("Doe")
        self.client.find_element(By.ID, "username").send_keys("johndoe2")
        exists_email = "john.doe@example.com"
        self.client.find_element(By.ID, "email_address").send_keys(exists_email)
        self.client.find_element(By.ID, "contact_no").send_keys("1234567890")
        self.client.find_element(By.ID, "postcode").send_keys("6000")
        self.client.find_element(By.ID, "password").send_keys("password123")
        self.client.find_element(By.ID, "re_password").send_keys("password123")

        signup_btn = self.client.find_element(By.XPATH, "//input[@value='Sign Up']")
        self.client.execute_script('arguments[0].click();', signup_btn)

        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-danger")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Please use a different email address.", error_message.text)

    def test_signup_password_not_same(self):
        self.client.get(localHost + 'signup')

        self.client.find_element(By.ID, "first_name").send_keys("John")
        self.client.find_element(By.ID, "last_name").send_keys("Doe")
        self.client.find_element(By.ID, "username").send_keys("johndoe2")
        self.client.find_element(By.ID, "email_address").send_keys("john.doe2@example.com")
        self.client.find_element(By.ID, "contact_no").send_keys("1234567890")
        invalid_postcode = 10
        self.client.find_element(By.ID, "postcode").send_keys(invalid_postcode)
        self.client.find_element(By.ID, "password").send_keys("password123")
        self.client.find_element(By.ID, "re_password").send_keys("password123")

        signup_btn = self.client.find_element(By.XPATH, "//input[@value='Sign Up']")
        self.client.execute_script('arguments[0].click();', signup_btn)

        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-danger")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Invalid Postcode.", error_message.text)

    def test_signup_is_seller_and_shop_name_empty(self):
        self.client.get(localHost + 'signup')

        self.client.find_element(By.ID, "first_name").send_keys("John")
        self.client.find_element(By.ID, "last_name").send_keys("Doe")
        self.client.find_element(By.ID, "username").send_keys("johndoe2")
        self.client.find_element(By.ID, "email_address").send_keys("john.doe2@example.com")
        self.client.find_element(By.ID, "contact_no").send_keys("1234567890")
        self.client.find_element(By.ID, "postcode").send_keys("6000")
        self.client.find_element(By.ID, "password").send_keys("password123")
        self.client.find_element(By.ID, "re_password").send_keys("password123")

        become_seller_checkbox = self.client.find_element(By.ID, "customCheck")
        if not become_seller_checkbox.is_selected():
            self.client.execute_script('arguments[0].click();', become_seller_checkbox)

        signup_btn = self.client.find_element(By.XPATH, "//input[@value='Sign Up']")
        self.client.execute_script('arguments[0].click();', signup_btn)

        WebDriverWait(self.client, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "alert-danger"))
        )

        error_message = self.client\
            .find_element(By.CLASS_NAME, "alert-danger")\
            .find_element(By.TAG_NAME, "div")
        self.assertIsNotNone(error_message)
        self.assertIn("Please enter a shop name if you wish to become a seller.", error_message.text)

if __name__ == '__main__':
    unittest.main(verbosity=1)