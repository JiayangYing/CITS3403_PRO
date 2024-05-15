import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        # Configure Chrome to run in headless mode
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(options=options)
        self.base_url = "http://localhost:5000/"

    def test_home_page(self):
        driver = self.driver
        driver.get(self.base_url)
        # Check the title of the home page
        self.assertIn("Home", driver.title)  # Adjust the expected title as needed

    def tearDown(self):
        # Close the Selenium driver
        self.driver.quit()
        # Terminate the Flask server thread if it's part of the test setup
        # Assuming you have a reference to the server thread
        # self.server_thread.terminate()
        # self.server_thread.join()

if __name__ == "__main__":
    unittest.main()
